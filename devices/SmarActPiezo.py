import ctypes
from ctypes import c_int32 as cint32
from ctypes import c_uint32 as cuint32
#from ctypes import c_float as cfloat
#from ctypes import c_char_p as cp
import numpy
#import time
#import string

class SmarActcomm():
    """
    Class to manage the connection to the PMAC controller using
    the dll interface. To be used with DeltaTau drivers version 4.0 
    or higher.
    """
    def __init__(self, CheckReference=False, Calibrate=False):
        self.io = ctypes.cdll.LoadLibrary('C:/Program Files (x86)/SmarAct/MCS/SDK/lib/MCSControl.dll')
        self.string_buffer = ctypes.create_string_buffer(600)
        self.intlist = (ctypes.c_int * 10)()
        self.uint32 = ctypes.c_uint32()
        self.int32 = ctypes.c_int32()
        self.uint32p = (ctypes.c_uint32 * 1)()
        self.int32p = (ctypes.c_int32 * 1)()
        
        self.io.SA_InitSystems(cint32(0))
        for ii in [0, 2, 3, 4]:
            if CheckReference:
                status = self.io.SA_FindReferenceMark_S(cint32(0), cint32(ii), cuint32(1), cuint32(60), cuint32(1))
                if status == 0:     print('Channel %i: reference found' % ii)
                elif status != 0:   print('Channel %i: error %i while scanning for reference' % (ii, status))
            if Calibrate:
                status = self.io.SA_CalibrateSensor_S(cint32(0), cint32(ii))
                if status == 0:     print('Channel %i: calibration ok' % ii)
                elif status != 0:   print('Channel %i: error %i while calibrating' % (ii, status))
        self.curPos = numpy.zeros((5))
        return None
    
    def GetStatus(self):
        tmp = self.io.SA_GetStatus_S(cint32(0), cint32(0), self.uint32p)
        print('Global Status: ', self.uint32p[0])
        return None
    
    def GetPositions(self):
        for ii in [0, 2, 3, 4]:
            pos = self.io.SA_GetPosition_S(cint32(0), cint32(ii), self.int32p)#, cuint32(1), cuint32(60), cuint32(1))
            self.curPos[ii] = self.int32p[0] * 1e-3
            print('Channel %i: Absolute position = %10.3f um' % (ii, self.int32p[0] * 1e-3))
        print('Center X = %10.3f' % (0.5 * (self.curPos[0] - self.curPos[3])))
        print('Center Z = %10.3f' % (0.5 * (-self.curPos[2] - self.curPos[4])))
        print('Delta X  = %10.3f' % ((self.curPos[0] + self.curPos[3])))
        print('Delta Z  = %10.3f' % ((-self.curPos[2] + self.curPos[4])))
    
    def ReturnPositions(self):
        for ii in [0, 2, 3, 4]:
            pos = self.io.SA_GetPosition_S(cint32(0), cint32(ii), self.int32p)
            self.curPos[ii] = self.int32p[0] * 1e-3
        return self.curPos[[0, 2, 3, 4]]
        
    def ZeroPositions(self):
        for ii in [0, 2, 3, 4]:
            status = self.io.SA_SetPosition_S(cuint32(0), cuint32(ii), cint32(0))
        return None

    def GotoPositions(self, _positions, silent=True):
        status = self.io.SA_GotoPositionAbsolute_S(cuint32(0), cuint32(0), cint32(int(_positions[0] * 1000)), cuint32(60))
        if not silent:
            if status == 0:   print('Channel %i: move successful' % _channel);
            elif status != 0: print('Channel %i: Error %i' % (_channel, status))
        status = self.io.SA_GotoPositionAbsolute_S(cuint32(0), cuint32(2), cint32(int(_positions[1] * 1000)), cuint32(60))
        if not silent:
            if status == 0:   print('Channel %i: move successful' % _channel);
            elif status != 0: print('Channel %i: Error %i' % (_channel, status))
        status = self.io.SA_GotoPositionAbsolute_S(cuint32(0), cuint32(3), cint32(int(_positions[2] * 1000)), cuint32(60))
        if not silent:
            if status == 0:   print('Channel %i: move successful' % _channel);
            elif status != 0: print('Channel %i: Error %i' % (_channel, status))
        status = self.io.SA_GotoPositionAbsolute_S(cuint32(0), cuint32(4), cint32(int(_positions[3] * 1000)), cuint32(60))
        if not silent:
            if status == 0:   print('Channel %i: move successful' % _channel);
            elif status != 0: print('Channel %i: Error %i' % (_channel, status))
        return None

    def Move(self, _channel, _position, silent=False):
        tmp = int(1e3 * _position)
        status = self.io.SA_GotoPositionAbsolute_S(cuint32(0), cuint32(_channel), cint32(int(_position * 1000)), cuint32(60))
        if not silent:
            if status == 0:   print('Channel %i: move successful' % _channel);
            elif status != 0: print('Channel %i: Error %i' % (_channel, status))
        return None

    def MoveRel(self, _channel, _position, silent=False):
        status = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(_channel), cint32(_position * 1000), cuint32(60))
        if not silent:
            if status == 0:   print('Channel %i: move successful' % _channel);
            elif status != 0: print('Channel %i: Error %i' % (_channel, status))
        return None
    
    def MoveRelLLx(self, _value, silent=False):
        status = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(3), cint32(-_value * 1000), cuint32(60))
        if not silent:
            if status == 0:   print('LL x: move successful');
            elif status != 0: print('LL x: Error %i' % (status))
        
    def MoveLLx(self, _value, silent=False):
        status = self.io.SA_GotoPositionAbsolute_S(cuint32(0), cuint32(3), cint32(-_value * 1000), cuint32(60))
        if not silent:
            if status == 0:   print('LL x: move successful');
            elif status != 0: print('LL x: Error %i' % (status))
    
    def MoveRelLLz(self, _value, silent=False):
        status = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(4), cint32(-_value * 1000), cuint32(60))
        if not silent:
            if status == 0:   print('LL x: move successful');
            elif status != 0: print('LL x: Error %i' % (status))
        
    def MoveLLz(self, _value, silent=False):
        status = self.io.SA_GotoPositionAbsolute_S(cuint32(0), cuint32(4), cint32(-_value * 1000), cuint32(60))
        if not silent:
            if status == 0:   print('LL x: move successful');
            elif status != 0: print('LL x: Error %i' % (status))

    def MoveRelURx(self, _value, silent=False):
        status = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(0), cint32(_value * 1000), cuint32(60))
        if not silent:
            if status == 0:   print('UR x: move successful');
            elif status != 0: print('UR x: Error %i' % (status))
        
    def MoveURx(self, _value, silent=False):
        status = self.io.SA_GotoPositionAbsolute_S(cuint32(0), cuint32(0), cint32(_value * 1000), cuint32(60))
        if not silent:
            if status == 0:   print('UR x: move successful');
            elif status != 0: print('UR x: Error %i' % (status))
    
    def MoveRelURz(self, _value, silent=False):
        status = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(2), cint32(-_value * 1000), cuint32(60))
        if not silent:
            if status == 0:   print('UR x: move successful');
            elif status != 0: print('UR x: Error %i' % (status))
        
    def MoveURz(self, _value, silent=False):
        status = self.io.SA_GotoPositionAbsolute_S(cuint32(0), cuint32(2), cint32(-_value * 1000), cuint32(60))
        if not silent:
            if status == 0:   print('UR x: move successful');
            elif status != 0: print('UR x: Error %i' % (status))

    def DeltaLR(self, _delta, silent=False):
        status0 = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(0), cint32(_delta * 1000), cuint32(60))
        status1 = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(3), cint32(-_delta * 1000), cuint32(60))
        if not silent:
            if status0 == 0 and status1 == 0:  
                print('Move slits in delta x: move successful')
            else:
                print('Move slits in delta x: Error %i' % (status))

    def DeltaUD(self, _delta, silent=False):
        status0 = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(4), cint32(-_delta * 1000), cuint32(60))
        status1 = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(2), cint32(-_delta * 1000), cuint32(60))
        if not silent:
            if status0 == 0 and status1 == 0:  
                print('Move slits in delta z: move successful')
            else:
                print('Move slits in delta z: Error %i' % (status))

    def DeltaWidth(self, _delta, silent=False):
        _value = int(500 * _delta)
        status0 = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(0), cint32(_value), cuint32(60))   ## x right
        status1 = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(2), cint32(-_value), cuint32(60))  ## z top
        status2 = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(3), cint32(_value), cuint32(60))  ## x left
        status3 = self.io.SA_GotoPositionRelative_S(cuint32(0), cuint32(4), cint32(_value), cuint32(60))  ## z bottom
        if not silent:
            if status0 == 0 and status1 == 0 and status2 == 0 and status3 == 0:  
                print('Move slit delta opening: move successful')
            else:
                print('Move slit delta opening: Errors %i / %i / %i / %i' % (status0, status1, status2, status3))
        return None

    def Exit(self):
        self.io.SA_ReleaseSystems()
        return None

    def Reconnect(self):
        self.io.SA_InitSystems(cint32(0))
        return None

if __name__ == '__main__':
    try:
        tmp = SmarActcomm()
        tmp.GetStatus()
        tmp.GetPositions()
        tmp.Exit()
    except:
        tmp.Exit()
