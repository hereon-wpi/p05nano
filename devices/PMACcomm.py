'''
Created on 06.03.2012

@author: ogurreck
'''
import ctypes

import p05.tools.misc as misc


#import numpy
#import time
#import string

class PMACcomm():
    """
    Class to manage the connection to the PMAC controller using
    the dll interface. To be used with DeltaTau drivers version 4.0 
    or higher.
    """
    def __init__(self, controller=0, silentmode=False, ioconsole = True):
        """
        Method to initialize the connection to the controllers
        calling parameters:
            - controller = <n>    with n= 1..6
            - silentmode = True / False
                with silentmode = True, no output will be printed on screen.
        
        Function overview of the controllers:
        Controller 1: In-Vacuum SpaceFab and pushers for photodiodes
        Controller 2: In-Vacuum long translation
        Controller 3: Granite sliders and aperture x/y/z stage
        Controller 4: Optics SpaceFab and pushers for photodiodes
        Controller 5: Tip/tilt pods and x-translation for rotational axis, 
                        rotational axis and detector x/z stage
        Controller 6: Sample SpaceFab
        """
        self.ControllerList = \
                 {1: [1, '192.168.10.3', 'Controller 1', 'In-Vacuum SpaceFab and pushers for photodiodes'], \
                  2: [2, '192.168.10.4', 'Controller 2', 'In-Vacuum long translation'], \
                  3: [3, '192.168.10.5', 'Controller 3', 'Granite sliders and aperture x/y/z stage'], \
                  4: [4, '192.168.10.6', 'Controller 4', 'Optics SpaceFab and pushers for photodiodes'], \
                  5: [5, '192.168.10.7', 'Controller 5', 'Tip/tilt pods and x-translation for\nrotational axis, rotational axis and detector x/z stage'], \
                  6: [6, '192.168.10.8', 'Controller 6', 'Sample SpaceFab'], \
                  7: [7, '192.168.10.9', 'Controller 7', 'Optics SpaceFab (slider 1)']
                  #  7: [7, '192.168.10.9', 'Controller 7', 'Optics SpaceFab (slider 1)']
                  }

        self.error = False
        self.connection_active = False
        self.ioconsole = ioconsole
        self.string_buffer = ctypes.create_string_buffer(600)
        #check and set silentmode parameter
        if silentmode not in [True, False]:
            self.silentmode = False
        else: 
            self.silentmode = silentmode
        # check and set controller number:
        if controller not in [1, 2, 3, 4, 5, 6, 7]:
            if self.ioconsole and not self.silentmode: print(misc.GetTimeString() + ': Error. Please choose a controller from 1 to 6')
            self.error = True
        else:
            self.pmac_num = self.ControllerList.get(controller)[0]
            self.pmac_ip =  self.ControllerList.get(controller)[1]
            self.io = ctypes.windll.LoadLibrary('PComm32W.dll')
            tmp = self.io.OpenPmacDevice(self.pmac_num)
            if tmp != 0:
                self.io.PmacGetVariableDouble.restype = ctypes.c_double
                self.connection_active = True
            else:
                self.error = True
        if self.error == False and not (self.silentmode):
            if self.ioconsole and not self.silentmode: 
                print(misc.GetTimeString() + ': Successfully established connection to PMAC Nr. %i.' %controller)
        
        return None
    # end __init__
    
    def GetVarValue(self, variable, valreturn = False, silent = False):
        """
        Method to read a variable value (number) from a PMAC.
        Variable has to consist of variable type representing char M, P, I, or Q
        and the variable number.
        
        Example:
        GetVarValue('Q1234')
        GetVarValue('p80')
        """
        if self.connection_active:
            self.var_value = None
            self.var_name = None
            self.var_syntaxerror = False
            _type = variable[0].upper()
            if _type not in ['Q', 'I', 'M', 'P']:
                self.var_syntaxerror = True
                if not self.silentmode and self.ioconsole:
                    print(misc.GetTimeString() + ': Error. the specified variable \'%s\' is unknown.' %variable)
                    return None
            try:
                count = int(variable[1:])
            except:
                self.var_syntaxerror = True
                print(misc.GetTimeString() + ': Error. the specified variable \'%s\' is unknown.' %variable)
                return None
            if not self.var_syntaxerror:
                tmp = self.io.PmacGetVariableDouble(self.pmac_num, ctypes.c_char(_type), ctypes.c_uint(count), ctypes.c_double(-12345))
                if tmp != -12345:
                    self.var_value = tmp
                    self.var_name = variable.upper()
                    if not (silent or self.silentmode) and self.ioconsole: 
                        print('%s = %f' %(variable, tmp))
                    
                    if not valreturn:  
                        return None
                    else:
                        return self.var_value
                else:
                    self.var_syntaxerror = True
                    if not (silent or self.silentmode) and self.ioconsole:
                        print(misc.GetTimeString() + ': Error. the specified variable \'%s\' is unknown.' %variable)
            return None
    #end GetVarValue
            
    def ReadVariable(self, variable, valreturn = True):
        """
        Method to read a variable value (number) from a PMAC.
        Variable has to consist of variable type representing char M, P, I, or Q
        and the variable number.
        
        Example:
        ReadVariable('Q1234')
        ReadVariable('p80')
        """
        if self.connection_active:
            self.var_value = None
            self.var_name = None
            _type = variable[0].upper()
            tmp = self.io.PmacGetVariableDouble(self.pmac_num, ctypes.c_char(variable[0].upper()), ctypes.c_uint(int(variable[1:])), ctypes.c_double(-12345))
            if tmp != -12345:
                self.var_value = tmp
                self.var_name = variable.upper()
                return self.var_value
    #end ReadVariable
    
    def CloseConnection(self):
        """
        Method to close the connection to the PMAC controller.
        """
        self.io.ClosePmacDevice(self.pmac_num)
        self.connection_active = False
    #end CloseConnection

    def OpenConnection(self, silent = False):
        """
        Method to close the connection to the PMAC controller.
        """
        if self.connection_active and not (self.silentmode):
            print(misc.GetTimeString() + ': Warning. Connection to PMAC already active. Request ignored' )
        if self.connection_active == False:
            tmp = self.io.OpenPmacDevice(self.pmac_num)
            if tmp != 0:
                self.io.PmacGetVariableDouble.restype = ctypes.c_double
                self.connection_active = True
            else:
                self.error = True
            if self.error == False and self.ioconsole and not self.silentmode: \
                print(misc.GetTimeString() + ': Successfully established connection to PMAC.')
        return None
    #end OpenConnection

    def IsReady(self):
        """
        Method to poll if the controller is ready for movement orders.
        """
        if self.connection_active:
            try:
                tmp = self.GetResponse('cpu', silent = True)
                if tmp != '':
                    return True
            except:
                return False
        return False
    #end IsReady
    
    def WriteVariable(self, var, value):
        """
        Method to write a variable. 
        
        Usage example:
        WriteVariable('q123', '12')
        """
        self.string_buffer.value = ''
        instruction = '%s = %s' %(var, value)
        tmp = self.io.PmacGetResponseExA(self.pmac_num, self.string_buffer, ctypes.c_uint(600), ctypes.c_char_p(instruction))
        return None
    #end WriteVariable
            
    def GetResponse(self, instruction, silent = False):
        """
        Method to get a response from the PMAC
        """
        if self.connection_active:
            self.string_buffer.value = ''
            tmp = self.io.PmacGetResponseExA(self.pmac_num, self.string_buffer, ctypes.c_uint(600), ctypes.c_char_p(instruction))
            if self.silentmode or silent:
                return self.string_buffer.value
            else:
                print('Query: %s' %instruction)
                print('Response: %s' %self.string_buffer.value)
        else:
            if self.ioconsole and not self.silentmode:
                print(misc.GetTimeString() + ': Warning. Connection to PMAC not active. Request ignored.')
        return None
    #end GetResponse

if __name__ == '__main__':
    #tmp = PMACcontrol()
    print('Compiled successfully')
    
