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



#scriptname, beamtime, prefix, rotCenter,sampleOut, exptime ,num_images,num_flat,CS = argv
#
#rotCenter = float(rotCenter)
#sampleOut = float (sampleOut)
#num_flat = int(num_flat)
#num_images = int(num_images)
#
#exptime = float (exptime)
#CS = bool(CS)        

       
######Check parameters from here ########################

beamtime = '11008942'
prefix = 'nano3624_mesh_vulcano'

rotCenter = -11.998
sampleOut = 10
num_flat = 20
smearing = 5
exptime = 2.0
speed = None

CS = True

start_x = -0.15
stop_x  = 0.15
start_z = -0.15
stop_z = 0.15
delta = 0.04

######Check parameters until here ########################

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

#fScanParamLogFile = open("T:/current/raw/%s/%s__ScanParam.txt" %(prefix,prefix), 'w')
#fScanParamLogFile.writelines("Scriptname: %s \n Beamtime: %s \n Prefix: %s \n RotCenter: %s \n SampleOut: %s \n Exposure Time: %s \n Number of Images: %s \n Number of Flats: %s \n CloseShutter %s" %(scriptname, beamtime, prefix, rotCenter,sampleOut, exptime ,num_images,num_flat,CS))
#fScanParamLogFile.close()


# Take reference images
pmac.Move('SampleStage_x', rotCenter+sampleOut)

nanoScript.SetCurrentName('ref',iNumber2 =0, imgNumber=0)
time.sleep(1)

nanoScript.HamaTakeRef(num_img=num_flat)

pmac.Move('SampleStage_x', rotCenter)
time.sleep(10)

start_x_pos = pmac.ReadMotorPos("SampleStage_x")
start_z_pos = pmac.ReadMotorPos("SampleStage_z")
posSlider2 = pmac.ReadMotorPos('GraniteSlab_2single')
stepsize = 3

xarray = numpy.arange(start_x, stop_x,delta)
zarray = numpy.arange(start_z,stop_z,delta)
for y in range(2):
    if y != 0:
        pmac.EventSendCommandManual(pmac.Controller3, 'Q70=128')
        time.sleep(10)
        
        pmac.Move('GraniteSlab_2single',posSlider2+stepsize*y,WaitForMove=True)
        time.sleep(1)
        pmac.EventSendCommandManual(pmac.Controller3, 'Q70=127')
        time.sleep(3)
        
    for k, x in enumerate(zarray):
        pmac.Move('SampleStage_z', start_z_pos + x)
        for l,z in enumerate(xarray): 
            pmac.Move('SampleStage_x', start_x_pos+ z)
            nanoScript.SetCurrentName('img_x%03i_z%03i_y%03i' %(k,l,y),iNumber = 0,imgNumber=0)
            nanoScript.TakeImage()
            time.sleep(exptime)
    

    # Take reference images at the end
    pmac.Move('SampleStage_x', rotCenter+sampleOut)
    
    for img_num in range(num_flat):
        nanoScript.SetCurrentName('ref_y%03i'%y ,iNumber2 =0, imgNumber=img_num)        
        nanoScript.TakeImage()
        time.sleep(exptime)
        
    
    time.sleep(1)
    
#    nanoScript.HamaTakeRef(num_img=num_flat)
    
    pmac.Move('SampleStage_x', rotCenter)


nanoScript.FinishScan()    