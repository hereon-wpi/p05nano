from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap


class Aerotech(DeviceCommon):
    """
    Motion class for the tripod controller in P05/EH2.

    tripod class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):
        # Aerotech Axis
        #self._tProxyAerotechMirror = TangoServerMap.getProxy('aerotechMirror')
        self._tProxyAerotechRot = TangoServerMap.getProxy('aerotechRot')
        self._tProxyAerotechXrot = TangoServerMap.getProxy('aerotechXrot')
        self._tProxyAerotechYrot = TangoServerMap.getProxy('aerotechYrot')
        self._tProxyAerotechX = TangoServerMap.getProxy('aerotechX')
        self._tProxyAerotechZ = TangoServerMap.getProxy('aerotechZ')
        self._tProxyAerotechCtrl = TangoServerMap.getProxy('aerotechCtrl')

        # defined in position
        self.center_position = 0
        self.ref_distance = -3
        self.change_position = -50
        self.ref_direction = 'x'

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            #'mirror': [self._tProxyAerotechMirror, ['Position', {'ismotor':
            #           True}]],
            'rot': [self._tProxyAerotechRot, ['Position', {'ismotor': True}]],
            'rotx': [self._tProxyAerotechXrot, ['Position', {'ismotor':
                                                             True}]], 'roty':
            [self._tProxyAerotechYrot, ['Position', {'ismotor': True}]], 'x':
            [self._tProxyAerotechX, ['Position', {'ismotor': True}]], 'z':
            [self._tProxyAerotechZ, ['Position', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def rot(self, position=None, wait=True, relative=False, backlash=None,
            verbose=True):
        """
        DESCRIPTION:
            Sample rotation axis in degrees (around z axis)
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set <value> to move to a position,
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            relative=<BOOLEAN>:
                move relative to current position. Default: False
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetVal = self._MoveMotor(self._tProxyAerotechRot, 'Position', position,
                                 wait=wait, relative=relative,
                                 backlash=backlash, verbose=verbose)
        return RetVal

    def rrot(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample rotation axis in degrees (around z axis)
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set <value> to move to a position,
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            relative=<BOOLEAN>:
                move relative to current position. Default: False
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetVal = self._MoveMotor(self._tProxyAerotechRot, 'Position', position,
                                 wait=wait, relative=True, backlash=backlash,
                                 verbose=verbose)
        return RetVal

    def x(self, position=None, wait=True, relative=False, backlash=None,
            verbose=True):
        """
        DESCRIPTION:
            Sample stage lateral motion (x, horizontally perpendicular to the
            beam)
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set <value> to move to a position,
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            relative=<BOOLEAN>:
                move relative to current position. Default: False
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetVal = self._MoveMotor(self._tProxyAerotechX, 'Position', position,
                                 wait=wait, relative=relative,
                                 backlash=backlash, verbose=verbose)
        return RetVal

    def rx(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample stage lateral motion (x, horizontally perpendicular to the
            beam) relative to current position
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set <value> to move to a position,
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetVal = self._MoveMotor(self._tProxyAerotechX, 'Position', position,
                                 wait=wait, relative=True, backlash=backlash,
                                 verbose=verbose)
        return RetVal

    def z(self, position=None, wait=True, relative=False, backlash=None,
          verbose=True):
        """
        DESCRIPTION:
            Sample stage vertical motion (z, vertically perpendicular to the
            beam)
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set <value> to move to a position,
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
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
            self._tProxyAerotechZ, 'Position', position,
            wait=wait, relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rz(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Sample stage vertical motion (z, vertically perpendicular to the
            beam) relative to current position
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set <value> to move to a position,
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetVal = self._MoveMotor(
            self._tProxyAerotechZ, 'Position', position,
            wait=wait, relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def rotX(self, position=None, wait=True, relative=False, backlash=None,
             verbose=True):
        """
        DESCRIPTION:
            Sample stage rotation around x axis in rad (horizontally
            perpendicular to the beam)
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set <value> to move to a position,
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
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
            self._tProxyAerotechXrot, 'Position', position,
            wait=wait, relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rotY(self, position=None, wait=True, relative=False, backlash=None,
             verbose=True):
        """
        DESCRIPTION:
            Sample stage rotation around z axis in rad (vertically
            perpendicular to the beam).
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set <value> to move to a position,
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
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
            self._tProxyAerotechYrot, 'Position', position,
            wait=wait, relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def center(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves the sample stage to a predefined position (usually the
            rotation axis centered on the CCD). The resulting move to the
            center position may happen laterally or vertically, depending on
            the value of self.ref_direction (= 'x' or 'z').

            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set predfined position to given value,
                sif position is None or omitted, move to predefined position
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if position is not None:
            self.center_position = position
        else:
            if self.ref_direction == 'x':
                self.x(self.center_position, wait=wait, backlash=backlash,
                       verbose=verbose)
            if self.ref_direction == 'z':
                self.z(self.center_position, wait=wait, backlash=backlash,
                       verbose=verbose)

    def ref(self, distance=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves the sample stage to a predefined position (usually a position
            without sample visible on the CCD). The resulting move to the
            center position may happen laterally or vertically, depending on
            the value of self.ref_direction (= 'x' or 'z').

            CTRL-C stops all motors in this class.
        KEYWORDS:
            Distance=<FLOAT>/None:
                set ref distance to predfined center value,
                sif position is None or omitted, move to predefined position
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if distance is not None:
            self.ref_distance = distance
        else:
            if self.ref_direction == 'x':
                self.x(self.center_position + self.ref_distance, wait=wait,
                       backlash=backlash, verbose=verbose)
            if self.ref_direction == 'z':
                self.z(self.center_position + self.ref_distance, wait=wait,
                       backlash=backlash, verbose=verbose)

    def change(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves the sample stage to a predefined position (usually a position
            where the sample can easily be changed).
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/None:
                set predfined position to given value,
                sif position is None or omitted, move to predefined position
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt
                is released.
                Default: True
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if position is not None:
            self.change_position = self.x()
        else:
            self.x(self.change_position, wait=wait, backlash=backlash,
                   verbose=verbose)
