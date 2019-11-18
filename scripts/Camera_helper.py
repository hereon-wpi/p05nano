###########################################################
#### Initialization --- do not change #####################
###########################################################
import p05.devices, p05.nano, p05.tools  ################
import time, os, PyTango  ################
from numpy import where
pmac = p05.devices.PMACdict()  ################
currScript = 'H:\_data\programming_python\p05\scripts\Camera_helper.py'  ################
print currScript
nano = p05.nano.NanoPositions()
import pylab as plt
import numpy as np
import numpy
import sys  ################
###########################################################
#### end initialization ###################################
###########################################################


def Test():
    print("ok")
    
    
def Flyscan(scriptname,beamtime ,prefix ,noproj,exptime,rotCenter,sampleOut):        
    binning = 1
    smearing = 1
    exptime = exptime
    speed = None
    if binning == 1:
        overhead = 0.08
        det_size = 2048
    elif binning == 2:
        overhead = 0.06
        det_size = 1024
    elif binning == 4:
        overhead = 0.04
        det_size = 512
    #overhead = 0.04 # for rbf no bin: 0.08, bin2: 0.05, bin4: 0.04
    
    if speed == None:
        speed = smearing * 180./ (numpy.pi *det_size/2*exptime)  # maximal speed of rotation axis for given exptime, maximum 1 pixel smearing
    elif exptime == None:
        exptime = smearing * 180./ (numpy.pi *det_size/2*speed) # exptime for maximal 1 pixel smearing, caculated from speed
    
    #exptime=0.27 # if exptime is set here, uncomment line 44 
    
    if noproj == None: 
        num_images = int(numpy.pi *det_size/2. / smearing *exptime/ (exptime+ overhead))  -1       # maximal number of images
    #num_images = int(180/speed /(exptime+ overhead))  -1  # if exptime set below calculation, uncomment this line!

    startangle = 0
    num_flat = 50
    
    target_pos = 171
    rotangle=180
    
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix)+'_log', exptime, \
                                      rotangle, 1, rotCenter, sampleOut, scriptname, \
                                      closeShutter=True, \
                                      useSmarAct=False, \
                                      useStatusServer=False, \
                                      usePCO=False, \
                                      useASAP=True, \
                                      useASAPcomm=False, \
                                      useHamamatsu=False, \
                                      disableSideBunchReacquisition = True,\
                                      logRotPos = True,\
                                      useHamaTrigger =True)
    
    
    #nanoScript.tBeamShutter.command_inout('CloseOpen_BS_1', 1)
    #time.sleep(30)
    #nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
    #time.sleep(30)
    
    # Move to start position
    pmac.SetRotSpeed(30)
    time.sleep(0.1)
    pmac.Move('Sample_Rot',-11,WaitForMove=True)
    i1Array = numpy.linspace(-10, 170, num=num_images)  
    while pmac.ReadMotorPos('Sample_Rot') > -11:
        time.sleep(0.1)
    
    # take references
    pmac.Move('SampleStage_x', rotCenter+sampleOut)
    for i2 in range(num_flat): 
        nanoScript.SendTriggerHama(position = -20, writeLogs=True)
        time.sleep(exptime+overhead)
    pmac.Move('SampleStage_x', rotCenter)
    time.sleep(15)
    
    # start rotation
    time.sleep(0.1)
    pmac.SetRotSpeed(speed)
    time.sleep(0.1)
    pmac.Move('Sample_Rot',target_pos, WaitForMove=False)
    
    # take images during rotation
    i1Array = numpy.linspace(-10, 170, num=num_images)
    for i1 in range(num_images): 
        #time.sleep(0.5)
        nanoScript.SendTriggerHama(position = i1Array[i1], writeLogs=True)
        print('%s: Acquiring image %s'% (misc.GetTimeString(),i1))
        #time.sleep(0.1)
    
    while pmac.ReadMotorPos('Sample_Rot') < target_pos:
        time.sleep(0.5)
        
    # take references end
    pmac.Move('SampleStage_x', rotCenter+sampleOut)
    for i2 in range(num_flat): 
        nanoScript.SendTriggerHama(position = i1Array[i1], writeLogs=True)
        time.sleep(exptime+overhead)
    
    # Move sample back to rot center, rot angle 0
    pmac.Move('SampleStage_x', rotCenter)
    pmac.SetRotSpeed(20)
    pmac.Move('Sample_Rot',0)
    
    nanoScript.FinishScan()    




def TakeImageSeries(scriptname,beamtime ,prefix ,noproj,exptime,rotCenter,sampleOut,noref):
    nanoScript = p05.nano.NanoScriptHelper(pmac,  currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle=None, noproj=noproj, rotCenter=rotCenter, sampleOut=sampleOut, scriptname=scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True)
    
    for i0 in range(noref):
        pmac.Move('SampleStage_x', rotCenter-sampleOut)
        time.sleep(0.5)
        nanoScript.SetCurrentName('ref', iNumber=None, iNumber2=None, imgNumber=i0)
        nanoScript.TakeImage()
        print(i0)
    
    for i1 in range(noproj): 
        pmac.Move('SampleStage_x', rotCenter)
        time.sleep(0.5)
        nanoScript.SetCurrentName('img', iNumber=None, iNumber2=None, imgNumber=i1)
        nanoScript.TakeImage()
        print(i1)
    
    nanoScript.FinishScan()    
    

def StartScanStandardTest(scriptname,beamtime ,prefix ,rotangle,noproj,exptime,rotCenter,sampleOut):
    """
    Scan for Testing GUI, Camera etc offline!
    Starts a Standard Scan.
    Takes 10 darks before the Scan.
    Takes 10 refs every 50 images. 
    Adds one projection automatically
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac,  currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=False, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True)

    # adding one extra projection at the end of the scan
    noproj = noproj + 1
    
    #PCO naming
    #nanoScript.SetCurrentName('dark', iNumber=None, iNumber2=None,currNum=0)
    #Hama naming
    for i in range(10):
        nanoScript.SetCurrentName('dark', iNumber= i, iNumber2= None,imgNumber=None)
        nanoScript.TakeImage()
    #time.sleep(30)
    #nanoScript.BeamshutterOpen()
    #nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
    time.sleep(20)
    
    i1Array = numpy.linspace(0, rotangle, num=noproj)
    iflat = 0
    pmac.Move('SampleStage_x', rotCenter)
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1   
        if numpy.mod(i1, 300) == 0:
            pmac.Move('SampleStage_x', rotCenter - sampleOut)
            for i4 in xrange(10):
                #PCO naming
                #nanoScript.SetCurrentName('flat', iNumber=None, iNumber2=None,currNum=refcount)
                #Hama naming              
                nanoScript.SetCurrentName('ref', iNumber=i1, iNumber2=i4, imgNumber=iflat)
                #below is standard for both PCO and Hama
                nanoScript.TakeImage()
                iflat += 1
                
            pmac.Move('SampleStage_x', rotCenter)
            
        pmac.Move('Sample_Rot', i1Array[i1])
        time.sleep(0.1)
        #PCO naming
        #nanoScript.SetCurrentName('tomo', iNumber = None, iNumber2 = None, currNum = i1)
        #Hama naming
        nanoScript.SetCurrentName('tomo', iNumber=i1, iNumber2=None, imgNumber=i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()

    #nanoScript.BeamshutterClose()        
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()                     ##########
    return None

def StartScanCameraTest(scriptname,beamtime ,prefix ,rotangle,noproj,exptime,rotCenter,sampleOut):
    """
    Scan for Test Camera
    No motor, no shutter
    Starts a Standard Scan.
    Takes 10 darks before the Scan.
    Takes 10 refs every 50 images. 
    Adds one projection automatically
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac,  currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=True, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True)

    # adding one extra projection at the end of the scan
    noproj = noproj + 1
    #PCO naming
    #nanoScript.SetCurrentName('dark', iNumber=None, iNumber2=None,currNum=0)
    #Hama naming
#     for i in range(10):
#         nanoScript.SetCurrentName('dark', iNumber= i, iNumber2= None,imgNumber=None)
#         print("ok")
#         nanoScript.TakeImage()
    #time.sleep(30)
    #nanoScript.BeamshutterOpen()
    #nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
    #time.sleep(20)
    
    i1Array = numpy.linspace(0, rotangle, num=noproj)
    iflat = 0
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1   
        if numpy.mod(i1, 10) == 0:
            for i4 in xrange(1):
                #PCO naming
                #nanoScript.SetCurrentName('flat', iNumber=None, iNumber2=None,currNum=refcount)
                #Hama naming              
                nanoScript.SetCurrentName('ref', iNumber=i1, iNumber2=i4, imgNumber=iflat)
                #below is standard for both PCO and Hama
                nanoScript.TakeImage()
                iflat += 1
                
        time.sleep(0.1)
        #PCO naming
        #nanoScript.SetCurrentName('tomo', iNumber = None, iNumber2 = None, currNum = i1)
        #Hama naming
        nanoScript.SetCurrentName('tomo', iNumber=i1, iNumber2=None, imgNumber=i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()

    #nanoScript.BeamshutterClose()        
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()                     ##########
    return None

def StartTakeCorrImage(scriptname, beamtime, prefix ,exptime,rotCenter,sampleOut):
    """
    Takes flat field corrected image
    """    
    rotangle = 0
    noproj = 1
    
   
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', beamtime, prefix, exptime, \
                                      rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                      closeShutter=True, \
                                      useSmarAct=True, \
                                      useStatusServer=True, \
                                      usePCO=False, \
                                      useASAP=True, \
                                      useHamamatsu=True,\
                                      disableSideBunchReacquisition = False)
    
    #nanoScript.BeamshutterOpen()
    #time.sleep(20)
    
    # make flat corrected images
    nanoScript.SetCurrentName('img', iNumber2=1)
    nanoScript.TakeFlatfieldCorrectedImage(pmac, inpos=rotCenter, refpos=rotCenter-sampleOut, motor='SampleStage_x')
    #nanoScript.TakeImage()
    #nanoScript.BeamshutterClose()
    
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()  ##########
    ######################################################

def StartScanStandard(scriptname,beamtime ,prefix,noproj,exptime,rotCenter,sampleOut, rotangle=180, noref=10,refpos= 100,startangle=0,closeShutter=False):
    """
    Starts a Standard Scan.
    Takes 10 darks before the Scan.
    Takes 10 refs every images. 
    Adds one projection automatically
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=closeShutter, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True)


    nanoScript.TakeDarkImages(num=10)

    nanoScript.BeamshutterOpen()
    nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
    time.sleep(5)
    
    i1Array = numpy.linspace(startangle, rotangle, num=noproj)
    iflat = 0
    pmac.Move('SampleStage_x', rotCenter)
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1   
        if numpy.mod(i1, refpos) == 0:
            pmac.Move('SampleStage_x', rotCenter-sampleOut)
            for i4 in xrange(noref):       
                nanoScript.SetCurrentName('ref', iNumber=i1, iNumber2=i4, imgNumber=iflat)
                print p05.tools.GetTimeString() + ': Acquiring flat no. %i' %i4   
                nanoScript.TakeImage()
                iflat += 1                
            pmac.Move('SampleStage_x', rotCenter)
        pmac.Move('Sample_Rot', i1Array[i1])
        time.sleep(0.1)
        nanoScript.SetCurrentName('tomo', iNumber=i1, iNumber2=None, imgNumber=i1)
        nanoScript.TakeImage()

    #nanoScript.BeamshutterClose()        
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()                     ##########
    return None

def StartScanNoDarks(scriptname,beamtime ,prefix ,rotangle,noproj,exptime,rotCenter,sampleOut):
    """
    Starts a Standard Scan.
    Takes 10 darks before the Scan.
    Takes 10 refs every 50 images. 
    Adds one projection automatically
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True)

    # adding one extra projection at the end of the scan
    noproj = noproj + 1
    
    #PCO naming
    #nanoScript.SetCurrentName('dark', iNumber=None, iNumber2=None,currNum=0)
    #Hama naming
    #nanoScript.TakeDarkImages(num=10)
    #time.sleep(30)
    nanoScript.BeamshutterOpen()
    nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
    time.sleep(20)
    
    i1Array = numpy.linspace(0, rotangle, num=noproj)
    iflat = 0
    pmac.Move('SampleStage_x', rotCenter)
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1   
        if numpy.mod(i1, 50) == 0:
            pmac.Move('SampleStage_x', rotCenter-sampleOut)
            for i4 in xrange(10):
                #PCO naming
                #nanoScript.SetCurrentName('flat', iNumber=None, iNumber2=None,currNum=refcount)
                #Hama naming              
                nanoScript.SetCurrentName('flat', iNumber=i1, iNumber2=i4, imgNumber=iflat)
                print p05.tools.GetTimeString() + ': Acquiring flat no. %i' %i4   
                #below is standard for both PCO and Hama
                nanoScript.TakeImage()
                iflat += 1                
            pmac.Move('SampleStage_x', rotCenter)
        pmac.Move('Sample_Rot', i1Array[i1])
        time.sleep(0.1)
        #PCO naming
        #nanoScript.SetCurrentName('tomo', iNumber = None, iNumber2 = None, currNum = i1)
        #Hama naming
        nanoScript.SetCurrentName('tomo', iNumber=i1, iNumber2=None, imgNumber=i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()

    #nanoScript.BeamshutterClose()        
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()                     ##########
    return None

def StartScanIntegrated(scriptname,beamtime ,prefix ,rotangle,noproj,exptime,rotCenter,sampleOut,integNo,noref=10,refpos= 100,startangle=0,closeShutter=False):
    """
    Starts a Standard Scan.
    Takes 10 darks before the Scan.
    Takes 10 refs every 50 images. 
    Adds one projection automatically\
    IntegNo gives the number of repeated acquisitions for each projection
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=closeShutter, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True)
    noproj = noproj 

    #nanoScript.TakeDarkImages(num=10) # darks currently not working
    #time.sleep(30)
    #nanoScript.BeamshutterOpen()
    #nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
    #time.sleep(20)
    
    i1Array = numpy.linspace(startangle, rotangle, num=noproj)
    iflat = 0
    itomo = 0
    pmac.Move('SampleStage_x', rotCenter)
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1   
        if numpy.mod(i1, refpos) == 0:
            pmac.Move('SampleStage_x', rotCenter-sampleOut)
            for i4 in xrange(noref):             
                nanoScript.SetCurrentName('flat', iNumber=i1, iNumber2=i4, imgNumber=iflat)
                print p05.tools.GetTimeString() + ': Acquiring flat no. %i' %i4   
                nanoScript.TakeImage()
                iflat += 1                
            pmac.Move('SampleStage_x', rotCenter)
            time.sleep(60)
        pmac.Move('Sample_Rot', i1Array[i1])
        time.sleep(0.1)
        for i in range(integNo):
            nanoScript.SetCurrentName('tomo', iNumber=i1, iNumber2=i, imgNumber=itomo)
            nanoScript.TakeImage()
            itomo += 1
            print(itomo)
            
    pmac.Move('SampleStage_x', rotCenter)
    pmac.Move('Sample_Rot',0)
    
    #nanoScript.BeamshutterClose()        
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()                     ##########
    return None




def StartScanIntegrated_Continued(scriptname,beamtime ,prefix ,rotangle,noproj,exptime,rotCenter,sampleOut,integNo,startImage):
    """
    Continues a Standard Scan with several Images at one rotPos.
    Start Image should be the last recorded image no (not FileName)
    Takes 10 darks before the Scan.
    Takes 10 refs every 50 images. 
    Adds one projection automatically\
    IntegNo gives the number of repeated acquisitions for each projection
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True)

    nanoScript.TakeDarkImages(num=10)
    #time.sleep(30)
    nanoScript.BeamshutterOpen()
    nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
    time.sleep(20)
    
    i2Array = numpy.linspace(0, rotangle, num=noproj)
    i1Array = i2Array[startImage:]
    iflat = 0
    itomo = startImage * integNo
    pmac.Move('SampleStage_x', rotCenter)
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1   
        if numpy.mod(i1, 50) == 0:
            pmac.Move('SampleStage_x', rotCenter-sampleOut)
            for i4 in xrange(10):
                #PCO naming
                #nanoScript.SetCurrentName('flat', iNumber=None, iNumber2=None,currNum=refcount)
                #Hama naming              
                nanoScript.SetCurrentName('flat', iNumber=i1, iNumber2=i4, imgNumber=iflat)
                print p05.tools.GetTimeString() + ': Acquiring flat no. %i' %i4   
                #below is standard for both PCO and Hama
                nanoScript.TakeImage()
                iflat += 1                
            pmac.Move('SampleStage_x', rotCenter)
        pmac.Move('Sample_Rot', i1Array[i1])
        time.sleep(0.1)
        #PCO naming
        #nanoScript.SetCurrentName('tomo', iNumber = None, iNumber2 = None, currNum = i1)
        for i in range(integNo):
            
            #Hama naming
            nanoScript.SetCurrentName('tomo', iNumber=i1, iNumber2=i, imgNumber=itomo)
            #below is standard for both PCO and Hama
            nanoScript.TakeImage()
            print(itomo)
            itomo += 1
            
            


    #nanoScript.BeamshutterClose()        
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()                     ##########
    return None



def StartScan_RefEnd(scriptname,beamtime ,prefix ,rotangle,noproj,exptime,rotCenter,sampleOut):
    '''
    Starts a scan, takes ref at the end
    '''
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True)

    # adding one extra projection at the end of the scan
    noproj = noproj + 1
    
    nanoScript.SetCurrentName('dark', imgNumber=0)
    nanoScript.TakeDarkImages(num=10)
    time.sleep(30)
    
    nanoScript.BeamshutterOpen()
    nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
    time.sleep(20)
    iflat =0
    for i4 in xrange(20):
        #PCO naming
        #nanoScript.SetCurrentName('flat', iNumber=None, iNumber2=None,currNum=refcount)
        #Hama naming
        nanoScript.SetCurrentName('ref', iNumber=i4, iNumber2=None, imgNumber=iflat)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
        iflat += 1
    i1Array = numpy.linspace(0, rotangle, num=noproj)
    pmac.Move('SampleStage_x', rotCenter)
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1
                   
        pmac.Move('Sample_Rot', i1Array[i1])
        time.sleep(2)
        #PCO naming
        #nanoScript.SetCurrentName('tomo', iNumber = None, iNumber2 = None, currNum = i1)
        #Hama naming
        nanoScript.SetCurrentName('tomo', iNumber=i1, iNumber2=None, imgNumber=i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
        #nanoScript.SetCurrentName('ref', iNumber = None, iNumber2 = None, currNum = i1)
        time.sleep(0.2)
        
    # Take flat field Images at the end of the scan    
    for i4 in xrange(20):
        #PCO naming
        #nanoScript.SetCurrentName('flat', iNumber=None, iNumber2=None,currNum=refcount)
        #Hama naming
        nanoScript.SetCurrentName('ref', iNumber=i4, iNumber2=None, imgNumber=iflat)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
        iflat += 1
    #nanoScript.BeamshutterClose()        
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()                     ##########
    return None

def StartScanStability_ref(scriptname,beamtime ,prefix ,rotangle,noproj,exptime,rotCenter,sampleOut):
    """
    Starts a stability test with rotation. Refs are taken at the end.
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True)

    # adding one extra projection at the end of the scan
    noproj = noproj + 1
    
    #PCO naming
    #nanoScript.SetCurrentName('dark', iNumber=None, iNumber2=None,currNum=0)
    #Hama naming
    #nanoScript.SetCurrentName('dark', imgNumber=0)
    #below is standard for both PCO and Hama
    #nanoScript.TakeDarkImages(num=10)
    #time.sleep(30)
    
    #nanoScript.BeamshutterOpen()
    #nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
    #time.sleep(20)
    
    i1Array = numpy.linspace(0, rotangle, num=noproj)
    iflat = 0
    pmac.Move('SampleStage_x', rotCenter)
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1   
        
        pmac.Move('Sample_Rot', i1Array[i1])
        #PCO naming
        #nanoScript.SetCurrentName('tomo', iNumber = None, iNumber2 = None, currNum = i1)
        #Hama naming
        nanoScript.SetCurrentName('tomo', iNumber=i1, iNumber2=None, imgNumber=i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
        #nanoScript.SetCurrentName('ref', iNumber = None, iNumber2 = None, currNum = i1)
        time.sleep(0.2)
    
    pmac.Move('SampleStage_x', rotCenter-sampleOut)
    time.sleep(20)
    for i4 in xrange(10):
        #PCO naming
        #nanoScript.SetCurrentName('flat', iNumber=None, iNumber2=None,currNum=refcount)
        #Hama naming
        nanoScript.SetCurrentName('flat', iNumber=i4, iNumber2=None, imgNumber=iflat)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
        iflat += 1
    nanoScript.BeamshutterClose()        
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()                     ##########
    return None

def StartStability_ref(scriptname,beamtime ,prefix ,rotangle, noproj, exptime, rotCenter,sampleOut):
    """
    Starts a static stability test. Refs are taken at the end.
    """
    
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True)

    # adding one extra projection at the end of the scan
    
    #nanoScript.BeamshutterOpen()
    #nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
    #time.sleep(20)
    
    i1Array = numpy.linspace(0, rotangle, num=noproj)
    iflat = 0
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1
        #pmac.Move('SampleStage_x', rotCenter)
       

        #PCO naming
        #nanoScript.SetCurrentName('tomo', iNumber = None, iNumber2 = None, currNum = i1)
        #Hama naming
        nanoScript.SetCurrentName('img', iNumber=i1, iNumber2=None, imgNumber=i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
        #nanoScript.SetCurrentName('ref', iNumber = None, iNumber2 = None, currNum = i1)
        #time.sleep(10)
    
    pmac.Move('SampleStage_x', rotCenter-sampleOut)
    time.sleep(20)
    for i4 in xrange(10):
        #PCO naming
        #nanoScript.SetCurrentName('flat', iNumber=None, iNumber2=None,currNum=refcount)
        #Hama naming
        nanoScript.SetCurrentName('ref', iNumber=i4, iNumber2=None, imgNumber=iflat)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
        iflat += 1
    
    nanoScript.BeamshutterClose()        
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()                     ##########
    return None

def StartScanTP(scriptname,beamtime ,prefix ,rotangle,noproj,exptime,rotCenter,sampleOut,tp_in_z,tp_out_z):
    """
    For focusing the TP in front of the scintillator with the PCO 
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=True, \
                                  useASAP=True, \
                                  useHamamatsu=False, \
                                  disableSideBunchReacquisition = True)

    sm_z = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha7') ## DetApxR = TP z 
    
    nanoScript.BeamshutterOpen()
    time.sleep(20)
    
    for i1 in xrange(noproj):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1
        
        sm_z.write_attribute('Position', tp_in_z)
        time.sleep(5)
        # naming for Hama
        #nanoScript.SetCurrentName('ref', iNumber=i1, iNumber2=None,imgNumber=i1)
        # naming for PCO
        nanoScript.SetCurrentName('img', iNumber = None, iNumber2 = None, currNum = i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
        
        sm_z.write_attribute('Position', tp_out_z)
        time.sleep(5)
        # naming for Hama
        #nanoScript.SetCurrentName('img', iNumber=i1, iNumber2=None,imgNumber=i1)
        # naming for PCO
        nanoScript.SetCurrentName('ref', iNumber = None, iNumber2 = None, currNum = i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
    
    nanoScript.BeamshutterClose()        
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()                     ##########
    ######################################################
    return None

def StartScanFocus(scriptname,beamtime,prefix,rotangle, noproj, exptime, rotCenter, sampleOut,sliderpos1,sliderpos2):
    """ Starts focal scan with PCO
        moves GraniteSlab 2 
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                              rotangle, noproj, rotCenter, sampleOut, scriptname, \
                              closeShutter=False, \
                              useSmarAct=False, \
                              useStatusServer=False, \
                              usePCO=False, \
                              useASAP=True, \
                              useHamamatsu=True, \
                              disableSideBunchReacquisition = True)
    i1Array = numpy.linspace(sliderpos1,sliderpos2, num = noproj)
    #nanoScript.BeamshutterOpen()
    #time.sleep(20)
    pmac.Move('SampleStage_x', rotCenter-sampleOut)    
    nanoScript.SetCurrentName('ref', iNumber = None, iNumber2 = None, imgNumber= 0)
    #below is standard for both PCO and Hama
    nanoScript.TakeImage()
    pmac.Move('SampleStage_x', rotCenter)  
    
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1
        pmac.Move('GraniteSlab_2single', i1Array[i1])
    
        #pmac.Move('SampleStage_x', rotCenter-sampleOut)    
        #nanoScript.SetCurrentName('ref', iNumber = None, iNumber2 = None, imgNumber= i1)
        #below is standard for both PCO and Hama
        #nanoScript.TakeImage()
        
        
        time.sleep(1)  
        nanoScript.SetCurrentName('img', iNumber = None, iNumber2 = None, imgNumber = i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
    
        #time.sleep(1.5)
    print('scan finished')
    return None

def StartScanFocusSample(scriptname,beamtime,prefix,rotangle, noproj, exptime, rotCenter, sampleOut):
    """ Starts focal scan with PCO
        moves Sample SF +- 2
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                              rotangle, noproj, rotCenter, sampleOut, scriptname, \
                              closeShutter=False, \
                              useSmarAct=False, \
                              useStatusServer=False, \
                              usePCO=False, \
                              useASAP=True, \
                              useHamamatsu=True, \
                              disableSideBunchReacquisition = True)
    i1Array = numpy.linspace(-2,2, num = noproj)
    step_size = (2+2)*1./noproj
    for i in range(4):
        nano.MvrSampleY(-0.5)
    #nanoScript.BeamshutterOpen()
    #time.sleep(20)
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1
        nano.MvrSampleY(step_size)
        
        pmac.Move('SampleStage_x', rotCenter-sampleOut)
        time.sleep(2)      
        nanoScript.SetCurrentName('ref', iNumber = None, iNumber2 = None, imgNumber= i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
        
        pmac.Move('SampleStage_x', rotCenter)  
        time.sleep(2)  
        nanoScript.SetCurrentName('img', iNumber = None, iNumber2 = None, imgNumber = i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
    for i in range(4):
        nano.MvrSampleY(-0.5)
    
    return None

def StartScanBrilleMesh(scriptname,beamtime,prefix,rotangle, noproj, exptime, rotCenter, sampleOut):
    """ Starts focal scan with PCO
        moves Brille
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                              rotangle, noproj, rotCenter, sampleOut, scriptname, \
                              closeShutter=False, \
                              useSmarAct=False, \
                              useStatusServer=False, \
                              usePCO=False, \
                              useASAP=True, \
                              useHamamatsu=True, \
                              disableSideBunchReacquisition = True)
    i1Array = numpy.linspace(-1686, -1694, num = 8)
    i2Array = numpy.linspace(24, 32, num = 8)
    BrilleZ = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha10')
    BrilleX = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha11')
    
    pmac.Move('SampleStage_x', rotCenter-sampleOut)
    iflat=0
    for i4 in xrange(10):
        #PCO naming
        #nanoScript.SetCurrentName('flat', iNumber=None, iNumber2=None,currNum=refcount)
        #Hama naming
        nanoScript.SetCurrentName('ref', iNumber=i4, iNumber2=None, imgNumber=iflat)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
        iflat += 1

    pmac.Move('SampleStage_x', rotCenter)  
    
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1
        
        BrilleZ.write_attribute('Position', i1Array[i1])
        for i2 in range(i2Array.size):
            BrilleX.write_attribute('Position', i2Array[i2])
            time.sleep(0.5)
            nanoScript.SetCurrentName('img', iNumber = None, iNumber2 = None)
            nanoScript.TakeImage()    
    
    pmac.Move('SampleStage_x', rotCenter-sampleOut)    
    nanoScript.SetCurrentName('ref', iNumber = None, iNumber2 = None, imgNumber=1)
    #below is standard for both PCO and Hama
    nanoScript.TakeImage()
    pmac.Move('SampleStage_x', rotCenter)  
    
    return None

def StartScanFocusHama(scriptname,beamtime,prefix,rotangle, noproj, exptime, rotCenter, sampleOut,sliderpos1,sliderpos2):
    """ Starts focal scan with Hamamatsu
        moves GraniteSlab 2 
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                              rotangle, noproj, rotCenter, sampleOut, scriptname, \
                              closeShutter=False, \
                              useSmarAct=False, \
                              useStatusServer=False, \
                              usePCO=False, \
                              useASAP=True, \
                              useHamamatsu=True, \
                              disableSideBunchReacquisition = True)
    i1Array = numpy.linspace(sliderpos1,sliderpos2, num = noproj)
    #nanoScript.BeamshutterOpen()
    #time.sleep(20)
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1
        pmac.Move('GraniteSlab_2single', i1Array[i1])
    
        pmac.Move('SampleStage_x', rotCenter-sampleOut)    
        nanoScript.SetCurrentName('ref', iNumber = None, iNumber2 = None, imgNumber= i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
        
        pmac.Move('SampleStage_x', rotCenter)    
        nanoScript.SetCurrentName('img', iNumber = None, iNumber2 = None, imgNumber = i1)
        #below is standard for both PCO and Hama
        nanoScript.TakeImage()
    
        time.sleep(1.5)
    return None


def StartScanFocusSF2(scriptname,beamtime,prefix,rotangle, noproj, exptime, rotCenter, sampleOut,sf2pos1,sf2pos2):
    """ Starts focal scan with PCO
        moves Space Fab 2 (FZP)
    """
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                              rotangle, noproj, rotCenter, sampleOut, scriptname, \
                              closeShutter=False, \
                              useSmarAct=False, \
                              useStatusServer=False, \
                              usePCO=True, \
                              useASAP=True, \
                              useHamamatsu=False, \
                              disableSideBunchReacquisition = True)
    i1Array = numpy.linspace(sf2pos1,sf2pos2, num = noproj)
    nanoScript.BeamshutterOpen()
    time.sleep(20)
    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Acquiring image no. %i' %i1
        pmac.Move('OpticsSF2_y', i1Array[i1])
    
        pmac.Move('SampleStage_x', rotCenter-sampleOut)    
        nanoScript.SetCurrentName('ref', iNumber = None, iNumber2 = None, currNum = i1)
        nanoScript.TakeImage()
        
        pmac.Move('SampleStage_x', rotCenter)    
        nanoScript.SetCurrentName('img', iNumber = None, iNumber2 = None, currNum = i1)
        nanoScript.TakeImage()
    
        time.sleep(1.5)
    
    nanoScript.BeamshutterClose()        
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    nanoScript.FinishScan()                     ##########
    ######################################################
    return None

def alignment_sample_stage(scriptname, beamtime,prefix, rotangle, exptime, rotCenter, sampleOut, rotstart, alignNo):
    """ Script acquires two different images at either 0 and 180 (for Rx) 
    or at -0.5 and +0.5 (for Ry) from the rotationStart position.
    
    @param exptime: exposure time in seconds
    @param rotangle: rotation angle either 180 (for Rx) or around 0.5 (for Ry) - depending on the FOV of the camera
    @param rotstart: rotstart value, which is 108 for 0 to 180 degrees (range: 108 to -72)  of Rx alignment or e.g. 108.23 (pin on the right side) for Ry alignment (e.g. range: 108.23 to 107.71)
    @param sampleOut: sampleOut position in Rotation values (using motor: SampleRot), in order to acquire the flat-field
    @param alignNo: Alignment Number is used as a prefix for the saved image file. Specify a new alignment number (alginNo) every time a new alignment task is initiated, otherwise old alignment images 
    will be overwritten."""

    exptime = float(exptime)
    rotangle = float(rotangle)
    rotstart = float(rotstart)
    sampleOut = float(sampleOut)
    alignNo = int(alignNo)
    
    rotCenter = rotstart
    
    print """
    Starting alignment procedure!
    start: %r
    end: %r """ % (rotstart, rotangle)
    
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), 'alignment_sample_stage', exptime, \
                                      rotangle, 2, rotCenter, sampleOut, scriptname, \
                                      closeShutter=True, \
                                      useSmarAct=True, \
                                      useStatusServer=True, \
                                      usePCO=False, \
                                      useASAP=True, \
                                      useHamamatsu=False,\
                                      usePixelLink=True,\
                                      disableSideBunchReacquisition = False)
    
    # only 2 projections needed for alignment
    i1Array = numpy.linspace(rotstart, rotstart+rotangle, num=2)
    
    #nanoScript.BeamshutterOpen()

    for i1 in xrange(i1Array.size):
        print p05.tools.GetTimeString() + ': Rotation position no. %i' % i1
    
        beamlost = nanoScript.WaitForBeam(PETRAcurrent=100., valreturn=True)
    
        # make flat corrected images
        nanoScript.SetCurrentName('align' + "%04d" % (alignNo,), iNumber2=i1Array[i1])
        nanoScript.TakeFlatfieldCorrectedImage(pmac, inpos=i1Array[i1], refpos=i1Array[i1]-10, motor='Sample_Rot')
        # nanoScript.TakeImage()
        #settling time for rot stage movement
        time.sleep(0.2)
    
        
        nanoScript.FinishScan()

def TakeDarkImages(scriptname,beamtime ,prefix ,rotangle,noproj,exptime,rotCenter,sampleOut):
    # Tango Server for Shutter changed! ICS Panel problem
    nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(beamtime), str(prefix), exptime, \
                                  rotangle, noproj, rotCenter, sampleOut, scriptname, \
                                  closeShutter=False, \
                                  useSmarAct=False, \
                                  useStatusServer=False, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  useHamamatsu=True, \
                                  disableSideBunchReacquisition = True)
    print('~~~~~~~~~ !!!! ~~~~~~~~~ Ready to take dark images?')
    tmp = raw_input('~~~~~~~~~ !!!! ~~~~~~~~~ Continue? y / n: ')
    if tmp not in ['yes', 'Y', 'y']:
        print('Aborting...')
        exit()
    
    time.sleep(1)
    nanoScript.SetCurrentName('dark', iNumber=None, iNumber2=None)
    for i in range(10):
        #nanoScript.SetCurrentName('dark', iNumber=None, iNumber2=None, imgNumber=i)
        nanoScript.TakeImage()     
    ######################################################
    #### Finishing routines  --- do not change  ##########
    ######################################################
    print('~~~~~~~~~ !!!! ~~~~~~~~~ Did you open the shutter?')
    tmp = raw_input('~~~~~~~~~ !!!! ~~~~~~~~~ Continue? y / n: ')
    if tmp not in ['yes', 'Y', 'y']:
        print('Aborting...')
        exit()
    
    nanoScript.FinishScan()                     ##########
    ######################################################
    return None

# please re-write the code so that exposure time, RotCenter, SampleOut are specified input parameters (these param. can be specified in the GUI)
#Also if the angle 0 180 is not determined we can also use the same script for 0 to 90 or -7 to +7.
def take0180(beamtime ,prefix,plot= True): 
    """
    Takes Images at rot 0, rot 180 and ref
    Calculates flat field corrected image and adds 0 and 180
    Saves the result
    Optional show image   
    """
    useASAP = False
    
    if useASAP:
        #self.sPath = 't:/current/raw/%s/' %(self.sPrefix)
        path = 't:/current/raw/%s/' %(prefix)
    else:
        path = 'w:/%s/%s/%s/' %('hzg', beamtime, prefix)

    thama= p05.nano.Hamamatsu_nanoCam(imageDir=path)
    
    pmac.Move('Sample_Rot',0,WaitForMove=True)
    thama.acquireImage()
    img0 = thama.getImage()
    
    pmac.Move('Sample_Rot',180,WaitForMove=True)
    thama.acquireImage()
    img180 = thama.getImage()
    
    pmac.MoveRel('SampleStage_x', 0.1)
    thama.acquireImage()
    ref = thama.getImage()
    pmac.MoveRel('SampleStage_x', -0.1)
    img0_corr = np.array(img0,dtype=np.float32) /np.array(ref,dtype=np.float32)
    img180_corr =np.array(img180,dtype=np.float32) / np.array(ref,dtype=np.float32)
    image = img0_corr + img180_corr
    # When Beamtime: change path to imagedir
    plt.matplotlib.image.imsave(path +'Image_0.tiff', img0_corr.transpose(), cmap = 'gray')
    # TO DO!: we should probably flip the Image_180 before subtracting
    plt.matplotlib.image.imsave(path +'Image_180.tiff', img180_corr.transpose(), cmap = 'gray')
    plt.matplotlib.image.imsave(path +'Image_0_180.tiff', image.transpose(), cmap = 'gray')
    if plot:
        plt.imshow(image)
        plt.show()



def InitSliders():
    ans = raw_input("Do you really want to start initilizing the sliders? Y or N?")
                    
    if ans == 'Y' or ans == 'y': #reply == QtGui.QMessageBox.Yes:
        #Controller 1
        pmac.EventSendCommandManual(pmac.Controller1, '&2Q70=1')
        pmac.checkInit(pmac.Controller1)
        ans2 = raw_input("Movement done?")
        
        if ans2 == 'Y' or ans2 == 'y' or ans2 == 'yes':
            pmac.EventSendCommandManual(pmac.Controller1, 'Q70=9')
            pmac.checkInit(pmac.Controller1)
            ans12 = raw_input("Movement done?")
            
            if ans12 == 'Y' or ans12 == 'y' or ans12 == 'yes':
                #Controller 2
                pmac.EventSendCommandManual(pmac.Controller2, '&2Q70=1')
                pmac.checkInit(pmac.Controller2)
                ans3 = raw_input("Movement done?")
            
                if ans3 == 'Y' or ans3 == 'y' or ans3 == 'yes':
                    #Controller 4
                    pmac.EventSendCommandManual(pmac.Controller4, '&2Q70=9')
                    pmac.checkInit(pmac.Controller4)
                    
                    ans4 = raw_input("Movement done?")
            
                    if ans4 == 'Y' or ans4 == 'y' or ans4 == 'yes':
                        #Controller 3
                        pmac.EventSendCommandManual(pmac.Controller3, '&2Q70=9')
                        pmac.checkInit(pmac.Controller3)
                        
                        ans5 = raw_input("Movement done?")
            
                        if ans5 == 'Y' or ans5 == 'y' or ans5 == 'yes':
                            #Controller 4
                            pmac.EventSendCommandManual(pmac.Controller4, '&2Q70=1')
                            pmac.checkInit(pmac.Controller4)
                            
                            ans6 = raw_input("Movement done?")
            
                            if ans6 == 'Y' or ans6 == 'y' or ans6 == 'yes':
                                #Controller 7
                                pmac.EventSendCommandManual(pmac.Controller7, '&2Q70=1')
                                pmac.checkInit(pmac.Controller7)
                                
                                ans7 = raw_input("Movement done?")
            
                                if ans7 == 'Y' or ans7 == 'y' or ans7 == 'yes':
                                    pmac.EventSendCommandManual(pmac.Controller7, 'Q70=9')
                                    pmac.checkInit(pmac.Controller7)
                                    
                                    ans8 = raw_input("Movement done?")
            
                                    if ans8 == 'Y' or ans8 == 'y' or ans8 == 'yes':
                                        #Controller 5
                                        pmac.EventSendCommandManual(pmac.Controller5, '&2Q70=5')
                                        pmac.checkInit(pmac.Controller5)
            # Message Box asking if air bearing axis is in right position
            #reply =  QtGui.QMessageBox.question(self, 'Warning!',
            #    "Is the rotation stage in position? (Please double-check that the reference lines on the rotation stage are in position.)", QtGui.QMessageBox.Yes | 
            #   QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            #if reply == QtGui.QMessageBox.Yes:
                                        ans9 = raw_input("Movement done?")
                                        if ans9 == 'Y' or ans9 == 'y':
                                            ans_rot = raw_input("Is the rotation stage in position? (Please double-check that the reference lines on the rotation stage are in position.)")
                                            if ans_rot == 'Y' or ans_rot == 'y':
                                                #Controller 5
                                                pmac.EventSendCommandManual(pmac.Controller5, 'Q70=9')
                                                pmac.checkInit(pmac.Controller5)
                                                ans9 = raw_input("Movement done?")
                                                if ans9 == 'Y' or ans9 == 'y':
                                                    pmac.EventSendCommandManual(pmac.Controller5, 'Q70=1')
                                                    pmac.checkInit(pmac.Controller5)
                                                    ans9 = raw_input("Movement done?")
                                                    if ans9 == 'Y' or ans9 == 'y':
                                                        pmac.EventSendCommandManual(pmac.Controller5, 'Q70=29')
                                                        pmac.checkInit(pmac.Controller5)
                                                        ans9 = raw_input("Movement done?")
                                                        if ans9 == 'Y' or ans9 == 'y':
                                                            #Controller 6
                                                            pmac.EventSendCommandManual(pmac.Controller6, '&2Q70=1')
                                                            pmac.checkInit(pmac.Controller6)
                                                            ans9 = raw_input("Movement done?")
                                                            if ans9 == 'Y' or ans9 == 'y':
                                                                #Controller 3
                                                                pmac.EventSendCommandManual(pmac.Controller3, '&2Q70=5')
                                                                pmac.checkInit(pmac.Controller3)
                                                                ans9 = raw_input("Movement done?")
                                                                if ans9 == 'Y' or ans9 == 'y':
                                                                    pmac.EventSendCommandManual(pmac.Controller3, 'Q70=1')
                                                                    pmac.checkInit(pmac.Controller3)
                                                                    print "Initialization successfully finished!"
                                                                #QtGui.QMessageBox.Information(self, 'Finished!')
                                            else:
                                                print("Initilization aborted!")
                
        else:
            print("Initilization aborted!")
        
        print("Program Finished!")
        return None

def closeShutter():
    shutter = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/shutter/all')
    shutter.command_inout('CloseOpen_BS_1', 0)
    print('Beamshutter Closed')

def warning():
    print('~~~~~~~~~ !!!! ~~~~~~~~~ Attention: Live image application stopped?')
    tmp = raw_input('~~~~~~~~~ !!!! ~~~~~~~~~ Continue? y / n: ')
    if tmp not in ['yes', 'Y', 'y']:
        print('Aborting...')
        exit()
    return None
        
def warning_ShutterOpen():
    print('~~~~~~~~~ !!!! ~~~~~~~~~Shutter Opened?')
    tmp = raw_input('~~~~~~~~~ !!!! ~~~~~~~~~ Continue? y / n: ')
    if tmp not in ['yes', 'Y', 'y']:
        print('Aborting...')
        exit()
    return None
