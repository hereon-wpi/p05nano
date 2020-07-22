###########################################################
#### Initialization --- do not change #####################
###########################################################
print('hallo')

import p05.devices, p05.nano, p05.tools  ################
import numpy, time, os, PyTango  ################
pmac = p05.devices.PMACdict()  ################
currScript = os.path.abspath(__file__)  ################
from sys import exit  ################
from sys import argv
import p05.scripts.Camera_helper as ch
import p05.tools.misc as misc
###########################################################
#### end initialization ###################################
###########################################################



scriptname, beamtime, prefix, rotCenter,sampleOut, exptime , speed, smearing, stepsize,num_dist,num_flat,CS = argv

rotCenter = float(rotCenter)
sampleOut = float (sampleOut)
num_flat = int(num_flat)

num_dist = int(num_dist)
stepsize = float(stepsize)
exptime = float (exptime)
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


posSlider2 = pmac.ReadMotorPos('GraniteSlab_2single')
print('exposure time: ' + str(exptime))

det_size = 2048
overhead = 0.01
if speed == None:
    speed = smearing * 180./ (numpy.pi *det_size/2*exptime)  # maximal speed of rotation axis for given exptime, maximum 1 pixel smearing
elif exptime == None:
    exptime = smearing * 180./ (numpy.pi *det_size/2*speed) # exptime for maximal 1 pixel smearing, caculated from speed

num_images = int(180/speed /(exptime+ overhead))  -1
print('speed: ' + str(speed))
print('total scan time (s): ' + str(180/speed))
print('scan time per distance (min): ' + str(180/speed/60))
print('overhead: ' + str(overhead))
print('detector size: ' + str(det_size))
print('exposure time: ' + str(exptime))
print('expected number of images: ' + str(num_images))
print('Efficency: ' + str(num_images*exptime/(180/speed )))


startangle = -11
startangle2 = 49
startangle3 = 109
target_pos1 = 51
target_pos2 = 111
target_pos3 = 171

scriptname = str(prefix) + '.py'
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
fScanParamLogFile.writelines("Scriptname: %s \n Beamtime: %s \n Prefix: %s \n RotCenter: %s \n SampleOut: %s \n Exposure Time: %s \n Speed: %s \n Smearing: %s \n Stepsize: %s \n Number of Distances: %s \n Number of Flats: %s \n CloseShutter %s \n Slider2 Pos: %s" %(scriptname, beamtime, prefix, rotCenter,sampleOut, exptime , speed, smearing, stepsize,num_dist,num_flat,CS,posSlider2))
fScanParamLogFile.close()

for i1 in range(num_dist):     
    
    if i1 != 0:
        pmac.EventSendCommandManual(pmac.Controller3, 'Q70=128')
        time.sleep(10)
        
        pmac.Move('GraniteSlab_2single',posSlider2+stepsize*i1,WaitForMove=True)
        time.sleep(1)
        pmac.EventSendCommandManual(pmac.Controller3, 'Q70=127')
        time.sleep(3)

    # Move to start position
    pmac.SetRotSpeed(30)
    time.sleep(0.1)
    
    pmac.Move('Sample_Rot',startangle, WaitForMove=True) 
    time.sleep(0.5)

    # Take reference images Start
    pmac.Move('SampleStage_x', rotCenter+sampleOut)
    nanoScript.SetCurrentName('ref_y'+ str(i1)+"_1", iNumber=i1, imgNumber=0)
    time.sleep(1)
    
    nanoScript.HamaTakeRef(num_img=num_flat)
    
    pmac.Move('SampleStage_x', rotCenter)
    time.sleep(10)
    
    # Start Tomo First Half
    pmac.SetRotSpeed(speed)
    time.sleep(0.1)
    nanoScript.SetCurrentName('img_y' + str(i1) +"_1",iNumber =i1,imgNumber=0)
    
    nanoScript.HamaTakeTomo(target_pos1)
    time.sleep(1 + 1/speed)
    
    # Take reference images
    pmac.SetRotSpeed(30)
    pmac.Move('SampleStage_x', rotCenter+sampleOut)
    nanoScript.SetCurrentName('ref_y'+ str(i1)+"_2", iNumber=i1, imgNumber=0)
    time.sleep(1)
    
    nanoScript.HamaTakeRef(num_img=num_flat)
    
    pmac.Move('SampleStage_x', rotCenter)
   
    
    # Start Tomo Second third
    pmac.Move('Sample_Rot',startangle2, WaitForMove=True)
    pmac.SetRotSpeed(speed)
    time.sleep(1) 
    
    nanoScript.SetCurrentName('img_y' + str(i1)+"_2",iNumber =i1,imgNumber=0)
    
    nanoScript.HamaTakeTomo(target_pos2)
    time.sleep(1 + 1/speed)
    
    # Take reference images
    pmac.SetRotSpeed(30)
    pmac.Move('SampleStage_x', rotCenter+sampleOut)
    nanoScript.SetCurrentName('ref_y'+ str(i1)+"_3", iNumber=i1, imgNumber=0)
    time.sleep(1)
    
    nanoScript.HamaTakeRef(num_img=num_flat)
    
    pmac.Move('SampleStage_x', rotCenter)
    
    
    # Start Tomo third third
    pmac.Move('Sample_Rot',startangle3, WaitForMove=True)
    time.sleep(10)
    pmac.SetRotSpeed(speed)
    time.sleep(0.1)
    nanoScript.SetCurrentName('img_y' + str(i1)+"_3",iNumber =i1,imgNumber=0)
    
    nanoScript.HamaTakeTomo(target_pos3)
    time.sleep(1 + 1/speed)
    
    

# Take reference images at the end
pmac.SetRotSpeed(30)
pmac.Move('SampleStage_x', rotCenter+sampleOut)

nanoScript.SetCurrentName('ref_y'+ str(i1+1), iNumber=i1+1, imgNumber=0)
time.sleep(1)

nanoScript.HamaTakeRef(num_img=num_flat)

pmac.Move('SampleStage_x', rotCenter)

pmac.SetRotSpeed(30)
pmac.Move('Sample_Rot',0)


pmac.EventSendCommandManual(pmac.Controller3, 'Q70=128')
time.sleep(10)

pmac.Move('GraniteSlab_2single',posSlider2,WaitForMove=True)
time.sleep(1)
pmac.EventSendCommandManual(pmac.Controller3, 'Q70=127')
time.sleep(3)

nanoScript.FinishScan()    