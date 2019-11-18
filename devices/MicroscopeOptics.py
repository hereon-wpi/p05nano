import time
from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap


class MicroscopeOptics(DeviceCommon):
    """
    Motion class for the micos five axis controller in P05/EH2.

    mi5 class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):
        # Microscope Optics
        self._tProxyMicroscopeFocus = TangoServerMap.getProxy('microscopeFocus')
        self._tProxyMicroscopeAperture = TangoServerMap.getProxy('microscopeAperture')
        self._tProxyMicroscopeFilter = TangoServerMap.getProxy('microscopeFilter')
        self._tProxyMicroscopeObjective = TangoServerMap.getProxy('microscopeObjective')
        self._tProxyMicroscopeRotHiCam = TangoServerMap.getProxy('microscopeRotHiCam')
        self._tProxyMicroscopeRotLoCam = TangoServerMap.getProxy('microscopeRotLoCam')
        self._tProxyMicroscopeCamZ = TangoServerMap.getProxy('microscopeCamZ')
        self._tProxyMicroscopeCtrl = TangoServerMap.getProxy('microscopeCtrl')
        self._tProxyAerotechMirror = TangoServerMap.getProxy('aerotechMirror')

        # Class variables
        self.m5 = {'focus': 3.05, 'camera z': 50, 'objective': 2.06}
        self.m10 = {'focus': 2.3245, 'camera z': 120, 'objective': 4.15}
        self.m20 = {'focus': 2.5555, 'camera z': 550, 'objective': 6.25}
        self.m40 = {'focus': 2.5555, 'camera z': 240, 'objective': 8.31}
        self.mBacklash = {'focus': -0.2, 'camera z': -3, 'objective': -0.3}

        # Dictionary of all real world (printed) names and PyTango object names
        # and their attributes
        self.__devdict = {
            'focus': [self._tProxyMicroscopeFocus, ['Position', {'ismotor': True}]],
            'aperture': [self._tProxyMicroscopeAperture, ['Position', {'ismotor': True}]],
            'filter': [self._tProxyMicroscopeFilter, ['Position', {'ismotor': True}]],
            'objective': [self._tProxyMicroscopeObjective, ['Position', {'ismotor': True}]],
            'rotation upper camera': [self._tProxyMicroscopeRotHiCam, ['Position', {'ismotor': True}]],
            'rotation lower camera': [self._tProxyMicroscopeRotLoCam, ['Position', {'ismotor': True}]],
            'camera z': [self._tProxyMicroscopeCamZ, ['Position', {'ismotor': True}]],
            'mirror': [self._tProxyAerotechMirror, ['Position', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def __call__(self):
        self.Pos()
        self.State()
        return None

    def focus(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves focus
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
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if position == 'home':
            RetVal = self._HomeAxis(self._tProxyMicroscopeFocus, 'HomeAxis')
            return RetVal
        else:
            RetVal = self._MoveMotor(
                self._tProxyMicroscopeFocus, 'Position', position,
                wait=wait, relative=relative, backlash=backlash, verbose=verbose)
            return RetVal

    def aperture(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Opens (1) or closes (0) the aperture.
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
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if position == 'home':
            RetVal = self._HomeAxis(self._tProxyMicroscopeAperture, 'HomeAxis')
            return RetVal
        else:
            RetVal = self._MoveMotor(
                self._tProxyMicroscopeAperture, 'Position', position, wait=wait,
                relative=relative, backlash=backlash, verbose=verbose)
            return RetVal

    def filter(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves the filterwheel
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
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if position == 'home':
            RetVal = self._HomeAxis(self._tProxyMicroscopeFilter, 'HomeAxis')
            return RetVal
        else:
            RetVal = self._MoveMotor(
                self._tProxyMicroscopeFilter, 'Position', position,
                wait=wait, relative=relative, backlash=backlash, verbose=verbose)
            return RetVal

    def objective(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Rotates the objective revolver.
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
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if position == 'home':
            RetVal = self._HomeAxis(
                self._tProxyMicroscopeObjective, 'HomeAxis')
            return RetVal
        else:
            RetVal = self._MoveMotor(
                self._tProxyMicroscopeObjective, 'Position', position, wait=wait,
                relative=relative, backlash=backlash, verbose=verbose)
            return RetVal

    def mirror(self, position=None, wait=True, relative=False, backlash=None,
            verbose=True):
        """
        DESCRIPTION:
            Moves the Aerotech controlled mirror in the camera housing in x
            dirction.
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
            self._tProxyAerotechMirror, 'Position', position,
            wait=wait, relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rotHiCam(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Rotates the upper camera
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
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if position == 'home':
            RetVal = self._HomeAxis(self._tProxyMicroscopeRotHiCam, 'HomeAxis')
            return RetVal
        else:
            RetVal = self._MoveMotor(
                self._tProxyMicroscopeRotHiCam, 'Position', position, wait=wait,
                relative=relative, backlash=backlash, verbose=verbose)
            return RetVal

    def rotLoCam(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Rotates the lower camera
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
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if position == 'home':
            RetVal = self._HomeAxis(self._tProxyMicroscopeRotLoCam, 'HomeAxis')
            return RetVal
        else:
            RetVal = self._MoveMotor(
                self._tProxyMicroscopeRotLoCam, 'Position', position, wait=wait,
                relative=relative, backlash=backlash, verbose=verbose)
            return RetVal

    def camZ(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves camera(s) along the z axis
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
            backlash=<FLOAT>:
                move with backlash. Default: 0
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if position == 'home':
            RetVal = self._HomeAxis(self._tProxyMicroscopeCamZ, 'HomeAxis')
            return RetVal
        else:
            RetVal = self._MoveMotor(
                self._tProxyMicroscopeCamZ, 'Position', position,
                wait=wait, relative=relative, backlash=backlash, verbose=verbose)
            return RetVal

    def setMagn(self, magn, verbose=True):
        """
        DESCRIPTION:
            Set the magnification of the microscope optics. This moves the focus, objective and camera z positions.
            The motors move sequentially and not simultaneously.
        PARAMETERS:
            mdict=<DICTIONARY>
                The dictionary contains the motor positions for each magnification. They are part of this class and can be
                called with MOP.m5, MOP.m10, MOP.m20 and MOP.m40
        KEYWORDS:
            verbose=<BOOLEAN>
                Print messages on screen
                Default: True
        """
        mdicts = {5: self.m5, 10: self.m10, 20: self.m20, 40: self.m40}
        mdict = mdicts[magn]
        for motor in mdict:
            self._MoveMotor(
                self.__devdict[motor][0], self.__devdict[
                    motor][1][0], mdict[motor], wait=True, verbose=verbose,
                backlash=self.mBacklash[motor], relative=False)
            time.sleep(0.1)
        return None

    def openShutter(self):
        """
        DESCRIPTION:
            Opens the shutter
        """
        self._tExec(
            self._tProxyMicroscopeCtrl, 'WriteAdsShort', param=[324, 1])
        return None

    def closeShutter(self):
        """
        DESCRIPTION:
            Closes the shutter
        """
        self._tExec(
            self._tProxyMicroscopeCtrl, 'WriteAdsShort', param=[324, 0])
        return None