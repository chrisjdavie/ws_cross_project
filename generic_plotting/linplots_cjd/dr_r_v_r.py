'''
Plots proportional perturbation size against radius of covergence,
on a semilog plot (log x-axis).

Created on 3 Jul 2014

@author: chris
'''
from dr_v_r import dr_v_r_plot

class dr_r_v_r_plot(dr_v_r_plot):
    
    # uses the semilog_plot library to plot dr/r against r
    
    def __init__(self,r,dr,dr_r_0 = 1.0):

        self.r      = r
        self.dr_r   = dr/r        
        self.dr_r_0 = dr_r_0
        
        self.dr_r = self.dr_r/dr_r_0     
        
        super(dr_v_r_plot,self).__init__(r,self.dr_r)    
        
    def plot_init(self,xlabel='$r$',ylabel='$\delta{r}/r$',x_out = None,linear_plot_init_kwargs={}):  
        super(dr_r_v_r_plot,self).plot_init(ylabel=ylabel,xlabel=xlabel,x_out = x_out,linear_plot_init_kwargs=linear_plot_init_kwargs)
                  
    def plot(self,ax=None,l=None,semilog_kwargs={}):
#             semilog_kwargs = { "label":'8192x4096',
#                        "linewidth":5,
#                        "colour":'g',
#                        "linestyle":':',
#                        "label":'bob'
#                       }
        super(dr_r_v_r_plot,self).plot(ax=ax,l=l,semilog_kwargs=semilog_kwargs)      

    def add_line(self,new_dr,new_r=None,label=''):
        if new_r == None: new_r = self.r
        dr_r = new_dr/new_r
        super(dr_r_v_r_plot,self).add_line(dr_r,new_r,label)