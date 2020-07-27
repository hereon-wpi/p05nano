import PyTango
import time
import p05.tools.misc as misc
import numpy
import p05.common.TangoFailsaveComm as tcom
import p05.tools
#import PIL

class PCO_nanoCam():
    def __init__(self, tPCO=None, tTrigger=None, imageDir=None, exptime=None):
        if tPCO == None:
            self.tPCO = PyTango.DeviceProxy('//hzgpp05ct09:10000/p05/pco/01')
        else:
            self.tPCO = tPCO
        
        if tTrigger == None:
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
        else:
            self.tTrigger = tTrigger
            
        time.sleep(0.2)
        if self.tPCO.state() == PyTango.DevState.MOVING:
            self.tPCO.command_inout('StopAcq')
            while self.tPCO.state() == PyTango.DevState.MOVING:
                time.sleep(0.1)
    
        if imageDir == None:
            raise Exception('Cannot set None-type image directory!')
        else:
            self.imageDir = imageDir
        
        if exptime != None:
            self.exptime = exptime
        else:
            self.exptime = 0.1 
        
        self.CAM_xlow  = self.tPCO.read_attribute('ROI_x_min').value 
        self.CAM_xhigh = self.tPCO.read_attribute('ROI_x_max').value
        self.CAM_ylow  = self.tPCO.read_attribute('ROI_y_min').value
        self.CAM_yhigh = self.tPCO.read_attribute('ROI_y_max').value
        
        self.tPCO.write_attribute('ExposureTime', self.exptime)
        self.tPCO.write_attribute('FilePostfix', 'tif')
        # Trigger mode 1 : Internal, 2: External
        self.tPCO.write_attribute('TriggerMode', 2)
        self.tPCO.write_attribute('FilePrefix', 'Image')
        self.tPCO.write_attribute('FramesPerFile',1)
        self.tPCO.write_attribute('NbFrames',1)
        self.tPCO.write_attribute('FileDir', self.imageDir)
        self.tPCO.write_attribute('FileSaving', True)
        self.tTrigger.write_attribute('Voltage', 0)
        time.sleep(0.2)
        self.iImage = 0
        return None
    # end __init__
    
    def setExptime(self, value):
        try:
            self.tPCO.write_attribute('ExposureTime', value)
            self.exptime = value
        except Exception, e:
            print misc.GetTimeString() + ': PCO server not responding while setting new ExposureTime:\n%s' % e
        return None
    # end setExptime

    def setROI(self, xlow, xhigh, ylow, yhigh):
        self.CAM_xlow, self.CAM_xhigh = xlow, xhigh
        self.CAM_ylow, self.CAM_yhigh = ylow, yhigh
        self.tPCO.write_attribute('Roi_x_min', long(self.CAM_xlow))
        self.tPCO.write_attribute('Roi_x_max', long(self.CAM_xhigh))
        self.tPCO.write_attribute('Roi_y_min', long(self.CAM_ylow))
        self.tPCO.write_attribute('Roi_y_max', long(self.CAM_yhigh))
        return None
    
    def readAttribute(self,attribute):
        return self.tPCO.read_attribute(attribute)

    def sendcommand(self,command):
        self.tPCO.command_inout(command)

    def startPCOacquisition(self):
        self.tTrigger.write_attribute('Voltage', 0)
        if self.tPCO.state() == PyTango.DevState.MOVING:
            self.tPCO.command_inout('StopAcq')
        self.tPCO.command_inout('StartAcq')
        self.imageTime = time.time()
        self.iImage = 0
        return None
    # end startPCOacquisition
    
    def setImageName(self,name):
        while not self.tPCO.state() == PyTango.DevState.ON:
            time.sleep(0.01)        
        self.tPCO.write_attribute('FilePrefix',name)
        
    def setImgNumber(self,i):
        while not self.tPCO.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        self.tPCO.write_attribute('FileStartNum',i)

    def finishScan(self):
        self.tPCO.command_inout('StopAcq')
        return None

    def state(self):
        return self.tPCO.state()

    def acquireImage(self):
        while not self.tPCO.state() == PyTango.DevState.ON:
            time.sleep(0.005)
        start = time.clock()
        self.tPCO.command_inout('StartAcq')
        while not self.tPCO.state() == PyTango.DevState.MOVING:
            time.sleep(0.01)
            print("waiting for running")
        time.sleep(0.01)
        self.tTrigger.write_attribute('Voltage', 3.5)
        # return pmac position here!
        time.sleep(0.01)
        self.tTrigger.write_attribute('Voltage', 0)
        self.iImage += 1

        # old tango server
        #tmp = numpy.fromstring(self.tPCO.read_attribute('Image').value[1], dtype=numpy.uint16).byteswap()
        
        return None
    # end acquireImage
    



    def getCameraInfo(self):
        _s = ''
        _s += 'ExpTime\t= %e\n' % self.tPCO.read_attribute('ExposureTime').value
        _s += 'ImageHeight\t= %i\n' % self.tPCO.read_attribute('Heigth').value
        _s += 'ImageWidth\t= %i\n' % self.tPCO.read_attribute('Width').value
        _s += 'DataType\t= Uint16\n' 
        _s += 'ROI\t= [%i, %i, %i, %i]\n' % (self.tPCO.read_attribute('ROI_x_min').value, self.tPCO.read_attribute('ROI_x_max').value, \
                                             self.tPCO.read_attribute('ROI_y_min').value, self.tPCO.read_attribute('ROI_y_max').value)
        return _s
    
    
class FLIeh2_nanoCam():
    def __init__(self, tFLI=None, imageDir=None, exptime=None):
        if tFLI == None:
            self.tFLI = PyTango.DeviceProxy('//hzgpp05ct1:10000/p05/eh2/smc0900')
        else:
            self.tFLI = tFLI
        
        if self.tFLI.state() == PyTango.DevState.RUNNING:
            self.tFLI.command_inout('Stop')
            time.sleep(0.3)
    
        if imageDir == None:
            raise Exception('Cannot set None-type image directory!')
        else:
            self.imageDir = imageDir
            tcom.tSaveCommWriteAttribute(self.tFLI, 'BaseDir', self.imageDir)
       
        self.CAM_PosX_FromPix = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array((Ytotal - Ymin, Ytotal - Ymax))
        self.CAM_PixY_FromPos = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array((Xtotal - Xmin, Xtotal - Xmax))
        self.CAM_PosY_FromPix = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array((Xtotal - Xmin, Xtotal - Xmax))
        self.CAM_PixX_FromPos = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array((Ytotal - Ymin, Ytotal - Ymax))
       
        self.CAM_Binning = self.tFLI.read_attribute('VBin')
        tmp_x1 = self.tFLI.read_attribute('Roi_ul_x').value / self.CAM_Binning
        tmp_x2 = self.tFLI.read_attribute('Roi_lr_x').value + tmp_x1
        tmp_y1 = self.tFLI.read_attribute('Roi_ul_y').value / self.CAM_Binning
        tmp_y2 = self.tFLI.read_attribute('Roi_lr_y').value + tmp_y1
        tmp_x = self.CAM_PosX_FromPix(tmp_x1, tmp_x2, 3056 / self.CAM_Binning, tmp_y1, tmp_y2, 3056 / self.CAM_Binning)
        tmp_y = self.CAM_PosY_FromPix(tmp_x1, tmp_x2, 3056 / self.CAM_Binning, tmp_y1, tmp_y2, 3056 / self.CAM_Binning)
        self.CAM_xlow = min(tmp_x)
        self.CAM_xhigh = max(tmp_x)
        self.CAM_ylow = min(tmp_y)
        self.CAM_yhigh = max(tmp_y)
        self.CAM_xPix = self.CAM_xhigh - self.CAM_xlow
        self.CAM_yPix = self.CAM_yhigh - self.CAM_ylow

        if exptime != None:
            self.exptime = exptime
        else:
            self.exptime = 0.1
            tcom.tSaveCommWriteAttribute(self.tFLI, 'ExposureTime', self.exptime)
        
        return None
    # end __init__
    
    def setExptime(self, value):
        try:
            self.tFLI.write_attribute('ExposureTime', value)
            self.exptime = value
        except Exception, e:
            print misc.GetTimeString() + ': FLI  server not responding while setting new ExposureTime:\n%s' % e
        return None
    # end setExptime

    def acquireImage(self):
        if self.tFLI.state() == PyTango.DevState.EXTRACT:
            tcom.tSaveCommCommand(self.tFLI, 'GrabFrame')
            time.sleep(1.5)
        
        tcom.tSaveCommCommand(self.tFLI, 'ExposeFrame')
        time.sleep(self.exptime + 0.15)
        tcom.tSaveCommCommand(self.tFLI, 'GrabFrame')
        
        im = numpy.fromstring(self.tFLI.read_attribute('Image').value, dtype=numpy.uint16)[2:].reshape(3056, 3056)
        return im
    # end acquireImage
    
    def setROI(self, xlow, xhigh, ylow, yhigh):
        tmp_x = self.CAM_PixX_FromPos(xlow, xhigh, 3056 / self.CAM_Binning, ylow, yhigh, 3056 / self.CAM_Binning)
        tmp_y = self.CAM_PixY_FromPos(xlow, xhigh, 3056 / self.CAM_Binning, ylow, yhigh, 3056 / self.CAM_Binning)
        self.CAM_xlow, self.CAM_xhigh = min(tmp_x), max(tmp_x)
        self.CAM_ylow, self.CAM_yhigh = min(tmp_y), max(tmp_y)
        self.tFLI.write_attribute('Roi_ul_x', long(self.CAM_xlow))
        self.tFLI.write_attribute('Roi_lr_y', long(self.CAM_yhigh - self.CAM_ylow))
        self.tFLI.write_attribute('Roi_lr_x', long(self.CAM_xhigh - self.CAM_xlow))
        self.tFLI.write_attribute('Roi_ul_y', long(self.CAM_ylow))
        return None
    
    def finishScan(self):
        pass
        return None
    
    def getCameraInfo(self):
        _s = ''
        _s += 'ExpTime\t= %e\n' % self.tFLI.read_attribute('ExposureTime').value
        _s += 'DataType\t= Uint16\n' 
        _s += 'Binning\t= %i' % self.CAM_Binning
        _s += 'ROI\t= [%i, %i, %i, %$i]\n' % (self.CAM_xlow, self.CAM_xhigh, self.CAM_ylow, self.CAM_yhigh)
        return _s


class Hamamatsu_nanoCam():
    def __init__(self, tHama=None, tTrigger=None, imageDir=None, exptime=None):
        if tHama == None:
            self.tHama = PyTango.DeviceProxy('//hzgpp05vme1.desy.de:10000/p05/camera/hama')
        else:
            self.tHama = tHama
        if tTrigger== None:
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out03')
        else:
            self.tTrigger = tTrigger
        

        self.CAM_Binning = 1

        time.sleep(0.1)
        if self.tHama.state() == PyTango.DevState.EXTRACT:
            self.tHama.command_inout('AbortAcq')
            while self.tHama.state() == PyTango.DevState.EXTRACT:
                time.sleep(0.01)
                
        if imageDir == None:
            raise Exception('Cannot set None-type image directory!')
        else:
            self.imageDir = imageDir

        if exptime != None:
            self.exptime = exptime
        else:
            self.exptime = 0.1
        
        self.CAM_xlow  = self.tHama.read_attribute('SUBARRAY_HPOS').value 
        self.CAM_xhigh = self.tHama.read_attribute('SUBARRAY_HSIZE').value + self.tHama.read_attribute('SUBARRAY_HPOS').value
        self.CAM_ylow  = self.tHama.read_attribute('SUBARRAY_VPOS').value
        self.CAM_yhigh = self.tHama.read_attribute('SUBARRAY_VSIZE').value + self.tHama.read_attribute('SUBARRAY_VPOS').value
        
        self.tHama.write_attribute('EXPOSURE_TIME', self.exptime)
        time.sleep(0.2)
        #self.tHama.write_attribute('FilePostfix', '.bin') #!!!!
        self.tHama.write_attribute('TRIGGER_SOURCE', 'EXTERNAL')
        time.sleep(0.2)
        self.tHama.write_attribute('TRIGGER_ACTIVE', 'EDGE')
        time.sleep(0.2)
        self.tHama.write_attribute('OUTPUT_TRIGGER_KIND[0]','TRIGGER READY')
        time.sleep(0.2)
        self.tHama.write_attribute('TRIGGER_POLARITY','POSITIVE')
        time.sleep(0.2)
        self.tHama.write_attribute('OUTPUT_TRIGGER_POLARITY[0]','POSITIVE')
        time.sleep(0.2)
        self.tHama.write_attribute('FilePrefix', 'Image')
        self.tHama.write_attribute('FileDirectory', self.imageDir)
        self.tHama.write_attribute('FileRefNumber', 0)
        self.tHama.write_attribute('SaveImageFlag', True)
        self.tTrigger.write_attribute('Value', 0)  #!!!!
        #self.tTrigger.write_attribute('Voltage', 0)  #!!!!
        time.sleep(0.2)
        self.iImage = 0
        
        return None
    # end __init__
    


    def setExptime(self, value):
        try:
            while not self.tHama.state() == PyTango.DevState.ON:
                time.sleep(0.01) 
            self.tHama.write_attribute('EXPOSURE_TIME', value)
            self.exptime = value
        except Exception, e:
            print misc.GetTimeString() + ': Hamamatsu server not responding while setting new ExposureTime:\n%s' % e
        while not self.tHama.state() == PyTango.DevState.ON:
            time.sleep(0.01) 
        return None
    # end setExptime
    
    def setImgNumber(self,i):
        while not self.tHama.state() == PyTango.DevState.ON:
            time.sleep(0.01) 
        self.tHama.write_attribute('FileRefNumber',i)
        
        return None

    def sendCommand(self,command):
        self.tHama.command_inout(command)

    def state(self):
        return self.tHama.state()

    def readAttribute(self,attribute):
        return self.tHama.read_attribute(attribute)

    def getImgNumber(self):
        i = self.tHama.read_attribute('FileRefNumber')
        return i
    
    def getImage(self):
        return self.tHama.read_attribute('IMAGE').value
    
    def acquireImage(self):
        start = time.clock()
        while not self.tHama.state() == PyTango.DevState.ON:
            time.sleep(0.005)
        end = time.clock()
#        print("waiting for on state:" + str(end-start) )
        self.tHama.command_inout('StartAcq')
        while not self.tHama.state() == PyTango.DevState.EXTRACT:
            time.sleep(0.005)
        #self.tTrigger.write_attribute('Voltage', 3.5)
        self.tTrigger.write_attribute('Value', 1) 
        time.sleep(0.005)
        #self.tTrigger.write_attribute('Voltage', 0)
        self.tTrigger.write_attribute('Value', 0) 
        self.imageTime = time.time()
        self.iImage = 0
#         while not self.tHama.state() == PyTango.DevState.ON:
#             time.sleep(0.01)
#         time.sleep(0.01)
        return None

    def startLive(self):
        self.tHama.StartVideoAcq()
        return None

    
    def stopHamaacquisition(self):
        self.tTrigger.write_attribute('Value', 0)
        #self.tTrigger.write_attribute('Voltage', 0) 
        while self.tHama.state() == PyTango.DevState.EXTRACT:
            self.tHama.command_inout('AbortAcq')
            time.sleep(0.1)
        self.tHama.command_inout('AbortAcq')
        self.imageTime = time.time()
        self.iImage = 0
        time.sleep(3)
        return None
    
    def setROI(self,xlow,xhigh,ylow,yhigh):
        self.CAM_xlow, self.CAM_xhigh = xlow, xhigh
        self.CAM_ylow, self.CAM_yhigh = ylow, yhigh
        self.tHama.write_attribute('SUBARRAY_MODE','ON')
        self.tHama.write_attribute('SUBARRAY_HPOS', long(self.CAM_xlow))
        self.tHama.write_attribute('SUBARRAY_HSIZE', long(self.CAM_xhigh-self.CAM_xlow))
        self.tHama.write_attribute('SUBARRAY_VPOS', long(self.CAM_ylow))
        self.tHama.write_attribute('SUBARRAY_VSIZE', long(self.CAM_yhigh-self.CAM_yhigh))
        return None
    
    def setImageName(self,name):
        while not self.tHama.state() == PyTango.DevState.ON:
            time.sleep(0.01)        
        self.tHama.write_attribute('FilePrefix',name)

    
    def finishScan(self):
        self.tHama.command_inout('AbortAcq')
        return None
    
    def getCameraInfo(self):
        _s = ''
        _s += 'ExpTime\t= externally set\n'
        _s += 'DataType\t= Uint16\n' 
        _s += 'Binning\t= 1'
        _s += 'ROI= [0, 2048,0, 20488]\n'
        return _s

class PixelLink_nanoCam():
    def __init__(self, tPixelLink=None, tTrigger=None, imageDir=None, exptime=None):
        if tPixelLink == None:
            self.tPixelLink = PyTango.DeviceProxy('//hzgpp05vme1.desy.de:10000/p05/camera/pixlink')
        else:
            self.tPixelLink = tPixelLink
            
        if tTrigger== None:
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
        else:
            self.tTrigger = tTrigger
        
        self.CAM_Binning = 1

        time.sleep(0.2)
        if self.tPixelLink.state() == PyTango.DevState.EXTRACT:
            self.tPixelLink.command_inout('AbortAcq')
            while self.tPixelLink.state() == PyTango.DevState.EXTRACT:
                time.sleep(0.1)
                
        if imageDir == None:
            raise Exception('Cannot set None-type image directory!')
        else:
            self.imageDir = imageDir

        if exptime != None:
            self.exptime = exptime
        else:
            self.exptime = 0.1

        print self.exptime
        self.tPixelLink.write_attribute('SHUTTER', 1)
        #self.tPixelLink.write_attribute('FilePostfix', '.bin') #!!!!
        #self.tPixelLink.write_attribute('TRIGGER_SOURCE', 'EXTERNAL')
        #self.tPixelLink.write_attribute('TRIGGER_ACTIVE', 'EDGE')
        self.tPixelLink.write_attribute('FilePrefix', 'Image')
        self.tPixelLink.write_attribute('FileDirectory', self.imageDir)
        self.tPixelLink.write_attribute('FileRefNumber', 0)
        self.tPixelLink.write_attribute('SaveImageFlag', True)
        #self.tTrigger.write_attribute('Value', 0)  #!!!!
        self.tTrigger.write_attribute('Voltage', 0)  #!!!!
        time.sleep(0.2)
        self.iImage = 0
        
        return None
    # end __init__
    
    def setExptime(self, value):
        try:
            self.tPixelLink.write_attribute('SHUTTER', value)
            self.exptime = value
        except Exception, e:
            print misc.GetTimeString() + ': PixelLink server not responding while setting new ExposureTime:\n%s' % e
        return None
    # end setExptime
    
    def setImgNumber(self,i):
        self.tPixelLink.write_attribute('FileRefNumber',i)
        return None

    def getImgNumber(self):
        i = self.tPixelLink.read_attribute('FileRefNumber')
        return i
    
    def getImage(self):
        return self.tPixelLink.read_attribute('IMAGE').value
    
    def acquireImage(self):
        while not self.tPixelLink.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        self.tPixelLink.command_inout('StartAcq')
        time.sleep(0.1)
        self.tTrigger.write_attribute('Voltage', 3.5)
        #self.tTrigger.write_attribute('Value', 1) 
        time.sleep(0.01)
        self.tTrigger.write_attribute('Voltage', 0)
        #self.tTrigger.write_attribute('Value', 0) 
        
        self.imageTime = time.time()
        self.iImage = 0
        while not self.tPixelLink.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        return self.tPixelLink.read_attribute('IMAGE').value

    
    def stopAcquisition(self):
        #self.tTrigger.write_attribute('Value', 0)
        self.tTrigger.write_attribute('Voltage', 0) 
        while self.tPixelLink.state() == PyTango.DevState.EXTRACT:
            self.tPixelLink.command_inout('AbortAcq')
            time.sleep(0.1)
        self.tPixelLink.command_inout('AbortAcq')
        self.imageTime = time.time()
        self.iImage = 0
        time.sleep(3)
        return None
    
    def setImageName(self,name): 
        self.tPixelLink.write_attribute('FilePrefix',name)
    
    def finishScan(self):
        self.tPixelLink.command_inout('AbortAcq')
        return None
    
    def getCameraInfo(self):
        _s = ''
        _s += 'ExpTime\t= externally set\n'
        _s += 'DataType\t= Uint16\n' 
        _s += 'Binning\t= 1'
        _s += 'ROI= [0, 2048,0, 20488]\n'
        return _s


class Zyla_nanoCam():
    def __init__(self, tZyla=None, tTrigger=None, imageDir=None, exptime=None):
        if tZyla == None:
            self.tZyla = PyTango.DeviceProxy('hzgpp05ct09:10000/p05/limaccds/ct09.01') # change Tango Server here!
        else:
            self.tZyla = tZyla
            
        if tTrigger== None:
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out03')   # Set Trigger here!
        else:
            self.tTrigger = tTrigger
        
        self.CAM_Binning = 1

        time.sleep(0.1)
        self.tZyla.command_inout('stopAcq')
        if self.tZyla.state() == PyTango.DevState.EXTRACT:
            self.tZyla.command_inout('abortAcq')
            while self.tZyla.state() == PyTango.DevState.EXTRACT:
                time.sleep(0.01)
                
        if imageDir == None:
            raise Exception('Cannot set None-type image directory!')
        else:
            self.imageDir = imageDir

        if exptime != None:
            self.exptime = exptime
        else:
            self.exptime = 0.1
        
        self.tZyla.write_attribute('acq_expo_time', self.exptime)
        self.tZyla.write_attribute('saving_format', 'tiff') #!!!!
        self.tZyla.write_attribute('saving_index_format', '%05d')
        self.tZyla.write_attribute('saving_mode', 'auto_frame')
        self.tZyla.write_attribute('acq_trigger_mode', 'external_trigger')

        self.tZyla.write_attribute('saving_prefix', 'Image')
        self.tZyla.write_attribute('saving_directory', self.imageDir)
		
        self.tZyla.write_attribute('saving_next_number', 1)
        self.tTrigger.write_attribute('Value', 0)  #!!!!
        time.sleep(0.2)
        self.iImage = 0
        
        return None
    # end __init__
    
    def setExptime(self, value):
        try:
            while self.tZyla.read_attribute('ready_for_next_acq') == False:
                time.sleep(0.01) 
            self.tZyla.write_attribute('acq_expo_time', value)
            self.exptime = value
        except Exception, e:
            print misc.GetTimeString() + ': Hamamatsu server not responding while setting new ExposureTime:\n%s' % e
        while not self.tZyla.state() == PyTango.DevState.ON:
            time.sleep(0.01) 
        return None
    # end setExptime
    
    def setImgNumber(self,i):
        while self.tZyla.read_attribute('ready_for_next_acq').value == False:
            time.sleep(0.001)
        self.tZyla.write_attribute('saving_next_number',i)
        
        return None

    def getImgNumber(self):
        i = self.tZyla.read_attribute('saving_next_number')
        return i
    
    def getImage(self):
        return self.tZyla.read_attribute('IMAGE').value
    
    def acquireImage(self):
        while self.tZyla.read_attribute('ready_for_next_acq').value == False:
            time.sleep(0.001)
        self.tZyla.command_inout('stopAcq')
        time.sleep(0.01)
        self.tZyla.command_inout('prepareAcq')
        time.sleep(0.01)
        self.tZyla.command_inout('startAcq')
		
        #while not self.tZyla.state() == PyTango.DevState.EXTRACT:
        time.sleep(0.1) 
        #time.sleep(1)
        #self.tTrigger.write_attribute('Voltage', 3.5)
        self.tTrigger.write_attribute('Value', 1) 
        time.sleep(0.1)
        #self.tTrigger.write_attribute('Voltage', 0)
        self.tTrigger.write_attribute('Value', 0) 
        #time.sleep(self.exptime)
        self.imageTime = time.time()
        self.iImage = 0
#         while not self.tZyla.state() == PyTango.DevState.ON:
#             time.sleep(0.01)
#         time.sleep(0.01)
        #self.tZyla.command_inout('stopAcq')
        return None

    
    def stopHamaacquisition(self):
        self.tTrigger.write_attribute('Value', 0)
        #self.tTrigger.write_attribute('Voltage', 0) 
        while self.tZyla.state() == PyTango.DevState.EXTRACT:
            self.tZyla.command_inout('abortAcq')
            time.sleep(0.1)
        self.tZyla.command_inout('abortAcq')
        self.imageTime = time.time()
        self.iImage = 0
        time.sleep(3)
        return None
    
    def setImageName(self,name):
        while self.tZyla.read_attribute('ready_for_next_acq').value == False:
            time.sleep(0.001)        
        self.tZyla.write_attribute('saving_prefix',name)

    
    def finishScan(self):
        self.tZyla.command_inout('abortAcq')
        return None
    
    def getCameraInfo(self):
        _s = ''
        _s += 'ExpTime\t= externally set\n'
        _s += 'DataType\t= Uint16\n' 
        _s += 'Binning\t= 1'
        _s += 'ROI= [0, 2048,0, 20488]\n'
        return _s

class KIT_nanoCam():
    def __init__(self, tKIT=None, tTrigger=None, imageDir=None, exptime=None):
        if tKIT == None:
            self.tKIT = PyTango.DeviceProxy('//hzgpp05ctcam1:10000/p05/hzguca/kit')
        else:
            self.tKIT = tKIT

        if tTrigger == None:
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/register/eh1.out01')
        else:
            self.tTrigger = tTrigger

        time.sleep(0.2)

        if imageDir == None:
            raise Exception('Cannot set None-type image directory!')
        else:
            self.imageDir = imageDir

        if exptime != None:
            self.exptime = exptime
        else:
            self.exptime = float( 1. / 5. *1.0062903)

#        if self.tKIT.state() == PyTango.DevState.STANDBY:
#            self.tKIT.command_inout('Stop')
#            time.sleep(0.1)
#        self.tKIT.write_attribute('exposure_time', self.exptime)
#        self.tKIT.write_attribute('trigger_source', 2)
#        self.tKIT.write_attribute('image_file_name_pattern', 'img_%04d.tif')
#        self.tKIT.write_attribute('image_path', self.imageDir)
#        self.tKIT.write_attribute('tiffWriteDisk', 1)
#        self.tKIT.write_attribute('number_of_frames',1)
#        self.tKIT.command_inout('Start')
#        while not self.tKIT.state() == PyTango.DevState.STANDBY:
#            time.sleep(0.01)
        self.tTrigger.write_attribute('Value', 0)
        time.sleep(0.2)
        self.iImage = 0
        return None
    # end __init__

    def setKITAttribute(self, attribute, value):
        try:
#            if self.tKIT.state() == PyTango.DevState.STANDBY:
#                self.tKIT.command_inout('Stop')
#            while not self.tKIT.state() == PyTango.DevState.ON:
#                time.sleep(0.01)
            self.tKIT.write_attribute(attribute, value)
#            self.tKIT.command_inout('Start')
#            while not self.tKIT.state() == PyTango.DevState.STANDBY:
#                time.sleep(0.01)
        except Exception, e:
            print misc.GetTimeString() + ': KIT server not responding while setting new ExposureTime:\n%s' % e
        return None

    def setImageName(self,name):
        imgname = name +'_%04d.tif'
        print(imgname)
        self.setKITAttribute('image_file_name_pattern',imgname)

    def setExptime(self,value):
        if self.tKIT.state() == PyTango.DevState.STANDBY:
            self.tKIT.command_inout('Stop')
            while not self.tKIT.state() == PyTango.DevState.ON:
                time.sleep(0.01)
        self.exptime = float(float(value)/ 5. *1.0062903)
        self.setKITAttribute('exposure_time',self.exptime)
        time.sleep(0.5)
        self.tKIT.command_inout('Start')
        while not self.tKIT.state() == PyTango.DevState.STANDBY:
            time.sleep(0.01)

    def setImgNumber(self,i):
        self.setKITAttribute('image_counter',i)

    def finishScan(self):
        self.tKIT.command_inout('Stop')
        return None

    def acquireImage(self):
        while self.tKIT.state() == PyTango.DevState.RUNNING:
            time.sleep(0.01)
        if self.tKIT.state() == PyTango.DevState.ON:
            self.tKIT.command_inout('Start')
            time.sleep(0.01)
        while not self.tKIT.state() == PyTango.DevState.STANDBY:
            time.sleep(0.01)
        self.tKIT.command_inout('Store',1)
        while not self.tKIT.state() == PyTango.DevState.RUNNING:
            time.sleep(0.01)

        self.tTrigger.write_attribute('Value', 1)
        time.sleep(0.01)
        self.tTrigger.write_attribute('Value', 0)
        self.iImage += 1
        return
    # end acquireImage

