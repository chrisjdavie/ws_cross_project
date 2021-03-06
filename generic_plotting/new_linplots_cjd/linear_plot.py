from plot_root import plot
        
class linear_plot(plot):
    # set up x and y
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
#    def quick_plot(self,xlabel='',ylabel='',title='',plot_loc=111,colour='b',linestyle='-',label='',linewidth=1):
#        self.plot_init(xlabel=xlabel,ylabel=ylabel,title=title,plot_loc=111)
#        self.plot(colour=colour,linestyle=linestyle,label=label,linewidth=linewidth)
        
    # this initialises axis - often need two linear plots on one axis
    def plot_init(self,*args,**kwargs):
        self._plot_init(args,kwargs)
    
    def _plot_init(self,fig_i=1,xlabel='',ylabel='',title='',plot_loc=111,sci_limits=(-2,2),plot_init_kwargs={}):
#        print xlabel
        self.fig_i = fig_i
        super(linear_plot,self).__init__(self.fig_i,plot_loc=plot_loc,xlabel=xlabel,ylabel=ylabel,title=title,sci_limits=sci_limits,**plot_init_kwargs)
        self.ax.spines['top'].set_color('none')
        self.ax.spines['right'].set_color('none')
        
    # simple linear plot, can be provided with external axis or use the ones generated by self.plot_init()
    def _plot(self,ax=None,y=None,colour=None,linestyle=None,label='',linewidth=2,marker='',dash_seq=None,plot_kwargs={}):
        #plot_kwargs={'zorder':1}
        if ax != None:
            self.ax = ax
        if y is None:
            y = self.y
        if colour    == None: colour = self.pick_colour() 
        if linestyle == None: linestyle = self.pick_linestyle()
        super(linear_plot,self).plot()
        if label != '' or label != None: label = '\\boldmath \\bf ' + label + ''
        self.p = self.ax.plot(self.x,y,color=colour,linestyle=linestyle,linewidth=linewidth,label=label,marker=marker,**plot_kwargs)
        # as this is initialised in super(linear_plot,self).__init__(), it doesn't appear if we don't
        # run self.plot_init().  Probably need to pass the other plot into here and then attach a number
        # or some such.  What would be best is if we could have this in the .plot, probably matplotlib
        # has this - it has nearly everything else.  might be related to gca().lines[-1].
        self.__line_i__ += 1
        if dash_seq is not None:
            self.p[0].set_dashes(dash_seq)

    def add_line(self,new_y,new_x=None,label=''):
        if new_x == None: new_x = self.x
        if label != '' or label != None: label = '\\boldmath \\bf ' + label + ''
        self.ax.plot(new_x,new_y,color=self.pick_colour(),linestyle=self.pick_linestyle(),linewidth=2,label=label)
        self.__line_i__ += 1

    def pick_linestyle(self):
        styles = [ '-', '--', '-.' ]
        return styles[self.__line_i__]