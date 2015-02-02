'''
Handles general functions for simulations of spherically converging 
and reflecting shocks.  

conv_file_2d     - many common functions for this in 2d
var_prof         - makes 1d profiles of data.  Is quite quick, at least
                    compared to the matplotlib version of this.
Zmp_plot         - these simulations are in cylindrical geometries, and
                    this does the standard plotting for that.

zeroth_conv_file - there is a number of things that need to be dealt with
                    at the very start, which are propogated, including the
                    initial peaks and troughs of the simulation.

Created on 3 Jul 2014

@author: chris
'''

import numpy as np

def main():
    fname = '/media/Cx1files/mat_behind_shk/l16/1024/zeus/exe90/hdfaa.000'
    l = 16
    test_0f = zeroth_conv_file(fname,l)
    print test_0f.fname
    test_0f.find_shkf()
    test_0f.leg_decomp()
    
    
class file_plot(object):
    ''' An attempt at a more formalised structure.  Turned out it was 
        overkill for this sort of thing and was abandoned.'''
    def cplot(self,*args,**kwargs):
        return self._cplot(*args,**kwargs)
    

class conv_file_2d(file_plot):
    '''
    classdocs
    '''
    t_c = 8.2003e-9

    def __init__(self,fname):
        
        self.mode_max = 32
        self.fname  = fname
        self.fnum_str = self.fname[-3:]
        
        from import_data import zmp_hdf_t
        self.t = zmp_hdf_t(fname)
        
    def find_shkf(self,zeroth_file):
        
        f0 = zeroth_file
        if self.t < self.t_c:
            from shock_front_tracking import inwards
            self.thetas, self.rs, _ = inwards(self.fname,f0.__glob_l_fill__,f0.Dx,f0.rho_0)
        else:
            from shock_front_tracking import outwards
            self.thetas, self.rs, _ = outwards(self.fname,f0.__glob_l_fill__,f0.Dx,f0.theta0)
            
    def leg_decomp(self,rs_thetas=None):
        if rs_thetas != None:
            self.rs     = rs_thetas[0]
            self.thetas = rs_thetas[1]
        
        l_q = isinstance( self.rs, ( int, long ) )
        if not l_q:
            from legendre_decomp import Leg_decomp
            self.mode_matrix = Leg_decomp(self.thetas,self.rs,self.mode_max)    
        else:
            self.mode_matrix = np.zeros(self.mode_max+1)
            
    def open_density(self):
        from import_data import sph_col_2d_hdfread
        self.rho, self.R, self.Z, _ = sph_col_2d_hdfread(self.fname, var_name = "gas density")
    
    def open_energy(self):
        from import_data import sph_col_2d_hdfread
        self.e, self.R, self.Z, _ = sph_col_2d_hdfread(self.fname, var_name = " gas energy")
        
    def open_v_x(self):
        from import_data import sph_col_2d_hdfread
        self.v_x, self.R, self.Z, _ = sph_col_2d_hdfread(self.fname, var_name = " i velocity")
    
    def open_v_y(self):
        from import_data import sph_col_2d_hdfread
        self.v_y, self.R, self.Z, _ = sph_col_2d_hdfread(self.fname, var_name = " j velocity")
                
    def _cplot(self,var,var_name, cplot_plot_kwargs = {}, half_clynd = False ):
        fnum_str = self.fnum_str
        
        class int_cplot(Zmp_plot):
            def __init__(self,outer_class, Zmp_plot_args, Zmp_plot_kwargs ):
                self.outer_class = outer_class
                super(int_cplot,self).__init__( *Zmp_plot_args, **Zmp_plot_kwargs )
            
            def plot2file_i(self,pic_dir):
                pic_fname = pic_dir + fnum_str
                super(int_cplot,self).plot2file(pic_fname)
                
            def shkf_n_arrows(self,len_adj=1.0):
                out_q = False
                if self.outer_class.t > self.outer_class.t_c:
                    out_q = True
                csv_dir = self.outer_class.fname[:-20] + 'shockf/' # Hack - 2 things - clearly, want a file dir that has a hdf, shkf and leg in for each.  Then make the hdf stuff a higher class than the dir stuff, which has the cplotting and shockfront finding and legendre stuff in.  I'm not doing this now.  
                super(int_cplot,self).shkf_n_arrows(self.outer_class.fnum_str,csv_dir,out_q=out_q,len_adj=len_adj)
            
            def time_title(self):
                super(int_cplot,self).time_title(self.outer_class.t,unit='s')
        
        '''Looks like I've got Z and R the wrong way round'''
        
#         print np.shape(self.Z), np.shape(var)
        R_plot = self.R
        Z_plot = self.Z
        
        if half_clynd:
            N_r = len(self.R)
            
            R_plot = self.R[N_r/2:]
            R_plot = R_plot - np.min(R_plot)
            Z_plot = self.Z - np.min(self.Z)
            var = var[N_r/2:,:]
#         print np.shape(R_plot), np.shape(var)
#         raw_input()
        Zmp_plot_args   = ( Z_plot, R_plot, var, var_name )
        Zmp_plot_kwargs = { 'cplot_plot_kwargs' : cplot_plot_kwargs }
        
        return int_cplot( self, Zmp_plot_args, Zmp_plot_kwargs )
        
    def rho_cplot(self, half_clynd = False, cplot_plot_kwargs = {}):
        self.open_density()
        self.cp_rho = self.cplot(self.rho,'gas density', half_clynd = half_clynd, cplot_plot_kwargs = cplot_plot_kwargs)
        return self.cp_rho
        
    def rho_line_out(self,theta=np.pi/4.0):
        self.open_density()
        return self._var_line_out(self.rho,theta)
    
    def energy_line_out(self,theta=np.pi/4.0):
        self.open_energy()
        return self._var_line_out(self.e,theta)    
    
    def v_x_line_out(self,theta=np.pi/4.0):
        self.open_v_x()
        return self._var_line_out(self.v_x,theta)    
     
    def v_y_line_out(self,theta=np.pi/4.0):
        self.open_v_y()
        return self._var_line_out(self.v_y,theta)    
       
    def _var_line_out(self,var,theta):
        from shock_front_tracking import pre_run
        __glob_l_fill__, _, _, _ = pre_run(self.fname,2)
        
        def __var_l_fill__(l_tmp,theta_tmp):
            return __glob_l_fill__(var,l_tmp,theta_tmp) 
        
        r_k, var_k  = var_prof(__var_l_fill__,theta,self.Z[len(self.Z)-10])
        return r_k, var_k
    
    def plot_circle(self,radius,colour=[30.0/255,144.0/255,255.0/255],dash_seq=[10,10,4,10]):
        plot_kwargs={'color':colour,'linestyle':'-','linewidth':4}
        add_line_kwargs = {'dash_seq':dash_seq}        
        
        n = 100
        thetaa = np.arange(0,np.pi,np.pi/n)
        RR = np.zeros_like(thetaa) + radius
        self.line_from_polars(RR,thetaa,plot_kwargs=plot_kwargs,add_line_kwargs=add_line_kwargs)
               
    
def var_prof(__var_l_fill__,theta,y_end):
    k = 0
    r_k_tmp = 0
    var_k = []
    r_k = []
    
    while ( r_k_tmp < y_end ):
        k = k + 1
        var_k_tmp, r_k_tmp, _ = __var_l_fill__(k,theta)
        r_k.append(r_k_tmp)
        var_k.append(var_k_tmp)
        
    r_k = np.array(r_k)
    var_k = np.array(var_k)
    
    return r_k, var_k    
  
from cplots_ig_cjd import R_Z_cplot

class Zmp_plot(R_Z_cplot):
    
    def __init__(self,r,z,var,hdf_var_nam, cplot_plot_kwargs = {}):
        print hdf_var_nam
#         raw_input()
        
        from cplots_ig_cjd import phys_cbar_lab_prep
        
        if hdf_var_nam == 'gas density': 
            var_nam = 'rho'
            units = 'g/cm$^3$'
        if hdf_var_nam == ' i velocity': 
            var_nam = 'v_x'
            units = 'cm/s'
        if hdf_var_nam == ' j velocity': 
            var_nam = 'v_y'
            units = 'cm/s'
        if hdf_var_nam == ' gas energy': 
            var_nam = 'e'
            units = 'Ergs/cc'
        
        cbar_label, pcolormesh_kwargs = phys_cbar_lab_prep(units,var_nam,var)
        
        super(Zmp_plot,self).__init__( r, z, var, pcolormesh_kwargs = pcolormesh_kwargs, cbar_label = cbar_label, cplot_plot_kwargs = cplot_plot_kwargs )
        
class zeroth_conv_file(conv_file_2d):
    
    def __init__(self,fname,l):
        
        self.l = l
        super(zeroth_conv_file,self).__init__(fname)
        
        from shock_front_tracking import pre_run
        self.__glob_l_fill__, self.Dx, self.theta0, self.rho_0 = pre_run(self.fname,self.l)
        

if __name__ == '__main__':
    main()