from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap
import PyTango
import time


class CDCM(DeviceCommon):
    """
    
    """

    def __init__(self):
        self._tProxyDCMEnergy = TangoServerMap.getProxy('dcmEnergy')
        self._tProxyDCMBragg = TangoServerMap.getProxy('dcmBragg')
        self._tProxyDCMPara = TangoServerMap.getProxy('dcmPara')
        self._tProxyDCMPerp = TangoServerMap.getProxy('dcmPerp')
        self._tProxyDCMX1Roll = TangoServerMap.getProxy('dcmX1Roll')
        self._tProxyDCMX2Roll = TangoServerMap.getProxy('dcmX2Roll')
        self._tProxyDCMX2Pitch = TangoServerMap.getProxy('dcmX2Pitch')
        self._tProxyDCMJack1 = TangoServerMap.getProxy('dcmJack1')
        self._tProxyDCMJack2 = TangoServerMap.getProxy('dcmJack2')
        self._tProxyDCMJack3 = TangoServerMap.getProxy('dcmJack3')

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            'Energy': [self._tProxyDCMEnergy, ['Position', {'ismotor': True}]],
            'Bragg': [self._tProxyDCMBragg, ['Position', {'ismotor': True}]],
            'Para': [self._tProxyDCMPara, ['Position', {'ismotor': True}]],
            'Perp': [self._tProxyDCMPerp, ['Position', {'ismotor': True}]],
            'X1Roll': [self._tProxyDCMX1Roll, ['Position', {'ismotor': True}]],
            'X2Roll': [self._tProxyDCMX2Roll, ['Position', {'ismotor': True}]],
            'X2Pitch': [self._tProxyDCMX2Pitch, ['Position', {'ismotor': True}]],
            'Jack1': [self._tProxyDCMJack1, ['Position', {'ismotor': True}]],
            'Jack2': [self._tProxyDCMJack2, ['Position', {'ismotor': True}]],
            'Jack3': [self._tProxyDCMJack3, ['Position', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def __call__(self):
        self.Pos()
        self.State()
        return None

    def energy(self, position=None, wait=True, relative=False, verbose=True):
        """
        DESCRIPTION:
            Set DCM energy (moves multiple axis). Energy is give in eV.
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
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetVal = self._MoveMotor(self._tProxyDCMEnergy, 'Position', position,
                                 wait=wait, relative=relative, verbose=verbose)
        return RetVal

    def bragg(self, position=None, wait=True, relative=False, verbose=True):
        """
        DESCRIPTION:
            Set DCM Bragg angle.
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
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetVal = self._MoveMotor(self._tProxyDCMBragg, 'Position', position,
                                 wait=wait, relative=relative, verbose=verbose)
        return RetVal

    def para(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Set DCM Para position
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
        RetVal = self._MoveMotor(self._tProxyDCMPara, 'Position', position,
                                 wait=wait, relative=relative, verbose=verbose)
        return RetVal

    def perp(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Set DCM Perp position
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
            self._tProxyDCMPerp, 'Position', position, wait=wait,
                                 relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def x1Roll(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Set DCM X1Roll angle
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
            self._tProxyDCMX1Roll, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def x2Roll(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Set DCM X2Roll angle
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
            self._tProxyDCMX2Roll, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def x2Pitch(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Set DCM X1Pitch angle
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
            self._tProxyDCMX2Pitch, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def jack1(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Set DCM Jack1 Position
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
            self._tProxyDCMJack1, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def jack2(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Set DCM Jack2 Position
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
            self._tProxyDCMJack2, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def jack3(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Set DCM Jack3 Position
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
            self._tProxyDCMJack3, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal
            
    def rz(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sets all DCM Jack Positions simultaneoulsy - move relative in z
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
        try:
            self.jack1(position=position, wait=False, relative=True,
                       backlash=backlash, verbose=verbose)
            self.jack2(position=position, wait=False, relative=True,
                       backlash=backlash, verbose=verbose)
            self.jack3(position=position, wait=False, relative=True,
                       backlash=backlash, verbose=verbose)
            if wait:
                while self._tProxyDCMJack1.state() != PyTango.DevState.ON: time.sleep(0.05)
                while self._tProxyDCMJack2.state() != PyTango.DevState.ON: time.sleep(0.05)
                while self._tProxyDCMJack3.state() != PyTango.DevState.ON: time.sleep(0.05)
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    def braggSim(self, position, verbose=True):
        """
        DESCRIPTION:
            Simulates Bragg angle for a given energy
        PARAMETER:
            position=<FLOAT>:
                Energy in eV
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        self._tWrite(self._tProxyDCMEnergy, 'PositionSim')
        BraggResult = self._tRead(self._tProxyDCMEnergy, 'ResultSim')
        if verbose is True:
            print('Bragg angle: ', BraggResult)
        else:
            return BraggResult

    def exitOffset(self, position, relative=False, verbose=True):
        """
        DESCRIPTION:
            Set DCM exit offset. Does not move anything (to actually move the DCM to the new exit offset apply Energy function of this class).
        PARAMETER:
            position=<FLOAT>:
                New exit offset
        KEYWORDS:
            relative=<BOOLEAN>:
                move relative to current position. Default: False
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        self._tWrite(self._tProxyDCMEnergy, 'ExitOffset', position,
                     relative=relative, verbose=verbose)
