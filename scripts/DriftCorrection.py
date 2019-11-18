import numpy
from p05.devices import CDCM
from p05.common import TangoServerMap


class DriftCorrection():
    def __init__(self, vOrigin=None, hOrigin=None, pitchConversion=None, rollConversion=None):
        # beam position origins and conversion factors
        self.pitchConversion = pitchConversion        # conversion factor between vertical displacement and DCM pitch
        self.verticalOrigin = vOrigin                 # origin of the vertical beam
        self.rollConversion = rollConversion          # conversion factor between horizontal displacement and DCM roll
        self.horizontalOrigin = hOrigin               # origin of the horizontal beam

        # get tango instance of DCM pitch motor and statusserver for QBPM
        # monitoring
        self._tDCM = CDCM()
        self._tProxyStatusserver = TangoServerMap.getProxy('statusserver')

    def findBeamSpotCM(self, image):
        imageSize = image.shape
        imageSum = image.sum()
        verticalImageSum = image.sum(axis=0)
        horizontalImageSum = image.sum(axis=1)
        verticalCM = numpy.sum(
            (numpy.arange(imageSize[0]) * verticalImageSum) / imageSum)
        horizontalCM = numpy.sum(
            (numpy.arange(imageSize[1]) * horizontalImageSum) / imageSum)
        return verticalCM, horizontalCM

    def beamOffset(self, verticalPosition, horizontalPosition):
        pitchDelta = (
            self.verticalOrigin - verticalPosition) * self.pitchConversion
        rollDelta = (
            self.horizontalOrigin - horizontalPosition) * self.rollConversion
        return verticalPitchDelta, horizontalRollDelta

    def moveToVerticalOrigin(self, verticalDelta):
        self._tDCM.x2Pitch(verticalDelta, relative=True, verbose=False)

    def moveToHorizontalOrigin(self, horizontalDelta):
        self._tDCM.x1roll(horizontalDelta, relative - True, vorbose=False)

    def start(self):
        # while statusserver.getSingle
        pass
