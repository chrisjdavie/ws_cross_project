'''
Expresses the spherical harmonics as perturbations from 
spherical symmetry, as used in my research.

Created on 30 Jan 2013

@author: chris
'''
import numpy as np
from my_real_sph_harm import my_real_sph_harm
# import scipy.misc as sc

def main():
    l = 4 
    m = 2
    
    r, theta, phi = pert_sphere(l,m)
    
    print np.shape(r), np.shape(theta), np.shape(phi)
    print np.min(r)
    
    cos = np.cos
    sin = np.sin
    
    x = r*sin(theta)*cos(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(theta) 
       
    from mayavi import mlab    

    mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(400, 300))
    mlab.clf()
    print np.shape(theta), np.shape(phi)
    s = my_real_sph_harm(l, m, theta, phi)
    print np.shape(s)
    mlab.mesh(x, y, z, scalars = r, colormap='jet')
    
    mlab.axes()
    
    mlab.show() 

def pert_sphere(l,m):
    
    pi = np.pi
    
    thetass, phiss = np.mgrid[0:pi:101j, 0:2*pi:202j]
    #print np.shape(thetass), np.shape(phiss)

    #print "max theta", thetass.max()

    r_0 = 6.35620e-2
    Ep = 0.2
    
    s = my_real_sph_harm(l, m, thetass, phiss)
    print np.min(s)
    print np.max(s)
    s /= s.max()
    
    rss = r_0*(1 + s*Ep)
    
    return rss, thetass, phiss

if __name__ == '__main__':
    main()