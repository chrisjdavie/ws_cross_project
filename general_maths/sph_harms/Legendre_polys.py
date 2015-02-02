'''
This generates the legendre polynomials, using the recursive definition
found in wikipedia (and checked using other sources)

Created on 30 Jan 2013

@author: chris
'''

import numpy as np
import scipy.misc as sc

def Legendre_polys(l,m,x):
    
    # the maths and flowchart for this code is on page 172 and 174 of lab book 4 

    l_i = 0
    m_j = 0
    
    P_l_m = 1
    # this sets up the equivalence between m and -m in Legendre polynomials.  See page 3 labbook 5.
    if m < 0:
        m = np.abs(m)
        P_l_m = np.power(-1,m)*sc.factorial(l-m)/sc.factorial(l+m)*P_l_m
        
    P_l_l = P_l_m
    P_lm1_m = 0
    
    while m_j < m:
        P_lp1_lp1 = -(2*l_i+1)*np.sqrt(1-x*x)*P_l_l
        l_i = l_i + 1
        m_j = l_i
        P_l_l = P_lp1_lp1
        P_l_m = P_l_l
        
    if l_i < l:
        P_lp1_l = x*(2*l_i+1)*P_l_l
        l_i = l_i + 1
        P_lm1_m = P_l_l
        P_l_m = P_lp1_l
    
    while l_i < l:
        
        P_lp1_m = ( (2*l_i+1)*x*P_l_m - (l_i+m)*P_lm1_m )/(l_i-m+1)
        l_i = l_i + 1
        P_lm1_m = P_l_m
        P_l_m = P_lp1_m
     
    return P_l_m