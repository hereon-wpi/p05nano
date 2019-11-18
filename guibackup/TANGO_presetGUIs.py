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


def NanoTangoGUI(parent=None):
    name = 'EH1 TANGO device GUI'
    allMotors = []
    allMotors.append({'DeviceName': 'Undulator',    'TangoAddress':'//hzgpp05vme0:10000/p05/undulator/1', \
                      'NumAttributes': 2,           'MainAttribute': 'Gap', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
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
    allMotors.append({'DeviceName': 'DCM pitch x2',    'TangoAddress':'//hzgpp05vme0:10000/p05/motor/mono.01', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Camera Ry',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.07', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Scintillator Y',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.05', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Lens Y',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.06', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Hamamatsu Trigger',    'TangoAddress':'//hzgpp05vme2:10000/p05/register/eh2.out01', \
                     'NumAttributes': 2,           'MainAttribute': 'Value', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

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
    allMotors.append({'DeviceName': '2nd optics scintillator Y',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha2', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})


    allMotors.append({'DeviceName': 'Aperture X right (cha. 3)',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha3', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture X left (cha. 0)',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha0', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture Z top (cha. 1)',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha1', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aperture Z bottom (cha. 4)',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha4', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Detector Aperture X right',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha6', \
                       'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Detector Aperture X left',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha9', \
                        'NumAttributes': 2,           'MainAttribute': 'Position', \
                        'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Detector Aperture Z bottom',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha10', \
                        'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})    
    allMotors.append({'DeviceName': 'Test pattern x',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha9', \
                       'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Test pattern z',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha10', \
                       'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Detector Aperture Z top',    'TangoAddress':'//hzgpp05vme1:10000/p05/smaract/eh1.cha7', \
                       'NumAttributes': 2,           'MainAttribute': 'Position', \
                       'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    
    allMotors.append({'DeviceName': 'PCO trigger',    'TangoAddress':'//hzgpp05vme1:10000/p05/dac/eh1.01', \
                      'NumAttributes': 3,           'MainAttribute': 'Voltage', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

#    allMotors.append({'DeviceName': 'JenaPiezo',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/jenapiezo', \
#                      'NumAttributes': 4, 'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    
    allMotors.append({'DeviceName': 'Decoherer',    'TangoAddress':'//hzgpp05vme1:10000/p05/motor/eh1.08', \
                      'NumAttributes': 2, 'MainAttribute': 'Position', 'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
 
    groups = []
    groups.append(['Beamline front end', 2, '#CCFFFF'])
    groups.append(['Camera system', 3, '#BBBBFF'])
    groups.append(['Hamamatsu Trigger', 1, '#CCFFCC'])
    groups.append(['EH1 slits', 4, '#FFFFBB'])
    groups.append(['Secondary optics', 3, '#BBEEBB'])
    groups.append(['Aperture slits', 4, '#EEBBAA'])
    groups.append(['PCO camera', 5, '#DDEEEE'])
    groups.append(['Decoherer', 1, '#FFCCFF'])
#     groups.append(['Jena Piezo', 1, '#FFCCFF'])
    TANGOgui(devices=allMotors, groups=groups, name=name, geometry = [4, 32, 1898, 1180])
    

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

    allMotors.append({'DeviceName': 'Frontend slits left',    'TangoAddress':'//hzgpp05vme0:10000/p05/slt/exp.01', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Frontend slits right',    'TangoAddress':'//hzgpp05vme0:10000/p05/slt/exp.02', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Frontend slits gap',    'TangoAddress':'//hzgpp05vme0:10000/p05/slt/exp.03', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Frontend slits offset',  'TangoAddress':'//hzgpp05vme0:10000/p05/slt/exp.04', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

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
    groups.append(['Frontend slits', 4, '#EEEECC'])
    groups.append(['Optics hutch slits', 4, '#CCEECC'])
    
    TANGOgui(devices=allMotors, groups=groups, name=name, geometry = [12, 32, 1428, 1000])
    

def MicroCTgui():
    name = 'microCT GUI'
    allMotors = []
    allMotors.append({'DeviceName': 'Substructure x',    'TangoAddress':'//hzgpp05vme2:10000/p05/tripod/pusher', \
                      'NumAttributes': 3,           'MainAttribute': 'PosX', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Substructure y',    'TangoAddress':'//hzgpp05vme2:10000/p05/tripod/pods', \
                      'NumAttributes': 3,           'MainAttribute': 'PosZ', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Camera aperture',    'TangoAddress':'//hzgpp05vme2:10000/p05/tripod/CCD_M3', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Camera z',    'TangoAddress':'//hzgpp05vme2:10000/p05/tripod/CCD_M8', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Camera focus',    'TangoAddress':'//hzgpp05vme2:10000/p05/tripod/CCD_M2', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Camera lens changer',    'TangoAddress':'//hzgpp05vme2:10000/p05/tripod/CCD_M5', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': False, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Attocube x',    'TangoAddress':'//hzgpp05vme2:10000/p05/attocubes/axis_x', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Attocube y',    'TangoAddress':'//hzgpp05vme2:10000/p05/attocubes/axis_y', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Attocube z',    'TangoAddress':'//hzgpp05vme2:10000/p05/attocubes/axis_z', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Attocube Rx',    'TangoAddress':'//hzgpp05vme2:10000/p05/attocubes/axis_p', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Attocube Ry',    'TangoAddress':'//hzgpp05vme2:10000/p05/attocubes/axis_t', \
                      'NumAttributes': 2,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    allMotors.append({'DeviceName': 'Aerotech rotation',    'TangoAddress':'//hzgpp05vme2:10000/p05ct/aerotech/s_rot', \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aerotech sample stage x',    'TangoAddress':'//hzgpp05vme2:10000/p05ct/aerotech/s_vert', \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})
    allMotors.append({'DeviceName': 'Aerotech sample stage z',    'TangoAddress':'//hzgpp05vme2:10000/p05ct/aerotech/s_stage_z', \
                      'NumAttributes': 3,           'MainAttribute': 'Position', \
                      'ShowRelMovementPanel': True, 'ReadOnly': False,  'ShowCommands': True})

    groups = []
    groups.append(['Substructure', 2, '#CCCCEE'])
    groups.append(['Camera motors', 4, '#EECCCC'])
    groups.append(['Attocubes', 5, '#EED6BF'])
    groups.append(['Aerotech axis', 3, '#EEEECC'])
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