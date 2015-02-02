'''Plots a semi-log x axis against a linear y-axis.

It is, I think, only used for perturbation size, as it reflects
the underlying physics of that behaviour, but I've split it up
for clarity.  Both bits do quite a lot of stuff.'''

from linear_plot import linear_plot
import matplotlib.pyplot as plt
import numpy as np

class semilog_plot(linear_plot):
    
    def __init__(self,x,y):
        super(semilog_plot,self).__init__(x,y)
        
    #if you were trying to pass title as a keyword argument, this is now included in plot_init_kwa
    def plot_init(self,xlabel='',i_end_buffer=0,bit_of_label_on_axis_centre='center',x_out = 1.0,linear_plot_init_kwargs={}):
        #print plot_init_kwa
#         linear_plot_init_kwargs = { 'fig_i':1, 'ylabel':'dr','plot_loc':111,'sci_limits':(-1,1) }
        super(semilog_plot,self).plot_init(xlabel=xlabel,**linear_plot_init_kwargs)
        self.ax.spines['bottom'].set_position('zero')
        
        # making the graph run from x_in to x_out in prep for a log plot which doesn't like zeroes
        x_out = x_out
        self.i_x_end = np.argmin(self.x)-i_end_buffer
        x_in = self.x[self.i_x_end]
        #print 'x_in = ', x_in, 'x_out', x_out
        plt.xlim(x_in, x_out)
        plt.xlim(plt.xlim()[::-1])         
        
        # horizontal alignment is the horizontal alignment of the label relative to the centre of the axis.  This seems absurd.  
        #  Found options are 'left', 'right', 'centre'
        if (xlabel != None) and (xlabel != ''): xlabel = '\\boldmath \\bf ' + xlabel + ''
        plt.xlabel( xlabel, horizontalalignment = bit_of_label_on_axis_centre)
            
    def plot(self,ax=None,y=None,colour='b',linestyle='-',label='',linewidth=2):
        if ax is None:
            ax = self.ax
        if y is None:
            y = self.y
        super(linear_plot,self).plot()
        if (label != None) and (label != ''): label = '\\boldmath \\bf ' + label + ''
        self.p = ax.semilogx(self.x,self.y,label=label,color=colour,linestyle=linestyle,linewidth=linewidth)    
        self.__line_i__ += 1
