'''
The base interface for the class that plots files.  The methods here are the ones
that dir_class.py (and often, the code itself), the classes that inherit from this
for specific hydro simulations handle the underlying specifics.

It also assumes an ideal gas, and that P, v and rho are the hydro variables stored.
 
Works for 1D and 2D, limited applicability to 3D.

Created on 27 Aug 2014

@author: chris
'''

# import h5py
import numpy as np

class plot_file(object):
    def __init__(self):
        self.fig_i = 1
        
    def _int_cplot(self, var, var_nam, cplot_plot_kwargs = {}, x_bound = None, pcolormesh_kwargs = {}):
        
        self.open_coords()                
        self.open_t()        
        
        x = self.x
        y = self.y - np.min(self.y)
        
        if x_bound != None:
            i_r = np.argmin(np.abs(self.x-x_bound*1.01))
            i_l = np.argmin(np.abs(self.x+x_bound))
            j_t = np.argmin(np.abs(self.y-x_bound*1.01))
#             print i_r, i_l, j_t, x_bound
#             raw_input()
            var = var[:j_t,i_l:i_r]
            x = x[i_l:i_r]
            y = y[:j_t]
        
        from cplots_ig_cjd import phys_cplot
        
        cont_class = self
        class int_cplot(phys_cplot):
            def savetofdir(self):
                cplot_fname = cont_class.file_dir + var_nam
                fformat = 'png'
                self.plot2file(cplot_fname,fformat)
                tmp_dir = '/tmp/' + var_nam + '/'
                import os
                if os.path.exists(tmp_dir):
                    import shutil
                    shutil.copy(cplot_fname+'.' +fformat,tmp_dir+cont_class.t_step_str+'.' +fformat)                
        
        p = int_cplot(x,y,var,var=var_nam, pcolormesh_kwargs = pcolormesh_kwargs)
        p.time_title(self.t,unit='')
#         self.p_rho_cplot.ax.set_aspect('equal')
        p.ax.set_aspect('equal', adjustable='box')
        p.fig.subplots_adjust(left=0.18,bottom=0.1,top=0.93,right=0.85)
        
        return p
        
    def v_r_cplot(self, cplot_plot_kwargs = {}, t_unit = ''):
        self.open_v_r()
        self.p_v_r_cplot = self._int_cplot(self.v_r,'v_r',cplot_plot_kwargs = cplot_plot_kwargs)
        return self.p_v_r_cplot    
        
    def e_cplot(self, cplot_plot_kwargs = {}, t_unit = ''):
        self.open_e()
        self.p_rho_cplot = self._int_cplot(self.e,'e',cplot_plot_kwargs = cplot_plot_kwargs)
        return self.p_rho_cplot        
        
    def rho_cplot(self, cplot_plot_kwargs = {}, t_unit = '',x_bound=None, pcolormesh_kwargs = {}):
        self.open_rho()
        self.p_rho_cplot = self._int_cplot(self.rho,'rho',cplot_plot_kwargs = cplot_plot_kwargs,x_bound=x_bound, pcolormesh_kwargs = pcolormesh_kwargs)
        return self.p_rho_cplot
    
    def plot_rho_line_out(self,label='',theta=np.pi/4.0):
        def rho_line_out():
            self.rho_line_out(theta)
        return self._plot_line_out(self.rho_line_out, r'$\rho$',label=label)
    
    def plot_P_line_out(self,label=''):
        return self._plot_line_out(self.P_line_out, r'$P$',label=label)
        
    def plot_e_line_out(self,label=''):
        return self._plot_line_out(self.e_line_out, r'$\epsilon$',label=label)
    
    def plot_v_x_line_out(self,label=''):
        return self._plot_line_out(self.v_x_line_out,r'$v_x$',label=label)
    
    def plot_v_y_line_out(self,label=''):
        return self._plot_line_out(self.v_y_line_out,r'$v_y$',label=label)

    def plot_v_r_line_out(self,label=''):
        return self._plot_line_out(self.v_r_line_out,r'$v_r$',label=label)
           
    def _plot_line_out(self,var_lo_fn,ylabel,label=''):
        r, var_r = var_lo_fn()
        
        from linplots_cjd import linear_plot
        cont_class = self
        
        class line_out(linear_plot):
            def savetofdir(self,nam='var',ftype='pdf'):
                _savetofdir(self,cont_class,nam+'_v_r',ftype)
            
        p_lin = line_out(r,var_r)
        p_lin.plot_init(xlabel=r'$r$/cm', ylabel=ylabel,fig_i=self.fig_i)
        self.fig_i += 1 
        p_lin.plot(label=label)
        return p_lin

    def rho_line_out(self,theta=np.pi/4.0):
        self.open_rho()
        return self._line_out(self.rho,theta)
        
    def e_line_out(self,theta=np.pi/4.0):
        self.open_e()
        return self._line_out(self.e,theta)
    
    def P_line_out(self,theta=np.pi/4.0):
        r, e_r = self.e_line_out(theta)
        P_r = e_r*(5.0/3.0-1.0)
        return r, P_r
    
    def v_r_line_out(self,theta=np.pi/4.0):
        self.open_v_r()
        return self._line_out(self.v_r,theta)
            
class plot_conv_file(plot_file):
        
    def _int_rho_cplot(self, cplot_plot_kwargs = {}):
        pass

def _savetofdir(p_class,cont_class,plot_nam,fformat='png'):
    cplot_fname = cont_class.file_dir + plot_nam
    p_class.plot2file(cplot_fname,fformat)
    tmp_dir = '/tmp/flash/'
    import os
    if os.path.exists(tmp_dir):
        import shutil
        shutil.copy(cplot_fname+'.' +fformat,tmp_dir+cont_class.t_step_str+'.' +fformat)