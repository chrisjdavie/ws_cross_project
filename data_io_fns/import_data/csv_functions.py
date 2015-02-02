'''Deals with reading various types of csv file'''

import numpy as np
import csv     
# moved np.array from str_2_num to the here - this helps sort out pcolor plots.  It might screw things up, though

def vect_read(fname):
    vect_out = __csv_vect_read__(fname)
    if np.all(vect_out) == 4:
        print "empty csv"
        return 4
#    print fname, vect_out
    if len(vect_out) < 2:
        vect_out = np.loadtxt(fname)
    if len(vect_out) < 2:
        print "unable to read file as a vector.  def vect_read, importing_data.py"
        return 4
    return vect_out
 
# reads in vectors from matlab-esq csv files
def __csv_vect_read__(fname):
    f = open(fname)
    if '\0' in f.read():
        print "empty csv"
        return 4    
    f.close()
    f = open(fname)
    tmp = csv.reader(f)
    vect_num = [-1]
    for i in tmp:
        vect_num = str_2_num(i)
    return np.array(vect_num)

# converts an array of strings to a vector of np floats, which are a bit faster and do maths more sensibly   
def str_2_num(strings):
    return map(float, strings)

# this is a hack for some older code.  Not guaranteed to be robust in any fashion, is for dealing with a scalar
def read_single_val(fname):
    scalar_out = __csv_vect_read__(fname)
    return scalar_out[0]

def csv_matrix_read(fname,del_num = None):
    vals = irreg_matrix_read(fname,del_num = del_num)
    return np.array(vals)

def irreg_matrix_read(fname,del_num = None):
    # numpy doesn't deal with irregular arrays happily.  Oddly,
    # it is fine with lists of arrays with different shapes
    tmp = csv.reader(open(fname))
    vals = [] 
    for i in tmp:
        if del_num is not None:
            del i[del_num]
#        print i
        vals.append(np.array(str_2_num(i)))  
    return vals   
    
