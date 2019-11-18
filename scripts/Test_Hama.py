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
#python standard_nct.py 11081017 npgscan1 180 450 1.5 0.9 5.0 && python standard_nct.py 11081017 npgscan2 180 900 1.5 0.9 5.0 && python standard_nct.py 11081017 npgscan3 180 1200 1.5 0.9 5.0

#scriptname, beamtime, prefix, rotangle, noproj, exptime, rotCenter, sampleOut = argv

scriptname, beamtime, prefix, rotangle, noproj, exptime, rotCenter, sampleOut = 'Test_Hama.py', '11003240_teh1', 'nano1349_Tardi_1_B001_Zernike_int3x', 180, 10, 2, -9.5,0.05

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

nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', beamtime, prefix, exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=False, \
                                  useHamamatsu=True,\
                                  disableSideBunchReacquisition = False)

i1Array = numpy.linspace(0, rotangle, num=noproj)


for i in range(10):
    nanoScript.SetCurrentName('dark', iNumber= i, iNumber2= None,imgNumber=i)
    nanoScript.TakeImage()


#nanoScript.TakeDarkImages()
#nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
#time.sleep(30)
iflat = 0
for i1 in xrange(i1Array.size):
    print p05.tools.GetTimeString() + ': Rotation position no. %i' % i1
 
    #beamlost = nanoScript.WaitForBeam(PETRAcurrent=100., valreturn=True)
 
    #at every 50th projection, move out rotation stage in x, make 10 flats
    if numpy.mod(i1, 50) == 0:
        #pmac.Move('SampleStage_x', rotCenter - sampleOut)
        time.sleep(0.1)
        for i4 in xrange(10):
            nanoScript.SetCurrentName('ref', iNumber=i1, iNumber2=i4, imgNumber=iflat)
            nanoScript.TakeImage( writeLogs = True)
            iflat += 1
        #pmac.Move('SampleStage_x', rotCenter)
        
 
    #pmac.Move('Sample_Rot', i1Array[i1])
    time.sleep(0.1)
 
    nanoScript.SetCurrentName('tomo', iNumber=i1, iNumber2=None,imgNumber=i1)
    nanoScript.TakeImage()


######################################################
#### Finishing routines  --- do not change  ##########
######################################################
nanoScript.FinishScan()  ##########
######################################################

