'''
Uses the Legendre polynomials to generate spherical harmonics

Created on 30 Jan 2013

@author: chris
'''
import numpy as np
import scipy.misc as sc
from Legendre_polys import Legendre_polys

def my_real_sph_harm(l,m_i,theta,phi):
    
    # the maths this code is on page 172 and 174 of lab book 4  

    m = np.abs(m_i)
    
    fact_bit = sc.factorial(l-m)/sc.factorial(l+m)
    N_l_m = np.sqrt( (2*l+1)/(4*np.pi)*fact_bit )
    #print np.shape(theta), np.shape(m), np.shape(l), 'd'
    P_l_m = Legendre_polys(l,m,np.cos(theta))
    #print np.shape(P_l_m), m_i, 'c'
    
    Y_l_m = np.zeros(np.shape(theta))
    
    if m_i > 0:
        Y_l_m = Y_l_m + np.sqrt(2)*N_l_m*P_l_m*np.cos(phi*m)

    elif m_i < 0:
        Y_l_m = Y_l_m + np.sqrt(2)*N_l_m*P_l_m*np.sin(phi*m)
#        print Y_l_m, np.sqrt(2)*N_l_m, P_l_m, 
    
    else:
        Y_l_m = Y_l_m + N_l_m*P_l_m
        #print Y_l_m, N_l_m, P_l_m
    return Y_l_m

def normalised_sph_harm(l,m_i,theta,phi):
    
    # as above, but returning something that has a maximum of zero.
    
    m = np.abs(m_i)
        
    P_l_m = Legendre_polys(l,m,np.cos(theta))
    
    Y_l_m = np.zeros(np.shape(theta))
    
    if m_i > 0:
        Y_l_m = Y_l_m + P_l_m*np.cos(phi*m)

    elif m_i < 0:
        Y_l_m = Y_l_m + P_l_m*np.sin(phi*m)
    
    else:
        Y_l_m = Y_l_m + P_l_m
        
    print 1, Legendre_polys(l,m,1)   
    return Y_l_m    
    