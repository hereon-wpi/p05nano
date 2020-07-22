import PyTango
import time
import p05.tools.misc as misc
import p05.devices as dev
import numpy
import getpass
import os
import sys
import pickle

class NanoPositions():
    def __init__(self, sampleOutDist = 0.2, writePosLog = True):
        self.__pmac = dev.PMACdict()

        self.__SM = numpy.zeros(6, dtype = object)
        self.__SM[0] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha6') #
        self.__SM[1] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha7') #
        self.__SM[2] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha9') #
        self.__SM[3] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha10') #
        self.__SM[4] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha4') # BS x
        self.__SM[5] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha5') # BS Z


        self.__SM_h = numpy.zeros(9, dtype = object)
        self.__SM_h[0] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha12') # xr
        self.__SM_h[1] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha0') # xl
        self.__SM_h[2] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha1') # zt
        self.__SM_h[3] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha13') # zb
        self.__SM_h[4] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha3') # Teil

        self.__SM_h[5] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.04') #  JJ xr
        self.__SM_h[6] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.03') # JJ xl
        self.__SM_h[7] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.01') # JJ zt
        self.__SM_h[8] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.02') # JJ zb



        #Optics working position
        self.__wp_ok = False
        self.__wp_pos = {}
        self.__wp_pos_h = {}
        #Optics alignment position
        self.__ap_ok = False
        self.__ap_pos = {}
        self.__ap_pos_h = {}
        #Sample rotation center
        self.__rc_ok = False
        self.writePosLog = writePosLog
        try:
            self.__sampleOutDist = float(sampleOutDist)
        except:
            print misc.GetShortTimeString() + ': Warning - could not convert sampleOutDist = %s to a number.' %sampleOutDist
            self.__sampleOutDist = 0.2
        
        self.__currDir = os.path.dirname(__file__).replace('\\', '/')
        if os.path.exists(self.__currDir + os.sep + 'nanoPositioning.log'):
            self.__fLogStr = """open(self.__currDir + os.sep + 'nanoPositioning.log', 'a')"""
        else:
            self.__fLogStr = """open(self.__currDir + os.sep + 'nanoPositioning.log', 'w')"""
    
    # Delete after Nanograinmapping Experiment!
            
#         self.__SP = numpy.zeros(6, dtype = object)
#         self.__SP[0] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano_01.01')
#         self.__SP[1] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano_01.02')
#         self.__SP[2] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano_01.03')
#         self.__SP[3] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano_01.04')
#         self.__SP[4] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano_01.05')
#         self.__SP[5] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano_01.06')
#         
#         self.__rotStage = PyTango.DeviceProxy('//haspp03nano:10000/p03nano/labmotion/exp.01')    
#         
    # Delete end
    
        return None
    #end __init__
    
    def SetWorkingPos_h(self,mode="TXM"):
        sys.stdout.write(misc.GetShortTimeString() + ': Do you really want to replace the working position with the current values? [Yes, no]: ')
        sys.stdout.flush()
        tmp = sys.stdin.readline()[:-1]
        if tmp not in ['yes', 'Y', 'y', 'Yes']:
            print('Aborting...')
            return None
        pw = getpass.getpass('Please confirm with command password: ')
        if pw != 'HejSchnupsi':
            print('Wrong password. Aborting...')
            return None
        #self.__wp_pos['SF1_x'] = self.__pmac.ReadMotorPos('OpticsSF1_x')
        #self.__wp_pos['BStop'] = self.__pmac.ReadMotorPos('Aperture_z')
        self.__wp_pos_h['SM_xr'] = self.__SM_h[0].read_attribute('Position').value
        self.__wp_pos_h['SM_xl'] = self.__SM_h[1].read_attribute('Position').value
        self.__wp_pos_h['SM_zt'] = self.__SM_h[2].read_attribute('Position').value
        self.__wp_pos_h['SM_zb'] = self.__SM_h[3].read_attribute('Position').value
        self.__wp_pos_h['Teil'] = self.__SM_h[4].read_attribute('Position').value
        self.__wp_pos_h['JJ_xr'] = self.__SM_h[5].read_attribute('Position').value
        self.__wp_pos_h['JJ_xl'] = self.__SM_h[6].read_attribute('Position').value
        self.__wp_pos_h['JJ_zt'] = self.__SM_h[7].read_attribute('Position').value
        self.__wp_pos_h['JJ_zb'] = self.__SM_h[8].read_attribute('Position').value
        self.__wp_ok = True
        try:
            with eval(self.__fLogStr) as fLog:
                fLog.write(misc.GetShortTimeString() + ': New Working Pos:\nSM_xr = %e\nSM_xl = %e\nSM_zt = %e\nSM_zb = %e\nTeil = %e\nJJ_xr = %e\nJJ_xl = %e\nJJ_zt = %e\nJJ_zb = %e\n\n' \
                            %(self.__wp_pos_h['SM_xr'], self.__wp_pos_h['SM_xl'],self.__wp_pos_h['SM_zt'], self.__wp_pos_h['SM_zb'],self.__wp_pos_h['Teil'],self.__wp_pos_h['JJ_xr'], self.__wp_pos_h['JJ_xl'],self.__wp_pos_h['JJ_zt'], self.__wp_pos_h['JJ_zb']))
        except:
            pass
        if self.__ap_ok and self.__wp_ok and self.__rc_ok and self.writePosLog:
            self.WritePosToIni()
        print misc.GetShortTimeString() + ': Successfully set new working position.'
        return None
    #end SetWorkingPos

    def SetWorkingPos(self):
        sys.stdout.write(misc.GetShortTimeString() + ': Do you really want to replace the working position with the current values? [Yes, no]: ')
        sys.stdout.flush()
        tmp = sys.stdin.readline()[:-1]
        if tmp not in ['yes', 'Y', 'y', 'Yes']:
            print('Aborting...')
            return None
        pw = getpass.getpass('Please confirm with command password: ')
        if pw != 'HejSchnupsi':
            print('Wrong password. Aborting...')
            return None
        #self.__wp_pos['SF1_x'] = self.__pmac.ReadMotorPos('OpticsSF1_x')
        #self.__wp_pos['BStop'] = self.__pmac.ReadMotorPos('Aperture_z')
        self.__wp_pos['SM_xr'] = self.__SM[2].read_attribute('Position').value
        self.__wp_pos['SM_xl'] = self.__SM[0].read_attribute('Position').value
        self.__wp_pos['SM_zt'] = self.__SM[1].read_attribute('Position').value
        self.__wp_pos['SM_zb'] = self.__SM[3].read_attribute('Position').value
        self.__wp_pos['BStop_x'] = self.__SM[4].read_attribute('Position').value
        self.__wp_pos['BStop_z'] = self.__SM[5].read_attribute('Position').value
        self.__wp_ok = True
        try:
            with eval(self.__fLogStr) as fLog:
                fLog.write(misc.GetShortTimeString() + ': New Working Pos:\nOpticsSFx = %e\nSM cha. 0 = %e\nSM cha. 1 = %e\nSM cha. 3 = %e\nSM cha. 4 = %e\n\n' \
                            %(self.__wp_pos['SF1_x'], self.__wp_pos['SM_xl'],self.__wp_pos['SM_zt'], self.__wp_pos['SM_xr'], self.__wp_pos['SM_zb']))
        except:
            pass
        if self.__ap_ok and self.__wp_ok and self.__rc_ok and self.writePosLog:
            self.WritePosToIni()
        print misc.GetShortTimeString() + ': Successfully set new working position.'
        return None
    #end SetWorkingPos
    
    def SaveWorkingPos(self,path,mode='TXM'):
        timestr = time.strftime("%Y%m%d-%H%M")
        if mode == 'TXM':
            workingPos = self.__wp_pos
            f = open(path+'\working_pos_TXM_'+ timestr +'.txt','w')
        elif mode =='holo':
            workingPos = self.__wp_pos_h
            f = open(path+'\working_pos_holo_'+ timestr +'.txt','w')
        f.write(str(workingPos))
        f.close()
        
    def LoadWorkingPos(self,filename,mode='TXM'):
        if mode == 'TXM':
            substring = 'working_pos_TXM'
            self.__wp_ok = True
            if substring in filename:
                f = open(filename,'r')
                data=f.read()
                f.close()
                self.__wp_pos = eval(data)
            else:
                print ('Warning! Wrong File! Please choose Working Position File.')
        if mode == 'holo':
            substring = 'working_pos_holo'
            self.__wp_ok = True
            if substring in filename:
                f = open(filename,'r')
                data=f.read()
                f.close()
                self.__wp_pos_h = eval(data)
            else:
                print ('Warning! Wrong File! Please choose Working Position File.')
        return None


    def SetAlignmentPos_h(self):
        sys.stdout.write(misc.GetShortTimeString() + ': Do you really want to replace the sample installation position with the current values? [Yes, no]: ')
        sys.stdout.flush()
        tmp = sys.stdin.readline()[:-1]
        if tmp not in ['yes', 'Y', 'y', 'Yes']:
            print('Aborting...')
            return None
        pw = getpass.getpass('Please confirm with command password: ')
        if pw != 'HejSchnupsi':
            print('Wrong password. Aborting...')
            return None
        #self.__ap_pos['SF1_x'] = self.__pmac.ReadMotorPos('OpticsSF1_x')
        self.__ap_pos_h['SM_xr'] = self.__SM_h[0].read_attribute('Position').value
        self.__ap_pos_h['SM_xl'] = self.__SM_h[1].read_attribute('Position').value
        self.__ap_pos_h['SM_zt'] = self.__SM_h[2].read_attribute('Position').value
        self.__ap_pos_h['SM_zb'] = self.__SM_h[3].read_attribute('Position').value
        self.__ap_pos_h['Teil'] = self.__SM_h[4].read_attribute('Position').value
        self.__ap_pos_h['JJ_xr'] = self.__SM_h[5].read_attribute('Position').value
        self.__ap_pos_h['JJ_xl'] = self.__SM_h[6].read_attribute('Position').value
        self.__ap_pos_h['JJ_zt'] = self.__SM_h[7].read_attribute('Position').value
        self.__ap_pos_h['JJ_zb'] = self.__SM_h[8].read_attribute('Position').value

        self.__ap_ok = True
        try:
            with eval(self.__fLogStr) as fLog:
                fLog.write(misc.GetShortTimeString() + ': New Alignment Pos:\nSM_xr = %e\nSM_xl = %e\nSM_zt = %e\nSM_zb = %e\nTeil = %e\nJJ_xr = %e\nJJ_xl = %e\nJJ_zt = %e\nJJ_zb = %e\n\n' \
                            %(self.__ap_pos_h['SM_xr'], self.__ap_pos_h['SM_xl'],self.__ap_pos_h['SM_zt'], self.__ap_pos_h['SM_zb'],self.__ap_pos_h['Teil'],self.__wp_pos_h['JJ_xr'], self.__wp_pos_h['JJ_xl'],self.__wp_pos_h['JJ_zt'], self.__wp_pos_h['JJ_zb']))
        except:
            pass
        if self.__ap_ok and self.__wp_ok and self.__rc_ok and self.writePosLog:
            self.WritePosToIni()
        print misc.GetShortTimeString() + ': Successfully set new installation position.'
        return None
    #end SetAlignmentPos

    def SetAlignmentPos(self):
        sys.stdout.write(misc.GetShortTimeString() + ': Do you really want to replace the sample installation position with the current values? [Yes, no]: ')
        sys.stdout.flush()
        tmp = sys.stdin.readline()[:-1]
        if tmp not in ['yes', 'Y', 'y', 'Yes']:
            print('Aborting...')
            return None
        pw = getpass.getpass('Please confirm with command password: ')
        if pw != 'HejSchnupsi':
            print('Wrong password. Aborting...')
            return None
        #self.__ap_pos['SF1_x'] = self.__pmac.ReadMotorPos('OpticsSF1_x')

        self.__ap_pos['BStop_x'] = self.__SM[4].read_attribute('Position').value
        self.__ap_pos['BStop_z'] = self.__SM[5].read_attribute('Position').value
        #self.__ap_pos['BStop'] = self.__pmac.ReadMotorPos('Aperture_z') Old BS 
        self.__ap_pos['SM_xr'] = self.__SM[2].read_attribute('Position').value
        self.__ap_pos['SM_xl'] = self.__SM[0].read_attribute('Position').value
        self.__ap_pos['SM_zt'] = self.__SM[1].read_attribute('Position').value
        self.__ap_pos['SM_zb'] = self.__SM[3].read_attribute('Position').value
        self.__ap_ok = True
        try:
            with eval(self.__fLogStr) as fLog:
                fLog.write(misc.GetShortTimeString() + ': New Alignment Pos:\nOpticsSFx = %e\nSM cha. 0 = %e\nSM cha. 1 = %e\nSM cha. 3 = %e\nSM cha. 4 = %e\n\n' \
                            %(self.__wp_pos['SF1_x'], self.__wp_pos['SM_xl'],self.__wp_pos['SM_zt'], self.__wp_pos['SM_xr'], self.__wp_pos['SM_zb']))
        except:
            pass
        if self.__ap_ok and self.__wp_ok and self.__rc_ok and self.writePosLog:
            self.WritePosToIni()
        print misc.GetShortTimeString() + ': Successfully set new installation position.'
        return None
    #end SetAlignmentPos
    
    
    def SaveAlignmentPos(self,path,mode="TXM"):
        timestr = time.strftime("%Y%m%d-%H%M")
        if mode == 'TXM':
            aligmentPos = self.__ap_pos
            f = open(path+'\lignment_pos_TXM_'+ timestr +'.txt','w')
        elif mode =='holo':
            aligmentPos = self.__ap_pos_h
            f = open(path+'\lignment_pos_holo_'+ timestr +'.txt','w')
        f.write(str(aligmentPos))
        f.close()
        return None
        
    def LoadAlignmentPos(self,filename,mode="TXM"):
        self.__ap_ok = True
        if mode == "TXM":
            substring = 'lignment_pos_TXM'
            if substring in filename:
                f = open(filename,'r')
                data=f.read()
                f.close()
                self.__ap_pos = eval(data)
            else:
                print ('Warning! Wrong File! Please choose Alignment Position File.')
        elif mode =="holo":
            substring = 'lignment_pos_holo'
            if substring in filename:
                f = open(filename,'r')
                data=f.read()
                f.close()
                self.__ap_pos_h = eval(data)
            else:
                print ('Warning! Wrong File! Please choose Alignment Position File.')
        return None

    def SetRotationCenter(self):
        sys.stdout.write(misc.GetShortTimeString() + ': Do you really want to replace the rotation center with the current position? [Yes, no]: ')
        sys.stdout.flush()
        tmp = sys.stdin.readline()[:-1]
        if tmp not in ['yes', 'Y', 'y', 'Yes']:
            print('Aborting...')
            return None
        pw = getpass.getpass('Please confirm with command password: ')
        if pw != 'HejSchnupsi':
            print('Wrong password. Aborting...')
            return None
        self.__pos_sin = self.__pmac.ReadMotorPos('SampleStage_x')
        self.__rc_ok = True
        try:
            with eval(self.__fLogStr) as fLog:
                fLog.write(misc.GetShortTimeString() + ': New Rotation Center:\nSampleStage_x= %e\n\n' %(self.__pos_sin))
        except:
            pass
        if self.__ap_ok and self.__wp_ok and self.__rc_ok and self.writePosLog:
            self.WritePosToIni()
        print misc.GetShortTimeString() + ': Successfully set new rotation center.'
        return None
    #end SetRotationCenter
        
    def GotoWorkingPos(self,mode= "TXM"):
        if self.__wp_ok == False:
            print misc.GetShortTimeString() + ': Warning - working position not set! Aborting ...'
            return None
        sys.stdout.write(misc.GetShortTimeString() + ': Do you want to move the setup to the working position? [Yes, no]: ')
        sys.stdout.flush()
        tmp = sys.stdin.readline()[:-1]
        if tmp not in ['yes', 'Y', 'y', 'Yes']:
            print('Aborting...')
            return None
        if mode == "TXM":
            self.__SM[0].write_attribute('Position', self.__wp_pos['SM_xl'])
            time.sleep(1)
            self.__SM[1].write_attribute('Position', self.__wp_pos['SM_zt'])
            time.sleep(1)
            self.__SM[2].write_attribute('Position', self.__wp_pos['SM_xr'])
            time.sleep(1)
            self.__SM[3].write_attribute('Position', self.__wp_pos['SM_zb'])
            time.sleep(1)
            self.__SM[4].write_attribute('Position', self.__wp_pos['BStop_x'])
            time.sleep(1)
            self.__SM[5].write_attribute('Position', self.__wp_pos['BStop_z'])
        elif mode == "holo":
            self.__SM_h[0].write_attribute('Position', self.__wp_pos_h['SM_xr'])
            time.sleep(1)
            self.__SM_h[1].write_attribute('Position', self.__wp_pos_h['SM_xl'])
            time.sleep(1)
            self.__SM_h[2].write_attribute('Position', self.__wp_pos_h['SM_zt'])
            time.sleep(1)
            self.__SM_h[3].write_attribute('Position', self.__wp_pos_h['SM_zb'])
            time.sleep(1)
            self.__SM_h[4].write_attribute('Position', self.__wp_pos_h['Teil'])
            time.sleep(1)
            self.__SM_h[5].write_attribute('Position', self.__wp_pos_h['JJ_xr'])
            time.sleep(1)
            self.__SM_h[6].write_attribute('Position', self.__wp_pos_h['JJ_xl'])
            time.sleep(1)
            self.__SM_h[7].write_attribute('Position', self.__wp_pos_h['JJ_zt'])
            time.sleep(1)
            self.__SM_h[8].write_attribute('Position', self.__wp_pos_h['JJ_zb'])

        print misc.GetShortTimeString() + ': Successfully moved to working position.'
        return None
    #end GotoWorkingPos

    def GotoAlignmentPos(self, mode ="TXM"):
        if self.__ap_ok == False:
            print misc.GetShortTimeString() + ': Warning - alignment position not set! Aborting ...'
            return None
        sys.stdout.write(misc.GetShortTimeString() + ': Do you want to move the setup to the alignment position? [Yes, no]: ')
        sys.stdout.flush()
        tmp = sys.stdin.readline()[:-1]
        if tmp not in ['yes', 'Y', 'y', 'Yes']:
            print('Aborting...')
            return None
        if mode == "TXM":
            self.__SM[0].write_attribute('Position', self.__ap_pos['SM_xl'])
            time.sleep(1)
            self.__SM[1].write_attribute('Position', self.__ap_pos['SM_zt'])
            time.sleep(1)
            self.__SM[2].write_attribute('Position', self.__ap_pos['SM_xr'])
            time.sleep(1)
            self.__SM[3].write_attribute('Position', self.__ap_pos['SM_zb'])
            time.sleep(1)
            self.__SM[4].write_attribute('Position', self.__ap_pos['BStop_x'])
            time.sleep(1)
            self.__SM[5].write_attribute('Position', self.__ap_pos['BStop_z'])
        elif mode == "holo":
            self.__SM_h[0].write_attribute('Position', self.__ap_pos_h['SM_xr'])
            time.sleep(1)
            self.__SM_h[1].write_attribute('Position', self.__ap_pos_h['SM_xl'])
            time.sleep(1)
            self.__SM_h[2].write_attribute('Position', self.__ap_pos_h['SM_zt'])
            time.sleep(1)
            self.__SM_h[3].write_attribute('Position', self.__ap_pos_h['SM_zb'])
            time.sleep(1)
            self.__SM_h[4].write_attribute('Position', self.__ap_pos_h['Teil'])
            time.sleep(1)
            self.__SM_h[5].write_attribute('Position', self.__ap_pos_h['JJ_xr'])
            time.sleep(1)
            self.__SM_h[6].write_attribute('Position', self.__ap_pos_h['JJ_xl'])
            time.sleep(1)
            self.__SM_h[7].write_attribute('Position', self.__ap_pos_h['JJ_zt'])
            time.sleep(1)
            self.__SM_h[8].write_attribute('Position', self.__ap_pos_h['JJ_zb'])


        print misc.GetShortTimeString() + ': Successfully moved to alignment position.'
        return None
    #end GotoAlignmentPos
        
    def SampleIn(self):
        if not self.__rc_ok:
            print misc.GetShortTimeString() + ': Warning - rotation center not set! Aborting ...'
            return None
        self.__pmac.Move('SampleStage_x', self.__pos_sin)
        print misc.GetShortTimeString() + ': Successfully moved the sample in the beam.'
        return None
    #end SampleIn
    
    def SampleOut(self):
        if not self.__rc_ok:
            print misc.GetShortTimeString() + ': Warning - rotation center not set! Aborting ...'
            return None
        self.__pmac.Move('SampleStage_x', self.__pos_sin + self.__sampleOutDist)
        print misc.GetShortTimeString() + ': Successfully moved the sample out of the beam.'
        return None
    #end SampleOut
    
    def GotoRot(self, value):
        if not (-180 <= value <= 180):
            print misc.GetShortTimeString() + ': Warning - requested rotation position outside allowed limits.\nAborting...'
            return None
        self.__pmac.Move('Sample_Rot', value)
        print misc.GetShortTimeString() + ': Rotation finished.'
        return None
    #end GotoRot

    def MvrRot(self, value):
        tmp = self.__pmac.ReadMotorPos('Sample_Rot')
        if not (-180 <= tmp + value <= 180):
            print misc.GetShortTimeString() + ': Warning - requested rotation position outside allowed limits.\nAborting...'
            return None
        self.__pmac.MoveRel('Sample_Rot', value)
        print misc.GetShortTimeString() + ': Rotation finished.'
        return None
    #end MvrRot
        
    def MvrSampleX(self, value): 
        if abs(value) > 0.5:
            print misc.GetShortTimeString() + ': Warning - large movement request will be ignored. (Delta max 0.5)'
            return None 
        self.__pmac.SampleSF_mvrX(value)
        print misc.GetShortTimeString() + ': Move finished.'
        return None
    #end MvrSampleX

    def MvrSampleY(self, value): 
        if abs(value) > 2:
            print misc.GetShortTimeString() + ': Warning - large movement request will be ignored. (Delta max 0.5)'
            return None 
        self.__pmac.SampleSF_mvrY(value)
        print misc.GetShortTimeString() + ': Move finished.'
        return None
    #end MvrSampleY

    def MvrSampleZ(self, value): 
        if abs(value) > 0.5:
            print misc.GetShortTimeString() + ': Warning - large movement request will be ignored. (Delta max 0.5)'
            return None 
        self.__pmac.MoveRel('Sample_z', value)
        print misc.GetShortTimeString() + ': Move finished.'
        return None
    #end MvrSampleZ

    def MvrSampleStageZ(self, value): 
        if abs(value) > 0.5:
            print misc.GetShortTimeString() + ': Warning - large movement request will be ignored. (Delta max 0.5)'
            return None 
        self.__pmac.MoveRel('SampleStage_z', value)
        print misc.GetShortTimeString() + ': Move finished.'
        return None
    #end MvrSampleZ

    def ReadPosFromIni(self):
        sys.stdout.write(misc.GetShortTimeString() + ': Do you really want to read all positions from file? [Yes, no]: ')
        sys.stdout.flush()
        tmp = sys.stdin.readline()[:-1]
        if tmp not in ['yes', 'Y', 'y', 'Yes']:
            print('Aborting...')
            return None
        pw = getpass.getpass('Please confirm with command password: ')
        if pw != 'Affendressur':
            print('Wrong password. Aborting...')
            return None
        try:
            with open(self.__currDir + os.sep + 'nanoPositioning.ini', 'r') as f:
                tmp = pickle.load(f)
            self.__pos_sin = tmp[0]
            self.__ap_pos = tmp[1]
            self.__wp_pos = tmp[2]
            self.__ap_ok = True
            self.__wp_ok = True
            self.__rc_ok = True
        except:
            print misc.GetShortTimeString() + ': Error reading ini file.'
            self.__ap_ok = False
            self.__wp_ok = False
            self.__rc_ok = False
        #self.__config_data.read()
        return None
    #end ReadPosFromIni

    def WritePosToIni(self):
        if self.__ap_ok and self.__wp_ok and self.__rc_ok:
            with open(self.__currDir + os.sep + 'nanoPositioning.ini', 'w') as f:
                pickle.dump([self.__pos_sin, self.__ap_pos, self.__wp_pos], f)
        else:
            print misc.GetShortTimeString() + ': Warning - Not all values are set! Aborting ...'
            return None
        return None

    def SetSampleOutDist(self, value):
        try:
            self.__sampleOutDist = value
            with eval(self.__fLogStr) as fLog:
                fLog.write(misc.GetShortTimeString() + ': New sample out dist:\nSampleOut = %e\n' %(self.__sampleOutDist))
        except:
            print misc.GetShortTimeString() + ': Warning - could not convert sampleOutDist = %s to a number.' %value
            self.__sampleOutDist = 0.2

    def ShowPositions(self):
        print misc.GetShortTimeString() + ': Currently saved position values:'
        print '\nAlignment Pos:\nOpticsSFx = %e\nSM cha. 0 = %e\nSM cha. 1 = %e\nSM cha. 3 = %e\nSM cha. 4 = %e\n' \
                            %(self.__wp_pos['SF1_x'], self.__wp_pos['SM_xl'],self.__wp_pos['SM_zt'], self.__wp_pos['SM_xr'], self.__wp_pos['SM_zb'])
        print 'Working Pos:\nOpticsSFx = %e\nSM cha. 0 = %e\nSM cha. 1 = %e\nSM cha. 3 = %e\nSM cha. 4 = %e\n' \
                            %(self.__wp_pos['SF1_x'], self.__wp_pos['SM_xl'],self.__wp_pos['SM_zt'], self.__wp_pos['SM_xr'], self.__wp_pos['SM_zb'])
        print 'Rotation center:\nSampleStage_x= %e\n' %(self.__pos_sin)
        
    # Delete after NGM Experiment    
    def MvrSampleX_NGM(self, value):
        __delta = float(value)
        __currentx = self.__SP[0].read_attribute('Position').value
        print __currentx
        __currenty = self.__SP[1].read_attribute('Position').value
        print __currenty
        __currentRot = self.__rotStage.read_attribute('Position').value
        print __currentRot
        #__currentRot += 180
        print __currentRot
        __valx = __currentx + numpy.cos(__currentRot * numpy.pi / 180) * __delta
        __valy = __currenty + numpy.sin(__currentRot * numpy.pi / 180) * __delta
        print __valx
        print __valy
        self.__SP[0].write_attribute('Position',__valx)
        #print self.__SP[0].read_attribute('State')
        #while self.__SP[0].read_attribute('State').value == 'MOVING':
        time.sleep(1)
        self.__SP[1].write_attribute('Position',__valy)
        
    #Delete end
            


             
if __name__ == '__main__':
    test = NanoPositions()