from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap


class Tripod(DeviceCommon):
    """
    Motion class for the tripod controller in P05/EH2.

    tripod class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):
        # Tripod
        self._tProxyTripodPods = TangoServerMap.getProxy('basestagePods')
        self._tProxyTripodPusher = TangoServerMap.getProxy('basestagePusher')

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            'pods': [self._tProxyTripodPods, ['PosZ', 'RotX', 'RotY', {'ismotor': True}]],
            'pusher': [self._tProxyTripodPusher, ['PosX', 'RotZ', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def x(self, position=None, wait=True, relative=False, verbose=True):
        """
        DESCRIPTION:
            Moves the tripod in x-direction (horizontally perpendicular to the beam)
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
        RetVal = self._MoveMotor(self._tProxyTripodPusher, 'PosX', position,
                                 wait=wait, relative=relative, verbose=verbose)
        return RetVal

    def rx(self, position=None, wait=True, verbose=True):
        """
        DESCRIPTION:
            Moves the tripod in x-direction (horizontally perpendicular to the beam) relative to current position
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set <value> to move to a position,
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt is released.
                Default: True
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetVal = self._MoveMotor(self._tProxyTripodPusher, 'PosX', position,
                                 wait=wait, relative=True, verbose=verbose)
        return RetVal

    def z(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves the slab in z-direction (vertically perpendicular to the beam)
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/<STRING>/None:
                set <value> to move to a position,
                set 'home' to home this motor
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
        if position == 'home':
            RetVal = self._HomeAxis(self._tProxyTripodPods, 'HomeAxis')
            return RetVal
        else:
            RetVal = self._MoveMotor(
                self._tProxyTripodPods, 'PosZ', position, wait=wait,
                relative=relative, backlash=backlash, verbose=verbose)
            return RetVal

    def rz(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves the slab in z-direction (vertically perpendicular to the beam) relative to current position
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/<STRING>/None:
                set <value> to move to a position,
                set 'home' to home this motor
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt is released.
                Default: True
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if position == 'home':
            RetVal = self._HomeAxis(self._tProxyTripodPods, 'HomeAxis')
            return RetVal
        else:
            RetVal = self._MoveMotor(self._tProxyTripodPods, 'PosZ', position,
                                     wait=wait, relative=True, backlash=backlash, verbose=verbose)
            return RetVal
