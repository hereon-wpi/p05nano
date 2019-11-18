from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap


class Undulator(DeviceCommon):
    """
    Motion class for the micos five axis controller in P05/EH2.
    ATTENTION: The coordinate system is not as usual. Zero is in the
    position near the hutch wall and 1483 is close to the rotation axis.

    mi5 class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):
        # Undalator
        self._tProxyUndulator = TangoServerMap.getProxy('undulator')

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {'undulator': [self._tProxyUndulator, ['Gap', 'Harmonic',
                                                                'Position', 'Taper', 'Velocity', {'ismotor': True}]]}

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def __call__(self):
        self.Pos()
        self.State()
        return None

    def gap(self, position=None, wait=True, relative=False, verbose=True):
        """
        DESCRIPTION:
            Change the undulator gap.
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
        RetVal = self._MoveMotor(self._tProxyUndulator, 'Gap', position,
                                 wait=wait, relative=relative, verbose=verbose)
        return RetVal

    def rgap(self, position=None, wait=True , verbose=True):
        """
        DESCRIPTION:
            Change the undulator gap. Moves relative to current position.
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
        RetVal = self._MoveMotor(self._tProxyUndulator, 'Gap', position,
                                 wait=wait, relative=True, verbose=verbose)
        return RetVal
    def energy(self, energy=None, wait=True, relative=False, verbose=True):
        """
        DESCRIPTION:
            Calculate undulator gap for given energy in eV and change the gap accordingly.
            Keep in mind to set the harmionic to zour needs.
            CTRL-C stops all motors in this class.
        KEYWORDS:
            energy=<FLOAT>/None:
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
        RetVal = self._MoveMotor(self._tProxyUndulator, 'Position', energy,
                                 wait=wait, relative=relative, verbose=verbose)
        return RetVal

    def harmonic(self, harmonic=None, verbose=True):
        """
        DESCRIPTION:
            Sets the harmonic for position calculation. Does not move anything,
        KEYWORDS:
            harmonic=<INTEGER>/None:
                new harmonic
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if harmonic is None:
            current_harmonic = self._tRead(self._tProxyUndulator, 'Harmonic')
            if verbose is True:
                print('harmonic: %i' % current_harmonic)
                return current_harmonic
        else:
            self._tWrite(self._tProxyUndulator, 'Harmonic', harmonic)
            return None

    def velocity(self, velocity):
        """
        DESCRIPTION:
            Sets the velocity of the undulator motors. Does not move anything.
        PARAMETER:
            velocity=<FLOAT>:
                new velocity
        """
        self._tWrite(self._tProxyUndulator, 'Velocity', velocity)
        return None

    def simPos(self, energy, harmonic=None, verbose=True):
        """
        DESCRIPTION:
            Simulates the undulator gap for a given harmonic and energy
        PARAMETER:
            velocity=<FLOAT>:
                new velocity
        KEYWORDS:
            harmonic=<INTEGER>/None:
                sets a new harmonic, resets the harmonic to old value
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if harmonic is None:
            self._tWrite(self._tProxyUndulator, 'PositionSim', energy)
            result = self._tRead(self._tProxyUndulator, 'ResultSim')
        else:
            current_harmonic = self._tRead(self._tProxyUndulator, 'Harmonic')
            self.Harmonic(harmonic)
            self._tWrite(self._tProxyUndulator, 'PositionSim', energy)
            result = self._tRead(self._tProxyUndulator, 'ResultSim')
            self.Harmonic(current_harmonic)
        if verbose is True:
            print('%s mm at %s.' % (result[0], energy))
        return result[0]
