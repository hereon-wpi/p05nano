import PyTango
import numpy, threading, copy, time, sys
import pylab
import matplotlib.backends.backend_tkagg as backend_tkagg
import scipy.optimize
from p05.common import ThreadControl

try:
    # try importing Python 2 modules...
    import Tkinter
    import tkMessageBox
    import Queue
except ImportError:
    # ...or load Python 3 muldes if that fails.
    import tkinter as Tkinter
    from tkinter import messagebox as tkMessageBox
    import queue as Queue
 

class Scan(threading.Thread):
    """Class to organize motor scans.
    Calling Parameters are:
    - motor = <String>    the name of the motor
                          (list of names is stored in the ScanDevices class)
    - counter = <String>  the name of the counter
                          (list of names is stored in the ScanDevices class)
    *or*
    - motor = <String>        the TANGO address of the device to be scanned
    - mattribute = <String>   the name of the TANGO attribute to be scanned
    - counter = <String>      the TANGO address of the counter
    - cattribute = <String>   the name of the TANGO attribute to be counted

    additional parameters:
    - x0 = <Float>            the starting point for the scan
    - x1 = <Float>            the endpoint for the scan
    - n = <Int>               the number of scanpoints
                              (including both endpoints)
                              (preset n = 20)
    - t = <Float>             the counting time
                              (preset t = 0.1)
    - showplot = <Boolean>    set to True if a window with a plot of the
                              scan should be created.
                              (preset showplot = True)
    - silent = <Boolean>      set to True if no command line output of
                              scan position and status is to be shown
                              (preset silent = False)

    Return values:
    return None    no values are directly returned
                   but the results are stored in:
    - self.xarr   array with motor position values
    - self.yarr   array with counter values
    """
    def __init__(self, motor='Test', mattribute=None, counter='EH1Diode1', cattribute=None, x0=1, x1=5, n=20, t=0.1, showplot=True, silent=False, QBPMdevice = False):
        """Method to initialize the scan.
        After successful initialization, the Scan method
        is called automatically."""
        threading.Thread.__init__(self)
        self.queue = Queue.Queue()

        self.showplot = showplot
        self.silent = silent
        self.QBPMdevice = QBPMdevice
        #Initializing of TANGO connections etc.
        tmp = _ScanDeviceDict()
        self.motordict = copy.copy(tmp.motordict)
        self.counterdict = copy.copy(tmp.counterdict)
        self.motor = motor
        del(tmp)
        if self.motor in self.motordict.keys():
            self.mname = self.motordict.get(motor)[0]
            self.mattribute = self.motordict.get(motor)[1]
            try:
                self.Mdevice = PyTango.DeviceProxy(self.mname)
                self.mattinfo = self.Mdevice.attribute_query(self.mattribute)
            except:
                print('Error: Could not connect to the Tango server\n(%s) or could not read\nattribute %s' %(self.motor, self.mattribute))
                return None
        else:
            self.mname = self.motor
            self.mattribute = mattribute
            try:
                self.Mdevice = PyTango.DeviceProxy(self.motor)
                self.mattinfo = self.Mdevice.attribute_query(self.mattribute)
            except:
                print('Error: Could not connect to the Tango server (%s)\n or could not read the attribute (%s)' %(self.motor, self.mattribute))
                return None
        if counter in self.counterdict.keys():
            self.cname = self.counterdict.get(counter)[0]
            self.cattribute = self.counterdict.get(counter)[1]
            try:
                self.Cdevice = PyTango.DeviceProxy(self.cname)
            except:
                print('Error. Could not connect to the counter TANGO server for %s (%s)' %(self.counter, self.cname))
                return None
        else:
            self.cname = counter
            self.cattribute = cattribute
            try:
                self.cname = counter
                self.cattribute = cattribute
                self.Cdevice = PyTango.DeviceProxy(self.cname)
                tmp = self.Cdevice.read_attribute(self.cattribute)
            except:
                print('Error: Could not connect to the Tango server\n(%s) or could not read\nattribute %s' %(self.cname, self.cattribute))
                return None
        if None in [self.mname, self.mattribute, self.cname, self.cattribute, x0, x1, n, t]:
            print('Error: Calling parameters missing. Correct syntax:')
            print('Scan(motor=<Str>, counter=<Str>, x0=<Float>, x1=<Float>, n=<Int>, t=<Float>')
            return None
        elif None not in [self.mname, self.mattribute, self.cname, self.cattribute, x0, x1, n, t]:
            try:
                self.x0=float(x0)
                self.x1=float(x1)
                self.n=int(n)
                self.t=float(t)
            except:
                print('Error: Not all parameters could be converted to numbers!')
                return None
        self.initialized = True
        self.Scan()
        return None
    #end __init__

    def Scan(self):
        """Method for performing the actual scan, i.e. moving
        the motors and counting."""
        if not self.silent: print('\n')
        self.xarr = numpy.linspace(self.x0, self.x1, self.n)
        self.carr = numpy.zeros((self.n))
        if self.showplot:
            while len(threading.enumerate()) > 1:
                ThreadControl.exit_flag = True
                time.sleep(0.05)
            ThreadControl.exit_flag = False
            _ScanPlot(self.queue).start()
        for ii in xrange(self.xarr.size):
            _pos = self.xarr[ii]
            try:
                self.Mdevice.write_attribute(self.mattribute, _pos)
            except:
                print('Error: could not move motor to requested position!')
                pass
            cn = 0
            while self.Mdevice.state() == PyTango.DevState.MOVING:
                time.sleep(0.01)
                cn += 1
                if cn > 3000: break
            if cn > 3000:
                print('Error: Timeout while moving.')
                return None
            self.carr[ii] = self.Count()
            self.queue.put([ii, self.xarr, self.carr])
            if not self.silent:
                print('\t%s %s: %f\r' %(self.motor, self.mattribute, self.xarr[ii]),
                      sys.stdout.flush())
        if not self.silent: print('\n')
        self.yarr = self.carr
        self.queue.put([None, None, None])
        self.peak_found = False
        return None
    #end Scan
    
    def Show(self):
        """Not in use yet."""
        return None
    #end Show
    
    def FindCenter(self):
        if self.yarr != None and self.xarr != None:
            #max index and max value
            imax = self.yarr.argmax()
            vmax = self.yarr[imax]
            tmp = numpy.where(self.yarr > 0.5*vmax)[0]
            i0, i1 = tmp[0], tmp[-1]
            f = lambda c,x,data: c[0]*numpy.exp(-(c[1]-x)**2/(2*c[2]**2)) -data
            c0 = numpy.array((vmax, self.xarr[imax], (self.xarr[i1]-self.xarr[i0])/2.5))
            c1 = scipy.optimize.leastsq(f, c0, args=(self.xarr, self.yarr))[0]
            if not self.silent:
                print('Center:', c1[1])
            self.peak_center = c1[1]
            self.peak_sigma = c1[2]
            self.peak_amp = c1[0]
            tmp = (numpy.sqrt(numpy.sum(f(c1, self.xarr, self.yarr)**2))/numpy.average(self.yarr))/self.yarr.size
            if tmp < 0.4 and (numpy.amin(self.xarr) < c1[1] < numpy.amax(self.xarr)):
                self.peak_found = True
            else:
                print('Could not fit peak!')
                self.peak_found = False
        else:
            print('No scan performed yet.')
        return None
    #end FindCenter
    
    def GotoCenter(self):
        if self.peak_found == True:
            self.Mdevice.write_attribute(self.mattribute, self.peak_center)
        time.sleep(0.05)
        while self.Mdevice.state() != PyTango.DevState.ON: time.sleep(0.05)
        return None
    #end GotoCenter
    
    def Count(self):
        """Method to count and average for the exposure time."""
        if not self.QBPMdevice:
            nn = max(int(self.t*80), 10)
            intcounts = 0.
            for i in xrange(nn):
                intcounts += self.Cdevice.read_attribute(self.cattribute).value
            intcounts/=nn
        else: 
            intcounts = 0.
            for i in xrange(5):
                intcounts += self.Cdevice.read_attribute(self.cattribute).value[2]
            intcounts/=nn
        return intcounts
    #end Count

    def __call__(self):
        """The __call__ method is not used."""
        pass
    #end __call__
### end Scan ###

class _ScanDeviceDict():
    """Class to store the references of the motor and counter names
    and their TANGO address information for performing scans.    
    """
    def __init__(self):
        """Init method, called automatically"""
        self.motordict = {}
        self.motordict['Undulator']=['//hasgksspp05s01:10000/p05/undulator/1', 'Gap']
        self.motordict['DCM_Bragg']= ['//hasgksspp05s01:10000/p05/dcmmotor/s01.01', 'Position']
        self.motordict['DCP_Par'] = ['//hasgksspp05s01:10000/p05/dcmmotor/s01.04', 'Position']
        self.motordict['DCM_Perp']= ['//hasgksspp05s01:10000/p05/dcmmotor/s01.03', 'Position']
        self.motordict['DCM_Jack1']= ['//hasgksspp05s01:10000/p05/motor/mono.03', 'Position']
        self.motordict['DCM_Jack2']= ['//hasgksspp05s01:10000/p05/motor/mono.04', 'Position']
        self.motordict['DCM_Jack3']= ['//hasgksspp05s01:10000/p05/motor/mono.07', 'Position']
        self.motordict['DCM_Xtal1_Roll']= ['//hasgksspp05s01:10000/p05/motor/mono.05', 'Position']
        self.motordict['DCM_Xtal2_Roll']= ['//hasgksspp05s01:10000/p05/motor/mono.02', 'Position']
        self.motordict['DCM_Xtal2_Pitch']= ['//hasgksspp05s01:10000/p05/motor/mono.01', 'Position']
        self.motordict['Test']= ['//hzgpp05eh2vme:10000/p05/dac/eh2.01', 'Voltage']
        self.counterdict = {}
        self.counterdict['EH1Diode1'] = ['//hzgpp05eh1vme:10000/p05/adc/eh1.05', 'Value']
        self.counterdict['QBPM1'] = ['//hasgksspp05s01:10000/p05/i404/exp.01', 'PosAndAvgCurr']
        self.counterdict['Test']= ['//hzgpp05eh2vme:10000/p05/adc/eh2.03', 'Value']
    #end __init__
    def __call__(self):
        pass
    #end __call__
    def ShowList(self):
        """ShowList method prints the dictionaries on screen for the user
        to check the motor and counter addresses. """ 
        _list = self.motordict.keys()
        print('\nMotor list:')
        for _key in _list:
            print(_key, ' (%s, %s)' %(self.motordict[_key][1], self.motordict[_key][0]))
        _list = self.counterdict.keys()
        print('\nCounter list:')
        for _key in _list:
            print(_key, ' (%s, %s)' %(self.counterdict[_key][1], self.counterdict[_key][0]))
    #end ShowList
### end _ScanDeviceDict ###


class _ScanPlot(threading.Thread):
    """Class to initialize and organize the threading.Thread
    for the Scan class scan window."""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        return None
    #end __init__
    def run(self):
        _ScanCanvas(self.queue)
        return None
    #end run
### end _ScanPlot ###


class _ScanCanvas(Tkinter.Frame):
    """Class for generation and event handling in the
    Scan class scan window."""
    def __init__(self, queue, master=None):
        self.destroy_self = False
        self.scan_done = False
        self.queue = queue
        self.master = master
        self.TkInstance = Tkinter.Tk()
        self.TkInstance.option_add('*Font', ('default', 14, 'bold'))
        self.TkInstance.protocol("WM_DELETE_WINDOW", self.Destroy)
        self.TkInstance.title('Scanning window')
        self.TkInstance.geometry('825x660+400+0')
        self.TkInstance.resizable(0,0)
        self.wWindow = Tkinter.Frame(self.TkInstance)
        #setup of Frame instance:
        Tkinter.Frame.__init__(self.wWindow)
        self.wWindow.place(width = 825, height = 660)
        self.wWindow.configure(bg='#FFFFFF')
        pylab.rcParams['font.size'] = 15
        self.fig= pylab.figure(facecolor='#FFFFFF', edgecolor='#FFFFFF')
        self.fig.clf()
        self.sfig = self.fig.add_subplot(111)
        self.Canvas = backend_tkagg.FigureCanvasTkAgg(self.fig, master =self.wWindow)
        self.Canvas.show()
        self.Canvas.get_tk_widget().place(x = 5, width = 815, y = 5, height = 615, anchor='nw')
        self.Button = Tkinter.Button(self.wWindow,  text = 'Exit',\
                                                 command = self.ClickButton_Exit)
        self.Button.place(x = 750, width = 70, y = 625, height = 30, anchor = 'nw')
        self.TkInstance.after(400, self.Update)
        self.wWindow.update()
        self.wWindow.configure(bg='#FFFFFF')
        self.TkInstance.mainloop()
        return None
    #end __init__
    def ClickButton_Exit(self):
        self.Destroy()
        return None
    #end ClickButton_Exit
    def Update(self):
        if self.destroy_self == False and self.scan_done == False:
            i, x, y = None, None, None
            while not self.queue.empty():
                i0,x0, y0 = copy.copy(i), copy.copy(x), copy.copy(y)
                i, x, y = self.queue.get()
                if i == None:
                    if x == y == None:
                        self.queue.task_done()
                        self.scan_done = True
                        i,x,y = i0, x0, y0
            if x != None and y != None and i > 0:
                self.fig.clf()
                self.sfig = self.fig.add_subplot(111)
                self.sfig.plot(x[:i+1], y[:i+1], 'd-', markeredgewidth=0, markersize =6, color='#2222FF', linewidth = 1.5)
                self.sfig.axis([x[0], x[-1], min(y[:i+1]), max(y[:i+1])])
                self.sfig.set_xlabel('Motor position')
                self.sfig.set_ylabel('Counter value')
                self.Canvas.show()
                self.Canvas.get_tk_widget().place(x = 5, width = 815, y = 5, height = 615, anchor='nw')
        if ThreadControl.exit_flag == True:
            ThreadControl.exit_flag = False
            self.TkInstance.destroy()
        self.TkInstance.after(50,self.Update)
        return None
    #end Update
    def run(self):
        return None
    #end run
    def Destroy(self):
        self.destroy_self = True
        #if True:
            #time.sleep(0.6)
        if tkMessageBox.askyesno('Quit?', 'Do you want to quit?', default='yes'):
            try:
                self.TkInstance.destroy()
            except:
                print('Error: Could not destroy GUI.')
                pass
        return None
    #end Destroy
### end _ScanCanvas ###


def ShowScanDeviceDict():
    scan = _ScanDeviceDict()
    scan.ShowList()
    return None
