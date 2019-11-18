import time
from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap


class Hexapod(DeviceCommon):
    """
    Motion class for the Hexapod controller in P05/EH1.

    Hexapod class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):
        # Hexapod
        self._tProxyHexapodU = TangoServerMap.getProxy('hexapodU')
        self._tProxyHexapodV = TangoServerMap.getProxy('hexapodV')
        self._tProxyHexapodW = TangoServerMap.getProxy('hexapodW')
        self._tProxyHexapodX = TangoServerMap.getProxy('hexapodX')
        self._tProxyHexapodY = TangoServerMap.getProxy('hexapodY')
        self._tProxyHexapodZ = TangoServerMap.getProxy('hexapodZ')

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            'rotx': [self._tProxyHexapodU, ['Position', {'ismotor': True}]],
            'roty': [self._tProxyHexapodV, ['Position', {'ismotor': True}]],
            'rotz': [self._tProxyHexapodW, ['Position', {'ismotor': True}]],
            'x': [self._tProxyHexapodX, ['Position', {'ismotor': True}]],
            'y': [self._tProxyHexapodY, ['Position', {'ismotor': True}]],
            'z': [self._tProxyHexapodZ, ['Position', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def rotx(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod rotation around x axis
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
            self._tProxyHexapodU, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rrotx(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod rotation around x axis, relative to current position
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
        RetVal = self._MoveMotor(
            self._tProxyHexapodU, 'Position', position, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def roty(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod rotation around y axis
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
            self._tProxyHexapodV, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rroty(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod rotation around y axis, relative to current position
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
        RetVal = self._MoveMotor(
            self._tProxyHexapodV, 'Position', position, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def rotz(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod rotation around z axis
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
            self._tProxyHexapodW, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rrotz(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod rotation around z axis, relative to current position
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
        RetVal = self._MoveMotor(
            self._tProxyHexapodW, 'Position', position, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def x(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod x axis
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
            self._tProxyHexapodX, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rx(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod x axis relative to current position
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
        RetVal = self._MoveMotor(
            self._tProxyHexapodX, 'Position', position, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def y(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod y axis
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
            self._tProxyHexapodY, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def ry(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod y axis relative to current position
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
            self._tProxyHexapodY, 'Position', position, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def z(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod z axis
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
            self._tProxyHexapodZ, 'Position', position, wait=wait,
            relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rz(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Hexapod z axis relative to current position
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
            self._tProxyHexapodZ, 'Position', position, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def y_beam(self, position, wait=True, backlash=None, verbose=True, xSlope=-46.2 / 5000, ySlope=-24.316 / 5000):
        """
        DESCRIPTION:
            Hexapod y axis motion along beam with slope in x and y
            Hexapod y axis relative to current position
            CTRL-C stops all motors in this class.
        PARAMETER
            position=<FLOAT>:
                set <value> to move to a position,
                set None to read the current position of the motor
        KEYWORDS:
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
        current_y = self.pos('y')
        delta_y = position - current_y['y']
        xPos = xSlope * delta_y
        zPos = ySlope * delta_y

        RetVal = self._MoveMotor(
            self._tProxyHexapodY, 'Position', delta_y, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        time.sleep(0.1)
        RetVal = self._MoveMotor(
            self._tProxyHexapodX, 'Position', xPos, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        time.sleep(0.1)
        RetVal = self._MoveMotor(
            self._tProxyHexapodZ, 'Position', zPos, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        time.sleep(0.1)
        return RetVal

    def ry_beam(self, position, wait=True, backlash=None, verbose=True, xSlope=-46.2 / 5000, ySlope=-24.316 / 5000):
        """
        DESCRIPTION:
            Hexapod y axis motion along beam with slope in x and y relative to current position
            Hexapod y axis relative to current position
            CTRL-C stops all motors in this class.
        PARAMETER
            position=<FLOAT>:
                set <value> to move to a position,
                set None to read the current position of the motor
        KEYWORDS:
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
        xPos = xSlope * position
        zPos = ySlope * position

        RetVal = self._MoveMotor(
            self._tProxyHexapodY, 'Position', position, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        time.sleep(0.1)
        RetVal = self._MoveMotor(
            self._tProxyHexapodX, 'Position', xPos, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        time.sleep(0.1)
        RetVal = self._MoveMotor(
            self._tProxyHexapodZ, 'Position', zPos, wait=wait,
            relative=True, backlash=backlash, verbose=verbose)
        time.sleep(0.1)
        return RetVal
