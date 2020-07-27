###########################################################
#### Initialization --- do not change #####################
###########################################################
print('hallo')
import sys
sys.path.append('D:\BeamlineControllPython\programming_python')
import p05.devices, p05.nano, p05.tools  ################
import numpy, time, os, PyTango  ################
pmac = p05.devices.PMACdict()  ################
currScript = os.path.abspath(__file__)  ################
from sys import exit  ################
from sys import argv
import p05.tools.misc as misc
###########################################################
#### end initialization ###################################
###########################################################



scriptname, beamtime, prefix, rotCenter,sampleOut, exptime, speed, smearing = argv

rotCenter = float(rotCenter)
sampleOut = float (sampleOut)
smearing = int(smearing)

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

num_flat = 20
startangle = -11
target_pos = 171
scriptname = str(prefix) + '.py'
nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=False, \
                                  useASAPcomm=False, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True,\
                                  logRotPos = True,\
                                  useHamaTrigger =False)


# Move to start position
pmac.SetRotSpeed(30)
time.sleep(0.1)

pmac.Move('Sample_Rot',startangle, WaitForMove=True) 
time.sleep(0.5)

# Take reference images
pmac.Move('SampleStage_x', rotCenter+sampleOut)

nanoScript.SetCurrentName('ref',iNumber2 =0, imgNumber=0)
time.sleep(1)

nanoScript.HamaTakeRef(num_img=num_flat)

pmac.Move('SampleStage_x', rotCenter)
#time.sleep(60)

# Start Tomo
pmac.SetRotSpeed(speed)
time.sleep(0.1)

nanoScript.SetCurrentName('img',iNumber = 0,imgNumber=0)
time.sleep(1)

nanoScript.HamaTakeTomo(target_pos)

time.sleep(0.5)

# Take reference images at the end
pmac.Move('SampleStage_x', rotCenter+sampleOut)

nanoScript.SetCurrentName('ref',iNumber2 =0, imgNumber=0)
time.sleep(1)

nanoScript.HamaTakeRef(num_img=num_flat)

pmac.Move('SampleStage_x', rotCenter)


nanoScript.FinishScan()    