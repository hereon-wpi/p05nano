import PyTango
import numpy
import time
from p05.scripts.xtmDisplay import xtmDisplay
from p05.scripts.FLIimage import FLIexpose, FLIgrabImage, FLIgetImage
from p05.devices.XrayShutter import XRayShutter
from p05.devices.MicroscopeOptics import MicroscopeOptics
from p05.common import TangoServerMap


class FLIcamera():
    """
    scripts for the FLI camera class.
    """

    def __init__(self):
        self._tProxyCameraFLI1 = TangoServerMap.getProxy('cameraFli1')
        self._tProxySampleMotor = TangoServerMap.getProxy('aerotechX')

        self.XRayShutter = XRayShutter()
        self.MOP = MicroscopeOptics()
        self.refOutDist = 10
        self.ROI = [self._tProxyCameraFLI1.read_attribute('Roi_ul_x').value,
                  self._tProxyCameraFLI1.read_attribute('Roi_ul_y').value,
                  self._tProxyCameraFLI1.read_attribute('Roi_lr_x').value,
                  self._tProxyCameraFLI1.read_attribute('Roi_lr_y').value,
                  ]
        self.HBin = None
        self.VBin = None
        self.ExposureTime = self._tProxyCameraFLI1.read_attribute(
                            'ExposureTime').value
        self.intImageData = {"data": None, "ROI": None, "ExposureTime": None,
                             "time": None}
        self.refImageData = {"data": None, "ROI": None, "ExposureTime": None,
                             "time": None}
        self.absImageData = {"data": None, "ROI": None, "ExposureTime": None,
                             "time": None}
        self.darkImageData = {"data": None, "ROI": None, "ExposureTime": None,
                              "time": None}
        self.coords = None
        self.useDarkImage = True

    def getIntImage(self):
        #self.XRayShutter.Open(verbose=False)
        self.MOP.openShutter()
        FLIexpose(self._tProxyCameraFLI1)
        self.MOP.closeShutter()
        #self.XRayShutter.Close(verbose=False)
        self.intImageData["data"] = FLIgrabImage(self._tProxyCameraFLI1)
        self.intImageData["ROI"] = self.getROI(verbose=False)
        self.intImageData["ExposureTime"] = self.setExposureTime(verbose=False)
        self.intImageData["time"] = time.time()
        return self.intImageData['data']

    def getDarkImage(self):
        #self.XRayShutter.Close(verbose=False)
        self.MOP.closeShutter()
        self.darkImageData["data"] = FLIgetImage(self._tProxyCameraFLI1)
        self.darkImageData["ROI"] = self.getROI(verbose=False)
        self.darkImageData["ExposureTime"] = self.setExposureTime(
                                             verbose=False)
        self.darkImageData["time"] = time.time()
        return None

    def saveImage(self):
        return None

    def getRefImage(self):
        current_sample_position = \
            self._tProxySampleMotor.read_attribute('Position').value
        self._tProxySampleMotor.write_attribute('Position',
                current_sample_position + self.refOutDist)
        while self._tProxySampleMotor.state() != PyTango.DevState.ON:
            time.sleep(0.1)
        self.refImageData["ROI"] = self.getROI(verbose=False)
        self.refImageData["ExposureTime"] = self.setExposureTime(verbose=False)
        self.refImageData["time"] = time.time()
        #self.XRayShutter.Open(verbose=False)
        self.MOP.openShutter()
        FLIexpose(self._tProxyCameraFLI1)
        self.MOP.closeShutter()
        #self.XRayShutter.Close(verbose=False)
        self.refImageData["data"] = FLIgrabImage(self._tProxyCameraFLI1)
        self._tProxySampleMotor.write_attribute('Position',
            current_sample_position)
        while self._tProxySampleMotor.state() != PyTango.DevState.ON:
            time.sleep(0.1)
        return self.refImageData['data']

    def getAbsImage(self, newRef=True):
        #currExposureTime = self.setExposureTime(verbose=False)
        self.GetIntImage()
        if newRef is True or self.__checkRefParams() is False:
            time.sleep(0.1)
            self.GetRefImage()

        if self.useDarkImage is False:
            self.absImageData["data"] = \
                1 - 1.0 * self.intImageData["data"].astype(float) / \
                self.refImageData["data"].astype(float)
            (i, j) = numpy.where(self.absImageData["data"] < 0)
            if i.size and j.size:
                self.absImageData["data"][i, j] = 0

        if self.useDarkImage is True:
            if self.__checkDarkParams() != True:
                self.GetDarkImage()
            CorrIntImageData = self.intImageData["data"] - \
                self.darkImageData["data"]
            (i, j) = numpy.where(CorrIntImageData < 0)
            if i.size and j.size:
                CorrIntImageData[i, j] = 0
            CorrRefImageData = self.refImageData["data"] - \
                self.darkImageData["data"]
            (i, j) = numpy.where(CorrRefImageData <= 0)
            if i.size and j.size:
                CorrRefImageData[i, j] = 1

            self.absImageData["data"] = 1 - 1.0 * \
                CorrIntImageData.astype(float) / CorrRefImageData.astype(float)
            (i, j) = numpy.where(self.absImageData["data"] < 0)
            if i.size and j.size:
                self.absImageData["data"][i, j] = 0

        self.absImageData["ROI"] = self.getROI(verbose=False)
        self.absImageData["ExposureTime"] = self.setExposureTime(verbose=False)
        self.absImageData["time"] = time.time()

        return self.absImageData['data']

    def setExposureTime(self, ExposureTime=None, verbose=True):
        if ExposureTime is None:
            self.ExposureTime = \
                self._tProxyCameraFLI1.read_attribute('ExposureTime').value
            if verbose is True:
                print('Current exposure time: %f') % self.ExposureTime
        else:
            self.ExposureTime = ExposureTime
            self._tProxyCameraFLI1.write_attribute('ExposureTime',
                self.ExposureTime)
            if verbose is True:
                print('Setting exposure time tom: %f') % self.ExposureTime
        return self.ExposureTime

    def setBinning(self, Binning=None, verbose=True):
        if Binning is None:
            self.HBin = self._tProxyCameraFLI1.read_attribute('HBin').value
            self.VBin = self._tProxyCameraFLI1.read_attribute('VBin').value
            if verbose is True:
                print('Current EHD binning [hbin,vbin]: [%i, %i]') % \
                    (self.HBin, self.VBin)
        else:
            self.HBin, self.VBin = Binning, Binning
            self._tProxyCameraFLI1.write_attribute('HBin', self.HBin)
            self._tProxyCameraFLI1.write_attribute('VBin', self.VBin)
            if verbose is True:
                print('Setting EHD binning to [hbin,vbin]: [%i, %i]') % \
                    (self.HBin, self.VBin)
        return self.HBin, self.VBin

    def setROI(self, ROI=None, full=False, fullHoriz=False,
        fullVert=False, verbose=True):
        """
        DESCRIPTION:
            Sets ROI as [x1,y1,x2,y2] region
        KEYWORDS:
            ROI=<LIST>
                ROI in [x1,y1,x2,y2] form
                Default=[0,0,3056,3056] full CCD
            fullHoriz=<BOOLEAN>
                use vertical values only, and the whole CCD horizontally
            fullVert=<BOOLEAN>
                use horizontal values only, and the whole CCD vertically
        """
        currROI = self.getROI(verbose=False)
        if verbose:
            print("Last EHD ROI: ", currROI["ehd"])
            print("Last Python ROI: ", currROI["python"])
        if full:
            x1, x2, y1, y2 = 0, 3056, 0, 3056
        if fullHoriz:
            x1 = 0
            x2 = 3056
        else:
            if ROI is not None:
                x1 = min(ROI[0], ROI[2])
                x2 = max(ROI[0], ROI[2])
            else:
                print('No ROI defined')
        if fullVert:
            y1 = 0
            y2 = 3056
        else:
            if ROI is not None:
                y1 = min(ROI[1], ROI[3])
                y2 = max(ROI[1], ROI[3])
            else:
                print('No ROI defined')

        newROI = self.__py2ehd([x1, y1, x2, y2])
        self.ROI = newROI
        currROI = self.getROI(verbose=False)
        if verbose:
            print("New EHD ROI: ", currROI["ehd"])
            print("New Python ROI: ", currROI["python"])
        self._tProxyCameraFLI1.SetROI(newROI)

    def getROI(self, verbose=True):
        ehdROI = [self._tProxyCameraFLI1.read_attribute('Roi_ul_x').value,
                 self._tProxyCameraFLI1.read_attribute('Roi_ul_y').value,
                 self._tProxyCameraFLI1.read_attribute('Roi_lr_x').value,
                 self._tProxyCameraFLI1.read_attribute('Roi_lr_y').value,
                 ]
        pyROI = self.__ehd2py(ehdROI)
        if verbose:
            print("EHD ROI: ", ehdROI)
            print("Python ROI: ", pyROI)
        return {'ehd': ehdROI, 'python': pyROI}

    def display(self, imStr='i'):
        d = xtmDisplay()
        d.ROI = self.getROI(verbose=False)['python']
        if 'd' in imStr:
            d.imageList.append(numpy.rot90(self.darkImageData["data"], k=-1))
            d.titleList.append('Dark')
        if 'r' in imStr:
            d.imageList.append(numpy.rot90(self.refImageData["data"], k=-1))
            d.titleList.append('Reference')
        if 'i' in imStr:
            d.imageList.append(numpy.rot90(self.intImageData["data"], k=-1))
            d.titleList.append('Sample')
        if 'a' in imStr:
            d.imageList.append(numpy.rot90(self.absImageData["data"], k=-1))
            d.titleList.append('Absorption')
        d.Display()
        self.coords = d.coords
        del(d)
        return None

    def __py2ehd(self, pycoords):
        # transforms [x1,y1,x2,y2] Python coordinate pair
        # into [x,y,dx,dy] in EHD system
        x1 = pycoords[0]
        y1 = pycoords[1]
        x2 = pycoords[2]
        y2 = pycoords[3]
        ehdcoords = [min(y1, y2), 3056 - (min(x1, x2) + abs(x1 - x2)),
            abs(y1 - y2), abs(x1 - x2)]
        return ehdcoords

    def __ehd2py(self, ehdcoords):
        # transforms [x,y,dx,dy] in EHD system into [x1,y1,x2,y2]
        # Python coordinate pair
        x = ehdcoords[0]
        y = ehdcoords[1]
        dx = ehdcoords[2]
        dy = ehdcoords[3]
        pycoords = [3056 - (y + dy), x, 3056 - y, x + dx]
        return pycoords

    def __checkRefParams(self):
        refOK = False
        if self.refImageData["ROI"] == self.setROI(verbose=False) and \
            self.refImageData["ExposureTime"] == \
            self.setExposureTime(verbose=False)\
            and self.refImageData["data"] != None:
            refOK = True
        return refOK

    def __checkDarkParams(self):
        darkOK = False
        if self.darkImageData["ROI"] == \
        self.setROI(verbose=False) and\
        self.darkImageData["ExposureTime"] == \
        self.setExposureTime(verbose=False) and\
        self.darkImageData["data"] != None:
            darkOK = True
        return darkOK
