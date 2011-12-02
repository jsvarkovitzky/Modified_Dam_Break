from numpy import *
from matplotlib import *
from pylab import *
from analytical_solution_landslide import analytical_sol


N = 100                        # number of cells
X = linspace(-1000.,1000.,N+1) # vertices of cells
t_compare = 15
(u,h,w,z,mom) = analytical_sol(X,t_compare)

figure(1)
plot(X,w,X,z)
title('State of the slide at time t = %s' %t_compare)
legend(('stage','topography'))
show()
