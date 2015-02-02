'''
The underlying plotting class.  It used to also be
the parent class of colour plots, but I switched
away from that.  I think it is only used for linear
plots now, but there's a lot of code referencing this
stuff.

Created on 29 May 2014

@author: chris
'''

import matplotlib.pyplot as plt

class plot(object):
    # plot initialisation
    def __init__(self,fig_i=1,plot_loc=111,xlabel='',ylabel='',title='',sci_limits=(-3,4), figsize=(8, 6),bottom=0.12):
        
        # separate-lines-on-plot counter
        self.__line_i__ = 0
        # fonts set up
        params = {'backend': 'ps', 
                    'axes.labelsize': 24, 
                    'title.fontsize' : 24,
                    'axes.titlesize': 24, 
                    'legend.fontsize': 24, 
                    'xtick.labelsize': 20, 
                    'ytick.labelsize': 20, 
                    'text.usetex': True,
                    #'text.latex.preamble':'\boldmath',
                    'font.family' : 'serif', # sets the latex fonts
                    'font.serif' : ['Computer Modern Roman'],#'Palatino'],
                    'axes.formatter.limits' : sci_limits 
                  } # forcing label notation to a.b*10^{x}
        plt.rcParams.update(params)
        #plt.rcParams['text.latex.preamble'] = [r'\boldmath']
        # figure details set up
        self.fig = plt.figure(fig_i,figsize)          
        
#        print 'subplot location ', plot_loc
        self.ax = self.fig.add_subplot(plot_loc)
        self.fig.subplots_adjust(bottom=bottom,left=0.15)
        
        # axis ticks set up
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('left')   

        # global labels at start
        self.xlabel = xlabel
        if self.xlabel != '': self.xlabel = '\\boldmath \\bf ' + self.xlabel  + ''
        self.ax.set_xlabel(self.xlabel)
        
        self.ylabel = ylabel
        if self.ylabel != '': self.ylabel = '\\boldmath \\bf ' + self.ylabel  + ''
        self.ax.set_ylabel(self.ylabel)
        # print ylabel, xlabel
        
        plt.title(title)
        
        print 'plot initialised' 

    def time_title(self,time,time_symbol='$t$',unit='s'):
        
        from shared_functions import time_title 
        title_str = time_title(time,time_symbol=time_symbol,unit=unit,i_trunk=3)        
        self.title(title_str)
        
    def title(self,title_str):
        title_str = '\\boldmath \\bf ' + title_str + ''
        plt.title(title_str)

    # potential for use later        
    def plot(self):
        pass

    # output as pdf
    def plot2file(self,word,pformat = 'pdf'): 
        fname =  word + '.' + pformat
        self.fig.savefig(fname, format=pformat)#, bbox_inches='tight')
        if pformat == 'pdf':
            import os
            os.system("pdfcrop " + fname + " " + fname )
    # put a legend on with no box
    def leg(self,loc='lower left',leg_kwargs={}):
        # leg = plot_zmp3d.ax.legend(bbox_to_anchor=(1.08, 0.77)) # this shifts the legend around.
        # leg_kwargs={'bbox_to_anchor':(1.08, 0.77)}
        leg = plt.legend(loc=loc,**leg_kwargs)
        leg.get_frame().set_alpha(0.0)
        
    # show the plot
    def show(self):
        plt.show()
        
    def clf(self):
        self.fig.clf()
        #plt.clf()

    def pick_colour(self):
        # might be reimplimenting plt.gca().set_color_cycle() or some such, probably more sensible to use that than below, but bleh.
        colours = [ 'blue', 'black', 'green', 'orange', 'yellow' ]
        self.current_colour = colours[self.__line_i__]
        return self.current_colour
        
    def pick_fmt(self):
        fmts = [ 'o', 'x', '^', 's', 'D' ]
        return fmts[self.__line_i__] 
