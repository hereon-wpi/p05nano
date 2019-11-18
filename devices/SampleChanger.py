from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap
from p05.devices.Attocube import Attocube
from p05.devices.Aerotech import Aerotech
from p05.devices.MicosFiveAxis import MicosFiveAxis
import time
import random
import numpy


class StagesSampleTransfer():
    """
    Motion class to control the stages for the p05 EH2 sample changer
    """
    def __init__(self):
        # instanciate all axis
        self.rotationstage = Aerotech()
        self.samplestage = Attocube()
        self.camerastage = MicosFiveAxis()

        # transfer and current positions for rotationstage
        self.rotationstageRot = 180
        self.rotationstageRotX = 0
        self.rotationstageRotY = 0
        self.rotationstageX = -52
        self.rotationstageZ = -15.3
        self.rotationstageCurrPos = self.rotationstage.pos(verbose=False)

        # transfer and current position for samplestage
        self.samplestageY = -2000
        self.samplestageZ = 0
        self.samplestageRotX = 0
        self.samplestageCurrPos = self.samplestage.pos(verbose=False)

        # transfer and current positions for camerastage
        self.camerstageY = 300
        self.camerastageCurrPos = self.camerastage.pos(verbose=False)

        # position storage
        self.positionContainer = {}

    def rotationstageToTransferPos(self):
        # move rotationstage into transfer position
        self.rotationstageCurrPos = self.rotationstage.pos(verbose=False)
        self.rotationstage.rot(self.rotationstageRot)
        #self.rotationstage.rotX(self.rotationstageRotX)
        #self.rotationstage.rotY(self.rotationstageRotY)
        self.rotationstage.x(self.rotationstageX)
        self.rotationstage.z(self.rotationstageZ)

    def samplestageToTransferPos(self):
        # move samplestage into transfer position, i.e. home position
        self.samplestageCurrPos = self.samplestage.pos(verbose=False)
        self.samplestage.home()
        self.samplestage.zero()
        self.samplestage.y(self.samplestageY)
        # samplestage.rotX(self.samplestageRotX)
        self.samplestage.z(self.samplestageZ)

    def camerastageToTransferPos(self):
        self.camerastageCurrPos = self.camerastage.pos(verbose=False)
        if float(self.camerastageCurrPos['slab'][0]) > 300:
            print('Camerastage at position: ',
                  str(self.camerastageCurrPos['slab']),
                  'move aborted.')
            return
        self.camerastage.pOn()
        time.sleep(3)
        self.camerastage.y(300)
        time.sleep(.1)
        self.camerastage.pOff()

    def camerastageToPrevPos(self):
        self.camerastage.pOn()
        time.sleep(2)
        self.camerastage.y(self.camerastageCurrPos['slab'][0])
        time.sleep(.1)
        self.camerastage.pOff()

    def samplestageToPrevPos(self):
        #self.samplestage.rotX(self.samplestageCurrPos['rotX'][0])
        self.samplestage.rotY(self.samplestageCurrPos['rotY'][0])
        self.samplestage.x(self.samplestageCurrPos['x'][0])
        self.samplestage.y(self.samplestageCurrPos['y'][0])
        self.samplestage.z(self.samplestageCurrPos['z'][0])

    def rotationstageToPrevPos(self):
        self.rotationstage.z(self.rotationstageCurrPos['z'][0])
        self.rotationstage.rot(self.rotationstageCurrPos['rot'][0])
        self.rotationstage.x(self.rotationstageCurrPos['x'][0])

    def allStagesToTransferPos(self, moveCamera=True):
        if moveCamera:
            self.camerastageToTransferPos()
        self.rotationstageToTransferPos()
        self.samplestageToTransferPos()

    def allStagesToPrevPos(self, moveCamera=True):
        self.rotationstageToPrevPos()
        self.samplestageToPrevPos()
        if moveCamera:
            self.camerastageToPrevPos()

    def _allStagesMoveRandom(self):
        self.rotationstage.rot(random.uniform(0, 180))
        #self.rotationstage.rotX(random.uniform(0, 0.03))
        #self.rotationstage.rotY(random.uniform(0, 0.03))
        self.rotationstage.x(random.uniform(-20, 20))
        self.rotationstage.z(random.uniform(-20, 0))

        # move samplestage into transfer position
        self.samplestage.x(random.uniform(-1000, 1000))
        self.samplestage.y(random.uniform(-1000, 1000))
        self.samplestage.z(random.uniform(10, 500))
        self.samplestage.rotX(random.uniform(-1000, 1000))
        self.samplestage.rotY(random.uniform(-1000, 1000))

    def showStagesPos(self):
        pos = self.samplestage.pos(verbose=False)
        print('samplestage positions:')
        for i in pos:
            print(i, pos[i])
        print('rotationstage positions:')
        self.rotationstage.pos()

    def saveCurrentPosition(self, name):
        rotationstage_rot = self.rotationstage.rot(verbose=False)
        rotationstage_x = self.rotationstage.x(verbose=False)
        rotationstage_z = self.rotationstage.z(verbose=False)
        camerastage_y = self.camerastage.y(verbose=False)
        samplestage_x = self.samplestage.x(verbose=False)
        samplestage_y = self.samplestage.y(verbose=False)
        samplestage_z = self.samplestage.z(verbose=False)
        #samplestage_rotx = self.samplestage.rotX(verbose=False)
        samplestage_roty = self.samplestage.rotY(verbose=False)
        self.positionContainer[name] = {'rotationstage_rot': rotationstage_rot,
                                        'rotationstage_x': rotationstage_x,
                                        'rotationstage_z': rotationstage_z,
                                        'camerastage_y': camerastage_y, 
                                        'samplestage_x': samplestage_x,
                                        'samplestage_y': samplestage_y,
                                        'samplestage_z': samplestage_z,
                                        #'samplestage_rotx': samplestage_rotx,
                                        'samplestage_roty': samplestage_y}

    def moveToSavedPosition(self, name):
        if name in self.positionContainer:
            self.rotationstage.rot(self.positionContainer[name]['rotationstage_rot'])
            self.rotationstage.x(self.positionContainer[name]['rotationstage_x'])
            self.rotationstage.z(self.positionContainer[name]['rotationstage_z'])
            self.samplestage.x(self.positionContainer[name]['samplestage_x'])
            self.samplestage.y(self.positionContainer[name]['samplestage_y'])
            self.samplestage.z(self.positionContainer[name]['samplestage_z'])
            #self.samplestage.rotX(self.positionContainer[name]['samplestage_rotx'])
            self.samplestage.rotY(self.positionContainer[name]['samplestage_roty'])
            self.camerastage.pOn()
            time.sleep(2)
            self.camerastage.y(self.positionContainer[name]['camerastage_y'])
            time.sleep(0.1)
            self.camerastage.pOff()





class RobotSampleTransfer(DeviceCommon):
    """
    Motion class to control the sample changer robot in p05 EH2
    """
    def __init__(self):
        self._tProxySampleChanger = TangoServerMap.getProxy('sampleChanger')
        self.__devdict = {
            'robot': [self._tProxySampleChanger,
                      ['BatchSampleIds', 'SampleIds', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def homeRobot(self, wait=True, verbose=True):
        """
        DESCRIPTION:
            Move sample changer robot to home position
            CTRL-C stops all motors in this class.
        KEYWORDS:G
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        self._HomeAxis(self._tProxySampleChanger, command='Home', wait=wait)

    def scanSampleContainer(self, wait=True, verbose=True):
        """
        DESCRIPTION:
            Lets the sample changer scan the sample container
            CTRL-C stops all motors in this class.
        KEYWORDS:G
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        self._tExec(self._tProxySampleChanger, command='ScanSampleContainer',
                    wait=wait)

    def nextStep(self, wait=True, verbose=True):
        """
        DESCRIPTION:
            Next step in sample change process
            CTRL-C stops all motors in this class.
        KEYWORDS:G
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        self._tExec(self._tProxySampleChanger, command='NextStep', wait=wait)

    def previousStep(self, wait=True, verbose=True):
        """
        DESCRIPTION:
            Next step in sample change process
            CTRL-C stops all motors in this class.
        KEYWORDS:G
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        self._tExec(self._tProxySampleChanger, command='PreviousStep',
                    wait=wait)

    def selectSample(self, sampleID, verbose=True):
        """
        DESCRIPTION:
            selects the sample which is to be changed
            CTRL-C stops all motors in this class.
        KEYWORDS:G
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        return self._tExec(self._tProxySampleChanger, command='SelectSample',
                           param=sampleID, wait=False)

    def startBatch(self, verbose=True):
        """
        DESCRIPTION:
            selects the sample which is to be changed
            CTRL-C stops all motors in this class.
        KEYWORDS:G
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        return self._tExec(self._tProxySampleChanger, command='StartBatch',
                           wait=False)

    def getSampleIDs(self, verbose=True):
        """
        DESCRIPTION:
            returns a list of all samples in the sample container
            CTRL-C stops all motors in this class.
        KEYWORDS:G
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        return self._tRead(self._tProxySampleChanger, 'SampleIDs')

    def getCurrentSampleID(self, verbose=True):
        """
        DESCRIPTION:
            returns the currently selected sample ID.
            CTRL-C stops all motors in this class.
        KEYWORDS:G
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        return self._tExec(self._tProxySampleChanger, 'GetCurrentSampleID',
                           wait=False)

    def getStepID(self, verbose=True):
        """
        DESCRIPTION:
            returns the current step ID.
            CTRL-C stops all motors in this class.
        KEYWORDS:G
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        return self._tExec(self._tProxySampleChanger, 'GetStepId', wait=False)

    def stop(self):
        """
        Overrride global stop script with stop for robot
        """
        self._tExec(self._tProxySampleChanger, 'Stop')

    def Reset(self):
        """
        Reset robot
        """
        return self._tExec(self._tProxySampleChanger, 'Reset')


class SampleChanger(StagesSampleTransfer, RobotSampleTransfer):
    """
    Motion class for the sample manipulation in P05/EH2.

    sample class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):

        StagesSampleTransfer.__init__(self)
        RobotSampleTransfer.__init__(self)

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = { 'robot': [self._tProxySampleChanger,
                                     ['BatchSampleIds', 'SampleIds',
                                      {'ismotor': True}]] }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def insertSample(self, sampleID, wait=True, verbose=True, axisInPos=False,
                     returnToPrev=False):
        if sampleID in self.getSampleIDs():
            # get all axes wherer they belong
            if not axisInPos:
                self.allStagesToTransferPos()
            # initiate Batchscan
            self.selectSample(sampleID)
            self.startBatch()
            for step in numpy.arange(15):
                self.nextStep()
            if returnToPrev:
                self.allStagesToPrevPos()

    def removeSample(self, wait=True, verbose=True, axisInPos=False,
                     returnToPrev=False):
        # get all axes wherer they belong
        if not axisInPos:
            self.allStagesToTransferPos()
        # initiate Batchscan
        for step in numpy.arange(15):
            self.nextStep()
        if returnToPrev:
            self.allStagesToPrevPos()
            


