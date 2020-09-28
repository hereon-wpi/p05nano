import p05.common.TangoFailsaveComm as tSave


def FLIimage(FLItango, SetRoi=None, FrameNumber=None, FramePrefix=None, ExposureTime=None, BaseDir = None, HBin= None, VBin = None):
    """
    Function to save an Image with the FLI camera.
    
    Calling Parameters:
    FLItango:    Instance of PyTango.DeviceProxy with the camera
    Others:      As in the Tango Server for the FLI camera.
                 If None, no change will be made to these attributes,
                 else they will be set to the new value.
    
    returns:    <Boolean>. Returns True if the image has been taken and saved,
                False in all other cases.
    """
    #arglist = [FrameNumber, FramePrefix, ExposureTime, BaseDir, HBin, VBin]
    #argstr  = ['FrameNumber', 'FramePrefix', 'ExposureTime', 'BaseDir', 'HBin', 'VBin'] 
    try:
        cmd_ok = True
        #Setting the Attributes
        for arg in ['FrameNumber', 'FramePrefix', 'ExposureTime', 'BaseDir', 'HBin', 'VBin']:
            if eval(arg) != None:
                FLItango.write_attribute(arg, eval(arg))
        if SetRoi != None:
            cmd_ok = tSave.tSaveCommCommand(FLItango, 'SetRoi', Argument=SetRoi)
        if not cmd_ok:
            print('Error: Could not write TANGO command')
            return False
        
        #Taking the image:
        cmd_ok = tSave.tSaveCommCommand(FLItango, 'ExposeFrame', waitforstate='EXTRACT')
        if cmd_ok == None: cmd_ok = True
        if not cmd_ok:
            print('Error: Could not write TANGO command')
            return False
        cmd_ok = tSave.tSaveCommCommand(FLItango, 'GrabAndSaveFrame')
        if cmd_ok == None: cmd_ok = True
        if not cmd_ok:
            print('Error: Could not write TANGO command')
            return False
        return True
    #Python 3 comaptibility (FW: I think PyTango needs to be fixed for catching errors in Python 3)
    except:
    #except (PyTango.DevFailed, PyTango.DevError, PyTango.CommunicationFailed, PyTango.ConnectionFailed):
        print('Tango Error')
        return False
#end FLIimage


def FLIgetImage(FLItango, SetRoi=None, FrameNumber=None, FramePrefix=None, ExposureTime=None, BaseDir = None, HBin= None, VBin = None):
    """
    Function to return an Image with the FLI camera.
    
    Calling Parameters:
    FLItango:    Instance of PyTango.DeviceProxy with the camera
    Others:      As in the Tango Server for the FLI camera.
                 If None, no change will be made to these attributes,
                 else they will be set to the new value.
    
    returns:    <Boolean>. Returns True if the image has been taken and saved,
                False in all other cases.
    """
    #arglist = [FrameNumber, FramePrefix, ExposureTime, BaseDir, HBin, VBin]
    #argstr  = ['FrameNumber', 'FramePrefix', 'ExposureTime', 'BaseDir', 'HBin', 'VBin'] 
    try:
        cmd_ok = True
        #Setting the Attributes
        for arg in ['FrameNumber', 'FramePrefix', 'ExposureTime', 'BaseDir', 'HBin', 'VBin']:
            if eval(arg) != None:
                FLItango.write_attribute(arg, eval(arg))
        if SetRoi != None:
            cmd_ok = tSave.tSaveCommCommand(FLItango, 'SetRoi', Argument=SetRoi)
        if not cmd_ok:
            print('Error: Could not write TANGO command')
            return False
        #Taking the image:
        cmd_ok = tSave.tSaveCommCommand(FLItango, 'ExposeFrame', waitforstate='EXTRACT')
        if cmd_ok == None: cmd_ok = True
        if not cmd_ok:
            print('Error: Could not write TANGO command')
            return False
        print(1)
        cmd_ok = tSave.tSaveCommCommand(FLItango, 'GrabFrame')
        if cmd_ok == None: cmd_ok = True
        if not cmd_ok:
            print('Error: Could not write TANGO command')
            return False
        image = tSave.tSaveCommReadAttribute(FLItango, 'Image')
        return image
    #Python 3 comaptibility (FW: I think PyTango needs to be fixed for catching errors in Python 3)
    except:
    #except (PyTango.DevFailed, PyTango.DevError, PyTango.CommunicationFailed, PyTango.ConnectionFailed):
        print('Tango Error')
        return False
#end FLIimage

def FLIexpose(FLItango, SetRoi=None, ExposureTime=None, HBin= None, VBin = None):
    """
    Function expose the FLI camera.
    
    Calling Parameters:
    FLItango:    Instance of PyTango.DeviceProxy with the camera
    Others:      As in the Tango Server for the FLI camera.
                 If None, no change will be made to these attributes,
                 else they will be set to the new value.
    
    returns:    <Boolean>. Returns True if the image has been taken and saved,
                False in all other cases.
    """
    #arglist = [FrameNumber, FramePrefix, ExposureTime, BaseDir, HBin, VBin]
    #argstr  = ['FrameNumber', 'FramePrefix', 'ExposureTime', 'BaseDir', 'HBin', 'VBin'] 
    try:
        cmd_ok = True
        #Setting the Attributes
        for arg in ['ExposureTime', 'HBin', 'VBin']:
            if eval(arg) != None:
                FLItango.write_attribute(arg, eval(arg))
        if SetRoi != None:
            cmd_ok = tSave.tSaveCommCommand(FLItango, 'SetRoi', Argument=SetRoi)
        if not cmd_ok:
            print('Error: Could not write TANGO command')
            return False
        
        #Taking the image:
        cmd_ok = tSave.tSaveCommCommand(FLItango, 'ExposeFrame', waitforstate='EXTRACT')
        if not cmd_ok:
            print('Error: Could not write TANGO command')
            return False
        return None
    #Python 3 comaptibility (FW: I think PyTango needs to be fixed for catching errors in Python 3)
    except:
    #except (PyTango.DevFailed, PyTango.DevError, PyTango.CommunicationFailed, PyTango.ConnectionFailed):
        print('Tango Error')
        return False
#end FLIexpose

def FLIgrabImage(FLItango, FrameNumber=None, FramePrefix=None, BaseDir = None):
    """
    Function to read out an Image from the FLI camera.
    
    Calling Parameters:
    FLItango:    Instance of PyTango.DeviceProxy with the camera
    Others:      As in the Tango Server for the FLI camera.
                 If None, no change will be made to these attributes,
                 else they will be set to the new value.
    
    returns:    <Boolean>. Returns True if the image has been taken and saved,
                False in all other cases.
    """
    #arglist = [FrameNumber, FramePrefix, ExposureTime, BaseDir, HBin, VBin]
    #argstr  = ['FrameNumber', 'FramePrefix', 'ExposureTime', 'BaseDir', 'HBin', 'VBin'] 
    try:
        cmd_ok = True
        #Setting the Attributes
        for arg in ['FrameNumber', 'FramePrefix', 'BaseDir']:
            if eval(arg) != None:
                FLItango.write_attribute(arg, eval(arg))
        
        #Reading the image:
        cmd_ok = tSave.tSaveCommCommand(FLItango, 'GrabFrame')
        if not cmd_ok:
            print('Error: Could not write TANGO command')
            return False
        image = tSave.tSaveCommReadAttribute(FLItango, 'Image')
        return image
    #Python 3 comaptibility (FW: I think PyTango needs to be fixed for catching errors in Python 3)
    except:
    #except (PyTango.DevFailed, PyTango.DevError, PyTango.CommunicationFailed, PyTango.ConnectionFailed):
        print('Tango Error')
        return False
#end FLIgrabImage
