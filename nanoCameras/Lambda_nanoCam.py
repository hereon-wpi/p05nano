import time

import PyTango

import p05.common.PyTangoProxyConstants as proxies
import p05.tools.misc as misc


class Lambda_nanoCam():
    def __init__(self, tDet=None, tTrigger=None, imageDir=None, exptime=None):
        if tDet == None:
            self.tDet = PyTango.DeviceProxy(proxies.camera_lambda)
        else:
            self.tDet = tDet
        if tTrigger == None:
            self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out03)
        else:
            self.tTrigger = tTrigger

        self.CAM_Binning = 1

        time.sleep(0.1)
        # if self.tDet.state() == PyTango.DevState.MOVING:
        #     self.tDet.command_inout('AbortAcq')
        #     while self.tDet.state() == PyTango.DevState.EXTRACT:
        #         time.sleep(0.01)

        if imageDir == None:
            raise Exception('Cannot set None-type image directory!')
        else:
            self.imageDir = imageDir

        if exptime != None:
            self.exptime = exptime
        else:
            self.exptime = 1000
        print("hallo")
        # self.CAM_xlow = self.tDet.read_attribute('SUBARRAY_HPOS').value
        # self.CAM_xhigh = self.tDet.read_attribute('SUBARRAY_HSIZE').value + self.tDet.read_attribute(
        #     'SUBARRAY_HPOS').value
        # self.CAM_ylow = self.tDet.read_attribute('SUBARRAY_VPOS').value
        # self.CAM_yhigh = self.tDet.read_attribute('SUBARRAY_VSIZE').value + self.tDet.read_attribute(
        #     'SUBARRAY_VPOS').value
        print(self.exptime)
        self.tDet.write_attribute('ShutterTime', self.exptime * 1000)
        time.sleep(0.2)
        # self.tDet.write_attribute('FilePostfix', '.bin') #!!!!
        self.tDet.write_attribute('TriggerMode', 0)
        time.sleep(0.2)
        self.tDet.write_attribute('FilePrefix', 'Image')
        time.sleep(0.2)
        self.tDet.write_attribute('SaveFilePath', self.imageDir)
        time.sleep(0.2)
        self.tDet.write_attribute('FileStartNum', 0)
        time.sleep(0.2)
        self.tDet.write_attribute('SaveAllImages', True)
        time.sleep(0.2)
        self.tDet.write_attribute('OperatingMode', 'TwentyFourBit')
        time.sleep(0.2)
        self.tDet.write_attribute('EnergyThreshold', 5500)
        time.sleep(0.2)
        self.tDet.write_attribute('FrameNumbers', 1)
        self.tTrigger.write_attribute('Value', 0)  # !!!!
        # self.tTrigger.write_attribute('Voltage', 0)  #!!!!
        time.sleep(0.2)
        self.iImage = 0

        return None

    # end __init__

    def setExptime(self, value):
        try:
            while not self.tDet.state() == PyTango.DevState.ON:
                time.sleep(0.01)
            self.tDet.write_attribute('ShutterTime', value)
            self.exptime = value
        except Exception as e:
            print(misc.GetTimeString() + ': Lambda server not responding while setting new ExposureTime:\n%s' % e)
        while not self.tDet.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        return None

    # end setExptime

    def setImgNumber(self, i):
        while not self.tDet.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        self.tDet.write_attribute('FileStartNum', int(i))
        return None

    def setFrameNumbers(self, i):
        while not self.tDet.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        self.tDet.write_attribute('FrameNumbers', i)
        return None

    def sendCommand(self, command):
        self.tDet.command_inout(command)

    def sendTrigger(self):
        self.tTrigger.write_attribute('Value', 1)
        time.sleep(0.005)
        self.tTrigger.write_attribute('Value', 0)

    def state(self):
        return self.tDet.state()

    def readAttribute(self, attribute):
        return self.tDet.read_attribute(attribute)

    def waitForCamera(self):
        while not self.tDet.state() == PyTango.DevState.ON:
            time.sleep(0.01)

    def writeAttribute(self, attribute, value):
        while not self.tDet.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        return self.tDet.write_attribute(attribute, value)

    def getImgNumber(self):
        i = self.tDet.read_attribute('FileStartNumber')
        return i

    def getImage(self):
        return self.tDet.read_attribute('LiveLastImageData').value

    def acquireImage(self):
        start = time.clock()
        while not self.tDet.state() == PyTango.DevState.ON:
            time.sleep(0.005)
        end = time.clock()
        #        print("waiting for on state:" + str(end-start) )
        self.tDet.command_inout('StartAcq')
        self.tTrigger.write_attribute('Value', 1)
        time.sleep(0.005)
        self.tTrigger.write_attribute('Value', 0)
        self.imageTime = time.time()
        self.iImage = 0
        return None

    def startLive(self):
        while not self.tDet.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        self.tDet.write_attribute('TriggerMode', 2)
        self.tDet.write_attribute('FrameNumbers', 10000)
        self.tDet.command_inout('StartAcq')
        return None

    def setImageName(self, name):
        while not self.tDet.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        self.tDet.write_attribute('FilePrefix', name)

    def finishScan(self):
        self.tDet.command_inout('StopAcq')
        time.sleep(self.exptime + 1)
        # self.tDet.write_attribute('SaveAllImages',False)
        # time.sleep(0.2)
        # self.tDet.write_attribute('FrameNumbers', 1)
        return None

    def getCameraInfo(self):
        _s = ''
        _s += 'ExpTime\t= externally set\n'
        _s += 'DataType\t= Uint16\n'
        _s += 'Binning\t= 1'
        _s += 'ROI= [0, 2048,0, 20488]\n'
        return _s
