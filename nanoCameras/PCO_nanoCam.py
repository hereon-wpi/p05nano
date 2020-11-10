import time

import PyTango

import p05.common.PyTangoProxyConstants as proxies
import p05.tools.misc as misc


class PCO_nanoCam():
    def __init__(self, tPCO=None, tTrigger=None, imageDir=None, exptime=None):
        if tPCO == None:
            self.tPCO = PyTango.DeviceProxy(proxies.camera_pco)
        else:
            self.tPCO = tPCO

        if tTrigger == None:
            self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_01)
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

        self.CAM_xlow = self.tPCO.read_attribute('ROI_x_min').value
        self.CAM_xhigh = self.tPCO.read_attribute('ROI_x_max').value
        self.CAM_ylow = self.tPCO.read_attribute('ROI_y_min').value
        self.CAM_yhigh = self.tPCO.read_attribute('ROI_y_max').value

        self.tPCO.write_attribute('ExposureTime', self.exptime)
        self.tPCO.write_attribute('FilePostfix', 'tif')
        # Trigger mode 1 : Internal, 2: External
        self.tPCO.write_attribute('TriggerMode', 2)
        self.tPCO.write_attribute('FilePrefix', 'Image')
        self.tPCO.write_attribute('FramesPerFile', 1)
        self.tPCO.write_attribute('NbFrames', 1)
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
        except Exception as e:
            print(misc.GetTimeString() + ': PCO server not responding while setting new ExposureTime:\n%s' % e)
        return None

    # end setExptime

    def setROI(self, xlow, xhigh, ylow, yhigh):
        self.CAM_xlow, self.CAM_xhigh = xlow, xhigh
        self.CAM_ylow, self.CAM_yhigh = ylow, yhigh
        self.tPCO.write_attribute('Roi_x_min', int(self.CAM_xlow))
        self.tPCO.write_attribute('Roi_x_max', int(self.CAM_xhigh))
        self.tPCO.write_attribute('Roi_y_min', int(self.CAM_ylow))
        self.tPCO.write_attribute('Roi_y_max', int(self.CAM_yhigh))
        return None

    def readAttribute(self, attribute):
        return self.tPCO.read_attribute(attribute)

    def sendcommand(self, command):
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

    def setImageName(self, name):
        while not self.tPCO.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        self.tPCO.write_attribute('FilePrefix', name)

    def setImgNumber(self, i):
        while not self.tPCO.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        self.tPCO.write_attribute('FileStartNum', i)

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
        # tmp = numpy.fromstring(self.tPCO.read_attribute('Image').value[1], dtype=numpy.uint16).byteswap()

        return None

    # end acquireImage

    def getCameraInfo(self):
        _s = ''
        _s += 'ExpTime\t= %e\n' % self.tPCO.read_attribute('ExposureTime').value
        _s += 'ImageHeight\t= %i\n' % self.tPCO.read_attribute('Heigth').value
        _s += 'ImageWidth\t= %i\n' % self.tPCO.read_attribute('Width').value
        _s += 'DataType\t= Uint16\n'
        _s += 'ROI\t= [%i, %i, %i, %i]\n' % (
            self.tPCO.read_attribute('ROI_x_min').value, self.tPCO.read_attribute('ROI_x_max').value, \
            self.tPCO.read_attribute('ROI_y_min').value, self.tPCO.read_attribute('ROI_y_max').value)
        return _s
