import PyTango
from p05.devices.DeviceCommon import DeviceCommon
import numpy
import time
from p05.common import TangoServerMap

class KIT4MPcamera(DeviceCommon):
    """
    KIT4MP camera class.
    """

    def __init__(self):
        self._tProxyCameraKIT4MP = TangoServerMap.getProxy('cameraKit4mp')
        self.HBin = None
        self.VBin = None
        self.ExposureTime = self._tProxyCameraKIT4MP.read_attribute(
                            'exposure-time').value
        self.dPath = self._tProxyCameraKIT4MP.read_attribute(
                            'Directory').value
        self.fPrefix= self._tProxyCameraKIT4MP.read_attribute(
                            'FilePrefix').value
        self.TriggerSource = self._tProxyCameraKIT4MP.read_attribute(
                            'trigger-source').value
        self.nImages = self._tProxyCameraKIT4MP.read_attribute(
                            'NumberOfImages').value
        self.WriteImageFiles= self._tProxyCameraKIT4MP.read_attribute(
                            'WriteImageFiles').value
        self.ImageData = {"data": None, "ROI": None, "ExposureTime": None,
                             "time": None}

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            'camera': [self._tProxyCameraKIT4MP, ['exposure-time',
                {'ismotor': False}]]
            }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def exposure_time(self, t=0, wait=False):
        if not t:
            self.ExposureTime = self._tRead(self._tProxyCameraKIT4MP, 'exposure-time')
            return self.ExposureTime
        else:
            self._tWrite(self._tProxyCameraKIT4MP, 'exposure-time',t, wait=wait)

    def Directory(self, directory=None, wait=False):
        if not directory:
            self.dPath = self._tRead(self._tProxyCameraKIT4MP, 'Directory')
            return self.dPath
        else:
            self._tWrite(self._tProxyCameraKIT4MP, 'Directory',directory,
                    wait=wait)

    def FilePrefix(self, fileprefix=None, wait=False):
        if not fileprefix:
            self.fPrefix = self._tRead(self._tProxyCameraKIT4MP, 'FilePrefix')
            return self.fPrefix
        else:
            self._tWrite(self._tProxyCameraKIT4MP, 'FilePrefix',fileprefix,
                    wait=wait)

    def trigger_source(self, triggersource=None, wait=False):
        if triggersource==None:
            self.TriggerSource = self._tRead(self._tProxyCameraKIT4MP,
                    'trigger-source')
            return self.TriggerSource
        else:
            self._tWrite(self._tProxyCameraKIT4MP, 'trigger-source',
                   triggersource, wait=wait)

    def NumberOfImages(self, numberofimages=None, wait=False):
        if numberofimages==None:
            self.nImages = self._tRead(self._tProxyCameraKIT4MP,
                    'NumberOfImages')
            return self.nImages
        else:
            self._tWrite(self._tProxyCameraKIT4MP, 'NumberOfImages',
                    numberofimages, wait=wait)

    def write_imagefiles(self, writeimagefiles=None, wait=False):
        if writeimagefiles==None:
            self.WriteImageFiles = self._tRead(self._tProxyCameraKIT4MP,
                    'WriteImageFiles')
            return self.WriteImageFiles
        else:
            self._tWrite(self._tProxyCameraKIT4MP, 'WriteImageFiles',
                    writeimagefiles, wait=wait)

    def start(self, wait=False):
        self._tExec(self._tProxyCameraKIT4MP, 'Start', wait=wait)

    def stop(self, wait=False):
        self._tExec(self._tProxyCameraKIT4MP, 'Stop', wait=wait)

    def store(self, wait=False):
        # Use tyhis is python Tango server is running:
        # self._tExec(self._tProxyCameraKIT4MP, 'Store', param=path)
        self._tWrite(self._tProxyCameraKIT4MP, 'WriteImage', True, wait=wait)
