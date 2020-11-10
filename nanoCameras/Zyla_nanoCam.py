import time

import PyTango

import p05.common.PyTangoProxyConstants as proxies
import p05.tools.misc as misc


class Zyla_nanoCam():
    def __init__(self, tZyla=None, tTrigger=None, imageDir=None, exptime=None):
        if tZyla == None:
            self.tZyla = PyTango.DeviceProxy(proxies.camera_zyla)  # change Tango Server here!
        else:
            self.tZyla = tZyla

        if tTrigger == None:
            self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out03)  # Set Trigger here!
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
        self.tZyla.write_attribute('saving_format', 'tiff')  # !!!!
        self.tZyla.write_attribute('saving_index_format', '%05d')
        self.tZyla.write_attribute('saving_mode', 'auto_frame')
        self.tZyla.write_attribute('acq_trigger_mode', 'external_trigger')

        self.tZyla.write_attribute('saving_prefix', 'Image')
        self.tZyla.write_attribute('saving_directory', self.imageDir)

        self.tZyla.write_attribute('saving_next_number', 1)
        self.tTrigger.write_attribute('Value', 0)  # !!!!
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
        except Exception as e:
            print(misc.GetTimeString() + ': Hamamatsu server not responding while setting new ExposureTime:\n%s' % e)
        while not self.tZyla.state() == PyTango.DevState.ON:
            time.sleep(0.01)
        return None

    # end setExptime

    def setImgNumber(self, i):
        while self.tZyla.read_attribute('ready_for_next_acq').value == False:
            time.sleep(0.001)
        self.tZyla.write_attribute('saving_next_number', i)

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

        # while not self.tZyla.state() == PyTango.DevState.EXTRACT:
        time.sleep(0.1)
        # time.sleep(1)
        # self.tTrigger.write_attribute('Voltage', 3.5)
        self.tTrigger.write_attribute('Value', 1)
        time.sleep(0.1)
        # self.tTrigger.write_attribute('Voltage', 0)
        self.tTrigger.write_attribute('Value', 0)
        # time.sleep(self.exptime)
        self.imageTime = time.time()
        self.iImage = 0
        #         while not self.tZyla.state() == PyTango.DevState.ON:
        #             time.sleep(0.01)
        #         time.sleep(0.01)
        # self.tZyla.command_inout('stopAcq')
        return None

    def stopHamaacquisition(self):
        self.tTrigger.write_attribute('Value', 0)
        # self.tTrigger.write_attribute('Voltage', 0)
        while self.tZyla.state() == PyTango.DevState.EXTRACT:
            self.tZyla.command_inout('abortAcq')
            time.sleep(0.1)
        self.tZyla.command_inout('abortAcq')
        self.imageTime = time.time()
        self.iImage = 0
        time.sleep(3)
        return None

    def setImageName(self, name):
        while self.tZyla.read_attribute('ready_for_next_acq').value == False:
            time.sleep(0.001)
        self.tZyla.write_attribute('saving_prefix', name)

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
