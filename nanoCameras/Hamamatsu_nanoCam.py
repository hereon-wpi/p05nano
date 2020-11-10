import time

import PyTango

import p05.common.PyTangoProxyConstants as proxies
import p05.tools.misc as misc


class Hamamatsu_nanoCam():
    def __init__(self, tHama=None, tTrigger=None, imageDir=None, exptime=None):
        if tHama == None:
            self.tHama = PyTango.DeviceProxy(proxies.camera_hama)
        else:
            self.tHama = tHama
        if tTrigger == None:
            self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out03)
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

        self.CAM_xlow = self.tHama.read_attribute('SUBARRAY_HPOS').value
        self.CAM_xhigh = self.tHama.read_attribute('SUBARRAY_HSIZE').value + self.tHama.read_attribute(
            'SUBARRAY_HPOS').value
        self.CAM_ylow = self.tHama.read_attribute('SUBARRAY_VPOS').value
        self.CAM_yhigh = self.tHama.read_attribute('SUBARRAY_VSIZE').value + self.tHama.read_attribute(
            'SUBARRAY_VPOS').value

        self.tHama.write_attribute('EXPOSURE_TIME', self.exptime)
        time.sleep(0.2)
        # self.tHama.write_attribute('FilePostfix', '.bin') #!!!!
        self.tHama.write_attribute('TRIGGER_SOURCE', 'EXTERNAL')
        time.sleep(0.2)
        self.tHama.write_attribute('TRIGGER_ACTIVE', 'EDGE')
        time.sleep(0.2)
        self.tHama.write_attribute('OUTPUT_TRIGGER_KIND[0]', 'TRIGGER READY')
        time.sleep(0.2)
        self.tHama.write_attribute('TRIGGER_POLARITY', 'POSITIVE')
        time.sleep(0.2)
        self.tHama.write_attribute('OUTPUT_TRIGGER_POLARITY[0]', 'POSITIVE')
        time.sleep(0.2)
        self.tHama.write_attribute('FilePrefix', 'Image')
        self.tHama.write_attribute('FileDirectory', self.imageDir)
        self.tHama.write_attribute('FileRefNumber', 0)
        self.tHama.write_attribute('SaveImageFlag', True)
        self.tTrigger.write_attribute('Value', 0)  # !!!!
        # self.tTrigger.write_attribute('Voltage', 0)  #!!!!
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
        except Exception as e:
            print(misc.GetTimeString() + ': Hamamatsu server not responding while setting new ExposureTime:\n%s' % e)
        while not self.tHama.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        return None

    # end setExptime

    def setImgNumber(self, i):
        while not self.tHama.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        self.tHama.write_attribute('FileRefNumber', i)

        return None

    def sendCommand(self, command):
        self.tHama.command_inout(command)

    def state(self):
        return self.tHama.state()

    def readAttribute(self, attribute):
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
        # self.tTrigger.write_attribute('Voltage', 3.5)
        self.tTrigger.write_attribute('Value', 1)
        time.sleep(0.005)
        # self.tTrigger.write_attribute('Voltage', 0)
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
        # self.tTrigger.write_attribute('Voltage', 0)
        while self.tHama.state() == PyTango.DevState.EXTRACT:
            self.tHama.command_inout('AbortAcq')
            time.sleep(0.1)
        self.tHama.command_inout('AbortAcq')
        self.imageTime = time.time()
        self.iImage = 0
        time.sleep(3)
        return None

    def setROI(self, xlow, xhigh, ylow, yhigh):
        self.CAM_xlow, self.CAM_xhigh = xlow, xhigh
        self.CAM_ylow, self.CAM_yhigh = ylow, yhigh
        self.tHama.write_attribute('SUBARRAY_MODE', 'ON')
        self.tHama.write_attribute('SUBARRAY_HPOS', int(self.CAM_xlow))
        self.tHama.write_attribute('SUBARRAY_HSIZE', int(self.CAM_xhigh - self.CAM_xlow))
        self.tHama.write_attribute('SUBARRAY_VPOS', int(self.CAM_ylow))
        self.tHama.write_attribute('SUBARRAY_VSIZE', int(self.CAM_yhigh - self.CAM_yhigh))
        return None

    def setImageName(self, name):
        while not self.tHama.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        self.tHama.write_attribute('FilePrefix', name)

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
