'''
p05 Package for TANGO Control of the beamline components
of the PETRA III beamline P05.

Author: M. Ogurreck
'''

__version__ = '2.0'
__date__ = '$Date: 2015 / 08 / 20'

__all__ = []

from p05.tools.misc import *
__all__ += ['StringFill', 'GetTimeString', 'GetArgTypeStr', 'CheckFilename', 'GetPath', 'GetShortTimeString']

from p05.tools.PETRAinfo import GetPETRAinfoStringShort, GetPETRAinfoString
__all__ += ['GetPETRAinfoStringShort', 'GetPETRAinfoString']


