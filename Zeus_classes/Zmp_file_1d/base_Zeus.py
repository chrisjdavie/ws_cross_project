'''Takes a file from ZeusMP and manipulates it.  Replaced with classes in File_classes (used
for hydro-simulations more generally, and learnt some structure lessons from this).

Zeus_file    - base file manipulation
Zeus_1d_file - a 1D Zeus simulation'''

class Zeus_file(object):
    
    def __init__(self,fname):
        
        self.fname  = fname
        self.fnum_str = self.fname[-3:]
        
        from import_data import zmp_hdf_t
        self.t = zmp_hdf_t(fname)  
        
    def open_density(self):
        self.rho, self.x, self.y, self.z, _ = self._open_var("gas density")
        
    def open_energy(self):
        self.e, self.x, self.y, self.z, _ = self._open_var(" gas energy")
        
    def open_i_vel(self):
        self.v_i , self.x, self.y, self.z, _ = self._open_var(" i velocity")
        
    def _open_var(self,var_name):
        from import_data import zmp3d_hdf_read
        return zmp3d_hdf_read(self.fname, var_name = var_name)
       
from linplots_cjd import linear_plot
class Zeus_f_linplot(linear_plot):
    def __init__(self,x,var,fnum_str):
        super(Zeus_f_linplot,self).__init__(x,var)
        self.fnum_str = fnum_str
    
    def plot2file_i(self, pic_dir):
        linear_plot.plot2file(self, pic_dir+self.fnum_str, pformat='png')
    
        
class Zeus_1d_file(Zeus_file):
    
    '''assumes x-direction variation'''
    
    def open_density(self):
        super(Zeus_1d_file,self).open_density()
        self.rho = self.rho[0,0,:]
        
    def open_energy(self):
        super(Zeus_1d_file,self).open_energy()
        self.e = self.e[0,0,:]        
        
    def open_i_vel(self):
        super(Zeus_1d_file,self).open_i_vel()
        self.v_i = self.v_i[0,0,:]           
        
    def plot_density(self):
        self.open_density()
        
        self.rho_v_r = self._lin_plot(self.rho, r'$\rho$')
        return self.rho_v_r
        
    def plot_vel(self):
        self.open_i_vel()
        
        self.v_i_v_r = self._lin_plot(self.v_i, r'$v$')
        return self.v_i_v_r
        
    def _lin_plot(self,var,var_y_label):
        var_v_r = Zeus_f_linplot(self.x,var,self.fnum_str)
        var_v_r.plot_init(xlabel=r'$x$',ylabel=var_y_label)
        var_v_r.plot()
        var_v_r.time_title(self.t, unit='')  
        return var_v_r
        
    def plot_velocity(self):
        self.open_i_vel()
        
        