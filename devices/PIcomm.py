'''
Created on 06.03.2012

@author: ogurreck
'''
import ctypes
#import numpy
import time
#import string

class PIcomm():
    def __init__(self, silent=False, silentmode = False):
        self.error = False
        self.connection_active = False
        self.string_buffer = ctypes.create_string_buffer(1200)
        #check and set silentmode parameter
        if silentmode not in [True, False]:
            self.silentmode = False
        else: 
            self.silentmode = silentmode
        self.io =ctypes.windll.LoadLibrary('C:/Users/Public/Documents/PI/E-712/E712_GCS_DLL/PI_GCS2_DLL.dll')
        #self.USBgetConnection()
        self.TCPIPopenConnection()
        ctrue = ctypes.c_bool(True)
        self.io.PI_SVO(self.id, self.c_char_p('1'), ctrue)
        self.io.PI_SVO(self.id, self.c_char_p('2'), ctrue)
        self.io.PI_SVO(self.id, self.c_char_p('3'), ctrue)
        return None
    # end __init__
    ctypes.c_bool
    def USBgetConnection(self):
        self.io.PI_EnumerateUSB(self.string_buffer, ctypes.c_int(1200), ctypes.c_char_p('E-712'))
        self.device = self.string_buffer
        return None

    def USBopenConnection(self):
        self.id = self.io.PI_ConnectUSB(self.device)
    
    def USBcloseConnection(self):
        self.io.PI_CloseConnection(self.id)
        return None
    
    def TCPIPopenConnection(self):
        self.id = self.io.PI_ConnectTCPIP(ctypes.c_char_p('192.168.168.10'), ctypes.c_int(50000))
        return None
    def qPos(self, silent= True):
        self.retval = (ctypes.c_double * 3)()
        self.io.PI_qPOS(self.id, ctypes.c_char_p(''), self.retval)
        if not silent:
            print('x = %07.4f\ty = %07.4f\tz = %07.4f' %(self.retval[0], self.retval[1], self.retval[2]))
        return self.retval
        
    def Mov(self, axis, value):
        tmp = (ctypes.c_double*1)(value)
        self.io.PI_MOV(self.id, ctypes.c_char_p(str(axis)), tmp)
        time.sleep(0.1)
    def Exit(self):
        
        self.io.PI_CloseConnection(self.id)
        
    def GetError(self):
        tmp = self.io.PI_GetError(self.id)
        print('Error: ', tmp)
