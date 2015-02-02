'''
ZeusMP 1D output file directory management

Created on 17 Sep 2014

@author: chris
'''
from base import base_dir

class zeus1d_dir(base_dir):
    
    def __init__(self,run_dir):
        from oned_circ_file import zeus1d_file
        
        super(zeus1d_dir,self).__init__(run_dir,'hdfaa.',zeus1d_file)