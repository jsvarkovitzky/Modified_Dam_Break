"""
Analytical solution for the debris avalanche problem.
Input: X is the one-dimensional domain (grids);
       t is the time.
Output: u is the velocity in the x-direction;
        h is the height of the fluid;
        w is the stage that is w=h+z, where
        z is the one-dimensional topography;
        mom is the momentum in the x-direction.
Parameters: g is the gravity acceleration;
            h_0 is the constant initial height of fluid;
            c0 is square root of g*h_0;
            m is -g*tan(theta) + g*cos(theta)*cos(theta)*tan(delta), where
            theta is the topography angle and delta is the friction angle.
            Usually, tan(theta) and tan(delta) are given.
            Here, tan(theta) is the topography slope called bed slope.
Ref.: Mungkasi and Roberts, 2011, ANZIAM Journal Vol.52: C349--363,
      "A new analytical solution for testing debris avalanche numerical models".
"""
def analytical_solution(t):
    N = 100                        # number of cells
    X = linspace(-1000.,1000.,N+1) # vertices of cells
    dx = 2000./N                   # uniform cell width
    C = zeros(N,float)
    for i in range(N):
        C[i] = -1000. + (i+0.5)*dx # centroids of cells
        
        g = 9.81                       # gravity
        h_0 = 20.                      # initial fluid height
        c0 = sqrt(g*h_0)               # wave speed relating to h_0
        bed_slope = 0.1                # put 0 for classical dam break problem
        m = -g*bed_slope #+F ,         no friction
        #t_stop =15.                    # time to look at
        
        N = len(X)
        u = zeros(N,float)
        h = zeros(N,float)
        w = zeros(N,float)
        z = zeros(N,float)
        mom = zeros(N,float)
        for i in range(N):
            # Calculate Analytical Solution at time t > 0
            if X[i] <= -2.0*c0*t + 0.5*m*t**2:
                u[i] = 0.0
                h[i] = 0.0
            elif X[i] <= c0*t + 0.5*m*t**2:
                u[i] = 2.0/3.0 * (X[i]/t - c0 + m*t)
                h[i] = 1.0/(9.0*g) * (X[i]/t + 2.0*c0 - 0.5*m*t)**2
            else:
                u[i] = m*t
                h[i] = h_0

            z[i] = bed_slope*X[i]
            w[i] = h[i] + z[i]
            mom[i] = u[i]*h[i]
        
