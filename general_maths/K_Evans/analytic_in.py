
'''Old style code for operating the K. Evans analytic codes, which all in all isn't bad, at least to my eyes'''
# def main():
#     output_dir = '/media/backup_ex4/long_term_data/thesis/dr_r_v_r/small_v_analy/l16-d0075-6400-3200/'#../../../zeusmp_analy/output/l16-d0075-6400-3200/'
#     labels = [ 'Model', 'Analytic' ]
#     linestyles = [ '-', ':' ]
#     seq = [2, 4, 7, 4]
#     colours = [ 'blue', 'y' ]
# #    r_in, t_in, dr_in, r_out, t_out, dr_out = read_in_and_out_zmp_deriv(output_dir,l=16)
#     a = read_in_and_out_zmp_deriv(output_dir,l=16)
#     r_in, dr_in = a[0], a[2]
#     t_in = a[1]
#     #r_0 = r_in[0]
#     
#     r_a, dr_a = dr_r_analy(2.10e-5,0.000393,r_in[0],0.00688)
#     
#     dr_in = 100*dr_in/2
#     r_in = 100*r_in#/r_0
#     dr_in = dr_in#/r_0
#     r_a = 100*r_a#/r_0
#     dr_a = 100*dr_a/2.0#/(2*r_0)
#     
#     a = draw_n_dr_r_v_r_lines([r_in,r_a],[dr_in,dr_a],labels=labels,colours=colours,linestyles=linestyles,ylim_u=0.02,ylim_l=-0.02,xlim_u=0.1,xlim_l=0.005,leg_loc='upper left')
#     p, leg_con = a[1], a[2]
#     p[1][0].set_dashes(seq)    
#     leg_con.leg('upper left')
# 
#     
#     plt.figure(16)
#     plt.plot(t_in,r_in)
#     
#     plt.show()


import numpy as np
gamma = np.float64(5.0/3.0)
lambdaa = 1.0 + 2.0/gamma + (2.0*gamma/(gamma-1.0))**0.5
chi_p = 1.0/2.0 -1.0/lambdaa


def dr_r_analy(r_min,r_peak_match,r_max,dr_r_strech,l=16):
    # this is matching r_peak and dr_r_strech.  The maths is reasonably straight forwards and probably in lab book 3 somewhere
    r_min_kev = r_min/r_peak_match 
    r_pow_min_kev = np.log10(r_min_kev)
    r_max_kev = r_max/r_peak_match
    r_pow_max_kev = np.log10(r_max_kev)
    print r_max_kev, r_min_kev
    print r_pow_max_kev, r_pow_min_kev
    dr_kev,r_kev = K_Evans_pert(r_pow_min_kev,l,r_pow_max=r_pow_max_kev)
    r = r_kev*r_peak_match
    dr = dr_kev*dr_r_strech*r_peak_match

    return r, dr


def K_Evans_pert(r_pow_min,l,r_pow_max=0):

# plots the growth of the K Evans perturbation growth from his Sonoluminescence paper

# could strip out the f_a bit and put in a different function - may do if I need to talk about the self
# similarity stuff some more
    
    envel, r = K_Evans_envelope(r_pow_min,r_pow_max=r_pow_max)
    
    const = (1/(2*lambdaa))*(-(lambdaa+2.0)**2.0+4.0*lambdaa*l*(l+1.0))**0.5
    f_a = np.cos(np.log(r)*const)
    
    return f_a*envel, r

def K_Evans_envelope(r_pow_min,r_pow_max=0):
    
# plots the envelop of the growth of the K Evans perturbations in the above mentioned paper    
    
    r_pow_min = -r_pow_min
    r_pow_max = -r_pow_max
    delta = 0.01
    expo = np.arange(r_pow_max,r_pow_min + delta,delta)

    expo = -expo
    r = np.power(10,expo)
    envel = np.power(r,chi_p)

        
    return envel, r      
    