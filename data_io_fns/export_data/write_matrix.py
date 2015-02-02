'''
writes various file strutures.

Created on 11 Oct 2012

@author: chris
'''
import h5py
import numpy as np
import csv
    
def write_zmp_matrix_hdf(fname,data,x,y,z,t,dname='gas density'):
        
    hdf_file = __open_hdf__(fname)
    __write_data__(hdf_file,dname,data)
    __write_data__(hdf_file,'i coord',x)
    __write_data__(hdf_file,'j coord',y)   
    __write_data__(hdf_file,'k coord',z)
    __write_data__(hdf_file,'   time',[t])
    hdf_file.close()
    
def __open_hdf__(fname):
    return h5py.File(fname,'w')

def __write_data__(hdf_file,dname,data):
    lower = data
    for i in range(len(np.shape(data))):
        lower = lower[i]    
    dtype = type(lower)    
    
    ds = hdf_file.create_dataset(dname, np.shape(data), dtype)
    ds[...] = data
    
def write_matrix_csv(fname,data):
    f = open(fname,'wb')
    csv_file = csv.writer(f)
    for d in data: csv_file.writerow(d)
    f.close()
    
def write_vector_csv(fname,data):
    f = open(fname,'wb')
    csv_file = csv.writer(f)
    for d in data: csv_file.writerow([d])    
    f.close()
    
def write_scalar_csv(fname,data):
    f = open(fname,'wb')
    csv_file = csv.writer(f) 
    csv_file.writerow([data])
    f.close()