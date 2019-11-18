import PyTango
import numpy, time, scipy.optimize
from p05.scripts import Scan

def OptimizeGap(diodemotor = '//hzgpp05eh2vme:10000/p05/motor/eh2.05', diodeoutpos =  0, diodeinpos = 35, counter='Diode1', scanmotor = 'Gap'):
    gap = PyTango.DeviceProxy('//hasgksspp05s01:10000/p05/undulator/1')
    gappos = gap.read_attribute('Gap').value
    
    dmot = PyTango.DeviceProxy(diodemotor)
    dmot.write_attribute('Position', diodeinpos)
    time.sleep(0.05)
    while dmot.state() != PyTango.DevState.ON: time.sleep(0.05)
    
    scan = Scan(motor = scanmotor, counter = counter, x0 = gappos+0.5, x1 = gappos-0.5,t=0.2, n=50, silent = True)
    scan.FindCenter()
    if scan.peak_found:
        scan.GotoCenter()
    else:
        gap.write_attribute('Gap', gappos)
    
    del(gap)
    dmot.write_attribute('Position', diodeoutpos)
    time.sleep(0.05)
    while dmot.state() != PyTango.DevState.ON: time.sleep(0.05)
    
    return None
#end OptimizeGap 

def OptimizeGapQBPM(qbpmadd = '//hasgksspp05s01:10000/p05/i404/exp.01', scanmotor = 'Gap', gaparr = None):
    gap = PyTango.DeviceProxy('//hasgksspp05s01:10000/p05/undulator/1')
    gappos = gap.read_attribute('Gap').value
    qbpm = PyTango.DeviceProxy(qbpmadd)
    if gappos<9.95+0.5:
        gapstart=9.95
    else:
        gapstart=gappos-0.5
    if gaparr == None:
        gaparr = numpy.linspace(gappos+0.5, gapstart, num =50, endpoint = True)
        gapres = numpy.zeros((50))
    else:
        gapres = numpy.zeros((gaparr.size))
    for i in xrange(gaparr.size):
        gap.write_attribute('Gap', gaparr[i])
        time.sleep(0.2)
        while gap.state() == PyTango.DevState.MOVING:
            time.sleep(0.2)
        gapres[i] = qbpm.read_attribute('PosAndAvgCurr').value[2]
  
    peak_found = False
    imax = gapres.argmax()
    vmax = gapres[imax]
    tmp = numpy.where(gapres > 0.5*vmax)[0]
    i0, i1 = tmp[0], tmp[-1]
    f = lambda c,x,data: c[0]*numpy.exp(-(c[1]-x)**2/(2*c[2]**2)) -data
    c0 = numpy.array((vmax, gaparr[imax], (gaparr[i1]-gaparr[i0])/2.5))
    c1 = scipy.optimize.leastsq(f, c0, args=(gaparr, gapres))[0]
    tmp = (numpy.sqrt(numpy.sum(f(c1, gaparr, gapres)**2))/numpy.average(gapres))/gapres.size
    if tmp < 0.4 and (numpy.amin(gaparr) < c1[1] < numpy.amax(gaparr)):
        peak_found = True
    if peak_found:
        gap.write_attribute('Gap', c1[1])
        time.sleep(0.05)
        while gap.state() != PyTango.DevState.ON: time.sleep(0.05)
    else:
        gap.write_attribute('Gap', gappos)
    
    del(gap)    
    return None
#end OptimizeGapQBPM    
