import PyTango
import time
from p05.scripts import FLIgetImage
import p05.tools.MTFroutines as mtf

def TakeMTF(camera, motor, xroi = None, yroi = None, interpkind='linear', interpfact = 5, threshold_val = 0.5, motoredgepos = None, motoredgedist = 10.0):
    """
    Function to take a MTF with the camera <<Camera>>, where the motor <<Motor>>
    moves the edge in and out of the beam. 
    
    Calling Parameters:
    camera:     Instance of PyTango.DeviceProxy for the camera

    motor:      Instance of PyTango.DeviceProxy for the motor moving the edge

    Camera control keywords:
    xroi:          list with xrois for the MTF calculation. If more than one
                   edge shall be calculated, extend the list:
                   List entries:
                   2-tuple or 2-list with the x-dimensions of the image 
                   to be processed. Only data inside tuple limits is 
                   used. 
                   xroi[0]: lower boundary
                   xroi[1]: upper boundary
                   if xroi == None, the whole x-range will be used
                   (preset: xroi = None)
    yroi:          list with yrois for the MTF calculation. If more than one
                   edge shall be calculated, extend the list:
                   List entries:
                   2-tuple or 2-list with the y-dimensions of the image 
                   to be processed. Only data inside tuple limits is 
                   used. 
                   yroi[0]: lower boundary
                   yroi[1]: upper boundary
                   if yroi == None, the whole y-range will be used
                   (preset: yroi = None)
    interpkind:    Kind of line interpolation. Available are 'linear'
                   and 'cubic'
                   (preset: interpkind = 'linear')
    interpfact:    Interpolation factor, i.e. how many intermediate points 
                   shall be introduced.
                   (preset: interpfact = 5)
    threshold_val: The threshold value for the edge detection procedures.
                   (preset: threshold_val = 0.5)

    Motor control keywords:
    motoredgepos:  The motor position for the edge in the beam
                   If None is selected, the starting position will be taken
                   (preset: motoredgepos = None)
    motoredgedist: The distance for the edge to be moved out of the beam.
                   (preset: motoredgedist = 10)
    
   
    returns:    
    """
    if motoredgepos== None:
        motoredgepos = motor.read_attribute('Position').value
    
    if len(xroi) != len(yroi):
        print('Error. xroi and yroi size do not match.\n\nExiting function.')
        return None

    #Go to MTF position and take edge image
    motor.write_attribute('Position', motoredgepos)
    time.sleep(0.05)
    while motor.state() != PyTango.DevState.ON: time.sleep(0.05)
    im_edge = FLIgetImage(camera)
    if im_edge == None:
        print('Error. Could not read image from camera.\n\nExiting function.')
        return None

    #Goto ref position and take reference image
    motor.write_attribute('Position', motoredgepos+motoredgedist)
    time.sleep(0.05)
    while motor.state() != PyTango.DevState.ON: time.sleep(0.05)
    im_ref =  FLIgetImage(camera)
    if im_ref == None:
        print('Error. Could not read image from camera.\n\nExiting function.')
        return None

    #For testing purposes!!!
#    im_edge = numpy.fromfile('D:/_ibl/20120618_xrayMTFx05/MTF_zf_0014.raw', dtype = numpy.uint16)
#    im_edge.shape = (2300,1500)
#    
#    im_ref = numpy.fromfile('D:/_ibl/20120618_xrayMTFx05/MTF_zf_ref_0014.raw', dtype = numpy.uint16)
#    im_ref.shape = (2300,1500)
#    
#    xroi = [[500,600],[600,900]]
#    yroi = [[700,1300],[1300,1400]]

    #Determine number of rois for further processing:
    if len(xroi) == 2:
        try:
            num_rois = len(xroi[0])
        except:
            num_rois = 1
    elif len(xroi) > 2:
        num_rois = len(xroi)

    #Process the ROI data
    print('Processing %i ROIs.' %num_rois)
    results = []
    dx_interpol = 1/float(interpfact)
#    try:
    if num_rois == 1:
        line, iy, shift, iy_new = mtf.CalcLineProfile(im_edge, im_ref, xroi=xroi, yroi=yroi, interpkind=interpkind, interpfact=interpfact, threshold_val=threshold_val)
        linederiv = mtf.Derivative(line, dxval= dx_interpol)
        linefft, mtfval = mtf.MTF(linederiv)
        resolution = (linederiv.size*dx_interpol)/mtfval
        results.append([resolution,linefft])
        
    elif num_rois > 1:
        for iroi in xrange(num_rois):
            line, iy, shift, iy_new = mtf.CalcLineProfile(im_edge, im_ref, xroi=xroi[iroi], yroi=yroi[iroi], interpkind=interpkind, interpfact=interpfact, threshold_val=threshold_val)
            linederiv = mtf.Derivative(line, dxval= dx_interpol)
            linefft, mtfval = mtf.MTF(linederiv)
            resolution = (linederiv.size*dx_interpol)/mtfval
            results.append([resolution,linefft])
#    except:
#        print('Could not compute MTFs. Check setup')
            
    motor.write_attribute('Position', motoredgepos)
    time.sleep(0.05)
    while motor.state() != PyTango.DevState.ON: time.sleep(0.05)

    return results
#end TakeMTF    
    

