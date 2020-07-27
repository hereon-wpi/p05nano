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
import p05.tools.misc as misc
###########################################################
#### end initialization ###################################
###########################################################



scriptname, beamtime, prefix, rotCenter,sampleOut, exptime ,num_images,num_flat,CS = argv

rotCenter = float(rotCenter)
sampleOut = float (sampleOut)
num_flat = int(num_flat)
num_images = int(num_images)

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



print('exposure time: ' + str(exptime))
print('number of images: ' + str(num_images))



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
fScanParamLogFile.writelines("Scriptname: %s \n Beamtime: %s \n Prefix: %s \n RotCenter: %s \n SampleOut: %s \n Exposure Time: %s \n Number of Images: %s \n Number of Flats: %s \n CloseShutter %s" %(scriptname, beamtime, prefix, rotCenter,sampleOut, exptime ,num_images,num_flat,CS))
fScanParamLogFile.close()


# Take reference images
if num_flat != 0:
    pmac.Move('SampleStage_x', rotCenter+sampleOut)
    
    nanoScript.SetCurrentName('ref',iNumber2 =0, imgNumber=0)
    time.sleep(1)
    
    nanoScript.HamaTakeRef(num_img=num_flat)
    
    pmac.Move('SampleStage_x', rotCenter)
    time.sleep(10)

# Take Images
nanoScript.SetCurrentName('img',iNumber = 0,imgNumber=0)
time.sleep(1)

nanoScript.HamaTakeRef(num_img = num_images)

time.sleep(0.5)

# Take reference images at the end
if num_flat != 0:
    pmac.Move('SampleStage_x', rotCenter+sampleOut)
    
    nanoScript.SetCurrentName('ref',iNumber2 =0, imgNumber=num_flat)
    time.sleep(1)
    
    nanoScript.HamaTakeRef(num_img=num_flat)
    
    pmac.Move('SampleStage_x', rotCenter)


nanoScript.FinishScan()    