import serial
from numpy import r_
import time

class JenaPiezoComm():
    """
    Class to manage the connection with the Jena d-Drive
    piezo controller using the virtual serial interface.
    """
    def __init__(self, port='COM3'):
        self.connect_error = False
        self.channels = {'X1':0, 'Y1':1, 'X2':2, 'Y2':3}
        try:
            self.connector = serial.Serial(port=port, \
                                baudrate=115200, \
                                bytesize=serial.EIGHTBITS, \
                                parity=serial.PARITY_NONE, \
                                stopbits=serial.STOPBITS_ONE, \
                                timeout=0.05, \
                                xonxoff=True)
        except:
            print('Error. Connection could not be established')
            self.connect_error = True
        
        #if not self.connect_error:
            #self.SetCL()
        return None
    #end __init__
    
    def GetPositions(self, silent = False):
        """Method to poll all for actuator positions."""
        tmp = self.SendCommand('mess', silent=True)
        if tmp == '-1':
            if silent:
                return r_[NaN, NaN, NaN, NaN]
            else:
                print('Current positions:\nx1 = NaN\nx2 = NaN\ny1 = NaN'\
                      +'\ny2 = NaN')
                return None
        else:
            val = r_[0.,0.,0.,0.]
            tmp = tmp.split()
            for i in xrange(4):
                tmp2 = (tmp[i].split(','))[2]
                val[i] = float(tmp2)
            if silent: 
                return val
            else:
                print('Current positions:\nx1 = %7.3f' %val[0]\
                      +'\nx2 = %7.3f\ny1 = %7.3f'%(val[2],val[1])\
                      +'\ny2 = %7.3f' %val[3])
                return None
    #end GetPositions
    
    def SetCL(self):
        """Method to set all Piezos in closed loop mode."""
        tmp = self.SendCommand('stat', silent = True)
        tmp = tmp.split()
        for i in xrange(4):
            tmp2 = (tmp[i].split(','))[2]
            tmp2 = bin(int(tmp2))
            cl_active = False
            if len(tmp2) >= 10:
                if tmp2[9] == '1':
                    cl_active = True
            if not cl_active:
                self.SendCommand('cl,%1i,1' %i)
    #end SetCL
    
    def SendCommand(self, command, silent = False):
        """Method to send a command to the piezo controller.""" 
        if self.connector.isOpen():
            tmp = self.connector.inWaiting()
            if tmp > 0: 
                tmp2 = self.connector.read(size=tmp)
            self.connector.write(command+'\r')
            time.sleep(0.05)
            tmp = self.connector.inWaiting()
            answer = self.connector.read(size=tmp)
            if silent == False:
                print(answer)
                return None
            else:
                return answer
        else:
            if silent == False:
                print('Error. Connection not open.')
            return '-1'
    #end SendCommand 
    
    def Status(self):
        if self.connector.isOpen():
            print('Connection status: Established and open.')
        else:
            print('Connection status: No connection')
        tmp = self.SendCommand('stat', silent=True)
        if tmp == '-1':
            print('Piezo x1 status: No information available')
            print('Piezo x2 status: No information available')
            print('Piezo y1 status: No information available')
            print('Piezo y2 status: No information available')
        else:
            tmp = tmp.split()
            tmp_name = ['x1', 'x2', 'y1', 'y2']
            for i in xrange(4):
                print('\nPiezo %s status:' %tmp_name[i])
                tmp2 = (tmp[i].split(','))[2]
                tmp2 = bin(int(tmp2))
                #bit 0:
                if tmp2[2] == '1': print('  actuator active')
                elif tmp2[2] == '0': print('  actuator not connected')
                #bit 1,2
                if tmp2[3:5] == '00': print('  no measurement system available')
                elif tmp2[3:5] == '10': print('  resistance strain gauge measurement system installed')
                elif tmp2[3:5] == '01': print('  capacitive  measurement system installed')
                elif tmp2[3:5] == '11': print('  inductive measurement system installed')
                #bit 4:
                if tmp2[6] == '1': print('  open loop system')
                if tmp2[6] == '0': print('  closed loop available')
                #bit 6:
                if len(tmp2) >= 10:
                    if tmp2[9] == '1': print('  closed loop enabled')
                    elif tmp2[9] == '0': print('  system in open loop')
    #end Status

    def Set(self, name, value):
        """Method to set a postion target for the
        actuator 'name'.
        - name:  name of the 4 axes: X1, X2, Y1, Y2
        - value: float value of the target position
        
        Usage example:
        Set('X1', 12.5)"""
        input_error = False
        name = name.upper()
        try:
            value=float(value)
        except:
            print('Error. Value is not a regular float value.')
            input_error = True
        if name not in ['X1', 'X2', 'Y1', 'Y2']:
            print('Error. Axis name unknown.')
            input_error = True
        if not input_error:
            chan = self.channels.get(name)
            self.SendCommand('set,%1i,%f' %(chan,value), silent=True)
        return None
    #end Set

    def SetAll(self, values, settleTime = None):
        """Method to set all Piezo positions at once. 
        Input:
        Array or list of 4 values, order x1, x2, y1, y2
        """
        try:
            self.Set('x1', values[0])
            self.Set('x2', values[1])
            self.Set('y1', values[2])
            self.Set('y2', values[3])
        except:
            pass
        if settleTime != None:
            time.sleep(settleTime)
        return None

    def Exit(self):
        self.connector.close()
    #end Exit
