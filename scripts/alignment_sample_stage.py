###########################################################
#### Initialization --- do not change #####################
###########################################################
import p05.devices, p05.nano, p05.tools  ################
import numpy, time, os, PyTango  ################
pmac = p05.devices.PMACdict()  ################
currScript = os.path.basename(__file__)  ################
from sys import argv  ################
import sys  ################
###########################################################
#### end initialization ###################################
###########################################################

#example of input
#python alignment_sample_stage.py 11003865 1.5 180 5.8 -9 1

scriptname, foldername, exptime, rotangle, rotCenter, sampleOut, alignNo= argv

exptime = float(exptime)
rotangle = float(rotangle)
rotCenter = float(rotCenter)
sampleOut = float(sampleOut)
#specify a new alignment number every time a new alignment task is initiated, otherwise old alignment images will be overwritten
alignNo = int(alignNo)

if rotangle == 180.0:
    rotstart = 108.0
elif rotangle == 90.0:
    rotstart = -90.0
else:
    print """
    Input angle not allowed for alignment.
    Only 180 or 90 are allowed input angles for alignment.
    Exiting program"""
    sys.exit()
    #return None

print """
Starting alignment procedure!
start: %r
end: %r """ % (rotstart, rotangle)

nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(foldername), 'alignment_sample_stage', exptime, \
                                  rotangle, 2, rotCenter, sampleOut, scriptname, \
                                  closeShutter=True, \
                                  useSmarAct=True, \
                                  useStatusServer=True, \
                                  usePCO=False, \
                                  useASAP=True, \
                                  exptime=exptime, \
                                  useHamamatsu=True,\
                                  disableSideBunchReacquisition = False)

# only 2 projections needed for alignment
i1Array = numpy.linspace(rotstart, rotstart-rotangle, num=2)

# nanoScript.TakeDarkImages()
# nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
# time.sleep(30)

for i1 in xrange(i1Array.size):
    print p05.tools.GetTimeString() + ': Rotation position no. %i' % i1

    beamlost = nanoScript.WaitForBeam(PETRAcurrent=100., valreturn=True)

    pmac.Move('Sample_Rot', i1Array[i1])
    time.sleep(0.5)

    # make flat corrected images
    nanoScript.SetCurrentName('align', iNumber="%04d" % (alignNo,), iNumber2=i1Array)
    nanoScript.TakeFlatfieldCorrectedImage(pmac, inpos=rotCenter, refpos=sampleOut, motor='SampleStage_x')
    # nanoScript.TakeImage()
    #settling time for rot stage movement
    time.sleep(0.2)

######################################################
#### Finishing routines  --- do not change  ##########
######################################################
nanoScript.FinishScan()  ##########
######################################################

