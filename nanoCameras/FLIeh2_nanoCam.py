import time

import PyTango
import numpy

import p05.common.PyTangoProxyConstants as proxies
import p05.common.TangoFailsaveComm as tcom
import p05.tools.misc as misc


class FLIeh2_nanoCam():
    def __init__(self, tFLI=None, imageDir=None, exptime=None):
        if tFLI == None:
            self.tFLI = PyTango.DeviceProxy(proxies.eh2_smc0900_tFLI)
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

        self.CAM_PosX_FromPix = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array(
            (Ytotal - Ymin, Ytotal - Ymax))
        self.CAM_PixY_FromPos = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array(
            (Xtotal - Xmin, Xtotal - Xmax))
        self.CAM_PosY_FromPix = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array(
            (Xtotal - Xmin, Xtotal - Xmax))
        self.CAM_PixX_FromPos = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array(
            (Ytotal - Ymin, Ytotal - Ymax))

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
        except Exception as e:
            print(misc.GetTimeString() + ': FLI  server not responding while setting new ExposureTime:\n%s' % e)
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
        self.tFLI.write_attribute('Roi_ul_x', int(self.CAM_xlow))
        self.tFLI.write_attribute('Roi_lr_y', int(self.CAM_yhigh - self.CAM_ylow))
        self.tFLI.write_attribute('Roi_lr_x', int(self.CAM_xhigh - self.CAM_xlow))
        self.tFLI.write_attribute('Roi_ul_y', int(self.CAM_ylow))
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
