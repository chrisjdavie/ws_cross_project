'''
Takes a directory from ZeusMP and manipulates it.    Replaced with classes in File_classes (used
for hydro-simulations more generally, and learnt some structure lessons from this).

Zeus_dir - standard simulation directory structure.
Zeus_1d_dir - 1d Zeus simulations

Created on 29 Jul 2014

@author: chris
'''

class Zeus_dir(object):
    '''
    classdocs
    '''


    def __init__(self,base_dir):
        '''
        Constructor
        '''
        self.base_dir   = base_dir
        self.hdf_dir    = base_dir + 'zeus/exe90/'
        
        from os_fns import open_file_list
        
        flist = open_file_list(self.hdf_dir)
        self.fname_list = [ f for f in flist if f[-9:-4] == 'hdfaa' ]
        
from base_Zeus import Zeus_1d_file
        
class Zeus_1d_dir(Zeus_dir):
        
    def rho_lin_plots(self,pic_dir='/tmp/zmp/'):
        
        for fname in self.fname_list:
            f = Zeus_1d_file(fname)
            f.plot_density()
            f.rho_v_r.plot2file_i(pic_dir)
            f.rho_v_r.clf()
            print f.fnum_str            