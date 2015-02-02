'''
ZeusMP 2D output file directory management

Created on 27 Aug 2014

@author: chris
'''
from base import base_dir

class zeus_dir(base_dir):
    
    def __init__(self,run_dir):
        from twod_plan_file import zeus_file
        
        super(zeus_dir,self).__init__(run_dir,'hdfaa.',zeus_file)