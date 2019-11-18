'''
Module for device classes used either individually or in advanced forms.
@authors: ogurreck, wilde
'''
__version__ = '1.0'
__date__ = '$Date: 2015 / 08 / 21'

__all__ = []

from p05.devices.Aerotech import Aerotech
__all__ += ['Aerotech']

from p05.devices.Attocube import Attocube
__all__ += ['Attocube']

from p05.devices.DCM import CDCM
__all__ += ['CDCM']

from p05.devices.DeviceCommon import DeviceCommon

from p05.devices.FlourescenceDetector import FlourescenceDetector
__all__ += ['FlourescenceDetector']

from p05.devices.Hexapod import Hexapod
__all__ += ['Hexapod']

from p05.devices.JenaPiezoComm import JenaPiezoComm
__all__ += ['JenaPiezoComm']

from p05.devices.MCA import MCA
__all__ += ['MCA']

from p05.devices.MicosFiveAxis import MicosFiveAxis
__all__ += ['MicosFiveAxis']

from p05.devices.MicroscopeOptics import MicroscopeOptics
__all__ += ['MicroscopeOptics']

from p05.devices.Optics import Optics
__all__ += ['Optics']

from p05.devices.PIcomm import PIcomm
__all__ += ['PIcomm']

from p05.devices.PMACcomm import PMACcomm
__all__ += ['PMACcomm']

from p05.devices.PMACdict import PMACdict
__all__ += ['PMACdict']

from p05.devices.PS2 import PS2
__all__ += ['PS2']

from p05.devices.QBPM import QBPM
__all__ += ['QBPM']

from p05.devices.Sample import Sample
__all__ += ['Sample']

from p05.devices.SampleChanger import RobotSampleTransfer, StagesSampleTransfer, SampleChanger
__all__ += ['RobotSampleTransfer', 'StagesSampleTransfer', 'SampleChanger']

from p05.devices.SmarActPiezo import SmarActcomm
__all__ += ['SmarActcomm']

from p05.devices.StatusServer import StatusServer
__all__ += ['StatusServer']

from p05.devices.Tripod import Tripod
__all__ += ['Tripod']

from p05.devices.Undulator import Undulator
__all__ += ['Undulator']

from p05.devices.XrayShutter import XRayShutter
__all__ += ['XRayShutter']

from p05.devices.camera_FLI import FLIcamera
__all__ += ['FLIcamera']

from p05.devices.camera_KIT4MP import KIT4MPcamera
__all__ += ['KIT4MPcamera']
