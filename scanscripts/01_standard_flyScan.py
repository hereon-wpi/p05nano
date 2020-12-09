###########################################################
#### Initialization --- do not change #####################
###########################################################
print('hallo')

import p05.tools  ################
import numpy, time, os  ################
pmac = p05.devices.PMACdict()  ################
currScript = os.path.abspath(__file__)  ################
from sys import argv

###########################################################
#### end initialization ###################################
###########################################################



scriptname, beamtime, prefix, rotCenter,sampleOut, exptime, speed, smearing,num_flat,CS = argv



rotCenter = float(rotCenter)
sampleOut = float (sampleOut)
smearing = int(float(smearing))
num_flat = int(num_flat)
CS = bool(CS)
if exptime == 'None':
    exptime = None
else:
    exptime = float (exptime)
        
if speed == 'None':
    speed = None
else:
    speed = float (speed)
       
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

det_size = 2048
overhead = 0.01
if speed == None:
    speed = smearing * 180./ (numpy.pi *det_size/2*exptime)  # maximal speed of rotation axis for given exptime, maximum 1 pixel smearing
elif exptime == None:
    exptime = smearing * 180./ (numpy.pi *det_size/2*speed) # exptime for maximal 1 pixel smearing, caculated from speed

num_images = int(180/speed /(exptime+ overhead))  -1
print('speed: ' + str(speed))
print('total scan time (s): ' + str(180/speed))
print('total scan time (min): ' + str(180/speed/60))
print('overhead: ' + str(overhead))
print('detector size: ' + str(det_size))
print('exposure time: ' + str(exptime))
print('expected number of images: ' + str(num_images))
print('Efficency: ' + str(num_images*exptime/(180/speed )))

#num_flat = 20
startangle = -91
target_pos = 91



nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  closeShutter=CS, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=False, \
                                  useASAPcomm=False, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True,\
                                  logRotPos = True,\
                                  useHamaTrigger =False)

#fScanParamLogFile = open("T:/current/raw/%s/%s__ScanParam.txt" %(prefix,prefix), 'w')
#fScanParamLogFile.writelines("Scriptname: %s \n Beamtime: %s \n Prefix: %s \n RotCenter: %s \n SampleOut: %s \n Exposure Time: %s \n Speed: %s \n Smearing: %s \n Number of Flats: %s \n CloseShutter %s" %(scriptname, beamtime, prefix, rotCenter,sampleOut, exptime, speed, smearing,num_flat,CS))
#fScanParamLogFile.close()

# Move to start position
pmac.SetRotSpeed(30)
time.sleep(0.1)

pmac.Move('Sample_Rot',startangle, WaitForMove=True) 
time.sleep(0.5)

# Take reference images
pmac.Move('SampleStage_x', rotCenter+sampleOut)
i1=1
#nanoScript.SetCurrentName('ref_y'+ str(i1)+"_1", iNumber=i1, imgNumber=0)
nanoScript.SetCurrentName('ref',iNumber2 =0, imgNumber=0)
time.sleep(1)

nanoScript.HamaTakeRef(num_img=num_flat)

pmac.Move('SampleStage_x', rotCenter)
time.sleep(10)

# Start Tomo
pmac.SetRotSpeed(speed)
time.sleep(0.1)

nanoScript.SetCurrentName('img',iNumber = 0,imgNumber=0)
time.sleep(1)

nanoScript.HamaTakeTomo(target_pos)
time.sleep(1 + 1/speed)
time.sleep(0.5)

# Take reference images at the end
pmac.Move('SampleStage_x', rotCenter+sampleOut)

nanoScript.SetCurrentName('ref',iNumber2 =0, imgNumber=num_flat)
time.sleep(1)

nanoScript.HamaTakeRef(num_img=num_flat)

pmac.Move('SampleStage_x', rotCenter)

pmac.SetRotSpeed(30)
time.sleep(0.1)
pmac.Move('Sample_Rot',0, WaitForMove=True) 

nanoScript.FinishScan()    