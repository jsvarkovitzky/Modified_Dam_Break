
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 
import os

slope = 1. / 19.85
print "slope = ",slope

outdir = os.path.abspath('_output')


    
from numpy import loadtxt

#--------------------------
def setplot(plotdata):
#--------------------------
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 

    from pyclaw.plotters import colormaps, geoplot

    plotdata.clearfigures()  # clear any old figures,axes,items data

    def set_drytol(current_data):
        # The drytol parameter is used in masking land and water and
        # affects what color map is used for cells with small water depth h.
        # The cell will be plotted as dry if h < drytol.
        # The best value to use often depends on the application and can
        # be set here (measured in meters):
        current_data.user.drytol = 1.e-4


    plotdata.beforeframe = set_drytol

    # To plot gauge locations on pcolor or contour plot, use this as
    # an afteraxis function:

    def addgauges(current_data):
        from pyclaw.plotters import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos='all', format_string='ko', add_labels=True)
    
    def save(current_data):
        from pylab import figure, savefig
        frameno = current_data.frameno
        figure(2)
        savefig('dam_break_%s.png' % frameno)

    plotdata.afterframe = save


    #-----------------------------------------
    # Figure for line plot
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='line', figno=2)
    #plotfigure.show = False

    def eta_slice(current_data):
        x = current_data.x[:,0]
        q = current_data.q
        eta = q[:,0,3]
        return x,eta

    def B_slice(current_data):
        x = current_data.x[:,0]
        q = current_data.q
        h = q[:,0,0]
        eta = q[:,0,3]
        B = eta - h
        return x,B


    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('line')
    plotaxes.title = 'Surface'
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = [0,3]
   
    # Water
    plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
    plotitem.map_2d_to_1d = eta_slice
    plotitem.color = 'g'
    plotitem.plotstyle = '-'
    plotitem.kwargs = {'linewidth':2}
    plotitem.outdir = outdir

    # Topography
    plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
    plotitem.map_2d_to_1d = B_slice
    plotitem.color = 'r'
    plotitem.kwargs = {'linewidth':2}
    plotitem.outdir = outdir

    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=300, \
                    type='each_gauge')

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [2,10]
    plotaxes.ylimits = [-0.001, 3]
    plotaxes.title = 'Surface'
    
    # Plot surface as blue curve:  
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'


    #plotitem = plotaxes.new_plotitem(plot_type='1d_plot')

    def gaugetopo(current_data):
        q = current_data.q
        h = q[:,0]
        eta = q[:,3]
        topo = eta - h
        return topo
        
    #plotitem.plot_var = gaugetopo
    plotitem.clf_each_gauge = False
    #plotitem.plotstyle = 'g-'
    def afteraxes(current_data):
        from pylab import plot, legend, loadtxt
        gaugeno = current_data.gaugeno   

    plotaxes.afteraxes = afteraxes


    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = [4,5,6,7,8,9,10,11]  # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

    
