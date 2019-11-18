'''
Package for QtGui for PMAC motors and TANGO devices
Created on 16.01.2015
@author: ogurreck
'''
__version__ = '1.0'
__date__ = '$Date: May 30th 2015'

__all__ = []

import gc
gc.enable()

from p05.gui.PMAC_gui_master import PMACgui, PMACUsergui
__all__ += ['PMACgui']

from p05.gui.PMAC_motorForm import cPMACmotor
from p05.gui.PMAC_sliderForm import cPMACair, cPMACslider

from p05.gui.TANGO_gui_master import TANGOgui
__all__ += ['TANGOgui']

from p05.gui.TANGO_deviceForm import cTANGOdevice

from p05.gui.PMAC_generic_motors import getPMACmotorList, getPMACmotorGroups

from p05.gui.TANGO_presetGUIs import *
__all__ += ['NanoTangoGUI', 'BeamlineOpticsGUI', 'NanoGrainMappingGUI', 'MicroCTgui', 'DMMgui','ConeBeamTangoGUI']

from p05.gui.PCO_LiveImage import PCO_LiveImage
__all__ += ['PCO_LiveImage']

from p05.gui.QBPM_monitor import QBPMmonitor
__all__ += ['QBPMmonitor']

from p05.gui.Counter_monitor import CounterMonitor
__all__ += ['CounterMonitor']

from p05.gui.EH1_EnvironMonitor import EH1_EnvironMonitor
__all__ += ['EH1_EnvironMonitor']

from p05.gui.Hama_LiveImage import *
__all__ += ['Hama_LiveImage']

from p05.gui.PixLink_LiveImage import *
__all__ += ['PixLink_LiveImage']

from p05.gui.Camera_LiveImage import Camera_LiveImage
__all__ += ['Camera_LiveImage']
