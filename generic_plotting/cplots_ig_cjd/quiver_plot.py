'''
This uses the ImageGrid_setup class from cplot_w_ImageGrid 
to draw some quiver plots.

This masks out the zero values.  It also has a control for 
quiver size - scale.  There was an attempt to automise this,
but it's a pain and was taken away from this base plotting file.

the method make_smaller_grid attempts to drop most of the data points,
having 22 arrows in one direction.  This is usually fine, but
sometimes requires more precise control.

Created on 1 Jul 2014

@author: chris
'''
from cplot_w_ImageGrid import ImageGrid_setup
import numpy as np
import pylab as pl

class qplot(ImageGrid_setup):
    def __init__( self, x, y, i_mom, j_mom, r_mom, cbar_label = '', scale = 15, filt = 0.8e7, cmap = 'copper', fig_kwargs = {} ):   
        
        IG_cbar_kwargs = { "cbar_location": "right",
                           "cbar_mode": "single",
                           "cbar_size": "5%",
                           "cbar_pad": 0.3 } 
         
        IG_setup_kwargs_int = { 'xlabel' : '$x$/cm', 
                                'ylabel' : '$y$/cm'
                                }        
        
        super(qplot,self).__init__(x, y, IG_kwargs_ext = IG_cbar_kwargs, fig_kwargs = fig_kwargs, **IG_setup_kwargs_int) 
          
        print np.shape(j_mom)
        self.r_mom_s = self.make_smaller_grid(r_mom)[0]
        self.V  = self.make_smaller_grid(i_mom)[0] 
        self.U  = self.make_smaller_grid(j_mom)[0]
        X_s     = self.make_smaller_grid(self.X)[0]
        Y_s     = self.make_smaller_grid(self.Y)[0] 
              
        UV_max = np.max((np.max(self.V),np.max(self.U)))
        self.U = self.U/UV_max
        self.V = self.V/UV_max     
            
#         self.filt = filt  
#         self.mask_U_V()
        
        '''getting the correct colourmap for velocities going
           through zero '''
        
        self.im = self.ax.quiver( X_s, Y_s, self.V, self.U, self.r_mom_s, width = 0.006, scale = scale, cmap = cmap, pivot = 'tip', rasterized = True  )
        self.gen_cbar(cbar_label)

        pl.figure(self.fig_i)

        pl.draw()  
        limyx = max([max(self.x),max(self.y),np.abs(min(self.y))])
        self.ax.set_xlim(0.0,limyx)
        self.ax.set_ylim(-limyx,limyx)
        
        self.fig.subplots_adjust(left=0.17,bottom=0.07,right=0.85)
#         pl.tight_layout()
        
    def mask_U_V(self):
        
        gap = 0
        
        Mask = np.zeros(self.U.shape, dtype='bool')
        
        for i in range(gap,len(self.U)-gap):
            for j in range(gap,len(self.U[0])-gap):
                if np.abs(self.r_mom_s[i,j]) < self.filt:            
                    for i_mask in np.arange(-gap,gap+1,1):
                        for j_mask in np.arange(-gap,gap+1,1):
                            Mask[i+i_mask,j+j_mask] = True       
                 
        self.U = np.ma.masked_array(self.U, mask=Mask)
        self.V = np.ma.masked_array(self.V, mask=Mask)
                 
    def make_smaller_grid(self,U):
        N_n_max = 22
        I = len(U)
        J = len(U[0])
        
        di = np.int32(J/N_n_max)
        dj = np.int32(J/N_n_max)
        I_n = I/di
        J_n = J/dj
        U_n = np.zeros([I_n,J_n]) 
        for i_n in range(0,I_n):
            i = (i_n)*di
            for j_n in range(0,J_n):
                j = (j_n)*dj
                U_n[i_n,j_n] = U[i,j]
          
        return U_n, di