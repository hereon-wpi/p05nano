from p05.devices.MicosFiveAxis import MicosFiveAxis
from p05.devices.MicroscopeOptics import MicroscopeOptics
from p05.devices.DeviceCommon import DeviceCommon


class Optics(MicosFiveAxis, MicroscopeOptics):
    """
    Motion class for the optics manipulation in P05/EH2.

    sample class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):

        MicosFiveAxis.__init__(self)
        MicroscopeOptics.__init__(self)

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
        #    'szintallator': [self._tProxyMicroscopeScintillator, ['Position', {'ismotor': True}]],
            'focus': [self._tProxyMicroscopeFocus, ['Position', {'ismotor': True}]],
            'aperture': [self._tProxyMicroscopeAperture, ['Position', {'ismotor': True}]],
            'filter': [self._tProxyMicroscopeFilter, ['Position', {'ismotor': True}]],
            'objective': [self._tProxyMicroscopeObjective, ['Position', {'ismotor': True}]],
            'rotation upper camera': [self._tProxyMicroscopeRotHiCam, ['Position', {'ismotor': True}]],
            'rotation lower camera': [self._tProxyMicroscopeRotLoCam, ['Position', {'ismotor': True}]],
            'camera z': [self._tProxyMicroscopeCamZ, ['Position', {'ismotor': True}]],
            'poda': [self._tProxyOpticsstagePodA, ['Position', {'ismotor': True}]],
            'podb': [self._tProxyOpticsstagePodB, ['Position', {'ismotor': True}]],
            'podc': [self._tProxyOpticsstagePodC, ['Position', {'ismotor': True}]],
            'slab': [self._tProxyOpticsstageSlab, ['Position', {'ismotor': True}]],
            'cabcar': [self._tProxyOpticsstageCablecar, ['Position', {'ismotor': True}]],
            'tilt': [self._tProxyOpticsstageMultipleAxis, ['RotX', 'RotY', {'ismotor': True}]]
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)
