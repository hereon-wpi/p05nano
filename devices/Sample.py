from p05.devices.Aerotech import Aerotech
from p05.devices.Attocube import Attocube
from p05.devices.DeviceCommon import DeviceCommon


class Sample(Aerotech, Attocube):
    """
    Motion class for the sample manipulation in P05/EH2.

    sample class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):

        Aerotech.__init__(self)
        Attocube.__init__(self)

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            'rot': [self._tProxyAerotechRot, ['Position', {'ismotor': True}]],
            'lateral': [self._tProxyAerotechX, ['Position', {'ismotor': True}]],
            'vertical': [self._tProxyAerotechZ, ['Position', {'ismotor': True}]],
            'rotx': [self._tProxyAerotechXrot, ['Position', {'ismotor': True}]],
            'roty': [self._tProxyAerotechYrot, ['Position', {'ismotor': True}]],
            #'p': [self._tProxyAttocubeP, ['Position', 'Frequency', 'DCLevel', {'ismotor': True}]],
            't': [self._tProxyAttocubeT, ['Position', 'Frequency', 'DCLevel', {'ismotor': True}]],
            'x': [self._tProxyAttocubeX, ['Position', 'Frequency', 'DCLevel', {'ismotor': True}]],
            'y': [self._tProxyAttocubeY, ['Position', 'Frequency', 'DCLevel', {'ismotor': True}]],
            'z': [self._tProxyAttocubeZ, ['Position', 'Frequency', 'DCLevel', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)
