from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap


class QBPM(DeviceCommon):
    """
    DESCRIPTION:
        QBPM Class. Enables readout and motor movement of QBPMs.
    ATTRIBUTES:
        qbpm <string>:
            which qbpm should be instanciated. The qbpm name have to be in the form of 'qbpm#' (e.g. 'qbpm1').
            Check with TangoServerMap class.
    """
    def __init__(self, qbpm):
        # QBPM
        tServerList = TangoServerMap.show(verbose=False, withaddress=False, grep=qbpm)
        for item in tServerList:
            if 'sensor' in item:
                qbpmsensor = item
            if 'motor' in item:
                qbpmmotor = item

        self._tProxyQBPMsensor = TangoServerMap.getProxy(qbpmsensor)
        self._tProxyQBPMmotor = TangoServerMap.getProxy(qbpmmotor)

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            'qbpm': [self._tProxyQBPMsensor, ['PosAndAvgCurr', 'Position_x', 'Position_y', 'Read_current1', 'Read_current2', 'Read_current3', 'Read_current4', {'ismotor': False}]],
            'qbpmmotor': [self._tProxyQBPMmotor, ['Position', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def __call__(self):
        self.Pos()
        self.State()
        return None

    def motor(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Set QBPM motor position
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set <value> to move to a position,
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt is released.
                Default: True
            relative=<BOOLEAN>:
                move relative to current position. Default: False
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetVal = self._MoveMotor(self._tProxyQBPMmotor, 'Position', position,
                                 wait=wait, relative=relative, verbose=verbose)
        return RetVal

    def rmotor(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Set QBPM motor position
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set <value> to move to a position,
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt is released.
                Default: True
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetVal = self._MoveMotor(self._tProxyQBPMmotor, 'Position', position,
                                 wait=wait, relative=True, verbose=verbose)
        return RetVal

    def readAvgCurrent(self, verbose=True):
        """
        DESCRIPTION:
            Reads the average current of the QBPM
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetVal = self._tProxyQBPMsensor.read_attribute(
            'PosAndAvgCurr').value[2]
        if verbose:
            print('Average QBPM current: %e' % RetVal)
        return RetVal

    def readCurrent(self, verbose=True):
        """
        DESCRIPTION:
            Reads the current of the QBPM and returns a list of four values.
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        current1 = self._tProxyQBPMsensor.read_attribute('Read_current1').value
        current2 = self._tProxyQBPMsensor.read_attribute('Read_current2').value
        current3 = self._tProxyQBPMsensor.read_attribute('Read_current3').value
        current4 = self._tProxyQBPMsensor.read_attribute('Read_current4').value
        if verbose:
            print('QBPM current1: %e') % current1
            print('QBPM current2: %e') % current2
            print('QBPM current3: %e') % current3
            print('QBPM current4: %e') % current4
        return current1, current2, current3, current4

    def readPosition(self, verbose=True):
        """
        DESCRIPTION:
            Reads the position of the beam from the QBPM and returns an (x,y) pair of values.
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        posX = self._tProxyQBPMsensor.read_attribute('Position_x').value
        posY = self._tProxyQBPMsensor.read_attribute('Position_y').value
        if verbose:
            print('Beam position x: %f') % posX
            print('Beam position y: %f') % posY
        return posX, posY
