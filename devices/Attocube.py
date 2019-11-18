from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap


class Attocube(DeviceCommon):
    """
    Motion class for the tripod controller in P05/EH2.

    tripod class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):
        # Attocube
        self._tProxyAttocubeP = TangoServerMap.getProxy('attocubeP')
        self._tProxyAttocubeT = TangoServerMap.getProxy('attocubeT')
        self._tProxyAttocubeX = TangoServerMap.getProxy('attocubeX')
        self._tProxyAttocubeY = TangoServerMap.getProxy('attocubeY')
        self._tProxyAttocubeZ = TangoServerMap.getProxy('attocubeZ')

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            'rotX': [self._tProxyAttocubeP, ['Position', 'Frequency', 'DCLevel', {'ismotor': True}]],
            'rotY': [self._tProxyAttocubeT, ['Position', 'Frequency', 'DCLevel', {'ismotor': True}]],
            'x': [self._tProxyAttocubeX, ['Position', 'Frequency', 'DCLevel', {'ismotor': True}]],
            'y': [self._tProxyAttocubeY, ['Position', 'Frequency', 'DCLevel', {'ismotor': True}]],
            'z': [self._tProxyAttocubeZ, ['Position', 'Frequency', 'DCLevel', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def rotX(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample positioner phi rotation axis (around x)
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
        RetVal = self._MoveMotor(
            self._tProxyAttocubeP, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rrotX(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample positioner phi rotation axis (around x), relative to current position
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
        RetVal = self._MoveMotor(self._tProxyAttocubeP, 'Position', position,
                                 wait=wait, relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def rotY(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample positioner theta rotation axis (around y)
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
        RetVal = self._MoveMotor(
            self._tProxyAttocubeT, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rrotY(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample positioner theta rotation axis (around y), relative to current position
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
        RetVal = self._MoveMotor(self._tProxyAttocubeT, 'Position', position,
                                 wait=wait, relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def x(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample positioner x axis
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
        RetVal = self._MoveMotor(
            self._tProxyAttocubeX, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rx(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample positioner x axis relative to current position
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
        RetVal = self._MoveMotor(self._tProxyAttocubeX, 'Position', position,
                                 wait=wait, relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def y(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample positioner y axis
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
        RetVal = self._MoveMotor(
            self._tProxyAttocubeY, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def ry(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample positioner y axis relative to current position
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
        RetVal = self._MoveMotor(self._tProxyAttocubeY, 'Position', position,
                                 wait=wait, relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def z(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample positioner z axis
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
        RetVal = self._MoveMotor(
            self._tProxyAttocubeZ, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rz(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample positioner z axis relative to current position
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
        RetVal = self._MoveMotor(self._tProxyAttocubeZ, 'Position', position,
                                 wait=wait, relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def frequency(self, frequency, device='all', verbose=True):
        """
        DESCRIPTION:
            Set the frequency of the attocube positioners.
        PARAMETER:
            frequency=<FLOAT>
                New frequency of the piezo controllers.
        KEYWORDS:
            verbose=<BOOLEAN>
                Print messages on screen.
                Default: True
        """
        if device == 'all':
            for iDev in sorted(self.__devdict):
                currentFrequency = self._tRead(
                    self.__devdict[iDev][0], 'Frequency')
                self._tWrite(self.__devdict[iDev][0], 'Frequency', frequency)
                if verbose is False:
                    print("Setting axis %s from %s Hz to %s Hz." % (iDev, currentFrequency, frequency))
        else:
            iDev = self.__devdict[device]
            currentFrequency = self._tRead(iDev[0], 'Frequency')
            self._tWrite(iDev[0], 'Frequency', frequency)
            if verbose is False:
                    print("Setting axis %s from %s Hz to %s Hz." % (iDev, currentFrequency, frequency))
        return None

    def home(self, wait=True, verbose=True):
        """
        DESCRIPTION:
            Move all sample positioner axis to home position and set this
            position to zero.
            CTRL-C stops all motors in this class.
        KEYWORDS:
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt is released.
                Default: True
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        for actuator in self.__devdict:
            RetVal1 = self._HomeAxis(self.__devdict[actuator][0],command='MoveHome', wait=wait)
        RetVal2 = self.zero()
    
    def zero(self, verbose=True):
        """
        DESCRIPTION:
            Move all sample positioner axis to home position
            CTRL-C stops all motors in this class.
        KEYWORDS:
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt is released.
                Default: True
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        for actuator in self.__devdict:
            RetVal = self._tExec(self.__devdict[actuator][0],command='Calibrate', param=0)
