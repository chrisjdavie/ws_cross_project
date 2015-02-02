'''
Making time into a latex format, for titles to plots.

Probably should have used standard number format functions,
but I didn't really know they were a thing in Python, so 
did it myself.  It works, mostly. 

Created on 29 May 2014

@author: chris
'''

def time_title(time,time_symbol='$t$',unit='s'):
    
    t_str = time_2_str(time)
    
    title_str = time_symbol + ' = ' + t_str
    if time > 1e-30:
        title_str = title_str + unit
    return title_str

def time_2_str(time,i_trunk=4):
#     print 'ugiie'
    def sci_not(t_str,i):
        mant, exp = t_str[:i], t_str[i+1:]
        if len(mant) > i_trunk:
            mant = np.float(mant)
            mant *= 10.0**(i_trunk-2)
            mant = np.round(mant)/10.0**(i_trunk-2)
            mant = str(mant)

        return mant + '$\\times 10^{' + str(int(exp)) + '}$'
    
    t_str = str(time)
    len_0 = len(t_str)
    
    import numpy as np
    
    i = -1
    if t_str == '0.0':
        pass
    elif len_0 > 3 and t_str[-3] == 'e': 
        i=-3
        t_str = sci_not(t_str,i)
#         print 'a'
        
    elif len_0 > 3 and t_str[-4] == 'e': 
        i=-4
        t_str = sci_not(t_str,i)
#         print 'b'
        
    elif t_str[:2] == '0.':
        i = 0
        for t_i in t_str[2:]:
            if t_i != '0':
                break
            i += 1
#         print 'c'
#         print t_str, t_str[2+i], t_str[2+i+1:2+i+2+1]
        suc_dig = t_str[2+i+1:2+i+2+1] + '.' + t_str[2+i+2+1]
        
        suc_dig = str(int(100+np.round(np.float(suc_dig))))[1:]
        t_str = t_str[2+i] + '.' + suc_dig + '$\\times 10^{-' + str(i+1) + '}$'
    else:
#         print 'd'
        t_tmp = np.round(time*100)
#         print t_tmp
        t_str = str(t_tmp)[0] + '.' + str(t_tmp)[1:3]
#         print t_str
#         raw_input()
    
    
#     di = len(t_str) - len_0
#     if len(t_str[:i-di]) > 4 and t_str[4] != '.':
#         t_str = t_str[:i_trunk+1] + t_str[i-di:]
#         print 'c'
    return t_str
