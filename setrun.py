""" 
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.
    
""" 

import os
from pyclaw import data 


#------------------------------
def setrun(claw_pkg='geoclaw'):
#------------------------------
    
    """ 
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "geoclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData 
    
    """ 

    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    ndim = 2
    rundata = data.ClawRunData(claw_pkg, ndim)

    #------------------------------------------------------------------
    # GeoClaw specific parameters:
    #------------------------------------------------------------------

    rundata = setgeo(rundata)   # Defined below
    
    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #   (or to amr2ez.data for AMR)
    #------------------------------------------------------------------

    clawdata = rundata.clawdata  # initialized when rundata instantiated


    # Set single grid parameters first.
    # See below for AMR parameters.


    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.ndim = ndim
    

    # Lower and upper edge of computational domain:
    clawdata.xlower = -1000.
    clawdata.xupper = 1000.
    # Number of grid cells:
    clawdata.mx =  2000
    clawdata.my =  2
    
    dx = (clawdata.xupper - clawdata.xlower) / clawdata.mx
    clawdata.ylower = 0.
    clawdata.yupper = .1*dx
        

    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.meqn = 3

    # Number of auxiliary variables in the aux array (initialized in setaux)
    clawdata.maux = 3
    
    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.mcapa = 0
    
    
    
    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = 0
    
    
    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.outstyle = 1

    if clawdata.outstyle==1:
        # Output nout frames at equally spaced times up to tfinal:
        clawdata.nout = 45
        clawdata.tfinal = clawdata.t0 + 15

    elif clawdata.outstyle == 2:
        # Specify a list of output times.  
        clawdata.tout =  [0.5, 1.0]   # used if outstyle == 2
        clawdata.nout = len(clawdata.tout)

    elif clawdata.outstyle == 3:
        # Output every iout timesteps with a total of ntot time steps:
        iout = 1
        ntot = 1
        clawdata.iout = [iout, ntot]
    


    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:  
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 1
    
    

    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==1: variable time steps used based on cfl_desired,
    # if dt_variable==0: fixed time steps dt = dt_initial will always be used.
    clawdata.dt_variable = 1
    
    # Initial time step for variable dt.  
    # If dt_variable==0 then dt=dt_initial for all steps:
    clawdata.dt_initial = 0.0001
    
    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99
    
    # Desired Courant number if variable dt used, and max to allow without 
    # retaking step with a smaller dt:
    clawdata.cfl_desired = 0.9
    clawdata.cfl_max = 1.0
    
    # Maximum number of time steps to allow between output times:
    clawdata.max_steps = 100000

    
    

    # ------------------
    # Method to be used:
    # ------------------

    # Order of accuracy:  1 => Godunov,  2 => Lax-Wendroff plus limiters
    clawdata.order = 2
    
    # Transverse order for 2d or 3d (not used in 1d):
    clawdata.order_trans = 2
    
    # Number of waves in the Riemann solution:
    clawdata.mwaves = 3
    
    # List of limiters to use for each wave family:  
    # Required:  len(mthlim) == mwaves
    clawdata.mthlim = [3,3,3]
    
    # Source terms splitting:
    #   src_split == 0  => no source term (src routine never called)
    #   src_split == 1  => Godunov (1st order) splitting used, 
    #   src_split == 2  => Strang (2nd order) splitting used,  not recommended.
    clawdata.src_split = 1
    
    
    # --------------------
    # Boundary conditions:
    # --------------------

    # Number of ghost cells (usually 2)
    clawdata.mbc = 2
    
    # Choice of BCs at xlower and xupper:
    #   0 => user specified (must modify bcN.f to use this option)
    #   1 => extrapolation (non-reflecting outflow)
    #   2 => periodic (must specify this at both boundaries)
    #   3 => solid wall for systems where q(2) is normal velocity
    
    clawdata.mthbc_xlower = 1
    clawdata.mthbc_xupper = 0
    
    clawdata.mthbc_ylower = 3
    clawdata.mthbc_yupper = 3
    

    # ---------------
    # AMR parameters:
    # ---------------


    # max number of refinement levels:
    mxnest = 1

    clawdata.mxnest = -mxnest   # negative ==> anisotropic refinement in x,y,t

    # List of refinement ratios at each level (length at least mxnest-1)
    clawdata.inratx = [4,2,4]
    clawdata.inraty = [2,2,2]

    clawdata.inratt = [1,1,1]   
    # Instead of setting these ratios, set the next parameter to True 
    # to automatically choose refinement ratios in time based on estimate 
    # of maximum wave speed on all grids at each level.
    variable_dt_refinement_ratios = True


    # Specify type of each aux variable in clawdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    clawdata.auxtype = ['center','center','yleft']


    clawdata.tol = -1.0     # negative ==> don't use Richardson estimator
    clawdata.tolsp = 0.5    # used in default flag2refine subroutine
                            # (Not used in geoclaw!)

    clawdata.kcheck = 3     # how often to regrid (every kcheck steps)
    clawdata.ibuff  = 2     # width of buffer zone around flagged points

    # More AMR parameters can be set -- see the defaults in pyclaw/data.py

    return rundata
    # end of function setrun
    # ----------------------


#-------------------
def setgeo(rundata):
#-------------------
    """
    Set GeoClaw specific runtime parameters.
    For documentation see ....
    """

    try:
        geodata = rundata.geodata
    except:
        print "*** Error, this rundata has no geodata attribute"
        raise AttributeError("Missing geodata attribute")

    # == setgeo.data values ==
    geodata.igravity = 1
    geodata.gravity = 9.81
    geodata.icoordsys = 1

    # == settsunami.data values ==
    geodata.sealevel = 0.
    geodata.drytolerance = 1.e-3
    geodata.wavetolerance = 1.e-2
    geodata.depthdeep = 1.e2
    geodata.maxleveldeep = 3
    geodata.ifriction = 0
    geodata.coeffmanning = 0.025
    geodata.frictiondepth = 20.

    # == settopo.data values ==
    geodata.topofiles = []
    # for topography, append lines of the form
    #   [topotype, minlevel, maxlevel, t1, t2, fname]
    geodata.topofiles.append([2, 1, 1, 0., 1.e10, 'landslide.topotype2'])

    # == setdtopo.data values ==
    geodata.dtopofiles = []
    # for moving topography, append lines of the form:  (<= 1 allowed for now!)
    #   [topotype,minlevel,maxlevel,fname]

    # == setqinit.data values ==
    geodata.iqinit = 0
    geodata.qinitfiles = []  
    # for qinit perturbations, append lines of the form: (<= 1 allowed for now!)
    #   [minlev, maxlev, fname]
    #geodata.qinitfiles.append([1, 2, 'hump.xyz'])


    # == setregions.data values ==
    geodata.regions = []
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]
    geodata.regions.append([2,2, 0.,1e9, 0,6, 0,1])
    geodata.regions.append([3,3, 0.,1e9, 0,3, 0,1])

    # == setgauges.data values ==
    geodata.gauges = []
    #wallPosit = 10.59 #Case A
    #wallPosit = 9.19 #Case B
    wallPosit = 8.83 #Case C
    geodata.gauges.append([4,               0 ,    0.00144 , 0., 1.e10])
    geodata.gauges.append([5,  wallPosit-8.19 ,   0.00144 , 0., 1.e10])
    geodata.gauges.append([6,  wallPosit-6.01 ,   0.00144 , 0., 1.e10])
    geodata.gauges.append([7,  wallPosit-3.83 ,   0.00144 , 0., 1.e10])
    geodata.gauges.append([8,  wallPosit-2.37 ,   0.00144 , 0., 1.e10])
    geodata.gauges.append([9,  wallPosit-0.9  ,   0.00144 , 0., 1.e10])
    geodata.gauges.append([10, wallPosit-0.43 ,   0.00144 , 0., 1.e10])
    geodata.gauges.append([11, wallPosit-0.02 ,   0.00144 , 0., 1.e10])
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]


    # == setfixedgrids.data values ==
    geodata.fixedgrids = []
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,
    #  ioutarrivaltimes,ioutsurfacemax]

    return rundata
    # end of function setgeo
    # ----------------------



if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    if len(sys.argv) == 2:
	rundata = setrun(sys.argv[1])
    else:
	rundata = setrun()

    rundata.write()
    
