import PyTango
import time


def tSaveCommCommand(tObject, Command, Argument=None, silent = False,
                     deadtime = 300, wait=True, waitforstate='ON'):
    """
    Function to execute the Tango command <<Command>> with the 
    calling argument <<Argument>> on the PyTango.DeviceProxy 
    <<tObject>> also in case of temporary unresponsive TANGO server. 
    
    Calling parameters:
    tObject:        PyTango.DeviceProxy instance of the TANGO device
    Command:        Command to be send to the TANGO device
    Argument:       Argument to be send with the command.
                    Only used if Argument != None
                    (preset Argument = None)
    silent:         If set to True, no screen output will be printed.
                    (preset silent = False)
    deadtime:       Time (in seconds) after which the device will be
                    declared non-active, i.e. no further attempts at
                    communication will be performed.
                    (preset deadtime = 300) 
    wait:           If True, tSaveCommand waits until waitforstate is
                    reached. Otherwise the command returns immediately.
                    Default: True
    waitforstate:   PyTango state to wait for. Currently, 'ON' and 'EXTRACT'
    		    are defined. Default: 'ON'
    """

    if waitforstate == 'ON':
        wst = PyTango.DevState.ON
    elif waitforstate == 'EXTRACT':
        wst = PyTango.DevState.EXTRACT
    
    t0 = time.time()
    while True:
        try:
            if Argument != None:
                retVal = tObject.command_inout(Command, Argument)
            else:
                retVal = tObject.command_inout(Command)
            time.sleep(0.05)
            if wait:
                while tObject.state() != wst: time.sleep(0.05)
            break
        #Python 3 comaptibility (FW: I think PyTango needs to be fixed for catching errors in Python 3)
        except:
        #except (PyTango.DevFailed, PyTango.DevError, PyTango.CommunicationFailed, PyTango.ConnectionFailed):
            if not silent:
                print('No communication with %s at ' %(tObject)+ time.strftime('%X', time.localtime()))
                print('exec', Command)
            time.sleep(0.5)
        if time.time() > t0 + deadtime: break
    if time.time() < t0 + deadtime:
        return retVal
    else:
        return False
#end TangoSecureCommand
    
def tSaveCommWriteAttribute(tObject, Attribute, Value, silent = False, deadtime
                            = 300, wait=True, waitforstate='ON'):
    """
    Function to write the value <<Value>> to the Tango attribute 
    <<Atttriubte>> on the PyTango.DeviceProxy <<tObject>> also 
    in case of temporary unresponsive TANGO server. 
    
    Calling parameters:
    tObject:    PyTango.DeviceProxy instance of the TANGO device
    Attribute:  Attribute to be set on the TANGO device
    Value:      Attribute value to be set
    silent:     If set to True, no screen output will be printed.
                (preset silent = False)
    deadtime:   Time (in seconds) after which the device will be
                declared non-active, i.e. no further attempts at
                communication will be performed.
                (preset deadtime = 300) 
    """
    if waitforstate == 'ON':
        wst = PyTango.DevState.ON
    elif waitforstate == 'EXTRACT':
        wst = PyTango.DevState.EXTRACT
        
    t0 = time.time()
    while True:
        try:
            tObject.write_attribute(Attribute, Value)
            time.sleep(0.05)
            if wait:
                while tObject.state() != wst: (0.05)
            break
        #Python 3 comaptibility (FW: I think PyTango needs to be fixed for catching errors in Python 3)
        except:
        #except (PyTango.DevFailed, PyTango.DevError, PyTango.CommunicationFailed, PyTango.ConnectionFailed):
            if not silent:
                print('No communication with %s at ' %(tObject)+ time.strftime('%X', time.localtime()))
                print('write', Attribute, Value)
            time.sleep(0.5)
        if time.time() > t0 + deadtime: break
    if time.time() < t0 + deadtime:
        return True
    else:
        return False
#end TangoSecureWriteAttribute

def tSaveCommReadAttribute(tObject, Attribute, silent = False, deadtime = 300):
    """
    Function to write the value <<Value>> to the Tango attribute 
    <<Atttribute>> on the PyTango.DeviceProxy <<tObject>> also 
    in case of temporary unresponsive TANGO server. 
    
    Calling parameters:
    tObject:    PyTango.DeviceProxy instance of the TANGO device
    Attribute:  Attribute to be read on the TANGO device
    silent:     If set to True, no screen output will be printed.
                (preset silent = False)
    deadtime:   Time (in seconds) after which the device will be
                declared non-active, i.e. no further attempts at
                communication will be performed.
                (preset deadtime = 300) 
    """
    t0 = time.time()
    attval = None
    while True:
        try:
            attval = tObject.read_attribute(Attribute).value
            time.sleep(0.05)
            break
        #Python 3 comaptibility (FW: I think PyTango needs to be fixed for catching errors in Python 3)
        except:
        #except (PyTango.DevFailed, PyTango.DevError, PyTango.CommunicationFailed, PyTango.ConnectionFailed):
            if not silent:
                print('No communication with %s at ' %(tObject)+ time.strftime('%X', time.localtime()))
                print('read', Attribute)
            time.sleep(0.5)
        if time.time() > t0 + deadtime: break
    return attval
#end TangoSecureReadAttribute
