'''
Reads a physics-centred data format into python

Created on 29 May 2014

@author: chris
'''

import h5py
import numpy as np

def zmp3d_hdf_read(fname, var_name = "gas density"):
    f =  __open_hdf__(fname)
#     print list(f)

    var = __read_matrix_hdf__(f,var_name)
#     print np.shape(var)
    x = __read_matrix_hdf__(f,'i coord')
    y = __read_matrix_hdf__(f,'j coord')
    z = __read_matrix_hdf__(f,'k coord') 
    t = f['   time'][0]
    
    f.close()
    
    return var, x, y, z, t

def zmp3d_var_read(fname, var_name):
    f =  __open_hdf__(fname)
    var = __read_matrix_hdf__(f,var_name)
    f.close()
    return var

def zmp3d_coords_read(fname):
    f =  __open_hdf__(fname)
    x = __read_matrix_hdf__(f,'i coord')
    y = __read_matrix_hdf__(f,'j coord')
    z = __read_matrix_hdf__(f,'k coord') 
    f.close()
    return x, y, z
    

def sph_col_2d_hdfread(fname, var_name = "gas density"):
    var, x, y, _, t = zmp3d_hdf_read(fname, var_name = var_name)
    var = var[:,:,0]
    return var, x, y, t

def zmp_hdf_t(fname):
    f =  __open_hdf__(fname)
    t = f['   time'][0]
    return t

def __read_matrix_hdf__(f,var_name):
    return np.array(f[var_name][...],dtype=np.float64)

def __open_hdf__(fname):
    #print fname
    return h5py.File(fname,'r')


