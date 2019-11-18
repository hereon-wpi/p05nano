from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap


class MicosFiveAxis(DeviceCommon):
    """
    Motion class for the micos five axis controller in P05/EH2.
    ATTENTION: The coordinate system is not as usual. Zero is in the
    position near the hutch wall and 1483 is close to the rotation axis.

    mi5 class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):
        # Micos Axis
        self._tProxyOpticsstagePodA = TangoServerMap.getProxy('opticsstagePodA')
        self._tProxyOpticsstagePodB = TangoServerMap.getProxy('opticsstagePodB')
        self._tProxyOpticsstagePodC = TangoServerMap.getProxy('opticsstagePodC')
        self._tProxyOpticsstageSlab = TangoServerMap.getProxy('opticsstageSlab')
        self._tProxyOpticsstageCablecar = TangoServerMap.getProxy('opticsstageCablecar')
        self._tProxyOpticsstageMultipleAxis = TangoServerMap.getProxy('opticsstageMultipleAxis')

        # Axis length to reverse axis orientation
        self.AxLength = 1483

        # Dictionary of all real world (printed) names and PyTango object names
        # and their attributes
        self.__devdict = {
            #'poda':[self._tProxyOpticsstagePodA,['Position',{'ismotor':True}]],
            #'podb':[self._tProxyOpticsstagePodB,['Position',{'ismotor':True}]],
            #'podc':[self._tProxyOpticsstagePodC,['Position',{'ismotor':True}]],
            'slab': [self._tProxyOpticsstageSlab, ['Position', {'ismotor': True}]],
            'cabcar': [self._tProxyOpticsstageCablecar, ['Position', {'ismotor': True}]],
            'multipleaxis': [self._tProxyOpticsstageMultipleAxis, ['RotX', 'RotY', 'PosZ', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def __call__(self):
        self.Pos()
        self.State()
        return None

    def y(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves the slab in y-direction (along beam)
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
            RetVal = self._HomeAxis(self._tProxyOpticsstageSlab, 'HomeAxis')
            return RetVal
        else:
            RetVal = self._MoveMotorY(
                self._tProxyOpticsstageSlab, 'Position', position,
                wait=wait, relative=relative, backlash=backlash, verbose=verbose)
            return RetVal

    def ry(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves the slab in y-direction (along beam) relative to current position
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/<STRING>/None:
                set <value> to move to a position,
                set 'home' to home this motor
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
        if position == 'home':
            RetVal = self._HomeAxis(self._tProxyOpticsstageSlab, 'HomeAxis')
            return RetVal
        else:
            RetVal = self._MoveMotorY(
                self._tProxyOpticsstageSlab, 'Position', position, wait=wait,
                relative=True, backlash=backlash, verbose=verbose)
            return RetVal

    def z(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves the slab in z-direction (perpendicular to the beam)
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
                self._tProxyOpticsstageMultipleAxis, 'HomeHubs')
            return RetVal
        else:
            RetVal = self._MoveMotor(
                self._tProxyOpticsstageMultipleAxis, 'PosZ', position, wait=wait,
                relative=relative, backlash=backlash, verbose=verbose)
            return RetVal

    def rz(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Moves the slab in z-direction (perpendicular to the beam) relative to current position
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/<STRING>/None:
                set <value> to move to a position,
                set 'home' to home this motor
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
        if position == 'home':
            RetVal = self._HomeAxis(
                self._tProxyOpticsstageMultipleAxis, 'HomeHubs')
            return RetVal
        else:
            RetVal = self._MoveMotor(
                self._tProxyOpticsstageMultipleAxis, 'PosZ', position, wait=wait,
                relative=True, backlash=backlash, verbose=verbose)
            return RetVal

    def rotX(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Rotates the camera stage  around x axis
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
        RetVal = self._MoveMotor(
            self._tProxyOpticsstageMultipleAxis, 'RotX', position,
            wait=wait, relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rrotX(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Rotates the camera stage  around x axis relative to current position
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/<STRING>/None:
                set <value> to move to a position,
                set 'home' to home this motor
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
            self._tProxyOpticsstageMultipleAxis, 'RotX', position,
            wait=wait, relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def rotY(self, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Rotates the camera stage  around y axis
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
        RetVal = self._MoveMotor(
            self._tProxyOpticsstageMultipleAxis, 'RotY', position,
            wait=wait, relative=relative, backlash=backlash, verbose=verbose)
        return RetVal

    def rrotY(self, position=None, wait=True, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Rotates the camera stage  around y axis relative to current position
            CTRL-C stops all motors in this class.
        KEYWORDS:
            position=<FLOAT>/<STRING>/None:
                set <value> to move to a position,
                set 'home' to home this motor
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
            self._tProxyOpticsstageMultipleAxis, 'RotY', position,
            wait=wait, relative=True, backlash=backlash, verbose=verbose)
        return RetVal

    def pOn(self):
        """
        DESCRIPTION:
            Switches the air pressure on.
        """
        self._tExec(self._tProxyOpticsstageSlab, 'PressureOn')
        return None

    def pOff(self):
        """
        DESCRIPTION:
            Switches the air pressure off.
        """
        self._tProxyOpticsstageSlab.command_inout('PressureOff')

        return None

    def pos(self, device='all', verbose=True):
        """
        DESCRIPTION:
            Returns the position of either all axis or a given axis.
        KEYWORDS:
            device=<STRING>:
                returns the position of axis <STRING>. Use Show() to list device names.
                if <STRING>=='all', the position of all devices of this class are shown.
                Default: 'all'
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetValue = {}
        if device == 'all':
            for iDev in sorted(self.__devdict):
                iDevValue = []
                if iDev in ["slab", "cabcar"]:
                    for attribute in self.__devdict[iDev][1]:
                        if type(attribute) is dict:
                            pass
                        else:
                            corrValue = self.AxLength - self._tRead(
                                self.__devdict[iDev][0], attribute)
                            iDevValue.append(corrValue)
                            if verbose is True:
                                print("%s %s: %s" % (iDev, attribute, corrValue))
                else:
                    for attribute in self.__devdict[iDev][1]:
                        if type(attribute) is dict:
                            pass
                        else:
                            iDevValue.append(self._tRead(
                                self.__devdict[iDev][0], attribute))
                            if verbose is True:
                                print("%s %s: %s" % (iDev, attribute, self._tRead(self.__devdict[iDev][0], attribute)))
                RetValue[iDev] = (iDevValue)
        else:
            iDev = self.__devdict[device]
            if device in ["slab", "cabcar"]:
                for attribute in iDev[1]:
                    corrValue = self.AxLength - self._tRead(iDev[0], attribute)
                    RetValue[iDev]=(corrValue)
                    if verbose is True:
                        print("%s %s: %s" % (device, attribute, corrValue))
            else:
                for attribute in iDev[1]:
                    RetValue[iDev] = (self._tRead(iDev[0], attribute))
                    if verbose is True:
                        print("%s %s: %s" % (device, attribute, self._tRead(iDev[0], attribute)))
        if verbose is False:
            return RetValue
        else:
            return None

    def _MoveMotorY(self, tObject, attribute, position=None, wait=True, relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Pass motion command to Tango server.
        PARAMETER:
            tObject:
                Tango Object
            attribute:
                The Tango Object's attribute
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
            backlash=<FLOAT>/None:
                move with backlash. Default: None
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        CurrentPosition = self._tRead(tObject, attribute)
        if position is None:
            current_position = self._tRead(tObject, attribute)
            if verbose is True:
                print('%s: %f' % (attribute, self.AxLength - current_position))
            return self.AxLength - current_position
        else:
            if relative is True:
                position = self.AxLength - (CurrentPosition - position)
            if verbose is True:
                print('Move from %s to %s.' % (self.AxLength - CurrentPosition, position))
            try:
                if backlash is None:
                    self._tWrite(tObject, attribute, self.AxLength - position)
                    if wait is True:
                        self._tMotionWait(tObject)
                else:
                    self._tWrite(
                        tObject, attribute, self.AxLength - position - backlash)
                    if wait is True:
                        self._tMotionWait(tObject)
                    self._tWrite(tObject, attribute, self.AxLength - position)
                    if wait is True:
                        self._tMotionWait(tObject)
            except (KeyboardInterrupt, SystemExit):
                self._tExec(tObject, 'StopMove')
            return None
