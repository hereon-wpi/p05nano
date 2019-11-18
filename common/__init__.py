'''
Module for device classes used either individually or in advanced forms.
@authors: ogurreck, wilde
'''
__version__ = '1.0'
__date__ = '$Date: 2015 / 08 / 21'

__all__ = []

from p05.common.Beamline import defineBeamline
__all__ += ['defineBeamline']

from p05.common.TangoServerMap import CTangoServerMap
TangoServerMap = CTangoServerMap()
__all__ += ['TangoServerMap']

from p05.common.TangoFailsaveComm import *
__all__ += ['tSaveCommCommand', 'tSaveWriteAttribute', 'tSaveReadAttribute']

from p05.common.ThreadControl import _ThreadControl
ThreadControl = _ThreadControl()
__all__ += ['ThreadControl']