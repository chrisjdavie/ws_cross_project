'''
returns files in a directory

Created on 29 May 2014

@author: chris
'''
import os

def open_file_list(file_dir):
    files_tmp = os.listdir(file_dir)
    files_tmp.sort()  
    files_tmp = [ file_dir + i for i in files_tmp ]
    return files_tmp