import pylab, time
import numpy
import scipy.optimize, scipy.interpolate, scipy.signal
from copy import copy

def CalcLineProfile(im, iref, xroi=None, yroi=None, interpkind='linear', interpfact = 5, threshold_val = 0.5):
    """Function to calculate a line profile from a 2d image.
    Data is interpolated and shifted to generate a steep profile
    and averaged over the x-range.
    
    calling parameters:
    im:            Image with edge (of arbitrary dimensions)
    ref:           Flat image (of same dimension as ><im>> image)
    xroi:          2-tuple or 2-list with the x-dimensions of the image 
                   to be processed. Only data inside tuple limits is 
                   used. 
                   xroi[0]: lower boundary
                   xroi[1]: upper boundary
                   if xroi == None, the whole x-range will be used
                   (preset: xroi = None)
    yroi:          2-tuple or 2-list with the y-dimensions of the image 
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
                 
    return values: <line>, <iy>, <max_shift>, <iy_new>
    <line>:        new interpolated line profile.
    <iy>:          Position of the edge in <line>, i.e. the index nearest 
                   to the function value 0.5
    <max_shift>:   maximum value that the lines have been shifted
                   (in interpolated indices) to achieve an overlay
                   of the <iy> values.
    <iy_new>:      Real position of the edge in pixel (corrected for rotation
                   and orientation)
    """
    if xroi == None:
        xroi = [0, im.shape[1]]
    if yroi == None:
        yroi = [0, im.shape[0]]

    inorm = 1.0 * im[yroi[0]:yroi[1],xroi[0]:xroi[1]] \
              / iref[yroi[0]:yroi[1],xroi[0]:xroi[1]]
    #get average value in the 4 corners:
    # corner 1 - top left  // corner 2 - top right // corner 3 - bottom left // corner 4 - bottom right
    corner1 = numpy.average(inorm[0:5, 0:5])
    corner2 = numpy.average(inorm[0:5, -5:])
    corner3 = numpy.average(inorm[-5:, 0:5])
    corner4 = numpy.average(inorm[-5:, -5:])
    rot_val = 0 
    if (corner1 > threshold_val) and (corner2 > threshold_val) and (corner3 < threshold_val) and (corner4 < threshold_val):
        pass
    elif (corner1 < threshold_val) and (corner2 > threshold_val) and (corner3 < threshold_val) and (corner4 > threshold_val):
        inorm = numpy.rot90(inorm,1)
        rot_val = 1
    elif (corner1 < threshold_val) and (corner2 < threshold_val) and (corner3 > threshold_val) and (corner4 > threshold_val):
        inorm = numpy.rot90(inorm,2)
        rot_val = 2
    elif (corner1 > threshold_val) and (corner2 < threshold_val) and (corner3 > threshold_val) and (corner4 < threshold_val):
        inorm = numpy.rot90(inorm,3)
        rot_val = 3
    else:
        print('Warning. Could not detect line profile. Aborting')
        print('Intensity in corners 1: %1.3f // 2: %1.3f // 3: %1.3f // 4: %1.3f ' %(corner1, corner2, corner3, corner4))
        return None

    yroi = [0, inorm.shape[0]]
    xroi = [0, inorm.shape[1]]
    
    yold = numpy.linspace(0, yroi[1], yroi[1], endpoint=False)
    ynew = numpy.linspace(0, yroi[1]-1, (yroi[1]-1)*interpfact, endpoint = False)

    data_new = numpy.zeros((ynew.size, xroi[1]))
    for ix in xrange(xroi[1]):
        data_old = copy(inorm[:,ix])
        data1 = numpy.roll(data_old, -1)
        data2 = numpy.roll(data_old, 1)
        tmp = numpy.where(abs(data_old - 0.5*data1- 0.5*data2) > 0.05)[0][1:-1]
        for iy in tmp:
            if (abs(data_old[iy]-data_old[iy-1]) > 0.08) \
            and (abs(data_old[iy]-data_old[iy+1]) > 0.08) \
            and (abs(data_old[iy+1]-data_old[iy-1]) < 0.08):
                data_old[iy] = 0.5*(data_old[iy-1]+data_old[iy+1])

        f_inter = scipy.interpolate.interp1d(yold, data_old, kind=interpkind)
        data_new[:,ix] = f_inter(ynew)
    
    max_shift = 0
    ix = xroi[1]/2
    iy = numpy.abs(data_new[:,ix]-threshold_val).argmin()

    for ix in xrange(xroi[1]):
        shift = iy- numpy.where(data_new[:,ix] > threshold_val)[0][-1]
        data_new[:,ix] = numpy.roll(data_new[:,ix], shift)
        max_shift = max(max_shift, abs(shift))
   
    if rot_val in [1,2]:
        iy_new = 1.0*(interpfact*yold.size - iy)/interpfact
    else:
        iy_new = iy

    if max_shift > 0: data_new = data_new[max_shift:-max_shift,:]
    linenew = numpy.average(data_new, axis=1)
    return linenew, iy, max_shift, iy_new 
#end CalcLine


def Derivative(line, dxval = 0.2, approxorder = 2):
    """Function to calculate the derivative of the line <line>
    
    Calling parameters:
    line:    numpy 1d-array with the line to be derived.
    dxval:   x-spacing of the function values stored in 
             <line>
             (preset: dxval = 0.2 -- compatible with the 
             interpolation preset in CalcLineProfile)
    approxorder:
             Select the approximation order for the 
             derivate. Possible are 1 or 2
             (preset: approxorder = 2)
    
    return value:
    d_line:  derivative of the line profile.
             numpy 1d-array of length line.size-4
    """ 
    #roll the line for derivation
    fxph = numpy.roll(line, 1)[2:-2]
    fxmh = numpy.roll(line, -1)[2:-2]
    if approxorder == 2:
        fxp2h = numpy.roll(line, 2)[2:-2]
        fxm2h = numpy.roll(line, -2)[2:-2]
        df_2nd = (-fxp2h + 8 * fxph - 8 * fxmh + fxm2h) / (12 * dxval)
        return df_2nd
    else:
        df_1st = (fxph - fxmh) / (2 * dxval)
        return df_1st
#end Derivative

def MTF(linederiv, return_smoothed = True):
    """
    Function to compute the spectrum of the derived line
    profile.
    
    Calling Parameter:
    linederiv:        derived line profile
    return_smoothed:  if set to True, the returned FFT data
                      will be smoothed by a window of 
                      [0.1, 0.2, 0.4, 0.2, 0.1]
                      (preset: return_smoothed = True)
    Return values:    ft_abs, x10
    ft_abs:    absolute of the Fourier transform of
               linederiv
    x10:       x value at which the normalized spectal
               power density drops below 10%.
               (in units of index of the spectrum)
    """
    line_ft = numpy.fft.rfft(linederiv)
    ft_abs = numpy.abs(line_ft)
    ft_abs/= numpy.amax(ft_abs)
    
    window = [0.1, 0.2, 0.4, 0.2, 0.1]
    ft2 = scipy.signal.convolve(ft_abs, window, mode='same')
    ft2[:2] = ft_abs[:2]

    i0 = 0
    while True:
        if i0+2 >= linederiv.size:
            break
        if ft2[i0] > 0.1:
            #if ft2[i0+1] > ft2[i0]: break
            i0 += 1
        elif ft2[i0] <= 0.1:
            i0 -= 1
            break
    
    #numpy.where(ft2-0.1 > 0)[0][-1]
    y0 = ft2[i0]
    y1 = ft2[i0+1]
    #the x value at which the spectrum has dropped to 10%:
    
    #x10 = i0
    x10 = i0+(0.1-y0)/(y1-y0)
    
    if return_smoothed:
        return ft2, x10
    else:
        return ft_abs, x10
#end MTF
