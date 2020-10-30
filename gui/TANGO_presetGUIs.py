import p05.common.PyTangoProxyConstants as proxies
from p05.gui.TANGO_gui_master import TANGOgui

"""    motors dictionary structure:
'DeviceName':      <string>    Screen name for the device
'TangoAddress':    <string>    Address of the TANGO server
'NumAttributes':   <integer>   Number of attribute lines to show
'MainAttribute':   <string>    If a device has a main attribute (e.g. motor position), this attribute can be locked
                               as first attribute to be shown
'ShowRelMovementPanel':     
                   <boolean>   Set to True if a panel for relative change of an attribute should be shown.
                               This is always coupled to the first attribute in the list. 
                               Preset: True
 'ShowCommands':   <boolean>   If set to True, a panel will appear to send commands to the device.
                               Preset: True  
 'ReadOnly':       <boolean>   If set to True, no attributes can be set but only read.
                               Preset: False
 'ZMXdevice':      <string>    Address of the ZMX device for a OMS motor. If set, the current ZMX error state will be shown.
                               If omitted, no ZMX will be polled.  

WARNING:    Complex data structures in attributes (e.g. arrays, lists) are not supported and will raise exceptions if polled.
    """


# TODO move all PyTango.DeviceProxy into dedicated file. Here use only links to that file

def NanoTangoGUI(parent=None):
    name = 'EH1 TANGO device GUI'
    allMotors = []
    #     allMotors.append({'DeviceName': 'Undulator',    'TangoAddress': proxies.tUndulator_1, \
#                       'NumAttributes': 2,           'MainAttribute': 'Gap', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    #     allMotors.append({'DeviceName': 'DCM energy server',    'TangoAddress': proxies.dcmener_s01_01_tDCMenergy, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    #     allMotors.append({'DeviceName': 'DCM Bragg axis',    'TangoAddress': proxies.dcmmotor_s01_01, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    #     allMotors.append({'DeviceName': 'DCM perpendicular',    'TangoAddress': proxies.motor_mono_11, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    #     allMotors.append({'DeviceName': 'DCM parallel',    'TangoAddress': proxies.motor_mono_12, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    #     allMotors.append({'DeviceName': 'DCM roll x1',    'TangoAddress': proxies.motor_mono_05, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    #     allMotors.append({'DeviceName': 'DCM roll x2',    'TangoAddress': proxies.motor_mono_02_tRoll, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    #     allMotors.append({'DeviceName': 'DCM pitch x2',    'TangoAddress': proxies.motor_mono_01_tPitch, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    #     allMotors.append({'DeviceName': 'Camera Ry',    'TangoAddress': proxies.motor_eh1_07_tCamRot, \
#                      'NumAttributes': 2,           'MainAttribute': 'Position', \
#                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    #   allMotors.append({'DeviceName': 'Scintillator Y',    'TangoAddress': proxies.motor_eh1_05_tScintiY, \
#                     'NumAttributes': 2,           'MainAttribute': 'Position', \
#                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    #   allMotors.append({'DeviceName': 'Lens Y',    'TangoAddress': proxies.motor_eh1_06_tLensY, \
#                     'NumAttributes': 2,           'MainAttribute': 'Position', \
#                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    #     allMotors.append({'DeviceName': 'Hamamatsu Trigger',    'TangoAddress': proxies.register_eh2_out01, \
#                      'NumAttributes': 2,           'MainAttribute': 'Value', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

###########________________________________ZMX______________________##################################################################

    allMotors.append({'DeviceName': 'EH1 slit X right', 'TangoAddress': proxies.motor_eh1_04, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit X left', 'TangoAddress': proxies.motor_eh1_03, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit Z top', 'TangoAddress': proxies.motor_eh1_01, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit Z bottom', 'TangoAddress': proxies.motor_eh1_02, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': '2nd optics X', 'TangoAddress': proxies.motor_eh1_16_tPixLinkMotorX, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': '2nd optics Z', 'TangoAddress': proxies.motor_eh1_15, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

##########_______________________SMARACT_______________________________________________###############################################################
    # Phase ring
    allMotors.append({'DeviceName': 'Phase Ring X', 'TangoAddress': proxies.smaract_eh1_cha15, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Phase Ring Z', 'TangoAddress': proxies.smaract_eh1_cha17, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Phase Ring Y', 'TangoAddress': proxies.smaract_eh1_cha16, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    # Apertures
    allMotors.append(
        {'DeviceName': 'Aperture X right (cha. 9)', 'TangoAddress': proxies.smaract_eh1_cha9, \
         'NumAttributes': 2, 'MainAttribute': 'Position', \
         'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    allMotors.append(
        {'DeviceName': 'Aperture X left (cha. 6)', 'TangoAddress': proxies.smaract_eh1_cha6, \
         'NumAttributes': 2, 'MainAttribute': 'Position', \
         'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})
    allMotors.append(
        {'DeviceName': 'Aperture Z top (cha. 7)', 'TangoAddress': proxies.smaract_eh1_cha10, \
         'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append(
        {'DeviceName': 'Aperture Z bottom (cha. 10)', 'TangoAddress': proxies.smaract_eh1_cha7, \
         'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    ### Beamshaper
    allMotors.append({'DeviceName': 'Beamshaper x (cha. 4)', 'TangoAddress': proxies.smaract_eh1_cha3, \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    allMotors.append({'DeviceName': 'Beamshaper z (cha. 5)', 'TangoAddress': proxies.smaract_eh1_cha2, \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    ## Beamstop
    allMotors.append({'DeviceName': 'Beamstop x (cha. 0)', 'TangoAddress': proxies.smaract_eh1_cha4, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Beamstop z (cha. 1)', 'TangoAddress': proxies.smaract_eh1_cha5, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                         'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
#

    allMotors.append({'DeviceName': 'Decoherer', 'TangoAddress': proxies.motor_eh1_14, \
                      'NumAttributes': 2, 'MainAttribute': 'Position', 'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})

    ## Camera Tower

    allMotors.append({'DeviceName': 'Aperture', 'TangoAddress': proxies.motor_eh1_06_tLensY, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Focus', 'TangoAddress': proxies.motor_eh1_05_tScintiY, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Mirror', 'TangoAddress': proxies.motor_eh1_08, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Tubus', 'TangoAddress': proxies.motor_eh1_07_tCamRot, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
     
 
 
 
    groups = []
    groups.append(['EH1 slits', 4, '#CCFFFF'])
#   groups.append(['Camera system', 3, '#BBBBFF'])
    groups.append(['Camera PixeLink', 2, '#CCFFCC'])
    groups.append(['Phase Ring', 3, '#FFFFBB'])
    groups.append(['Apertures OSA', 4, '#BBEEBB'])
    groups.append(['Beamshaper', 2, '#BBBBFF'])
    groups.append(['Beamstop', 2, '#EEBBAA'])
    groups.append(['Decoherer', 1, '#DDEEEE'])
    groups.append(['Camera Tower', 4, '#7B68EE'])
    TANGOgui(devices=allMotors, groups=groups, name=name, geometry = [4, 32, 1898, 1180])


def ConeBeamTangoGUI(parent=None):
    name = 'ConeBeamTangoGUI'
    allMotors = []

    allMotors.append({'DeviceName': 'EH1 slit X right', 'TangoAddress': proxies.motor_eh1_04, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit X left', 'TangoAddress': proxies.motor_eh1_03, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit Z top', 'TangoAddress': proxies.motor_eh1_01, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit Z bottom', 'TangoAddress': proxies.motor_eh1_02, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': '2nd optics X', 'TangoAddress': proxies.motor_eh1_16_tPixLinkMotorX, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': '2nd optics Z', 'TangoAddress': proxies.motor_eh1_15, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    
              

 
########### TAKEN OUT 201803_Problems with SMARACT SERVER! ERROR MESSAGE: Unknown sensor power status....IG##################################################################
    allMotors.append({'DeviceName': 'Teil x', 'TangoAddress': proxies.smaract_eh1_cha0, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Teil z', 'TangoAddress': proxies.smaract_eh1_cha1, \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    allMotors.append({'DeviceName': 'Aperture X right', 'TangoAddress': proxies.smaract_eh1_cha3, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    ##hzgpp05vme1:10000/p05/smaract/eh1.cha3
    allMotors.append({'DeviceName': 'Aperture X left', 'TangoAddress': proxies.smaract_eh1_cha4, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture Z top', 'TangoAddress': proxies.smaract_eh1_cha2, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture Z bottom', 'TangoAddress': proxies.smaract_eh1_cha5, \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    allMotors.append({'DeviceName': 'Lens x', 'TangoAddress': proxies.smaract_eh1_cha12, \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})
    allMotors.append({'DeviceName': 'Lens z', 'TangoAddress': proxies.smaract_eh1_cha13, \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    allMotors.append({'DeviceName': 'Decoherer', 'TangoAddress': proxies.motor_eh1_14, \
                      'NumAttributes': 2, 'MainAttribute': 'Position', 'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})



    groups = []
    groups.append(['EH1 slits', 4, '#CCFFFF'])
#   groups.append(['Camera system', 3, '#BBBBFF'])
    groups.append(['Camera PixeLink', 2, '#CCFFCC'])
    groups.append(['Teil', 2, '#FFFFBB'])
    groups.append(['Apertures OSA', 4, '#BBEEBB'])
    groups.append(['Lens', 2, '#FFFFBB'])
    groups.append(['Decoherer', 1, '#DDEEEE'])

    TANGOgui(devices=allMotors, groups=groups, name=name, geometry = [4, 32, 1898, 1180])
    

    
def NanoGrainMappingGUI():
    name = 'Nanograinmapping GUI'
    allMotors = []
    allMotors.append({'DeviceName': 'Hexapod X ', 'TangoAddress': proxies.hexapodsmall_x, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod Y ', 'TangoAddress': proxies.hexapodsmall_y, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod Z', 'TangoAddress': proxies.hexapodsmall_z, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Hexapod Rot X ', 'TangoAddress': proxies.hexapodsmall_u, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod Rot Y ', 'TangoAddress': proxies.hexapodsmall_v, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod Rot Z', 'TangoAddress': proxies.hexapodsmall_w, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

# Smarpod P03
    ##allMotors.append({'DeviceName': 'Smarpod X ',    'TangoAddress': proxies.smarpodmotor_p03nano_01_01, \ ## controller 2
##'NumAttributes': 2,           'MainAttribute': 'Position', \
##'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
## controller 1 (smarpod 1):                 

    allMotors.append({'DeviceName': 'Smarpod X ', 'TangoAddress': proxies.smarpodmotor_p03nano_01_01, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Smarpod X ', 'TangoAddress': proxies.smarpodmotor_p03nano_01_02, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Smarpod X ', 'TangoAddress': proxies.smarpodmotor_p03nano_01_03, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Smarpod X ', 'TangoAddress': proxies.smarpodmotor_p03nano_01_04, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Smarpod X ', 'TangoAddress': proxies.smarpodmotor_p03nano_01_05, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Smarpod X ', 'TangoAddress': proxies.smarpodmotor_p03nano_01_06, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Rotation ', 'TangoAddress': proxies.labmotion_exp01, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})


    groups = []
    groups.append(['Hexapod', 6, '#AB82FF'])
    groups.append(['Smarpod', 6, '#B9D3EE'])
    groups.append(['Labmotion Rotation Axis', 1, '#54ff9f'])
    TANGOgui(devices=allMotors, groups=groups, name=name, geometry = [4, 32, 1898, 1000])

##############################################LIGHTFIELD MICR    

def LightFieldGUI(parent=None):
    name = 'Lightfield device GUI'
    allMotors = []
#     
########### TAKEN OUT 201803_Problems with SMARACT SERVER! ERROR MESSAGE: Unknown sensor power status....IG##################################################################
    

 
    
#                    ###Scinti helps optics taken out since port needed for phase rings#####
    #     allMotors.append({'DeviceName': '2nd optics scintillator Y',    'TangoAddress': proxies.smaract_eh1_cha2, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
#

########################### ############################    
########################### PI Hexpod_P06 ###########################
########################### ###########################
## PI HEXA x,y,z 

    allMotors.append({'DeviceName': 'Hexapod x (mc01.02)', 'TangoAddress': proxies.hexapodmotor_mc01_02, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod y (mc01.01)', 'TangoAddress': proxies.hexapodmotor_mc01_01, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod z (mc01.03)', 'TangoAddress': proxies.hexapodmotor_mc01_03, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})    
    
############################# HEXA ROT Rx, Ry, Rz   

    allMotors.append({'DeviceName': 'Hexapod Rx (mc01.05)', 'TangoAddress': proxies.hexapodmotor_mc01_05, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod Ry (mc01.04)', 'TangoAddress': proxies.hexapodmotor_mc01_04, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod Rz (mc01.06)', 'TangoAddress': proxies.hexapodmotor_mc01_06, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True}) 

 
########################### Focusser

    allMotors.append({'DeviceName': 'OptPeters Foc', 'TangoAddress': proxies.motor_eh1_13, \
                      'NumAttributes': 2, 'MainAttribute': 'Position', 'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    

    
    groups = []
#    groups.append(['EH1 slits', 4, '#CCFFFF'])
#    groups.append(['Camera PixeLink', 2, '#CCFFCC'])
#    groups.append(['Apertures OSA', 4, '#BBEEBB'])
    groups.append(['PI HEXA', 3, '#FFFFBB'])
    groups.append(['PI HEXA ROT', 3, '#BBBBFF'])
    TANGOgui(devices=allMotors, groups=groups, name=name, geometry = [4, 32, 1898, 1180])


########################### ############################    
########################### PI Hexpod_P06 END!!! ###########################
########################### ###########################












#########################################Lightfield Mic END


def BeamlineOpticsGUI():
    name = 'Beamline optics GUI'
    allMotors = []
    allMotors.append({'DeviceName': 'Undulator', 'TangoAddress': proxies.tUndulator_1, \
                      'NumAttributes': 2,           'MainAttribute': 'Gap', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM energy server', 'TangoAddress': proxies.dcmener_s01_01_tDCMenergy, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM Bragg axis', 'TangoAddress': proxies.dcmmotor_s01_01, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM perpendicular', 'TangoAddress': proxies.motor_mono_11, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM parallel', 'TangoAddress': proxies.motor_mono_12, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM roll x1', 'TangoAddress': proxies.motor_mono_05, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM roll x2', 'TangoAddress': proxies.motor_mono_02_tRoll, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM pitch x2', 'TangoAddress': proxies.motor_mono_01_tPitch, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    #     allMotors.append({'DeviceName': 'Frontend slits left',    'TangoAddress': proxies.slt_exp_01, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    #     allMotors.append({'DeviceName': 'Frontend slits right',    'TangoAddress': proxies.slt_exp_02, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    #     allMotors.append({'DeviceName': 'Frontend slits gap',    'TangoAddress': proxies.slt_exp_03, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    #     allMotors.append({'DeviceName': 'Frontend slits offset',  'TangoAddress': proxies.slt_exp_04, \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'OH slits x1', 'TangoAddress': proxies.motor_mono_09, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'OH slits x2', 'TangoAddress': proxies.motor_mono_13, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'OH slits z1', 'TangoAddress': proxies.motor_mono_14, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'OH slits z2', 'TangoAddress': proxies.motor_mono_10, \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    groups = []
    groups.append(['Base components', 2, '#CCCCEE'])
    groups.append(['Monochromator main motors', 3, '#EECCCC'])
    groups.append(['Monochromator crystal motors', 3, '#EED6BF'])
    #groups.append(['Frontend slits', 4, '#EEEECC'])
    groups.append(['Optics hutch slits', 4, '#CCEECC'])
    
    TANGOgui(devices=allMotors, groups=groups, name=name, geometry = [12, 32, 1428, 1000])
    

def MicroCTgui():
    name = 'microCT GUI'
    allMotors = []
    allMotors.append({'DeviceName': 'Aperture X left (x1)', 'TangoAddress': proxies.motor_eh2_01, \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture X right (x2)', 'TangoAddress': proxies.motor_eh2_02, \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture Z top (z2)', 'TangoAddress': proxies.motor_eh2_04, \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture Z bottom (z1)', 'TangoAddress': proxies.motor_eh2_03, \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Hama Rot', 'TangoAddress': proxies.motor_eh2_11, \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hama X', 'TangoAddress': proxies.motor_eh2_07, \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hama Z', 'TangoAddress': proxies.micos_multipleaxis, \
                      'NumAttributes': 3, 'MainAttribute': 'PosZ', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    groups = []
    groups.append(['EH2 Apertures', 4, '#CCCCEE'])
    groups.append(['Camera motors', 3, '#EECCCC'])

    TANGOgui(devices=allMotors, groups=groups, name=name, geometry = [12, 32, 1428, 840])
    

def DMMgui():
    name = 'DMM GUI'
    allMotors = []
    allMotors.append({'DeviceName': 'Bragg 1st crystal', 'TangoAddress': proxies.motor_multi_21, \
                      'NumAttributes': 4,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True,
                      'ZMXdevice': proxies.zmx_multi_21})
    allMotors.append({'DeviceName': 'Roll 1st crystal', 'TangoAddress': proxies.motor_multi_17, \
                      'NumAttributes': 4,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True,
                      'ZMXdevice': proxies.zmx_multi_17})
    allMotors.append({'DeviceName': 'x translation 1st crystal', 'TangoAddress': proxies.motor_multi_22, \
                      'NumAttributes': 4,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True,
                      'ZMXdevice': proxies.zmx_multi_22})
    allMotors.append({'DeviceName': 'z translation 1st crystal', 'TangoAddress': proxies.motor_multi_19, \
                      'NumAttributes': 4,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True,
                      'ZMXdevice': proxies.zmx_multi_19})
    allMotors.append({'DeviceName': 'Bragg 2nd crystal', 'TangoAddress': proxies.motor_multi_25_tPitch, \
                      'NumAttributes': 4,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True,
                      'ZMXdevice': proxies.zmx_multi_25})
    allMotors.append({'DeviceName': 'x translation 2nd crystal', 'TangoAddress': proxies.motor_multi_30, \
                      'NumAttributes': 4,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True,
                      'ZMXdevice': proxies.zmx_multi_30})
    allMotors.append({'DeviceName': 'y translation 2nd crystal', 'TangoAddress': proxies.motor_multi_29, \
                      'NumAttributes': 4,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True,
                      'ZMXdevice': proxies.zmx_multi_29})
    allMotors.append({'DeviceName': 'z translation 2nd crystal', 'TangoAddress': proxies.motor_multi_26, \
                      'NumAttributes': 4,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True,
                      'ZMXdevice': proxies.zmx_multi_26})
#    allMotors.append({'DeviceName': 'Temperature 1st Crystal',    'TangoAddress':'//hzgpp05vme0:10000/hzg_dmm/hzg_ticom_dmm/cantemp01', \
#                  'NumAttributes': 4,           'MainAttribute': 'Temp1', \
#                  'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    
    groups = []
    groups.append(['1st Crystal', 4, '#CCCCEE'])
    groups.append(['2nd Crystal', 4, '#EECCCC'])
#    groups.append(['Temperature', 1, '#CCCCCC'])
    TANGOgui(devices=allMotors, groups=groups, name=name, geometry = [12, 32, 1488, 1030])