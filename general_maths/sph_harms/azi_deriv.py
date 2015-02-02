'''
Examining the gradients of the azimuthally symmetric legendre polynomial.

Created on 1 May 2013

@author: chris
'''
def main():
    l = 4
    a = max_n_minimas(l)
    print a
    
def leg_poly(l):
    m = 0
    from pert_sphere import pert_sphere
    rs, thetas, _ = pert_sphere(l,m)
    
    rs = rs[:,0]
    thetas = thetas[:,0]
    return rs, thetas
    
def dr_dtheta(l):
    rs, thetas = leg_poly(l)
    
    dr_dthetas = (rs[:-1] - rs[1:])/(thetas[:-1] - thetas[1:])
    thetas_d = (thetas[:-1] + thetas[1:])/2.0    
    return dr_dthetas, thetas_d
    
def max_n_minimas(l):
    dr_dthetas, thetas_d = dr_dtheta(l)
    num_m2 = dr_dthetas[0]
    num_m1 = dr_dthetas[0]
    
    maxima_i = []
    minima_i = []
    for i, num in enumerate(dr_dthetas):
        if num_m1 > num_m2 and num_m1 > num:
            maxima_i.append(i)
        if num_m1 < num_m2 and num_m1 < num:
            minima_i.append(i)
        
        num_m2 = num_m1
        num_m1 = num
        
    return thetas_d[maxima_i], thetas_d[minima_i]
    

if __name__ == '__main__':
    main()