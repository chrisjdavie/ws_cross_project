'''
Dealing with the directories for converging and reflected shock simulations.

Not many comments, but the function names are clear to me, and reasonably
short in terms of code.

This expects my post-processing code to have been run on the simulation output.

Created on 3 Jul 2014

@author: chris
'''
import numpy as np
import os
from Zmp_conv_2d import conv_file_2d

class conv_dir_2d(object):
    '''
    classdocs
    '''


    def __init__(self,base_dir,l):
        '''
        Constructor
        '''
        self.base_dir   = base_dir
        self.hdf_dir    = base_dir + 'zeus/exe90/'
        self.l          = l
        
        self.shkf_dir   = self.base_dir + 'shockf/'
        self.leg_dir    = self.base_dir + 'legendre/'
        
        from os_fns import open_file_list
        
        flist = open_file_list(self.hdf_dir)
        self.fname_list = [ f for f in flist if f[-9:-4] == 'hdfaa' ]
        from Zmp_conv_2d import zeroth_conv_file
        self.zerof = zeroth_conv_file(self.fname_list[0],self.l)
#         from Zmp_conv_2d import zeroth_conv_file
#         self.zerof = zeroth_conv_file(self.fname_list[0],self.l)
        
#         self.files = []
#         for fname in self.fname_list:
#             self.files.append(conv_file_2d(fname,self.zerof))   
        
    def shock_track(self,i_0=0,i_e=None):
        
        if not os.path.exists(self.shkf_dir):
#             import shutil
#             shutil.rmtree(self.shkf_dir)
#         
            os.makedirs(self.shkf_dir)
            os.makedirs(self.shkf_dir + 'rshkfs/')
            os.makedirs(self.shkf_dir + 'thetas/')
            os.makedirs(self.shkf_dir + 'ts/')
        
        def save_each_file(rs,thetas,t,t_step_str):
            from export_data import write_vector_csv, write_scalar_csv
            write_vector_csv( self.shkf_dir + 'rshkfs/' + t_step_str + '.csv', rs )
            write_vector_csv( self.shkf_dir + 'thetas/' + t_step_str + '.csv', thetas )
            write_scalar_csv( self.shkf_dir + 'ts/'     + t_step_str + '.csv', t )   
        
        from Zmp_conv_2d import zeroth_conv_file
        
        
        for fname in self.fname_list[i_0:i_e]:
            f = conv_file_2d(fname)
            f.find_shkf(self.zerof)
            save_each_file(f.rs,f.thetas,f.t,f.fname[-3:])
            print f.fnum_str
            del f
            
    def leg_decomp(self):
        
        if os.path.exists(self.leg_dir):
            import shutil
            shutil.rmtree(self.leg_dir)   
        os.makedirs(self.leg_dir)
        
        mode_matrixx = []
        for fname in self.fname_list:
            f = conv_file_2d(fname)            
            print f.fnum_str
            rs_thetas = None
            if not hasattr(f,'thetas'):
                if os.path.exists( self.shkf_dir ):
                    from import_data import vect_read
                    thetas = vect_read( self.shkf_dir + 'thetas/' + f.fnum_str + '.csv')
                    rs     = vect_read( self.shkf_dir + 'rshkfs/' + f.fnum_str + '.csv') 
                    rs_thetas = (rs,thetas)
                else:
                    print 'No thetas or rshkfs found, conv_dir_2d.leg_decomp'
                    exit(2)
                    
            f.leg_decomp(rs_thetas)
            mode_matrixx.append(f.mode_matrix)
            del f
            
        from export_data import write_matrix_csv
        write_matrix_csv(self.leg_dir + 'mode_matrix.csv',mode_matrixx)
        print "file written, conv_dir_2d.leg_decomp"
     
    def plot_dr_v_r(self,l=None):
        self.get_dr_n_r(l)
        
        from linplots_cjd import dr_v_r_plot
        self.dr_v_r_p = dr_v_r_plot(self.rs_in,self.drs_in)
        self.dr_v_r_p.plot_init(xlabel='$r$/cm')
        self.dr_v_r_p.plot()
        
    def plot_dr_r_v_r(self,l=None,semilog_kwargs={},in_l=True,i_l_gap=0):
        self.get_dr_n_r(l,i_l_gap=i_l_gap)
        
        from linplots_cjd import dr_r_v_r_plot
        
        if in_l: rs, drs = self.rs_in,  self.drs_in
        else:    rs, drs = self.rs_out, self.drs_out
        
        self.dr_r_v_r_p = dr_r_v_r_plot(rs,drs)
        self.dr_r_v_r_p.plot_init(xlabel='$r$/cm')
        self.dr_r_v_r_p.plot(semilog_kwargs=semilog_kwargs)
        return self.dr_r_v_r_p
        
    def plot_r_v_t(self,analy=True):
        self.__get_r_in_n_out()
        self.__get_t()
        i=0
        while self.rs[i] > self.rs[i+1]: i += 1
        i_l = i
        i = -1
        while self.rs[i] > self.rs[i-1]: i -= 1
        i_r = i
        self.rs = np.concatenate((self.rs[:i_l],self.rs[i_r:]))
        self.ts = np.concatenate((self.ts[:i_l],self.ts[i_r:]))
        
        from linplots_cjd import linear_plot
        self.r_v_t_p = linear_plot(self.ts,self.rs)
        self.r_v_t_p.plot_init(xlabel='$t$/s',ylabel='$r$/cm')
        self.r_v_t_p.plot(label='Simulation')
        if analy:
            r_a, _ = Goldman_solution_4plot(self.ts, self.rs)
            self.r_v_t_p.add_line(r_a, label='Analytic')
        
        
    def get_dr_n_r(self,l=None,i_l_gap=0):
        self.__get_r_in_n_out(i_l_gap)
        self.__get_dr(l,i_l_gap=i_l_gap)
        return self.rs_in, self.rs_out, self.drs_in, self.drs_out
        
    def match_t_to_file(self,t_match):#
        self.__get_t()
        for i, t in enumerate(self.ts):
            if t > t_match:
                break
        i_adj = np.argmin(np.abs([self.ts[i]-t_match,self.ts[i-1]-t_match]))
        i = i - i_adj
        zf = conv_file_2d(self.fname_list[i+2])
        return zf
        
    def __get_t(self):
        from import_data import zmp_hdf_t
        self.ts = [ zmp_hdf_t(fname) for fname in self.fname_list ]
        
    def __get_dr(self,l=None,i_l_gap=0):
        

        if l == None:
            l = self.l
            
        drs = self.leg_mat[:,l]
        
        i = 0
        self.drs_in = drs[:self.i_in_f]        
        self.drs_out = drs[self.i_out_f:]
        
    def __open_leg_mat(self):
        from import_data import csv_matrix_read
        
        if os.path.exists(self.leg_dir):
            self.leg_mat = csv_matrix_read( self.leg_dir + 'mode_matrix.csv' )
        else:
            print 'No legendre compts found, conv_dir_2d.leg_decomp'
            exit(3)        
        
    def __get_r_in_n_out(self,i_l_gap=0):
        
        self.__open_leg_mat()
        self.rs  = self.leg_mat[:,0]
        
        r_m1 = 1.0e30
        for i, r in enumerate(self.rs):
            if r > r_m1:
                break
            r_m1 = r
        self.i_in_f = i - 1 - i_l_gap
        
        i = -1
        while self.rs[i-1] < self.rs[i]:
            i -= 1
        self.i_out_f = i + 1
        
        self.rs_in  = self.rs[:self.i_in_f]
        self.rs_out = self.rs[self.i_out_f:]
        
    def rho_cplot(self,pic_dir='/tmp/conv/',i_0=0,i_e=-1):
        import gc
#         from guppy import hpy
        import matplotlib.pyplot as pl
        for fname in self.fname_list[i_0:i_e]:
#             print gc.get_objects()
            
            f = conv_file_2d(fname)
            f.rho_cplot()
            f.cp_rho.plot2file_i(pic_dir)
            f.cp_rho.clf()
            print f.fnum_str
            pl.close(f.cp_rho.fig)
            f = None
            gc.collect()
            gc.collect()
    
    def single_file(self,i):
        f = conv_file_2d(self.fname_list[i])
        return f
#             print gc.is_tracked(f)
#             h = hpy()
#             print h.heap()
        
def Goldman_solution_4plot(t,r):
    
    # this produces the analytic curve for an array t, with t_c the point of convergence, r_0 being the initialised r
    
    r_0 = r[0] - 0.02e-4
    
    for i,r_i in enumerate(r):
        i_c = i
        if r[i+1] > r_i:
            break
        
    t_c = t[i_c]
    print t[i_c], t[i_c-1], t[i_c+1]
    
    ntilde = np.float32(0.688377) 
    
    tp = t/t_c - 1.0
    ep_in = 1.0
    tp_l1 = np.array([ -t_i for t_i in tp if t_i < 0 ])
    rp_in = ep_in*np.power(tp_l1,ntilde)
    
    ep_out = 0.7405
    tp_ge1 = np.array([ t for t in tp if t >= 0 ])
    rp_out = ep_out*np.power(tp_ge1,ntilde)
    
    rp = np.concatenate((rp_in,rp_out))
    r = rp*r_0
    
    return r, t_c
        

            
        
            
        