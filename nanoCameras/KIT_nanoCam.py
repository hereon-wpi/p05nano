import time

import PyTango

import p05.common.PyTangoProxyConstants as proxies
import p05.tools.misc as misc


class KIT_nanoCam():
    def __init__(self, tKIT=None, tTrigger=None, imageDir=None, exptime=None):
        if tKIT == None:
            self.tKIT = PyTango.DeviceProxy(proxies.camera_kit)
        else:
            self.tKIT = tKIT

        if tTrigger == None:
            self.tTrigger = PyTango.DeviceProxy(proxies.register_eh1_out01)
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
            self.exptime = float(1. / 5. * 1.0062903)

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
        except Exception as e:
            print(misc.GetTimeString() + ': KIT server not responding while setting new ExposureTime:\n%s' % e)
        return None

    def setImageName(self, name):
        imgname = name + '_%04d.tif'
        print(imgname)
        self.setKITAttribute('image_file_name_pattern', imgname)

    def setExptime(self, value):
        if self.tKIT.state() == PyTango.DevState.STANDBY:
            self.tKIT.command_inout('Stop')
            while not self.tKIT.state() == PyTango.DevState.ON:
                time.sleep(0.01)
        self.exptime = float(float(value) / 5. * 1.0062903)
        self.setKITAttribute('exposure_time', self.exptime)
        time.sleep(0.5)
        self.tKIT.command_inout('Start')
        while not self.tKIT.state() == PyTango.DevState.STANDBY:
            time.sleep(0.01)

    def setImgNumber(self, i):
        self.setKITAttribute('image_counter', i)

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
        self.tKIT.command_inout('Store', 1)
        while not self.tKIT.state() == PyTango.DevState.RUNNING:
            time.sleep(0.01)

        self.tTrigger.write_attribute('Value', 1)
        time.sleep(0.01)
        self.tTrigger.write_attribute('Value', 0)
        self.iImage += 1
        return
    # end acquireImage
