import time
import numpy

import p05.devices
from p05.nano.NanoScriptHelper import NanoScriptHelper
import p05.tools.misc as misc


class Tomo():
    def __init__(self, scanname = None,\
         exptime = 1.0, \
         rotValues = None, \
         rotCenter = None, \
         refPos =    None, \
         currScript = 'unknown', \
         PETRAcurrent = 90, \
         #standard parameters:
         useStatusServer = True, \
         usePCO = True, \
         useSmarAct = True, \
         useASAP = True, \
         useJenaPiezo = True, \
         useEnviroLog = True, \
         oriInterval = 15, \
         refInterval = 2, \
         DCMdetune = 0.000, \
         takeDarkImages = True, \
         #optional parameters:
         group = 'hzg',\
         beamtime = 'test', \
         useKITcamera = False, \
         KITcameraParameters = None, \
         useDiode = False, \
         closeShutter = False, \
         usePCOcamware = False, \
         useEHD = False):
    
    
        if not isinstance(rotValues, numpy.ndarray):
            print misc.GetTimeString() + ': Error: rotValues is not a numpy ndarray. Aborting ...........'
            return None
        
        if not rotValues.dtype in [numpy.float32, numpy.float64, numpy.int16, numpy.int32, numpy.uint16, numpy.uint32]:
            print misc.GetTimeString() + ': Error: rotValues datatype not understood. Aborting ...........'
            return None
        
        if not type(rotCenter) in [numpy.float32, numpy.float64, numpy.int16, numpy.int32, numpy.uint16, numpy.uint32, float]:
            print misc.GetTimeString() + ': Error: rotCenter data type not not a number. Aborting ...........'
            return None
        
        if not type(refPos) in [numpy.float32, numpy.float64, numpy.int16, numpy.int32, numpy.uint16, numpy.uint32, float]:
            print misc.GetTimeString() + ': Error: refPos data type not not a number. Aborting ...........'
            return None
    
        self.pmac = p05.devices.PMACdict()
        self.group = group
        self.beamline = beamtime
        self.scanname = scanname
        self.exptime = exptime
        self.useKITcamera = useKITcamera
        self.KITcameraParameters = KITcameraParameters
        self.usePCO = usePCO
        self.usePCOcamware = usePCOcamware
        self.useSmarAct = useSmarAct
        self.useStatusServer = useStatusServer
        self.useEHD = useEHD
        self.useASAP = useASAP
        self.useJenaPiezo = useJenaPiezo
        self.DCMdetune = DCMdetune
        self.useEnviroLog = useEnviroLog
        self.oriInterval = oriInterval
        self.refInterval = refInterval
        self.rotValues = rotValues
        self.rotCenter = rotCenter
        self.refPos = refPos
        self.PETRAcurrent = PETRAcurrent
        self.takeDarkImages = takeDarkImages
        
        self.nanoScript = NanoScriptHelper(self.pmac, currScript, group, beamtime, scanname, exptime = exptime, \
                     useKITcamera = useKITcamera, KITcameraParameters = None, usePCO = usePCO, useSmarAct = useSmarAct, \
                     useDiode = useDiode, closeShutter = closeShutter, useStatusServer = useStatusServer, \
                     usePCOcamware = usePCOcamware, useEHD = useEHD, useASAP = useASAP, \
                     useJenaPiezo = useJenaPiezo, DCMdetune = DCMdetune, useEnviroLog = useEnviroLog)

        self.currGap  = self.nanoScript.tUndulator.read_attribute('Gap').value
        
        self.run()
        return None
    
    
    def __FormattedString(self, __string, __length = 15):
        if len(__string) >= __length:
            return __string[:__length]
        else:
            return __string + (__length-len(__string))*' ' 
    #end __FormattedString

    
    def TakeImage(self):
        self.currLogMotors += self.nanoScript.GetCurrentMotorPosString(self.nanoScript.sIdentifier, 'start')
        self.currLogGeneral += self.nanoScript.GetCurrentDataString(self.nanoScript.sIdentifier, 'start')
        self.nanoScript.TakeImage(writeLogs = False)
        if self.useStatusServer:
            self.currLogP3int += self.CreateBeamLogEntry(self.nanoScript.StatusServerReadData())
            self.nanoScript.StatusServerSendCommand('eraseData')
        self.currLogGeneral += self.nanoScript.GetCurrentDataString(self.nanoScript.sIdentifier, 'end')
        return None
    
    
    def CreateBeamLogEntry(self, beamdata):
        if self.nanoScript.iNumber == None: 
            iNumber = -1
        else:
            iNumber = self.nanoScript.iNumber
        if self.nanoScript.iNumber2 == None: 
            iNumber2 = -1
        else:
            iNumber2 = self.nanoScript.iNumber2
        if self.nanoScript.iCurr== None: 
            iCurr = -1
        else:
            iCurr = self.nanoScript.iCurr
        tmp = '%s\t%s\t%04i\t%04i\t%04i\n' %(self.__FormattedString(self.nanoScript.sIdentifier, 18), \
                                       self.__FormattedString('PETRA', 5), iNumber, iNumber2, iCurr) 
        return tmp+ beamdata
    
    
    def run(self):
        if self.takeDarkImages: self.nanoScript.TakeDarkImages()
        self.pmac.Move('SampleStage_x', self.rotCenter)
        
        for i1 in xrange(self.rotValues.size):
            print misc.GetTimeString() + ': Rotation position no. %i' % i1

            beamlost = False
            
            while True:
                self.currBeam = self.nanoScript.tPETRAinfo.read_attribute('BeamCurrent').value
                self.currLogGeneral= ''
                self.currLogP3int = ''
                self.currLogMotors = ''
                
                if numpy.mod(i1, self.oriInterval) == 0 or beamlost or (i1 == self.rotValues.size -1):
                    self.pmac.Move('Sample_Rot', 0)
                    self.nanoScript.SetCurrentName('ori', iNumber=0, iNumber2=None, currNum=i1)
                    time.sleep(0.3)
                    self.TakeImage()
                                        
                    self.pmac.Move('Sample_Rot', 90)
                    time.sleep(0.3)
                    self.nanoScript.SetCurrentName('ori', iNumber=90, iNumber2=None, currNum=i1)
                    self.TakeImage()

                self.pmac.Move('Sample_Rot', self.rotValues[i1])

                if numpy.mod(i1, self.refInterval) == 0 or beamlost:
                    self.pmac.Move('SampleStage_x', self.refPos)
                    self.nanoScript.SetCurrentName('ref', iNumber=None, iNumber2=None, currNum=i1)
                    
                    self.TakeImage()
                    self.pmac.Move('SampleStage_x', self.rotCenter)
    
                time.sleep(0.3)
                self.nanoScript.SetCurrentName('img', iNumber=None, iNumber2=None, currNum=i1)
                self.TakeImage()

                if  self.nanoScript.tUndulator.read_attribute('Gap').value == self.currGap and \
                        self.nanoScript.tPETRAinfo.read_attribute('BeamCurrent').value >= 0.95 * self.currBeam:
                    self.nanoScript.fBeamLog.write(self.currLogP3int)
                    self.nanoScript.fMotorLog.write(self.currLogMotors)
                    self.nanoScript.fLog.write(self.currLogGeneral)
                    break 
                else:
                    print(misc.GetTimeString()+': Beam lost ... waiting for beam')
                    beamlost = True
                    self.t_beamloss = time.time()
                    while True:
                        try:
                            time.sleep(60)
                            if self.nanoScript.tPETRAinfo.read_attribute('BeamCurrent').value >= 0.95*self.PETRAcurrent \
                            and self.nanoScript.tUndulator.read_attribute('Gap').value == self.currGap:
                                break
                            else:
                                print(misc.GetTimeString()+': Beam lost ... waiting for beam')
                        except:
                            print(misc.GetTimeString()+': TINE connection error. ')
                    self.t_beamback = time.time()
                    deltaT = min((self.t_beamback - self.t_beamloss)*60, 3600)
                    while True:
                        print(misc.GetTimeString()+': Optimizing pitch and waiting for thermal equilibrium ...')
                        self.nanoScript.OptimizePitchAndLog(Detune = self.DCMdetune)
                        time.sleep(300)
                        if time.time() - self.t_beamback > deltaT:
                            break

        print(misc.GetTimeString()+': Finished scan.')        
        return None