'''
Colourplotting.  ImageGrid gives finer control over positioning of components
of a plot than the default matplotlib implimentation, but is also a bit harder
to deal with.

Class structure -
ImageGrid_setup - plot-type agnostic functions
cplot_plot      - basic colour plot, inherits from ImageGrid_setup
phys_cplot      - automates plotting of hydrodynamic variables, creates a consistent
                  colour scheme and labelling for each.  Inherits from cplot_plot
R_Z_cplot       - Plots R, Z cylindrical polar colourmaps.  Inherits from cplot.  Should inherit
                    from phys_cplot but that would involve significant refactoring and testing
phi-theta cplot - Plots phi, theta plots.  Inherits from cplot_plot.  Usually used
                    for surface plots.

Created on 28 Sep 2012

@author: chris
'''
from mpl_toolkits.axes_grid1 import ImageGrid
import pylab as plt
import numpy as np

class ImageGrid_setup(ImageGrid):
    def __init__(self,x,y,fig_i=1,nrows = 1, ncols = 1, title='', IG_kwargs_ext = {}, ylabel = '', xlabel = '', fig_kwargs = {}, font_setup_kwargs = {} ):
        
        self.fig = plt.figure(**fig_kwargs)
        self.x = x
        self.y = y
        self.fig_i = fig_i
        
        print font_setup_kwargs
        plot_font_setup(**font_setup_kwargs)
        
#        plt.xlabel('Z/cm')
        IG_kwargs_int = { "nrows_ncols": (nrows, ncols),
                      "direction": "row",
                      "axes_pad": 0.3,
                      "aspect": False
                     }
        
        IG_kwargs = dict(IG_kwargs_int, **IG_kwargs_ext)
        #print IG_kwargs
        super(ImageGrid_setup,self).__init__( self.fig, 111,
                                              **IG_kwargs
                                              )
        if ylabel != '': ylabel = '\\boldmath \\bf '+ylabel+''
        self[0].set_ylabel(ylabel)
        if xlabel != '': xlabel = '\\boldmath \\bf '+xlabel+''
        self[0].set_xlabel(xlabel)
        
        self.X,self.Y = plt.meshgrid(x,y)
        
        #print font_setup_kwargs
        #raw_input()
        #plot_font_setup(font_setup_kwargs)
        
        self.ax = self[0]
#        plt.title(title)
        self.ax.set_title(title)

    def time_title(self,time,time_symbol='$t$',unit='s',pre_str=''):
        
        if pre_str != '':
            pre_str += ', '
        from shared_functions import time_title 
        
        title_str = time_title(time,time_symbol='$t$',unit=unit)        
        self.set_title(pre_str+title_str)
        
    def set_title(self,title_str,x_pos=0.5):
        title_str = '\\boldmath \\bf '+title_str+''
        
#         print title_str
        self.title_str = self.ax.set_title(title_str,x=x_pos)
        #self.tt.set_x(0.6) 
                
    def plot2file(self,word,pformat = 'png'):  
        fname =  word + '.' + pformat
        self.fig.savefig(fname, format=pformat)#, bbox_inches='tight')
        if pformat == 'pdf':
            import os
            os.system("pdfcrop " + fname + " " + fname )        
        #self.fig.savefig(word + '.' + pformat,format=pformat)
              
    def show(self):
        plt.show() 
        
    def clf(self):
        plt.clf()
        plt.close(self.fig)
        

    def overlay_shk(self,fnum_str,csv_dir):
        from import_data import vect_read
        self.thetas = vect_read( csv_dir + 'thetas/' + fnum_str + '.csv' )
        self.rs     = 10.0*vect_read( csv_dir + 'rshkfs/' + fnum_str + '.csv' )
        
        plot_kwargs={'color':[0.0,0.647,0.314],'linestyle':'-','linewidth':4}
        add_line_kwargs = {'dash_seq':[10,10]}
        self.__line_from_polars__(plot_kwargs=plot_kwargs,add_line_kwargs=add_line_kwargs)
        
    def line_from_polars(self,rs,thetas,plot_kwargs={},add_line_kwargs={}):
        #int_line_kwargs={ 'dash_seq':[10, 10] }
        self.thetas = thetas
        self.rs     = rs
        self.__line_from_polars__(plot_kwargs=plot_kwargs,add_line_kwargs=add_line_kwargs)
        
    def __line_from_polars__(self,plot_kwargs={},add_line_kwargs={}):
        Zs = self.rs*np.cos(self.thetas)
        Rs = self.rs*np.sin(self.thetas)
        
        #from linplots_cjd import linear_plot
        self.add_line(Rs,Zs,plot_kwargs=plot_kwargs,**add_line_kwargs)
#         R_v_Z = linear_plot(Rs,Zs)
#         #R_v_Z.plot_init()
#         R_v_Z.plot(ax=self.ax,**linear_plot_kwargs)
        
    def add_line(self,x,y,dash_seq=[10,10],plot_kwargs={'color':[0.0,0.647,0.314],'linewidth':4}):
        # plot_kwargs={'color':[0.0,0.647,0.314],'linestyle':'-','linewidth':4}
#         print 'hi dan'
        p = self.ax.plot(x,y,**plot_kwargs)
        if dash_seq != None:
            p[0].set_dashes(dash_seq)

    def centred_resize_z2d_xy_n_coords(self,Dx_plot):
        self.ax.set_aspect('equal', adjustable='box')
#         print "this"
#         self.Dx_plot = Dx_plot
#         g_d = 1.05  
#         y_max = np.max(self.y)
#         pc_Dy = Dx_plot/y_max/2*g_d
#         J     = len(self.y)
#         Dj    = np.round(J*pc_Dy)
#         
#         self.j_l = J/2-Dj
#         self.j_r = J/2+Dj
#         print min(self.y), max(self.y)
#         self.y = self.y[self.j_l:self.j_r]        
#         print min(self.y), max(self.y)
#         
#         x_max = np.max(self.x)
#         self.zoom_rat = Dx_plot/x_max*g_d
#         I     = len(self.x)
#         Di    = np.round(I*self.zoom_rat)
#         
#         self.i_l = 0
#         self.i_r = Di
#         #print min(self.x), max(self.x)
#         self.x = self.x[self.i_l:self.i_r]
#         #print min(self.x), max(self.x)
#         self.X,self.Y = plt.meshgrid(self.x,self.y)        

    
    def centred_zoom(self,Dx_plot):
        g_p = 1.001
        self.ax.set_xlim([self.ax.get_xlim()[0],Dx_plot*g_p])
        self.ax.set_ylim([-Dx_plot*g_p,Dx_plot*g_p])
#         print "that"
        
    def centred_zoom_xy(self,Dx_plot):
        g_p = 1.001
        self.ax.set_xlim([-Dx_plot*g_p,Dx_plot*g_p])
        self.ax.set_ylim([-Dx_plot*g_p,Dx_plot*g_p])        
        #
    def centred_zoom_xy_upper(self,Dx_plot):
        g_p = 1.001
        self.ax.set_xlim([self.ax.get_xlim()[0],Dx_plot*g_p])
        self.ax.set_ylim([self.ax.get_ylim()[0],Dx_plot*g_p])        
        
    def gen_cbar(self,cbar_label):
        self.cbar = plt.colorbar(self.im, self.ax.cax)

#         print dir(cbar)
#         from matplotlib.ticker import MaxNLocator
#         cbar.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
#         cbar.update_ticks()
#         raw_input()
        ''' the following line can cause difficulties, specifically
            in the case of transparencies in the plot.
            It is introduced to suppress errors in vector viewers 
            which will introduce white lines in the colour bar'''
        self.cbar.solids.set_edgecolor("face")
        if cbar_label != '': cbar_label = '\\boldmath \\bf ' + cbar_label + ''
        self.cbar.set_label(cbar_label) 
        
class cplot_plot(ImageGrid_setup):
    def __init__( self, x, y, cp_dat,cbar_label = '', axis_zoom_rat=1.0, Dx_plot=0, IG_setup_kwargs_ext = {}, fig_kwargs = {}, pcolormesh_kwargs = {}, font_setup_kwargs = {}):
        
        self.cp_dat = cp_dat
#        fig_kwargs = { "num":1,
#                       "figsize":( 8, 6 ) #inches
#                     }
#        # IG_setup_kwargs_ext = { 'title':var_name + ', ' + str(t)+'/s' +', ' +  fname[-3:], 
#                                  'xlabel' : '$R$/cm', 
#                                  'ylabel' : '$Z$/cm'}
#        pcolormesh_kwargs = { "cmap" :'jet',
#                              "vmin" : vmin,
#                              "vmax" : vmax }
#
#        font_setup_kwargs = { 'sci_lims':(2,3) }

        IG_cbar_kwargs = { "cbar_location": "right",
                           "cbar_mode": "single",
                           "cbar_size": "5%",
                           "cbar_pad": 0.3 }
        
        super(cplot_plot,self).__init__(x,y, IG_kwargs_ext = IG_cbar_kwargs, fig_kwargs = fig_kwargs, font_setup_kwargs = font_setup_kwargs, **IG_setup_kwargs_ext )
#        vmax = np.max(cp_dat)
#        #print "vmax = ", vmax
#        if vmin is None:
#            vmin = np.min(cp_dat)
#        #print "vmin = ", vmin
        
        if (np.shape(self.X) != np.shape(self.Y)) or (np.shape(cp_dat) != np.shape(self.X)) or (np.shape(cp_dat) != np.shape(self.Y) ):
            print "X-grid shape", np.shape(self.X),"Y-grid shape", np.shape(self.Y), "Z-grid shape", np.shape(cp_dat)
            print "The grids and data are not the same shape. \nAlthough something may appear on the screen, it probably won't be an accurate reflection of the data you're trying to plot. \nIf the shape of the grids are a transpose of the shape of the data, \nit may be that you've got your indexes pointed the Fortran way round in your data analysis (x,y,z) rather than the c-esq way (z,y,x)"
           


           
        '''rasterized - pdf friendly'''         
        self.im = self.ax.pcolormesh(self.X,self.Y,self.cp_dat,rasterized=True,**pcolormesh_kwargs)
        self.ax.set_xlim(min(self.x),max(self.x))
        self.ax.set_ylim(min(self.y),max(self.y))
 
#        print np.min(cp_dat), np.max(cp_dat)
#        print np.min(self.X), np.max(self.X)


        plt.figure(self.fig_i)

        
        self.Dx_plot = Dx_plot
        self.zoom_rat = 1.0
        resize_q = self.Dx_plot > 1.0e-15        
        if resize_q:
            if np.abs(np.min(x))*1.01 <  np.abs(np.max(x)) and np.abs(np.min(y))*1.01 <  np.abs(np.max(y)):
                self.centred_zoom_xy_upper(Dx_plot)
            else:
                self.centred_zoom(self.Dx_plot)
            self.centred_resize()
        else:
            self.Dx_plot = plt.xlim()[1]
        
        plt.draw()       
                        
        self.gen_cbar(cbar_label)
                         
        #print self.x[53], "self.x"

    def centred_resize(self):
        #print np.shape(self.cp_dat), np.shape(self.x), np.shape(self.y)
        self.centred_resize_z2d_xy_n_coords(self.Dx_plot)
#         self.cp_dat = self.cp_dat[self.j_l:self.j_r,self.i_l:self.i_r]
        #print np.shape(self.cp_dat), np.shape(self.x), np.shape(self.y)
        
    def _circ_arrows(self,out_q=False,len_adj=1.0):
        dirn = 1.0
        if out_q:
            dirn = -1.0        
    
        r_0 = 0.64

        Dr = r_0/20.0
        
        g_d = 1.50*len_adj
        x_max = np.max(self.x)
        self.zoom_rat = self.Dx_plot/x_max*g_d
        
        n_arr = 5
        for i in np.arange(0,n_arr):
            k_arrow = (i+0.5)*(len(self.thetas) - 1)/n_arr
            theta_arr = self.thetas[k_arrow]
            r_arr = self.rs[k_arrow]
            
            dz = Dr*np.cos(theta_arr)
            dR = Dr*np.sin(theta_arr)
            addn = 3.0*dirn*Dr*self.zoom_rat
            z_arr = (r_arr+addn)*np.cos(theta_arr) 
            R_arr = (r_arr+addn)*np.sin(theta_arr)
            self.ax.arrow(R_arr,z_arr,-4*dirn*dR*self.zoom_rat,-4*dirn*dz*self.zoom_rat,color=[0.0,0.647,0.314], head_length=0.05*self.zoom_rat, head_width=0.04*self.zoom_rat, width=0.005*self.zoom_rat)

    def plot_circle(self,radius,colour=[30.0/255,144.0/255,255.0/255],dash_seq=[10,10,4,10]):
        plot_kwargs={'color':colour,'linestyle':'-','linewidth':4}
        add_line_kwargs = {'dash_seq':dash_seq}        
        
        n = 100
        thetaa = np.arange(0,np.pi,np.pi/n)
        RR = np.zeros_like(thetaa) + radius
        self.line_from_polars(RR,thetaa,plot_kwargs=plot_kwargs,add_line_kwargs=add_line_kwargs)


class phys_cplot(cplot_plot):
    def __init__(self,x,y,cp_dat,var='rho',var_units=r'',axis_units=r'',fig_kwargs = {}, font_setup_kwargs={}, cplot_plot_kwargs = {}, pcolormesh_kwargs = {}):
#        fig_kwargs = { "num":1,
#                       "figsize":( 8, 6 ) #inches
#                     }
#        font_setup_kwargs={'sci_lims':(-3,2)}
        if axis_units != '':  axis_units = '/' + axis_units
        cbar_label, pcolormesh_kwargs_phys = phys_cbar_lab_prep(var_units,var,cp_dat)
        pcolormesh_kwargs = dict(pcolormesh_kwargs_phys,**pcolormesh_kwargs)
        super(phys_cplot,self).__init__(x,y,cp_dat,IG_setup_kwargs_ext={'xlabel': '$x$' + axis_units,'ylabel': '$y$' + axis_units},cbar_label = cbar_label,pcolormesh_kwargs = pcolormesh_kwargs,fig_kwargs = fig_kwargs, font_setup_kwargs = font_setup_kwargs,**cplot_plot_kwargs)

def phys_cbar_lab_prep(units,var,cp_dat):
    if units != '':
        units = '/' + units
    if var == 'rho':
        pcolormesh_kwargs = { "cmap" :'gist_heat_r'}
        cbar_label = r'$\rho$' + units
    elif var == 'e':
        pcolormesh_kwargs = { "cmap" :'bone_r'}
        cbar_label = r'$\epsilon$' + units
    elif var == 'P':
        pcolormesh_kwargs = { "cmap" :'bone_r'}
        cbar_label = r'$P$' + units        
    elif var[:2] == 'v_':
        vmin = np.min(cp_dat)
        vmax = np.max(cp_dat)
        vmax = np.max((vmax,-vmin))
        pcolormesh_kwargs = { "cmap" :'RdBu','vmax':vmax,'vmin':-vmax}
        if var[2] == 'x':
            cbar_label = r'$v_x$' + units   
        if var[2] == 'y':
            cbar_label = r'$v_y$' + units     
        if var[2] == 'r':
            cbar_label = r'$v_r$' + units                     
    return cbar_label, pcolormesh_kwargs
 
class R_Z_cplot(cplot_plot):
    def __init__(self, RR, ZZ, SSS, fig_kwargs_ext = {}, pcolormesh_kwargs = {}, IG_setup_kwargs_ext ={}, cbar_label = '', cplot_plot_kwargs = {}):
        RR = 10*RR
        ZZ = 10*ZZ
        
        fig_kwargs_int = { "figsize":(5.75,8) } 
        if (np.abs(np.min(ZZ))*100.0 < np.max(ZZ) and np.abs(np.min(RR)*100.0) < np.max(RR)):
            fig_kwargs_int = {}
            
        fig_kwargs = dict(fig_kwargs_int, **fig_kwargs_ext)
        
        pcolormesh_kwargs_int = { }
        pcolormesh_kwargs = dict(pcolormesh_kwargs_int, **pcolormesh_kwargs)
 
        IG_setup_kwargs_int = { 'xlabel' : '$R$/mm', 
                                'ylabel' : '$Z$/mm'
                                }
        IG_setup_kwargs = dict(IG_setup_kwargs_int, **IG_setup_kwargs_ext)
        #cplot_plot_kwargs = { 'Dx_plot':1.05 }
        super(R_Z_cplot,self).__init__(RR,ZZ,SSS,cbar_label = cbar_label,fig_kwargs=fig_kwargs,IG_setup_kwargs_ext = IG_setup_kwargs,pcolormesh_kwargs = pcolormesh_kwargs, **cplot_plot_kwargs )
        self.fig.subplots_adjust(left=0.18,bottom=0.1,top=0.93,right=0.85)
#         print self.fig
        
    def shkf_n_arrows(self,fnum_str,csv_dir,out_q=False,len_adj=1.0):
        self.overlay_shk(fnum_str,csv_dir)
        self._arrows(out_q=out_q,len_adj=len_adj)
        
    def _arrows(self,out_q=False,len_adj=1.0):
        self._circ_arrows(out_q, len_adj)
    
class phi_theta_cplot(cplot_plot):
    def __init__(self,phis,thetas,s,IG_setup_kwargs_ext={},pcolormesh_kwargs = { "cmap" :'spring' },cbar_label='r/r$_0$'):
        
        IG_setup_kwargs_int = { 'xlabel' : '$\phi$', 
                                'ylabel' : '$\\theta$' } 
        
        IG_setup_kwargs = dict(IG_setup_kwargs_int, **IG_setup_kwargs_ext)
        
        super(phi_theta_cplot,self).__init__(phis,thetas,s,cbar_label = cbar_label,IG_setup_kwargs_ext = IG_setup_kwargs,pcolormesh_kwargs = pcolormesh_kwargs )
        
        xticks = [ 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi ]
        self.ax.set_xticks(xticks)
        self.ax.xaxis.set_ticklabels( [ "$0$", "$\pi/2$", "$\pi$", "$3\pi/2$", "$2\pi$" ] )
        
        yticks = [ 0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi ]
        self.ax.set_yticks(yticks)
        self.ax.yaxis.set_ticklabels( [ "$0$", "$\pi/4$", "$\pi/2$", "$3\pi/4$", "$\pi$" ] )
        self.fig.subplots_adjust(left=0.15,bottom=0.15,right=0.85,top=0.95)
        
def plot_font_setup(big_font=24,small_font=20,sci_lims=(-1,2)):
        # fonts set up
    print 'sci_lims', sci_lims
    params = {'backend': 'ps', 
                'axes.labelsize': big_font, 
                'title.fontsize' : big_font,
                'axes.titlesize': big_font, 
                'legend.fontsize': big_font, 
                'xtick.labelsize': small_font, 
                'ytick.labelsize': small_font, 
                'text.usetex': True,
                'font.family' : 'serif', # sets the latex fonts
                'font.serif' : ['Computer Modern Roman'],#'Palatino'],
                'axes.formatter.limits' : sci_lims } # forcing label notation to a.b*10^{x}
    plt.rcParams.update(params)        
    