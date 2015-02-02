'''Does a scatter plot.  Inherits from plot, not linear plot,
although I could have done it either way (it's an oddity of how
matplotlib operates, very consistent across both scatter and linear
plotting.'''

from plot_root import plot

class scatter_plot(plot):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def plot_init(self,fig_i=1,plot_init_kwargs={}):
        #plot_init_kwargs = { 'xlabel':'','ylabel':'','title':'','plot_loc':111,'sci_limits':(-2,2) }
        super(scatter_plot,self).__init__(fig_i,**plot_init_kwargs)
        self.ax.spines['top'].set_color('none')
        self.ax.spines['right'].set_color('none')         
        
    def plot(self,ax=None,fmt=None,colour=None,errbar_kwargs={},label=''): 
        #errbar_kwargs={'yerr':es, 'capthick':2, 'zorder':2}
        if ax is not None: self.ax = ax
        if fmt   == None: fmt   = self.pick_fmt()
        if colour == None: colour = self.pick_colour()
        if label != '' or label != None: label = '\\boldmath \\bf ' + label + ''
        super(scatter_plot,self).plot()
        self.p = self.ax.errorbar(self.x,self.y,fmt=fmt,color=colour,label=label,**errbar_kwargs)
        self.__line_i__ += 1
    
    def add_line(self,new_y,new_x=None,label=''):
        if new_x == None: new_x = self.x
        if label != '' or label != None: label = '\\boldmath \\bf ' + label + ''
        self.ax.errorbar(new_x,new_y,fmt=self.pick_fmt(),color=self.pick_colour(),label=label)
        self.__line_i__ += 1
    
                
    def leg(self,loc='lower left',leg_kwargs={}):
        leg_kwargs=dict({'numpoints':1},**leg_kwargs)
        super(scatter_plot,self).leg(loc=loc,leg_kwargs=leg_kwargs)

