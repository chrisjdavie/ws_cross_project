'''
ZeusMP 2D planar simulation output file.

Created on 27 Aug 2014

@author: chris
'''
from base import plot_file
import h5py
import numpy as np
# import matplotlib.pyplot as pl

class zeus_file(plot_file):
    '''
    classdocs
    '''
    
    def __init__(self,file_dir):
        '''
        Constructor
        '''
        self.file_dir = file_dir
        self.hdf_fname = self.file_dir + 'sens.hdf5'
        self.t_step_str = self.file_dir[-4:-1]
        
        super(zeus_file,self).__init__()
        
    def open_rho(self):
        self.rho = self._open_array("gas density")[0,:,:] #2D
        
    def open_e(self):
        self.e = self._open_array(" gas energy")[0,:,:] #2D
        
    def open_v_x(self):
        self.v_x = self._open_array(" i velocity")[0,:,:] #2D
        
    def open_v_y(self):
        self.v_y = self._open_array(" j velocity")[0,:,:] #2D
        
    def open_v_r(self):
        self.open_v_x()
        self.open_v_y()
        v_r_mag = np.sqrt(self.v_x*self.v_x+self.v_y*self.v_y)
        self.open_coords()
        phi = np.arctan2(self.yy,self.xx)
        sign = np.sign(self.v_x*np.cos(phi) + self.v_y*np.sin(phi))
        self.v_r = v_r_mag*sign
        
    def open_coords(self):
        self.x = self._open_array('i coord')
#         self.x  = self.xx[0,:]
        self.y = self._open_array('j coord')
#         self.y  = self.yy[:,0]
        self.xx,self.yy = np.meshgrid(self.x,self.y)
        self.Dx = self.x[1]-self.x[0]
        
    def open_t(self):
        self.t = self._open_array('   time')[0]
        
    def _open_array(self,var_nam):
        f = h5py.File(self.hdf_fname,'r')
        var = self.__read_matrix_hdf__(f, var_nam)
        f.close()
        return var
    
    def __read_matrix_hdf__(self,f,var_name): return np.array(f[var_name][...],dtype=np.float64)

    def _line_out(self,var,theta):
        self.open_coords()
        
        i_r = np.array(range(0,len(self.x)),dtype=np.float)
        var_r = self._line_out_int(var, theta, i_r, len(self.x), len(self.y))
        
#         self.open_coords()
        r = i_r*self.Dx
#         print self.x[len(var)/2], np.max(self.x), np.min(self.x)
#         print self.rho[len(var)/2,len(var)/2]
#         raw_input()
        return r, var_r
       
    def _line_out_int(self,var,theta,i_r,N_x,N_y):
        '''This assumes equal dx and dy.  Returns things in units of
           cell number'''
        
        i_x = N_x/2.0 + i_r*np.sin(theta)
        i_y = i_r*np.cos(theta)
        
        import scipy.ndimage
        var_r = scipy.ndimage.map_coordinates(var, np.vstack((i_y,i_x)))
        
        return var_r    
    
        