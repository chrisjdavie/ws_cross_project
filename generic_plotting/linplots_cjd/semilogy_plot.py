'''Plots a linear x-axis and a log y-axis.'''

from linear_plot import linear_plot
# import matplotlib.pyplot as pl
# import numpy as np

class semilogy_plot(linear_plot):
    
#     def __init__(self,x,y):
#         super(semilogy_plot,self).__init__(x,y)
        
#     def plot_init(self,ylabel='',i_end_buffer=0,bit_of_label_on_axis_centre='center',y_out = 1.0,linear_plot_init_kwargs={}):
#         super(semilogy_plot,self).plot_init(**linear_plot_init_kwargs)
        
#         pl.xlim(np.min())
        
#         if (ylabel != None) and (ylabel != ''): ylabel = '\\boldmath \\bf ' + ylabel + ''
        
        
    def plot(self,ax=None,y=None,colour='b',linestyle='-',label='',linewidth=2):
        if ax is None:
            ax = self.ax
        if y is None:
            y = self.y
        super(linear_plot,self).plot()
        if (label != None) and (label != ''): label = '\\boldmath \\bf ' + label + ''
        self.p = ax.semilogy(self.x,self.y,label=label,color=self.pick_colour(),linestyle=linestyle,linewidth=linewidth)    
        self.__line_i__ += 1
        
    def add_line(self,new_y,new_x=None,label=''):
        if new_x == None: new_x = self.x
        if label != '' or label != None: label = '\\boldmath \\bf ' + label + ''
        self.ax.plot(new_x,new_y,color=self.pick_colour(),linestyle=self.pick_linestyle(),linewidth=2,label=label)
        self.__line_i__ += 1    
        
class semilogy_scatter(linear_plot):
    
    def plot(self,ax=None,y=None,colour='b',label=''):
        if ax is None:
            ax = self.ax
        if y is None:
            y = self.y
        super(linear_plot,self).plot()
        if (label != None) and (label != ''): label = '\\boldmath \\bf ' + label + ''
        self.p = ax.semilogy(self.x,self.y,label=label,color=self.pick_colour(),linestyle='',marker=self.pick_fmt())    
        self.__line_i__ += 1
        
                
    def leg(self,loc='lower left',leg_kwargs={}):
        leg_kwargs=dict({'numpoints':1},**leg_kwargs)
        super(linear_plot,self).leg(loc=loc,leg_kwargs=leg_kwargs)        
    