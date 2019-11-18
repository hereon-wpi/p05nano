from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap


class PS2(DeviceCommon):
    """
    Motion class for the Powerslit 2 in P05 Frontend.

    PS2 class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):
        # Powerslit 2
        self._tProxyPS2Left = TangoServerMap.getProxy('ps2Left')
        self._tProxyPS2Right = TangoServerMap.getProxy('ps2Right')
        self._tProxyPS2Gap = TangoServerMap.getProxy('ps2Gap')
        self._tProxyPS2Offset = TangoServerMap.getProxy('ps2Offset')


        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            'left': [self._tProxyPS2Left, ['Position', {'ismotor': True}]],
            'right': [self._tProxyPS2Right, ['Position', {'ismotor': True}]], 
            'gap': [self._tProxyPS2Gap, ['Position', {'ismotor': True}]],
            'offset': [self._tProxyPS2Offset, ['Position', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def left(self, position=None, wait=True, relative=False, backlash=None,
            verbose=True):
        """
        DESCRIPTION:
            Powerslit 2 left edge.
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
        RetVal = self._MoveMotor(self._tProxyPS2Left, 'Position', position,
                                 wait=wait, relative=relative,
                                 backlash=backlash, verbose=verbose)
        return RetVal

    def rleft(self, position=None, wait=True, relative=True, backlash=None,
            verbose=True):
        """
        DESCRIPTION:
            Powerslit 2 left edge. Relative motion.
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
        RetVal = self._MoveMotor(self._tProxyPS2Left, 'Position', position,
                                 wait=wait, relative=relative,
                                 backlash=backlash, verbose=verbose)
        return RetVal

    def right(self, position=None, wait=True, relative=False, backlash=None,
            verbose=True):
        """
        DESCRIPTION:
            Powerslit 2 right edge.
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
        RetVal = self._MoveMotor(self._tProxyPS2Right, 'Position', position,
                                 wait=wait, relative=relative,
                                 backlash=backlash, verbose=verbose)
        return RetVal

    def rright(self, position=None, wait=True, relative=True, backlash=None,
            verbose=True):
        """
        DESCRIPTION:
            Powerslit 2 right edge. Relative Motion.
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
        RetVal = self._MoveMotor(self._tProxyPS2Right, 'Position', position,
                                 wait=wait, relative=relative,
                                 backlash=backlash, verbose=verbose)
        return RetVal

    def gap(self, position=None, wait=True, relative=False, backlash=None,
            verbose=True):
        """
        DESCRIPTION:
            Powerslit 2 gap. Higher values close the gap!
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
        RetVal = self._MoveMotor(self._tProxyPS2Gap, 'Position', position,
                                 wait=wait, relative=relative,
                                 backlash=backlash, verbose=verbose)
        return RetVal

    def rgap(self, position=None, wait=True, relative=True, backlash=None,
            verbose=True):
        """
        DESCRIPTION:
            Powerslit 2 gap. Higher values close the gap! Relative motion.
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
        RetVal = self._MoveMotor(self._tProxyPS2Gap, 'Position', position,
                                 wait=wait, relative=relative,
                                 backlash=backlash, verbose=verbose)
        return RetVal

    def offset(self, position=None, wait=True, relative=False, backlash=None,
            verbose=True):
        """
        DESCRIPTION:
            Powerslit 2 offset. Higher values increase offset in z.
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
        RetVal = self._MoveMotor(self._tProxyPS2Offset, 'Position', position,
                                 wait=wait, relative=relative,
                                 backlash=backlash, verbose=verbose)
        return RetVal

    def roffset(self, position=None, wait=True, relative=True, backlash=None,
            verbose=True):
        """
        DESCRIPTION:
            Powerslit 2 offset. Higher values increase the offset in z. Relative motion.
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
        RetVal = self._MoveMotor(self._tProxyPS2Offset, 'Position', position,
                                 wait=wait, relative=relative,
                                 backlash=backlash, verbose=verbose)
        return RetVal
