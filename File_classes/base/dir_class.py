'''
The base class for functions over a directory of data files output from a hydrodynamics simulation.  Plots physical quantities, mainly.

These directories use files output from my post-processing 
routines, whatever they do (sometimes just sorting).

Created on 27 Aug 2014

@author: chris
'''
import matplotlib.pyplot as pl

class base_dir(object):
    '''
    classdocs
    '''


    def __init__(self,run_dir,op_str,file_class):
        '''
        run_dir - the directory of the code being run
        op_str - the string that indicates the output is from the simulation
        file_class - the class that manages the file, has different levels of 
                     generality (see plot_file.py)
        
        Constructor
        '''
        self.pp_dir  = run_dir + 'sensible_hdfs/'
        
        from os_fns import open_file_list
        tmp_dirlist = open_file_list(self.pp_dir)
        
        self.pp_dirlist = [ dirname +'/' for dirname in tmp_dirlist if op_str in dirname ]
        self.file_class = file_class
        
    def rho_cplots(self,x_bound=None,pcolormesh_kwargs={}): 
        def fn(ff):
            p = ff.rho_cplot(x_bound=x_bound,pcolormesh_kwargs=pcolormesh_kwargs)
#             p.overlayshk()
            p.savetofdir()
#             print ff.t
#             p.show()
            pl.close(p.fig)
            return p
        self._fn_over_pp_dirs(fn)
             
    def rho_lineouts(self,xlims=None):
        def fn(ff):
            p = ff.plot_rho_line_out()
            if xlims != None: p.ax.set_xlim(xlims)
            p.savetofdir(ftype='png')
            pl.close(p.fig)
            return p
        self._fn_over_pp_dirs(fn)
             
    def P_lineouts(self):
        def fn(ff):
            p = ff.plot_P_line_out()
            p.savetofdir(ftype='png')
            pl.close(p.fig)
            return p
        self._fn_over_pp_dirs(fn)
                
    def v_r_lineouts(self,xlims=None):
        def fn(ff):
            p = ff.plot_v_r_line_out()
            if xlims != None: p.ax.set_xlim(xlims)
            p.savetofdir(ftype='png')
            pl.close(p.fig)
            return p
        self._fn_over_pp_dirs(fn)
                    
    def _fn_over_pp_dirs(self,fn):
        '''runs the function fn on each file in the directory'''
        import gc
        for pp_dir in self.pp_dirlist:
            print pp_dir
            f = self.file_class(pp_dir)
            fn(f)
            gc.collect()        