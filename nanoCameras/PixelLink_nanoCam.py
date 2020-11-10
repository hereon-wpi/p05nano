import time

import PyTango

import p05.common.PyTangoProxyConstants as proxies
import p05.tools.misc as misc


class PixelLink_nanoCam():
    def __init__(self, tPixelLink=None, tTrigger=None, imageDir=None, exptime=None):
        if tPixelLink == None:
            self.tPixelLink = PyTango.DeviceProxy(proxies.camera_pixlink)
        else:
            self.tPixelLink = tPixelLink

        if tTrigger == None:
            self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_01)
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

        print(self.exptime)
        self.tPixelLink.write_attribute('SHUTTER', 1)
        # self.tPixelLink.write_attribute('FilePostfix', '.bin') #!!!!
        # self.tPixelLink.write_attribute('TRIGGER_SOURCE', 'EXTERNAL')
        # self.tPixelLink.write_attribute('TRIGGER_ACTIVE', 'EDGE')
        self.tPixelLink.write_attribute('FilePrefix', 'Image')
        self.tPixelLink.write_attribute('FileDirectory', self.imageDir)
        self.tPixelLink.write_attribute('FileRefNumber', 0)
        self.tPixelLink.write_attribute('SaveImageFlag', True)
        # self.tTrigger.write_attribute('Value', 0)  #!!!!
        self.tTrigger.write_attribute('Voltage', 0)  # !!!!
        time.sleep(0.2)
        self.iImage = 0

        return None

    # end __init__

    def setExptime(self, value):
        try:
            self.tPixelLink.write_attribute('SHUTTER', value)
            self.exptime = value
        except Exception as e:
            print(misc.GetTimeString() + ': PixelLink server not responding while setting new ExposureTime:\n%s' % e)
        return None

    # end setExptime

    def setImgNumber(self, i):
        self.tPixelLink.write_attribute('FileRefNumber', i)
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
        # self.tTrigger.write_attribute('Value', 1)
        time.sleep(0.01)
        self.tTrigger.write_attribute('Voltage', 0)
        # self.tTrigger.write_attribute('Value', 0)

        self.imageTime = time.time()
        self.iImage = 0
        while not self.tPixelLink.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        return self.tPixelLink.read_attribute('IMAGE').value

    def stopAcquisition(self):
        # self.tTrigger.write_attribute('Value', 0)
        self.tTrigger.write_attribute('Voltage', 0)
        while self.tPixelLink.state() == PyTango.DevState.EXTRACT:
            self.tPixelLink.command_inout('AbortAcq')
            time.sleep(0.1)
        self.tPixelLink.command_inout('AbortAcq')
        self.imageTime = time.time()
        self.iImage = 0
        time.sleep(3)
        return None

    def setImageName(self, name):
        self.tPixelLink.write_attribute('FilePrefix', name)

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
