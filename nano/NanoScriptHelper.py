import PyTango
import time
import os
import sys
import subprocess
import shutil
import numpy
import string
import copy
from p05.nano.Cameras import PCO_nanoCam, FLIeh2_nanoCam, Hamamatsu_nanoCam, PixelLink_nanoCam, Zyla_nanoCam,KIT_nanoCam
from p05.nano.JJ_slits import JJslits
from p05.scripts.OptimizePitch import OptimizePitchDCM
import p05.tools.misc as misc
import p05.tools
import p05.common.TangoFailsaveComm as tcom
from PIL import Image
#from libtiff import TIFF

class NanoScriptHelper():
    """Class to help scripting for nanotomography measurement.
    Class initialization parameters:
    <pmac>:     PMACdict instance
    <group>:    abbreviation for group name (e.g. 'hzg')
    <beamtime>: name of the current beamtime (e.g. 'nanoXTM_201302')
    <prefix>:   prefix for the scan (logfile and images)
    
    assumptions made in class:
    - usage of EH1 FLI camera
    - usage of hzgpp05ct2 for data storage
    """
    
    def __init__(self, pmac, currScript, group, beamtime, prefix, exptime= None, \
                 useKITcamera = False, KITcameraParameters = None, usePCO = False, useSmarAct = True, \
                 useDiode = False, closeShutter = True, useStatusServer = True, \
                 usePCOcamware = False, useEHD = False, useASAP = True, useASAPcomm = False,\
                 useJenaPiezo = False, DCMdetune = 0.0, useEnviroLog = False, useNGM = False, disableSideBunchReacquisition = True,\
                 useHamamatsu = False,usePixelLink=False, useZyla = False, useKIT = False, useHamaTrigger = False, logRotPos = False):
        """
        Class initialization:
        
        <pmac>:     PMACdict instance
        <group>:    abbreviation for group name (e.g. 'hzg')
        <beamtime>: name of the current beamtime (e.g. 'nanoXTM_201302')
        <prefix>:   prefix for the scan (logfile and images)
        """

        self.sGroup = group
        self.sBeamtime = beamtime
        self.sPrefix = prefix



        if useASAP:
            #self.sPath = 't:/current/scratch_bl/%s/' %(self.sPrefix)
            self.sPath = 't:/current/raw/%s/' %(self.sPrefix)
        elif useASAP == False and useASAPcomm == True:
            self.sPath = 't:/current/scratch_bl/%s/' %(self.sPrefix)
        else:
            #self.sPath = 'd:/%s/%s/%s/' %(self.sGroup, self.sBeamtime, self.sPrefix)
            self.sPath = 'd:/hzg/' + str(beamtime) + '/%s/' %(self.sPrefix)

        if useZyla or useKIT or usePCO:
            if useASAP:
                self.sPath_Cam = '/gpfs/current/raw/%s/' %(self.sPrefix)
            elif useASAP == False and useASAPcomm == True:
                self.sPath_Cam = '/gpfs/current/scratch_bl/%s/' %(self.sPrefix)
            else:
                self.sPath_Cam = '/home/p05user/data/' + str(beamtime) + '/%s/' %(self.sPrefix)

        self.sPathBeamLogs = self.sPath+'beamLogs/'
        self.sLogfile = self.sPath + '%s__LogScan.log' %(self.sPrefix)
        self.sCameraLogfile = self.sPath + '%s__LogCamera.log' %(self.sPrefix)
        self.sMotorLogFile = self.sPath + '%s__LogMotors.log' %(self.sPrefix)
        self.sBeamLogFile = self.sPath + '%s__LogBeam.log' %(self.sPrefix)     
        if not os.path.exists(os.path.split(self.sLogfile)[0]):
            os.makedirs(os.path.split(self.sLogfile)[0])
        shutil.copy2(currScript, self.sPath + '%s__LogScript.py.log' %(self.sPrefix))


        self.starttime = time.time()
        self.exptime = exptime

        #Boolean variables:
        self.useKITcamera = useKITcamera
        self.useKIT = useKIT
        self.useSmarAct = useSmarAct
        self.useJenaPiezo = useJenaPiezo
        self.usePCO = usePCO
        self.usePCOcamware = usePCOcamware
        self.useEHD = useEHD
        self.useStatusServer = useStatusServer
        self.closeShutter = closeShutter
        self.KITcameraParameters = KITcameraParameters
        self.useDiode = useDiode
        self.DCMdetune = DCMdetune
        self.useEnviroLog = useEnviroLog
        self.disableSideBunchReacquisition = disableSideBunchReacquisition 
        self.useHamamatsu = useHamamatsu
        self.useHamaTrigger = useHamaTrigger
        self.usePixelLink = usePixelLink
        self.logRotPos = logRotPos
        self.useZyla = useZyla
        self.useNGM = useNGM
        #########################################
        ######## initialize camera ##############
        #########################################
        self.camera = None
        if self.useEHD:
            self.camera = FLIeh2_nanoCam(imageDir = self.sPath, exptime = self.exptime)


        if self.useHamamatsu:
            self.camera = 'Hamamatsu'
            self.hamamatsu = Hamamatsu_nanoCam(imageDir = self.sPath, exptime = self.exptime)
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out03') #  '//hzgpp05vme1:10000/p05/dac/eh1.02')
            self.tTriggerOut = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.in08')
            #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out01')
            self.currimage = None
            #self.hamamatsu.sendCommand('StartVideoAcq')
            #Hamamatsu_nanoCam(exptime=self.exptime)
            #print('~~~~~~~~~ !!!! ~~~~~~~~~ Attention: Hamamatsu image application running?')
            #tmp = raw_input('~~~~~~~~~ !!!! ~~~~~~~~~ Continue? y / n: ')
            #if tmp not in ['yes', 'Y', 'y']:
                #print('Aborting...')
                #sys.exit()
        if self.useHamaTrigger:
            self.tTrigger =  PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out03')#('//hzgpp05vme1:10000/p05/dac/eh1.01')
            self.tTriggerOut = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.in08')

        if self.usePixelLink:
            self.camera = 'PixelLink'
            self.hamamatsu = PixelLink_nanoCam(imageDir = self.sPath, exptime = 1.0)
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01') #  '//hzgpp05vme1:10000/p05/dac/eh1.02')
            self.currimage = None

        if self.useZyla:
            self.camera = 'Zyla'
            self.hamamatsu = Zyla_nanoCam(imageDir = self.sPath, exptime = self.exptime)
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out03') #  '//hzgpp05vme1:10000/p05/dac/eh1.02')
            #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out01')
            self.currimage = None

        if self.useKIT:
            self.camera = 'KIT'
            self.hamamatsu = KIT_nanoCam(imageDir = self.sPath_Cam, exptime = self.exptime)
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/register/eh1.out01')
            self.currimage = None

        if self.usePCO:
            self.camera = 'PCO'
            self.hamamatsu = PCO_nanoCam(imageDir = self.sPath_Cam, exptime = self.exptime)
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')#  '//hzgpp05vme1:10000/p05/dac/eh1.02')
            #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out01')
            self.currimage = None
        
        # for Hergens rotations stage
        if self.useNGM:
            self.rot_Stage_NGM = PyTango.DeviceProxy('//haspp03nano:10000/p03nano/labmotion/exp.01')
        
        #########################################
        ######## initialize TANGO ###############
        #########################################
        self.tPMAC = pmac
        self.EH1slits = JJslits()
        self.tQBPM = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/i404/exp.02')
        self.tPETRAinfo = PyTango.DeviceProxy('//hzgpp05vme1:10000/PETRA/GLOBALS/keyword')
        self.tPETRAcell4 = PyTango.DeviceProxy('//hzgpp05vme0:10000/PETRA/UNDBPOS/Zelle4')
        self.tPETRAnbCleaning = PyTango.DeviceProxy('//hzgpp05vme1:10000/linac2/umschaltmanager/umschaltmanager')
        self.tBeamShutter = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/shutter/all')
        self.tPitch =  PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/motor/mono.01')
        self.tRoll  =  PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/motor/mono.02')
        self.tUndulator = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/undulator/1')
        self.tScintiY = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.05')
        self.tLensY = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.06')
        self.tCamRot = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.07')
        self.tDCMenergy = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/dcmener/s01.01')
        if self.useStatusServer:
            self.tStatusServer = PyTango.DeviceProxy('//hzgpp05ct1:10000/p05/status_server/p05ct')
            #self.tStatusServer = PyTango.DeviceProxy('//hzgpp05ct1:10000/p05/status_server/p05beamline') #gives wrong values for current?

            #self.tStatusServer.command_inout('createAttributesGroup',['beamcurrent','/PETRA/Idc/Buffer-0/I.SCH'])

            #self.tStatusServer.command_inout('stopCollectData')
            #self.tStatusServer.command_inout('eraseData')
            #self.tStatusServer.command_inout('startCollectData')
            self.StatusServerSendCommand('stopCollectData')            
            self.StatusServerSendCommand('eraseData')
            #self.StatusServerSendCommand('startCollectData') 
        if self.useSmarAct:
            self.SM = numpy.zeros(4, dtype = object)
            self.SM[0] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha0')
            self.SM[1] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha1')
            self.SM[2] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha3')
            self.SM[3] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha4')
#           self.SM[4] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha2')
        if self.useJenaPiezo:
            self.tJenaPiezo = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/jenapiezo')
        if useDiode:
            self.tDiode = PyTango.DeviceProxy('//hzgpp05eh1vme1:10000/p05/adc/eh1.01')
        if self.useEnviroLog:
            self.Environ = numpy.zeros(6, dtype = object)
            for i1 in xrange(6):
                self.Environ[i1] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/adc/eh1.%02i' %(i1+1))

        #########################################
        ######## initialize logging #############
        #########################################
        if os.path.exists(self.sLogfile):
            print('~~~~~~~~~ !!!! ~~~~~~~~~ Warning: Logfile exists')
            tmp = raw_input('~~~~~~~~~ !!!! ~~~~~~~~~ Continue? y / n: ')
            if tmp not in ['yes', 'Y', 'y']:
                print('Aborting...')
                sys.exit()
        
        # Prepare _LogScan
        self.fLog = open(self.sLogfile, 'w')
        self.fLog.write('#00: image identifier\n#01: infostr\n#02: image number I\n#03: image number II\n#04: current number\n#04: file number\
        \n#06: timestamp\n#07: PETRA Beam Current\n#08: Position of rotation stage \n')
        if self.useEnviroLog: # Not implemented at the moment
            self.fLog.write('#24: Air temperature 01\n#25: Air humidity 01\n#26: Air temperature 02\
            \n#27:Air humidity 02\n#28: Air temperature 03\n#29: Air humidity 03\n')
        self.fLog.write('#starttime = %e\n' %self.starttime)
        tmp = '%s\t%s\t%s\t%s\t%s\t' %(self.__FormattedString('#00', 18), self.__FormattedString('#01', 5), self.__FormattedString('#02', 5),\
                self.__FormattedString('#03', 5), self.__FormattedString('#04', 5))+ \
                        '#05:\t#06:\t\t#07:\t\t#08::'
        if self.useEnviroLog: tmp += '\t\t#22:\t#23:\t\t#24:\t\t#25:\t\t#26:\t\t#27:\t\t#28:\t\t#29:'
        self.fLog.write(tmp + '\n')

        # Prepare _LogMotor
        self.fMotorLog = open(self.sMotorLogFile, 'w')
        __list = ['VacuumSF_x', 'VacuumSF_y', 'VacuumSF_z', 'VacuumSF_Rx', 'VacuumSF_Ry', 'VacuumSF_Rz', 'VacuumTrans_y',\
                  'GraniteSlab_1', 'GraniteSlab_2', 'GraniteSlab_3','GraniteSlab_4', 'Aperture_x', 'Aperture_y', \
                  'Aperture_z', 'OpticsSF1_x', 'OpticsSF1_y', 'OpticsSF1_z', 'OpticsSF1_Rx', 'OpticsSF1_Ry', 'OpticsSF1_Rz', \
                  'OpticsStage1_y', 'OpticsSF2_x', 'OpticsSF2_y', 'OpticsSF2_z', 'OpticsSF2_Rx', 'OpticsSF2_Ry', 'OpticsSF2_Rz', \
                  'Diode1_z','Diode2_z', 'SampleStage_x', 'SampleStage_z', 'SampleStage_Rx', 'SampleStage_Ry', \
                  'Sample_Rot', 'Sample_x', 'Sample_y', 'Sample_z', 'Sample_Rx', 'Sample_Ry', 'Sample_Rz', \
                  'Detector_x', 'Detector_z', 'Slits_xLeft', 'Slits_xRight', 'Slits_zLow', 'Slits_zHigh', 'ScintillatorY', 'CamLensY', 'CameraRot',\
                  'UndulatorPos', 'Pitch', 'DCM']
        if self.useSmarAct:
            __list += ['SmarAct ch. 0 (x left)', 'SmarAct ch. 1 (z top)', 'SmarAct ch. 3 (x right)', 'SmarAct ch. 4 (z bottom)']
        if self.useJenaPiezo:
            __list += ['JenaPiezo X1', 'JenaPiezo X2', 'JenaPiezo Y1', 'JenaPiezo Y2']

        self.fMotorLog.write('#00: Identifier\n#01: Infostring\n#02: Index number I\n#03: Index number II\n#04: Current number\n')
        __ii = 5   # start counter after first block of text
        for __item in __list:
            self.fMotorLog.write('#%02i: %s\n' %(__ii, __item))
            __ii += 1
        
        tmp = '%s\t%s\t%s\t%s\t%s\t' %(self.__FormattedString('#00', 18), \
                                       self.__FormattedString('#01', 5), self.__FormattedString('#02', 5),\
                                       self.__FormattedString('#03', 5), self.__FormattedString('#04', 5))
        __ii = 5
        for i1 in xrange(len(__list)):
            tmp += '#%02i\t\t' %(i1 + 5)
        self.fMotorLog.write(tmp+ '\n')


        time.sleep(0.1)
        
        # Prepare _LogBeam
        self.fBeamLog = open(self.sBeamLogFile, 'w')
        self.fBeamLog.write('#00: Identifier\n#01: Infostring\n#02: Index number I\n#03: Index number II\n#04: Current number\
                            \n@Timestamp[PETRA current@Timestamp]\n')
        

        self.sIdentifier = ''
        self.iNumber  = None
        self.iNumber2 = None
        self.iCurr = 0
        self.imgNumber = 0
        tmp = self.GetCurrentMotorPosString("Before Scan", "Start Scan")
        self.fMotorLog.write(tmp)

        return None
    #end __init__


    def __FormattedString(self, __string, __length = 15):
        if len(__string) >= __length:
            return __string[:__length]
        else:
            return __string + (__length-len(__string))*' ' 
    #end __FormattedString
        
        
    def BeamshutterOpen(self, SilentMode = False):
        try:
            self.tBeamShutter.command_inout('CloseOpen_BS_1', 1)
            if not SilentMode:
                print(misc.GetTimeString()+': Beamshutter opened')
        except:
            pass
        return None
    #end BeamshutterOpen
    
    def BeamshutterClose(self, SilentMode = False):
        try:
            self.tBeamShutter.command_inout('CloseOpen_BS_1', 0)
            if not SilentMode:
                print(misc.GetTimeString()+': Beamshutter closed')
        except:
            pass
        return None
    #end BeamshutterClose


    def TakeDarkImages(self, num = 10,imgNumber=0):
        self.BeamshutterClose()
        time.sleep(40)
        for i1 in xrange(num):
            #self.SetCurrentName('dark', iNumber= i1, iNumber2= None, imgNumber=imgNumber+i1)
            self.SetCurrentName('dark', iNumber= i1, iNumber2= None, imgNumber=None)
            self.TakeImage()
            print(i1)
        self.BeamshutterOpen()
        time.sleep(20)
        return None
    #end TakeDarkImages


    def SetCurrentName(self, _identifier, iNumber = None, iNumber2 = None, currNum = None, imgNumber=None):
        """
        Method to set the current identifier and image number
        """
        if currNum != None:
            self.iCurr = currNum    
        if self.useHamaTrigger != True:
            if self.camera == 'Hamamatsu' or "Zyla" or "PCO":
                self.hamamatsu.setImageName(_identifier)
                if imgNumber != None:
                    self.hamamatsu.setImgNumber(imgNumber)
                    self.imgNumber = imgNumber
        self.sIdentifier = _identifier
        if iNumber == None:
            self.iNumber = None
            self.curname = '%s_%s_%04i' %(self.sPrefix, self.sIdentifier, self.iCurr)
        elif iNumber != None:
            self.iNumber = iNumber
            if iNumber2 == None:
                self.iNumber2 = None
                self.curname = '%s_%s_%04i_%04i' %(self.sPrefix, self.sIdentifier, self.iNumber, self.iCurr)
            elif iNumber2 != None:
                self.iNumber2 = iNumber2
                self.curname = '%s_%s_%04i_%04i_%04i' %(self.sPrefix, self.sIdentifier, self.iNumber, self.iNumber2, self.iCurr)
    #end SetCurrentName
    
    
    def SetCurrentNumber(self, iNumber = None, iNumber2 = None, currNum = None):
        """
        Method to set the current image number
        """
        if currNum != None:
            self.iCurr = currNum

        if iNumber != None: 
            if iNumber2 == None:
                self.iNumber  = iNumber
                self.iNumber2 = None
            elif iNumber2 != None:
                self.iNumber  = iNumber
                self.iNumber2 = iNumber2
        if currNum != None:
            self.iCurr = currNum
        return None
    #end SetCurrentName
    
    def SetExposureTime(self,exptime):
        self.exptime = exptime  
        self.hamamatsu.setExptime(self.exptime)
        
    def StatusServerSendCommand(self, _command):
        i0 = 0
        while True:
            try:
                self.tStatusServer.command_inout(_command)
                break
            except:
                print misc.GetTimeString() + ': StatusServer not responding while executing command "%s"...' %_command
                time.sleep(10)
                i0 += 1
            if i0 > 5: break
        return 
    #end StatusServerSendCommand
    
    
    def StatusServerReadData(self):
        i0 = 0
        while True:
            #try:
                #self.StatusServerSendCommand('getLatestSnapshot').value
            tmp = self.tStatusServer.read_attribute('data').value[1]
            tmp = tmp.split('\n')[1:]
            if tmp[0].split('[')[1] == '0.0@0]': tmp.pop(0)
            if tmp[-1] == '':   tmp.pop(-1)
#             tmp = string.join(tmp, '\n')+ '\n'
#                 break
#             except:
#                 print misc.GetTimeString() + ': StatusServer not responding while reading data...'
#                 time.sleep(10)
#                 i0 += 1
#             if i0 > 5: 
#                 tmp = 'StatusServer error'
#                 break
        return tmp
    #end StatusServerReadData
    
    
    def TakeImage(self, verbose = False, writeLogs = True,inum=None,iname=None):
        """Method to take and image and write beam parameters to logfile."""
        if verbose:  print('%s: Acquiring image %s'% (misc.GetTimeString(),'bla'))#, self.curname
        while True:
            tmp_count = self.tPETRAnbCleaning.read_attribute('SweepCounter').value
            self.reacquire = False
            if writeLogs:   _logdata = self.GetCurrentDataString(self.sIdentifier, 'start')
            if self.useStatusServer:
                self.StatusServerSendCommand('eraseData')
                self.StatusServerSendCommand('startCollectData')
            
            # For PCO camera class
            if self.camera not in ['KIT', 'PCOcamware', 'Hamamatsu', 'PixelLink','Zyla','PCO']:
                self.lastimage = copy.copy(self.currimage)
                self.currimage = self.camera.acquireImage()
                if self.useStatusServer:    self.StatusServerSendCommand('stopCollectData')
                self.currimage.tofile(self.sPath + '/%s.raw' %self.curname)
    
            elif self.camera == 'PCOcamware':
                self.tTrigger.write_attribute('Voltage', 5)
                time.sleep(self.exptime)
                self.tTrigger.write_attribute('Voltage', 0)
                if self.useStatusServer:    self.StatusServerSendCommand('stopCollectData')
                
            elif self.camera == 'KITnikon':
                tmp = subprocess.Popen('W:/nanoXTM_IMT/NikonController/NikonCMD.exe w:/nanoXTM_IMT/NikonController/Type0007.md3 -p "D:\Pictures" '+ self.KITcameraParameters)
                tmp.wait()
                if self.useStatusServer:    self.StatusServerSendCommand('stopCollectData')
                shutil.copy2('D:/Pictures/image.jpg', self.sPath + self.curname + '.jpg')
                shutil.copy2('D:/Pictures/image.nef', self.sPath + self.curname + '.nef')
                self.LogWriteCurrentData(self.sIdentifier, 'end')
                os.remove('D:/Pictures/image.jpg')
                os.remove('D:/Pictures/image.nef')
            
            elif self.camera == 'Hamamatsu':
                self.lastimage = copy.copy(self.currimage)
                
                self.currimage = self.hamamatsu.acquireImage()
                if self.useStatusServer:    self.StatusServerSendCommand('stopCollectData')
                
            elif self.camera == 'Zyla':
                self.hamamatsu.acquireImage()
                if self.useStatusServer:    self.StatusServerSendCommand('stopCollectData')
            
            elif self.camera == 'KIT':
                self.hamamatsu.acquireImage()

            elif self.camera == 'PCO':
                self.hamamatsu.acquireImage()
                #self.image = numpy.float32(im)
#                im2 = Image.fromarray(self.image.transpose(), mode="F" ) # float32
#                im2.save(self.sPath + iname +'_%03i' % inum + '.tiff' , "TIFF"  )


                if self.useStatusServer:    self.StatusServerSendCommand('stopCollectData')
                        
            elif self.camera == 'PixelLink':
                self.lastimage = copy.copy(self.currimage)
                self.tTrigger.write_attribute('Voltage', 5)
                time.sleep(self.exptime)
                self.tTrigger.write_attribute('Voltage', 0)
                if self.useStatusServer:    self.StatusServerSendCommand('stopCollectData')
                
            elif self.camera == None:
                time.sleep(self.exptime)
                if self.useStatusServer:    self.StatusServerSendCommand('stopCollectData')
    
            if self.useStatusServer and writeLogs:
                self.BeamLogWriteData(self.StatusServerReadData())
                self.StatusServerSendCommand('eraseData')

            tmp_count2 = self.tPETRAnbCleaning.read_attribute('SweepCounter').value


            ###comment out from here  #### WHy__
            if self.reacquire and self.useHamamatsu:
                self.iCurr += 1
            ### comment out until here
            if (not self.reacquire) or self.disableSideBunchReacquisition:
                break
        
        if writeLogs:
            self.fLog.write(_logdata) # writes logdata from start of image aquisition
            self.LogWriteCurrentData(self.sIdentifier, 'end', logMotors= True)  # writes logdata from end of image aquisition
            self.iCurr += 1
            #self.SetCurrentName(self.sIdentifier, iNumber= self.iNumber, iNumber2 = self.iNumber2, currNum = self.iCurr)
        return None
    #end TakeImage


    def TakeOneDummyImage(self):
         self.tTrigger.write_attribute('Value', 1)
         time.sleep(0.010)
         self.tTrigger.write_attribute('Value', 0)


    def TakeFastImage(self,writeLogs = True,inum=None,iname=None, WaitForCamera= False):
        if writeLogs:   _logdata = self.GetCurrentDataString(self.sIdentifier, 'start')
        ##### for PCO camera ####
        if self.camera == 'PCO':
            while not self.hamamatsu.state() == PyTango.DevState.ON:
                continue
            if not self.hamamatsu.state() == PyTango.DevState.RUNNING:
                self.hamamatsu.startPCOacquisition()
            while not self.hamamatsu.state() == PyTango.DevState.RUNNING:
                continue
            #time.sleep(0.01)
            self.tTrigger.write_attribute('Voltage', 3.5)
            rot_pos = self.tPMAC.ReadMotorPos('Sample_Rot')
            time.sleep(self.exptime + 0.01)
            self.tTrigger.write_attribute('Voltage', 0)
            tmp = numpy.fromstring(self.hamamatsu.readAttribute('Image').value[1], dtype=numpy.uint16).byteswap()
            self.image = (tmp[2:]).reshape(tmp[0], tmp[1])
            self.image = numpy.float32(self.image)
            im2 = Image.fromarray(self.image.transpose(), mode="F" ) # float32
            im2.save(self.sPath + iname +'_%03i' % inum + '.tiff' , "TIFF" )

        ##### for Hamamatsu camera #######
        elif self.camera == 'Hamamatsu':

            out = self.tTriggerOut.read_attribute('Value')
            while out.value != 1:
                out = self.tTriggerOut.read_attribute('Value')

#            while not self.hamamatsu.state() == PyTango.DevState.ON:
#               continue

#            while not self.hamamatsu.state() == PyTango.DevState.EXTRACT:
#                continue

            self.tTrigger.write_attribute('Value', 1)
            rot_pos = self.tPMAC.ReadMotorPos('Sample_Rot')
            time.sleep(0.005) # will be 10-13 ms
            self.tTrigger.write_attribute('Value', 0)


            if WaitForCamera:
                out = self.tTriggerOut.read_attribute('Value')
                while out.value != 1:
                    out = self.tTriggerOut.read_attribute('Value')

        if writeLogs:
            self.fLog.write(_logdata.split('\n')[0]+str(rot_pos)+'\n')
            self.iCurr += 1
        return None


    def SendTriggerInOut(self,writeLogs = True,name = 'tomo',WaitForCamera= False):
        """ Method to send trigger when camera is ready (trigger ready from camera) """
        #self.sIdentifier = name
        if writeLogs:   _logdata = self.GetCurrentDataString(self.sIdentifier, 'start')
        # Wait for Trigger Ready from Camera
        out = self.tTriggerOut.read_attribute('Value')
        while out.value == 0:
            out = self.tTriggerOut.read_attribute('Value')
        # Send trigger
        self.tTrigger.write_attribute('Value', 1)
        # Read rotation stage position
        rot_pos = self.tPMAC.ReadMotorPos('Sample_Rot')
        self.tTrigger.write_attribute('Value', 0)
        if writeLogs:
            self.fLog.write(_logdata.split('\n')[0]+str(rot_pos)+'\n')
            self.iCurr += 1
        if WaitForCamera:
            out = self.tTriggerOut.read_attribute('Value')
            while out.value == 0:
                out = self.tTriggerOut.read_attribute('Value')
        return None


    def SendTriggerHama(self, position, verbose = False, writeLogs = True):
        """Method to send tigger and write beam parameters to logfile. ---- OLD VERSION"""
        if verbose:  print('%s: Acquiring image %s'% (misc.GetTimeString(),'bla'))#, self.curname
       
        self.reacquire = False
        if writeLogs:   _logdata = self.GetCurrentDataString(self.sIdentifier, 'start')
        if self.useStatusServer:
            self.StatusServerSendCommand('eraseData')
            self.StatusServerSendCommand('startCollectData')
        
        rot_pos =self.tPMAC.ReadMotorPos('Sample_Rot')
        while rot_pos  <= position:
            rot_pos =self.tPMAC.ReadMotorPos('Sample_Rot')


            
        # send trigger
        self.tTrigger.write_attribute('Value', 1) 
        #self.tTrigger.write_attribute('Voltage', 3.5)
        #time.sleep(0.010)
        print(rot_pos)
        self.tTrigger.write_attribute('Value', 0) 
        #self.tTrigger.write_attribute('Voltage', 0)
        
        
        if self.useStatusServer:    self.StatusServerSendCommand('stopCollectData')

       
        if self.useStatusServer and writeLogs:
            self.BeamLogWriteData(self.StatusServerReadData())
            self.StatusServerSendCommand('eraseData')
        
        if writeLogs:
            self.fLog.write(_logdata.split('\n')[0]+str(rot_pos)+'\n')  
            
            self.LogWriteCurrentData(self.sIdentifier, 'end', logMotors= False)
            self.iCurr += 1
            #self.SetCurrentName(self.sIdentifier, iNumber= self.iNumber, iNumber2 = self.iNumber2, currNum = self.iCurr)
        return None
        # waiting time to write image
        #time.sleep(0.1)
    #end TakeImage
    
    
    def SendTriggerHama_NGM(self, position, verbose = False, writeLogs = True):
        """Method to send tigger and write beam parameters to logfile."""
        if verbose:  print('%s: Acquiring image %s'% (misc.GetTimeString(),'bla'))#, self.curname
       
        self.reacquire = False
        if writeLogs:   _logdata = self.GetCurrentDataString(self.sIdentifier, 'start')
        if self.useStatusServer:
            self.StatusServerSendCommand('eraseData')
            self.StatusServerSendCommand('startCollectData')
        
        while True:
            rot_pos = self.rot_Stage_NGM.read_attribute('Position').value  
            time.sleep(0.002)
            if rot_pos >= position:
                break
            
        # send trigger
        self.tTrigger.write_attribute('Value', 1) 
        #self.tTrigger.write_attribute('Voltage', 3.5)
        time.sleep(0.01)
        print(rot_pos)
        self.tTrigger.write_attribute('Value', 0) 
        #self.tTrigger.write_attribute('Voltage', 0)
        
        
        if self.useStatusServer:    self.StatusServerSendCommand('stopCollectData')

       
        if self.useStatusServer and writeLogs:
            self.BeamLogWriteData(self.StatusServerReadData())
            self.StatusServerSendCommand('eraseData')
        
        if writeLogs:
            self.fLog.write(_logdata.split('\n')[0]+str(rot_pos)+'\n')  
            
            self.LogWriteCurrentData(self.sIdentifier, 'end', logMotors= False)
            self.iCurr += 1
            #self.SetCurrentName(self.sIdentifier, iNumber= self.iNumber, iNumber2 = self.iNumber2, currNum = self.iCurr)
        return None
        # waiting time to write image
        #time.sleep(0.1)
    #end TakeImage
    

    def TakeFlatfieldCorrectedImage(self, pmac, inpos = None, refpos = None, motor = None, verbose = False):
        if verbose:  print('%s: Acquiring image %s'% (misc.GetTimeString(), self.curname))
        if not os.path.exists(self.sPath + os.sep + 'abs'): os.mkdir(self.sPath + os.sep + 'abs')
        #try:
        pmac.Move(motor, refpos)
        time.sleep(0.1)
        self.sIdentifier = 'ref'
        self.SetCurrentName(self.sIdentifier, iNumber= self.iNumber, iNumber2 = self.iNumber2, currNum = self.iCurr)
        self.LogWriteCurrentData(self.sIdentifier, 'start', logMotors = True)
        self.TakeImage(writeLogs = False)
        ref = copy.copy(self.currimage)
        self.LogWriteCurrentData(self.sIdentifier, 'end')

        pmac.Move(motor, inpos)
        time.sleep(0.1)
        self.sIdentifier = 'img'
        self.SetCurrentName(self.sIdentifier, iNumber= self.iNumber, iNumber2 = self.iNumber2, currNum = self.iCurr)
        self.LogWriteCurrentData(self.sIdentifier, 'start', logMotors = True)
        self.TakeImage(writeLogs = False)
        img = copy.copy(self.currimage)
        self.LogWriteCurrentData(self.sIdentifier, 'end')

        _abs = (1.0* img /ref).astype(numpy.float32)
        self.sIdentifier = 'abs'
        self.SetCurrentName(self.sIdentifier, iNumber= self.iNumber, iNumber2 = self.iNumber2, currNum = self.iCurr)
        _abs.tofile(self.sPath + '/abs/%s.raw' %self.curname)
#        except:
#            print('%s: Error acquiring flatfield corrected image.'% (misc.GetTimeString()))
#            return None
        self.iCurr += 1
        return None

    def HamaTakeRef(self, num_img=20):
        time.sleep(0.1)
        i=-1
        self.hamamatsu.startLive()
        time.sleep(0.1)
        #self.TakeOneDummyImage()
        for i2 in range(num_img):
            i = i + 1
            time.sleep(0.01)
            self.TakeFastImage()
            print(i)
        #time.sleep(0.5)
        out = self.tTriggerOut.read_attribute('Value')
        while out.value != 1:
            out = self.tTriggerOut.read_attribute('Value')
        #time.sleep(0.1)
        self.hamamatsu.finishScan()
        return None

    def HamaTakeTomo(self,target_pos):
        self.tPMAC.Move('Sample_Rot',target_pos, WaitForMove=False)
        i=-1
        self.hamamatsu.startLive()
        time.sleep(0.1)
        #nanoScript.TakeOneDummyImage()
        while self.tPMAC.ReadMotorPos('Sample_Rot') <= target_pos-1:
            i = i + 1
            self.TakeFastImage()
            print(i)
        out = self.tTriggerOut.read_attribute('Value')
        while out.value != 1:
            out = self.tTriggerOut.read_attribute('Value')
        time.sleep(0.1)
        self.hamamatsu.finishScan()
        return None

    def ReadDiode(self, avg = 5):
        """Method to read the diode current from the self.tDiode device."""
        tmp = 0
        num = 1.0 / avg
        for i1 in xrange(avg):
            tmp +=  num * abs(self.tDiode.read_attribute('Value').value)
            time.sleep(0.015)
        return tmp


    def OptimizePitchAndLog(self, Detune = None, DeltaRange = 0.0004, dummy = False):
        """Method to optimize the pitch (using QBPM 1 for feedback) 
        and detuning the pitch by delta = 0.0002 degree"""
        self.fLog.write('%s\t%s\t%04i\t%04i\t%04i\t%s%s%e\n' %(self.__FormattedString('OptimizePitch', 18),\
                                                 self.__FormattedString('start', 5), -1, -1, -1, self.GetPETRAbeaminfo(), self.GetPETRAcell4(), self.tDCMenergy.read_attribute('Position').value))
#         self.fLog.write('%s\t%s\t%04i\t%04i\t%04i\t%s%s%e\n' %(self.__FormattedString('OptimizePitch', 18),\
#                                                  self.__FormattedString('start', 5), -1, -1, -1, self.GetPETRAbeaminfo(), self.GetPETRAcell4(), self.tDCMenergy.read_attribute('Position').value))
        if not dummy:
            if Detune == None:
                Detune = self.DCMdetune
            OptimizePitchDCM(Detune = Detune, DeltaRange = DeltaRange)
        self.fLog.write('%s\t%s\t%04i\t%04i\t%04i\t%s%s%e\n' %(self.__FormattedString('OptimizePitch',  18),\
                                                 self.__FormattedString('end', 5), -1, -1, -1, self.GetPETRAbeaminfo(), self.GetPETRAcell4(), self.tDCMenergy.read_attribute('Position').value))
#         self.fLog.write('%s\t%s\t%04i\t%04i\t%04i\t%s%s%e\n' %(self.__FormattedString('OptimizePitch',  18),\
#                                                  self.__FormattedString('end', 5), -1, -1, -1, self.GetPETRAbeaminfo(), self.GetPETRAcell4(), self.tDCMenergy.read_attribute('Position').value))
        return None
    #end OptimizePitchNoHarmonicsAndLog


    def LogWriteCurrentData(self, __identifier, __infostr, logMotors = False):
        """Write standard data in the scan logfile."""
        tmp = self.GetCurrentDataString(__identifier, __infostr)
        self.fLog.write(tmp)
        if logMotors:
            tmp = self.GetCurrentMotorPosString(__identifier, __infostr)
            self.fMotorLog.write(tmp)
        return None
    #end WriteToScanLog


    def GetCurrentDataString(self, __identifier, __infostr):
        if self.iNumber == None: 
            iNumber = -1
        else:
            iNumber = self.iNumber
        if self.iNumber2 == None: 
            iNumber2 = -1
        else:
            iNumber2 = self.iNumber2
        if self.iCurr== None: 
            iCurr = -1
        else:
            iCurr = self.iCurr
        if self.imgNumber == None:
            imgNumber = self.hamamatsu.getImgNumber()
        else:
            imgNumber = self.imgNumber
        tmp = '%s\t%s\t%04i\t%04i\t%04i\t%04i\t' %(self.__FormattedString(__identifier, 18), \
                                       self.__FormattedString(__infostr, 5), iNumber, iNumber2, iCurr,imgNumber) 
        tmp += self.GetPETRAbeaminfo()
        # tmp += self.GetPETRAcell4() # Orbit position beam, not needed ?!
        # tmp += '%e\t' %self.tDCMenergy.read_attribute('Position').value # write dcm pos at begnning of scan
        if self.disableSideBunchReacquisition == False:
            tmp += '%04i\t%04i\t' %(self.tPETRAnbCleaning.read_attribute('SweepCounter').value, self.tPETRAnbCleaning.read_attribute('SweepThreshold').value)
        if self.useEnviroLog:
            for i1 in xrange(6):
                tmp+= '%e\t' %(self.Environ[i1].read_attribute('Value').value*5*(numpy.mod(i1,2) + 1))
        return tmp + '\n'
    #end

    def GetCurrentMotorPosString(self, __identifier, __infostr):
        if self.iNumber == None: 
            iNumber = -1
        else:
            iNumber = self.iNumber
        if self.iNumber2 == None: 
            iNumber2 = -1
        else:
            iNumber2 = self.iNumber2
        if self.iCurr== None: 
            iCurr = -1
        else:
            iCurr = self.iCurr
        tmp = '%s\t%s\t%04i\t%04i\t%04i\t' %(self.__FormattedString(__identifier, 18), \
                                   self.__FormattedString(__infostr, 5), iNumber, iNumber2, iCurr)
        tmp += self.tPMAC.ReadAllMotorPos()
        tmp += self.EH1slits.GetPos()
        try:
            tmp += '%e\t%e\t%e\t' %(self.tScintiY.read_attribute('Position').value, self.tLensY.read_attribute('Position').value, self.tCamRot.read_attribute('Position').value)
        except:
            tmp += '%e\t%e\t%e\t' %(-1, -1, -1)
        
        try:
            tmp += '%e\t%e\t' %(self.tUndulator.read_attribute('Gap').value, self.tPitch.read_attribute('Position').value)
        except:
            tmp += '%e\t%e\t' %(-1, -1)
        if self.useSmarAct:
            try:
                tmp += '%e\t%e\t%e\t%e\t' %(self.SM[0].read_attribute('Position').value, self.SM[1].read_attribute('Position').value, \
                                            self.SM[2].read_attribute('Position').value, self.SM[3].read_attribute('Position').value)
            except:
                tmp += '%e\t%e\t%e\t%e\t' %(-1, -1, -1, -1)
        if self.useJenaPiezo:
            try:
                tmp += '%e\t%e\t%e\t%e\t' %(self.tJenaPiezo.read_attribute('PositionX1').value, self.tJenaPiezo.read_attribute('PositionX2').value, \
                                            self.tJenaPiezo.read_attribute('PositionY1').value, self.tJenaPiezo.read_attribute('PositionY2').value)
            except:
                tmp += '%e\t%e\t%e\t%e\t' %(-1, -1, -1, -1)
        return tmp + '\n'
    #end GetCurrentMotorPosString

    def BeamLogWriteData(self, beamdata):
        if self.iNumber == None: 
            iNumber = -1
        else:
            iNumber = self.iNumber
        if self.iNumber2 == None: 
            iNumber2 = -1
        else:
            iNumber2 = self.iNumber2
        if self.iCurr== None: 
            iCurr = -1
        else:
            iCurr = self.iCurr
        tmp = '%s\t%s\t%04i\t%04i\t%04i\n' %(self.__FormattedString(self.sIdentifier, 18), \
                                       self.__FormattedString('PETRA', 5), iNumber, iNumber2, iCurr) 
        self.fBeamLog.write(tmp+beamdata)
        return None
    #end BeamLogWriteData


    def WaitForBeam(self, PETRAcurrent = 95, valreturn  = True):
        """Method to check for beam loss and wait until the beam is back to more 
        than 90% of the target value.
        <PETRAcurrent>: current of the ring to be compared to."""
        __retval = False
        try:
            while self.tPETRAinfo.read_attribute('BeamCurrent').value < 0.9*PETRAcurrent:
                time.sleep(60)
                print(misc.GetTimeString()+': Beam lost ... waiting for beam')
                __retval = True
        except:
            print(misc.GetTimeString()+': TINE connection error')
        if __retval:
            OptimizePitchDCM(Detune = self.DCMdetune)
            time.sleep(300)
        if valreturn:
            return __retval
        else:
            return None
    #end WaitForBeam
    
    
    def GetPETRAbeaminfo(self):
        """Layout: timestamp // Petra Beam Current (// Orbit RMSx // Orbit RMSy // QBPM current // QBPM pos x //QBPM pos  y)
         if not readable, return value is -1"""
        __infostr = '%e\t' %(time.time()-self.starttime)
        _attributevals = ['BeamCurrent'] # , 'OrbitRMSX', 'OrbitRMSY']
        for _att in _attributevals:
            try:
                tmp = self.tPETRAinfo.read_attribute(_att).value
                __infostr += '%010.6f\t' %tmp
            except:
                __infostr+= '-01.000000\t'
#        try:   # this block was for qbpm
#            __infostr += '-01.000000\t-01.000000\t-01.000000\t'
#            #tmp = self.tQBPM.read_attribute('PosAndAvgCurr').value
#            #__infostr += '%e\t%e\t%e\t' %(tmp[2], tmp[0], tmp[1])
#        except:
#            __infostr += '-01.000000\t-01.000000\t-01.000000\t'
        return __infostr
    #end GetPETRAbeaminfo
    
    def GetPETRAcell4(self):
        """Layout: BeamXAngleDeltaCell4 (in umrad) / BeamXPosDeltaCell4 (in um) / BeamYAngleDeltaCell4 (in umrad) / BeamYPosDeltaCell4 (in um)
         if not readable, return value is -1"""
        __infostr = ''
        _attributevals = ['Xposition', 'XpositionSoll','Xangle', 'XangleSoll', 'Yangle', 'YangleSoll', 'Yposition', 'YpositionSoll']
        for _att in _attributevals:
            try:
#                 tmp = self.tPETRAcell4.read_attribute(_att).value
                __infostr += '%010.6f\t' %(-1)  #tmp
            except:
                __infostr+= '-01.000000\t'
        return __infostr
    #end GetPETRAcell4
    
    
    def FinishScan(self):
        """Cleanup routines and closing of logfile"""
        tmp = self.GetCurrentMotorPosString("End Scan", "Stop")
        self.fMotorLog.write(tmp)

        self.fLog.close()
        self.fMotorLog.close()
        self.fBeamLog.close()
#         if self.camera not in ['KITnikon', 'PCOcamware', None, 'Hamamatsu','Zyla']:
#             self.camera.finishScan()
        if self.camera == 'Hamamatsu':
            self.hamamatsu.finishScan()
        if self.closeShutter:
            self.BeamshutterClose()
        print(misc.GetTimeString()+': Finished scan %s' %self.sPrefix)
        return None
    #end FinishScan
