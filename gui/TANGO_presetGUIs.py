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
#     allMotors.append({'DeviceName': 'Undulator',    'TangoAddress':'//hzgpp05vme0:10000/p05/undulator/1', \
#                       'NumAttributes': 2,           'MainAttribute': 'Gap', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
#     allMotors.append({'DeviceName': 'DCM energy server',    'TangoAddress':'//hzgpp05vme0:10000/p05/dcmener/s01.01', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
#     allMotors.append({'DeviceName': 'DCM Bragg axis',    'TangoAddress':'//hzgpp05vme0:10000/p05/dcmmotor/s01.01', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
#     allMotors.append({'DeviceName': 'DCM perpendicular',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.11', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
#     allMotors.append({'DeviceName': 'DCM parallel',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.12', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
#     allMotors.append({'DeviceName': 'DCM roll x1',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.05', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
#     allMotors.append({'DeviceName': 'DCM roll x2',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.02', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
#     allMotors.append({'DeviceName': 'DCM pitch x2',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.01', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

#     allMotors.append({'DeviceName': 'Camera Ry',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.07', \
#                      'NumAttributes': 2,           'MainAttribute': 'Position', \
#                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
#   allMotors.append({'DeviceName': 'Scintillator Y',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.05', \
#                     'NumAttributes': 2,           'MainAttribute': 'Position', \
#                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
#   allMotors.append({'DeviceName': 'Lens Y',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.06', \
#                     'NumAttributes': 2,           'MainAttribute': 'Position', \
#                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

#     allMotors.append({'DeviceName': 'Hamamatsu Trigger',    'TangoAddress':'//hzgpp05vme2:10000/p05/register/eh2.out01', \
#                      'NumAttributes': 2,           'MainAttribute': 'Value', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

###########________________________________ZMX______________________##################################################################
    

    allMotors.append({'DeviceName': 'EH1 slit X right',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.04', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit X left',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.03', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit Z top',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.01', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit Z bottom',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.02', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
  
    allMotors.append({'DeviceName': '2nd optics X',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.16', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': '2nd optics Z',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.15', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

##########_______________________SMARACT_______________________________________________###############################################################
    # Phase ring
    allMotors.append({'DeviceName': 'Phase Ring X',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha15', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Phase Ring Z',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha17', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Phase Ring Y',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha16', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    # Apertures
    allMotors.append(
        {'DeviceName': 'Aperture X right (cha. 9)', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha9', \
         'NumAttributes': 2, 'MainAttribute': 'Position', \
         'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    allMotors.append(
        {'DeviceName': 'Aperture X left (cha. 6)', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha6', \
         'NumAttributes': 2, 'MainAttribute': 'Position', \
         'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})
    allMotors.append(
        {'DeviceName': 'Aperture Z top (cha. 7)', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha10', \
         'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append(
        {'DeviceName': 'Aperture Z bottom (cha. 10)', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha7', \
         'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    ### Beamshaper
    allMotors.append({'DeviceName': 'Beamshaper x (cha. 4)', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha3', \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    allMotors.append({'DeviceName': 'Beamshaper z (cha. 5)', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha2', \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    ## Beamstop
    allMotors.append({'DeviceName': 'Beamstop x (cha. 0)', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha4', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Beamstop z (cha. 1)', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha5', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                         'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
#

    allMotors.append({'DeviceName': 'Decoherer',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.14', \
                      'NumAttributes': 2, 'MainAttribute': 'Position', 'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})

    ## Camera Tower

    allMotors.append({'DeviceName': 'Aperture',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.06', \
                         'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})    
    allMotors.append({'DeviceName': 'Focus',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.05', \
                        'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True}) 
    allMotors.append({'DeviceName': 'Mirror',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.08', \
                         'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Tubus',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.07', \
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

    

    allMotors.append({'DeviceName': 'EH1 slit X right',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.04', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit X left',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.03', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit Z top',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.01', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'EH1 slit Z bottom',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.02', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
  
    allMotors.append({'DeviceName': '2nd optics X',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.16', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': '2nd optics Z',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.15', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    
              

 
########### TAKEN OUT 201803_Problems with SMARACT SERVER! ERROR MESSAGE: Unknown sensor power status....IG##################################################################
    allMotors.append({'DeviceName': 'Teil x', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha0', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Teil z', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha1', \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    allMotors.append({'DeviceName': 'Aperture X right', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha3', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    ##hzgpp05vme1:10000/p05/smaract/eh1.cha3
    allMotors.append({'DeviceName': 'Aperture X left', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha4', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture Z top', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha2', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture Z bottom', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha5', \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    allMotors.append({'DeviceName': 'Lens x', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha12', \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})
    allMotors.append({'DeviceName': 'Lens z', 'TangoAddress': '//hzgpp05vme1:10000/p05/smaract/eh1.cha13', \
                      'NumAttributes': 2, 'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False, 'ShowCommands': True})

    allMotors.append({'DeviceName': 'Decoherer',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.14', \
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
    allMotors.append({'DeviceName': 'Hexapod X ',    'TangoAddress':'//hzgpp07EH3:10000/p07/hexapodsmall/X', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod Y ',    'TangoAddress':'//hzgpp07EH3:10000/p07/hexapodsmall/Y', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod Z',    'TangoAddress':'//hzgpp07EH3:10000/p07/hexapodsmall/Z', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
     
    allMotors.append({'DeviceName': 'Hexapod Rot X ',    'TangoAddress':'//hzgpp07EH3:10000/p07/hexapodsmall/U', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod Rot Y ',    'TangoAddress':'//hzgpp07EH3:10000/p07/hexapodsmall/V', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hexapod Rot Z',    'TangoAddress':'//hzgpp07EH3:10000/p07/hexapodsmall/W', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

# Smarpod P03
##allMotors.append({'DeviceName': 'Smarpod X ',    'TangoAddress':'//haspp03nano:10000/p03/smarpodmotor/p03nano_01.01', \ ## controller 2
##'NumAttributes': 2,           'MainAttribute': 'Position', \
##'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
## controller 1 (smarpod 1):                 

    allMotors.append({'DeviceName': 'Smarpod X ',    'TangoAddress':'//haspp03nano:10000/p03/smarpodmotor/p03nano_01.01', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Smarpod X ',    'TangoAddress':'//haspp03nano:10000/p03/smarpodmotor/p03nano_01.02', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Smarpod X ',    'TangoAddress':'//haspp03nano:10000/p03/smarpodmotor/p03nano_01.03', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Smarpod X ',    'TangoAddress':'//haspp03nano:10000/p03/smarpodmotor/p03nano_01.04', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Smarpod X ',    'TangoAddress':'//haspp03nano:10000/p03/smarpodmotor/p03nano_01.05', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Smarpod X ',    'TangoAddress':'//haspp03nano:10000/p03/smarpodmotor/p03nano_01.06', \
                     'NumAttributes': 2,           'MainAttribute': 'Position', \
                     'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Rotation ',    'TangoAddress':'//haspp03nano:10000/p03nano/labmotion/exp.01', \
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
#     allMotors.append({'DeviceName': '2nd optics scintillator Y',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha2', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
#

########################### ############################    
########################### PI Hexpod_P06 ###########################
########################### ###########################
## PI HEXA x,y,z 




    allMotors.append({'DeviceName': 'Hexapod x (mc01.02)',    'TangoAddress':'//haspp06mc01:10000/p06/hexapodmotor/mc01.02', \
                        'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})    
    allMotors.append({'DeviceName': 'Hexapod y (mc01.01)',    'TangoAddress':'//haspp06mc01:10000/p06/hexapodmotor/mc01.01', \
                        'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})       
    allMotors.append({'DeviceName': 'Hexapod z (mc01.03)',    'TangoAddress':'//haspp06mc01:10000/p06/hexapodmotor/mc01.03', \
                        'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})    
    
############################# HEXA ROT Rx, Ry, Rz   
    
    
   
    allMotors.append({'DeviceName': 'Hexapod Rx (mc01.05)',    'TangoAddress':'//haspp06mc01:10000/p06/hexapodmotor/mc01.05', \
                        'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})      
    allMotors.append({'DeviceName': 'Hexapod Ry (mc01.04)',    'TangoAddress':'//haspp06mc01:10000/p06/hexapodmotor/mc01.04', \
                        'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})      
    allMotors.append({'DeviceName': 'Hexapod Rz (mc01.06)',    'TangoAddress':'//haspp06mc01:10000/p06/hexapodmotor/mc01.06', \
                        'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True}) 

 
########################### Focusser


    allMotors.append({'DeviceName': 'OptPeters Foc',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.13', \
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
    allMotors.append({'DeviceName': 'Undulator',    'TangoAddress':'//hzgpp05vme0:10000/p05/undulator/1', \
                      'NumAttributes': 2,           'MainAttribute': 'Gap', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM energy server',    'TangoAddress':'//hzgpp05vme0:10000/p05/dcmener/s01.01', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM Bragg axis',    'TangoAddress':'//hzgpp05vme0:10000/p05/dcmmotor/s01.01', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM perpendicular',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.11', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM parallel',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.12', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM roll x1',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.05', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM roll x2',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.02', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'DCM pitch x2',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.01', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

#     allMotors.append({'DeviceName': 'Frontend slits left',    'TangoAddress':'//hzgpp05vme0:10000/p05/slt/exp.01', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
#     allMotors.append({'DeviceName': 'Frontend slits right',    'TangoAddress':'//hzgpp05vme0:10000/p05/slt/exp.02', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
#     allMotors.append({'DeviceName': 'Frontend slits gap',    'TangoAddress':'//hzgpp05vme0:10000/p05/slt/exp.03', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
#     allMotors.append({'DeviceName': 'Frontend slits offset',  'TangoAddress':'//hzgpp05vme0:10000/p05/slt/exp.04', \
#                       'NumAttributes': 2,           'MainAttribute': 'Position', \
#                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'OH slits x1',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.09', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'OH slits x2',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.13', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'OH slits z1',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.14', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'OH slits z2',  'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.10', \
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
    allMotors.append({'DeviceName': 'Aperture X left (x1)',    'TangoAddress':'//hzgpp05vme2:10000/p05/motor/eh2.01', \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture X right (x2)',    'TangoAddress':'//hzgpp05vme2:10000/p05/motor/eh2.02', \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture Z top (z2)',    'TangoAddress':'//hzgpp05vme2:10000/p05/motor/eh2.04', \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture Z bottom (z1)',    'TangoAddress':'//hzgpp05vme2:10000/p05/motor/eh2.03', \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})


    allMotors.append({'DeviceName': 'Hama Rot',    'TangoAddress':'//hzgpp05vme2:10000/p05/motor/eh2.11', \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hama X',    'TangoAddress':'//hzgpp05vme2:10000/p05/motor/eh2.07', \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Hama Z', 'TangoAddress': '//hzgpp05vme2:10000/p05/micos/multipleaxis', \
                      'NumAttributes': 3, 'MainAttribute': 'PosZ', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    groups = []
    groups.append(['EH2 Apertures', 4, '#CCCCEE'])
    groups.append(['Camera motors', 3, '#EECCCC'])

    TANGOgui(devices=allMotors, groups=groups, name=name, geometry = [12, 32, 1428, 840])
    

def DMMgui():
    name = 'DMM GUI'
    allMotors = []
    allMotors.append({'DeviceName': 'Bragg 1st crystal',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/multi.21', \
                  'NumAttributes': 4,           'MainAttribute': 'Position', \
                  'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True, 'ZMXdevice': '//hzgpp05vme0:10000/p05/ZMX/multi.21'})
    allMotors.append({'DeviceName': 'Roll 1st crystal',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/multi.17', \
                  'NumAttributes': 4,           'MainAttribute': 'Position', \
                  'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True, 'ZMXdevice': '//hzgpp05vme0:10000/p05/ZMX/multi.17'})
    allMotors.append({'DeviceName': 'x translation 1st crystal',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/multi.22', \
                  'NumAttributes': 4,           'MainAttribute': 'Position', \
                  'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True, 'ZMXdevice': '//hzgpp05vme0:10000/p05/ZMX/multi.22'})
    allMotors.append({'DeviceName': 'z translation 1st crystal',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/multi.19', \
                  'NumAttributes': 4,           'MainAttribute': 'Position', \
                  'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True, 'ZMXdevice': '//hzgpp05vme0:10000/p05/ZMX/multi.19'})
    allMotors.append({'DeviceName': 'Bragg 2nd crystal',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/multi.25', \
                  'NumAttributes': 4,           'MainAttribute': 'Position', \
                  'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True, 'ZMXdevice': '//hzgpp05vme0:10000/p05/ZMX/multi.25'})
    allMotors.append({'DeviceName': 'x translation 2nd crystal',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/multi.30', \
                  'NumAttributes': 4,           'MainAttribute': 'Position', \
                  'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True, 'ZMXdevice': '//hzgpp05vme0:10000/p05/ZMX/multi.30'})
    allMotors.append({'DeviceName': 'y translation 2nd crystal',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/multi.29', \
                  'NumAttributes': 4,           'MainAttribute': 'Position', \
                  'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True, 'ZMXdevice': '//hzgpp05vme0:10000/p05/ZMX/multi.29'})
    allMotors.append({'DeviceName': 'z translation 2nd crystal',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/multi.26', \
                  'NumAttributes': 4,           'MainAttribute': 'Position', \
                  'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True, 'ZMXdevice': '//hzgpp05vme0:10000/p05/ZMX/multi.26'})
#    allMotors.append({'DeviceName': 'Temperature 1st Crystal',    'TangoAddress':'//hzgpp05vme0:10000/hzg_dmm/hzg_ticom_dmm/cantemp01', \
#                  'NumAttributes': 4,           'MainAttribute': 'Temp1', \
#                  'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    
    groups = []
    groups.append(['1st Crystal', 4, '#CCCCEE'])
    groups.append(['2nd Crystal', 4, '#EECCCC'])
#    groups.append(['Temperature', 1, '#CCCCCC'])
    TANGOgui(devices=allMotors, groups=groups, name=name, geometry = [12, 32, 1488, 1030])