"""
Portfolio optimization with CVXPY
See examples at http://cvxpy.org
Author: Shabbir Ahmed
"""

import pandas as pd
import numpy as np
from cvxpy import *

# read monthly_prices.csv
mp = pd.read_csv("monthly_prices.csv",index_col=0)
mr = pd.DataFrame()

# compute monthly returns
for s in mp.columns:
    date = mp.index[0]
    pr0 = mp[s][date] 
    for t in range(1,len(mp.index)):
        date = mp.index[t]
        pr1 = mp[s][date]
        ret = (pr1-pr0)/pr0
        mr.set_value(date,s,ret)
        pr0 = pr1
        
# get symbol names
symbols = mr.columns

# convert monthly return data frame to a numpy matrix
return_data = mr.as_matrix().T

# compute mean return
r = np.asarray(np.mean(return_data, axis=1))

# covariance
C = np.asmatrix(np.cov(return_data))

# print out expected return and std deviation
print "----------------------"
for j in range(len(symbols)):
    print '%s: Exp ret = %f, Risk = %f' %(symbols[j],r[j], C[j,j]**0.5)
   

# set up optimization model
n = len(symbols)
x = Variable(n)
req_return = 0.02
ret = r.T*x
risk = quad_form(x, C)
prob = Problem(Minimize(risk), 
               [sum_entries(x) = 1, ret >= req_return,
                x >= 0])

# solve problem and write solution
try:
    prob.solve()
    print "----------------------"
    print "Optimal portfolio"
    print "----------------------"
    for s in range(len(symbols)):
        print 'x[%s] = %f' %(symbols[s],x.value[s,0])
    print "----------------------"
    print 'Exp ret = %f' %(ret.value)
    print 'risk    = %f' %((risk.value)**0.5)
    print "----------------------"
except:
    print 'Error'
