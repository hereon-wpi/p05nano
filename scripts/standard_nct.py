###########################################################
#### Initialization --- do not change #####################
###########################################################
import p05.devices, p05.nano, p05.tools  ################
import numpy, time, os, PyTango  ################
pmac = p05.devices.PMACdict()  ################
currScript = os.path.basename(__file__)  ################
from sys import argv  ################
###########################################################
#### end initialization ###################################
###########################################################

#run text example
#python standard_nct.py 11081017 TEST2 180 100 1 -9.8 0.05 && python standard_nct.py 11081017 npgscan2 180 900 1.5 0.9 5.0 && python standard_nct.py 11081017 npgscan3 180 1200 1.5 0.9 5.0

#scriptname, beamtime, prefix, rotangle, noproj, exptime, rotCenter, sampleOut = argv

scriptname, beamtime, prefix, rotangle, noproj, exptime, rotCenter, sampleOut = 'standard_nct.py', '11081017', 'TEST10', 5, 10, 1, -9.8, 0.05

rotangle = float(rotangle)
noproj = int(noproj)
exptime = float(exptime)
rotCenter = float(rotCenter)
sampleOut = float(sampleOut)

# adding on more rotation angle for extra rotation step
rotangleplus = rotangle / noproj
rotangle = rotangle + rotangleplus

# adding one extra projection at the end of the scan
noproj = noproj + 1

nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useHamamatsu=True,\
                                  disableSideBunchReacquisition = True)

i1Array = numpy.linspace(0, rotangle, num=noproj)

nanoScript.SetCurrentName('dark', imgNumber=0)
nanoScript.TakeDarkImages()
num = 10
nanoScript.BeamshutterClose()
time.sleep(20)
nanoScript.SetCurrentName('dark', iNumber= 0, iNumber2=0, currNum = 0, imgNumber=0)
for i1 in xrange(num):
     nanoScript.SetCurrentName('dark', iNumber= i1, iNumber2=None,  imgNumber=i1)
     nanoScript.TakeImage()
     print(i1)
nanoScript.BeamshutterOpen()
time.sleep(20)

nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
time.sleep(30)
iflat = 0
 
for i1 in xrange(i1Array.size):
     print p05.tools.GetTimeString() + ': Rotation position no. %i' % i1
 
     #beamlost = nanoScript.WaitForBeam(PETRAcurrent=100., valreturn=True)
 
     #at every 50th projection, move out rotation stage in x, make 10 flats
     if numpy.mod(i1, 10) == 0:
         pmac.Move('SampleStage_x', rotCenter - sampleOut)
         for i4 in xrange(2):
             nanoScript.SetCurrentName('flat', iNumber=i1, iNumber2=i4, imgNumber=iflat)
             nanoScript.TakeImage()
             #time.sleep(0.1)
             iflat += 1
         pmac.Move('SampleStage_x', rotCenter)
         time.sleep(2)
 
     pmac.Move('Sample_Rot', i1Array[i1])
     time.sleep(0.5)
 
     nanoScript.SetCurrentName('tomo', iNumber=i1, iNumber2=None,imgNumber=i1)
     nanoScript.TakeImage()
     #setting time for rot stage movement
     time.sleep(0.2)

######################################################
#### Finishing routines  --- do not change  ##########
######################################################
#nanoScript.FinishScan()  ##########
######################################################

