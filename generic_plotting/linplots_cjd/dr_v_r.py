'''
Plots perturbation size against raidius.  On a semilog 
plot (log x-axis).

Created on 3 Jul 2014

@author: chris
'''
from semilog_plot import semilog_plot
# import numpy as np

class dr_v_r_plot(semilog_plot):
    
    # uses the semilog_plot library to plot dr/r against r
    
    def __init__(self,r,dr,dr_0 = 1.0):    

        dr = dr/dr_0     
        
        super(dr_v_r_plot,self).__init__(r,dr)    
        
    def plot_init(self,xlabel='$r$',ylabel='$\delta{r}$',x_out=None,linear_plot_init_kwargs={}):
        if x_out is None:
            x_out=max(self.x)
        linear_plot_init_kwargs= dict({'ylabel':ylabel},**linear_plot_init_kwargs)
        super(dr_v_r_plot,self).plot_init(xlabel=xlabel,x_out=x_out,linear_plot_init_kwargs=linear_plot_init_kwargs)
             
    def plot(self,ax=None,l=None,semilog_kwargs={}):
#             semilog_kwargs = { "label":'8192x4096',
#                        "linewidth":5,
#                        "colour":'g',
#                        "linestyle":':'
#                       }
        if ax is None:
            ax = self.ax
        label_overwrite = {}
        if l is not None:
            label = '$l =' + str(l) +'$'
            label_overwrite ={ "label":label }
            
        semilog_kwargs = dict(semilog_kwargs.items() + label_overwrite.items())
        super(dr_v_r_plot,self).plot(ax=ax,**semilog_kwargs)      
