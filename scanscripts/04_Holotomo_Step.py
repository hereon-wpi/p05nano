###########################################################
#### Initialization --- do not change #####################
###########################################################
print('hallo')

import numpy  # ###############
import os
import time

import p05.tools  ################

pmac = p05.devices.PMACdict()  ################
currScript = os.path.abspath(__file__)  ################
from sys import argv

###########################################################
#### end initialization ###################################
###########################################################



scriptname, beamtime, prefix, rotCenter,sampleOut, exptime ,num_img, stepsize,num_dist,num_flat,CS = argv

rotCenter = float(rotCenter)
sampleOut = float (sampleOut)
num_flat = int(num_flat)

num_img = int(num_img)
num_dist = int(num_dist)
stepsize = float(stepsize)
exptime = float (exptime)
CS = bool(CS)        

      
######Check parameters from here ########################

#beamtime = '11008942'
#prefix = '20200616_02_NEWHAMA_50'
#
#rotCenter = -10.9250
#sampleOut = 5
#
#smearing = 5
#exptime = 0.05
#speed = None

######Check parameters until here ########################


posSlider2 = pmac.ReadMotorPos('GraniteSlab_2single')
print('exposure time: ' + str(exptime))

det_size = 2048
overhead = 0.01

print('total scan time (min): ' + str(num_img*exptime*num_dist/60))
print('scan time per distance (min): ' + str(num_img*exptime/60))
print('overhead: ' + str(overhead))
print('detector size: ' + str(det_size))
print('exposure time: ' + str(exptime))
print('number of images: ' + str(num_img))




i1Array = numpy.linspace(0,180, num=num_img)

nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  closeShutter=CS, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useASAPcomm=False, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True,\
                                  logRotPos = True,\
                                  useHamaTrigger =False)


fScanParamLogFile = open("T:/current/raw/%s/%s__ScanParam.txt" %(prefix,prefix), 'w')
fScanParamLogFile.writelines("Scriptname: %s \n Beamtime: %s \n Prefix: %s \n RotCenter: %s \n SampleOut: %s \n Exposure Time: %s \n Number of Images: %s \n Stepsize: %s \n Number of Distances: %s \n Number of Flats: %s \n CloseShutter %s" %(scriptname, beamtime, prefix, rotCenter,sampleOut, exptime ,num_img, stepsize,num_dist,num_flat,CS))
fScanParamLogFile.close()


for i1 in range(num_dist):     
    if i1 != 0:
        pmac.EventSendCommandManual(pmac.Controller3, 'Q70=128')
        time.sleep(10)
        
        pmac.Move('GraniteSlab_2single',posSlider2+stepsize*i1,WaitForMove=True)
        time.sleep(2)
        pmac.EventSendCommandManual(pmac.Controller3, 'Q70=127')
        time.sleep(3)

    # Move to start position
    pmac.SetRotSpeed(30)
    time.sleep(0.1)
    
    pmac.Move('Sample_Rot',0, WaitForMove=True) 
    time.sleep(0.5)

#    # Take reference images
#    pmac.Move('SampleStage_x', rotCenter+sampleOut)
#    nanoScript.SetCurrentName('ref_y'+ str(i1), iNumber=i1, imgNumber=0)
#    time.sleep(1)
#    nanoScript.HamaTakeRef(num_img=num_flat)
#    
#    pmac.Move('SampleStage_x', rotCenter)
#    time.sleep(10)
    
    # Start Tomo

    for i2 in range(i1Array.size):
        
        if numpy.mod(i2, 300) == 0:
            pmac.Move('SampleStage_x', rotCenter-sampleOut)
            nanoScript.SetCurrentName('ref_y'+ str(i1)+ '_' + str(i2), iNumber=i1, iNumber2=i2,imgNumber=0)    
            nanoScript.HamaTakeRef(num_img=num_flat)
            pmac.Move('SampleStage_x', rotCenter)
            time.sleep(10)
        print(p05.tools.GetTimeString() + ': Acquiring image no. %i' % i2)
        pmac.Move('Sample_Rot', i1Array[i2])
        time.sleep(0.05)
        nanoScript.SetCurrentName('tomo_y'+ str(i1), iNumber=i2, iNumber2=i1, imgNumber=i2)
        nanoScript.TakeImage()
        time.sleep(exptime)

    time.sleep(1)    

# Take reference images at the end
pmac.Move('SampleStage_x', rotCenter+sampleOut)

nanoScript.SetCurrentName('ref_y'+ str(i1+1), iNumber=i1+1, imgNumber=0)
time.sleep(1)

nanoScript.HamaTakeRef(num_img=num_flat)

pmac.Move('SampleStage_x', rotCenter)


nanoScript.FinishScan()    