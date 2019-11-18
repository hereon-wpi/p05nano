###########################################################
#### Initialization --- do not change #####################
###########################################################
import p05.devices, p05.nano, p05.tools  ################
import numpy, time, os, PyTango,pylab  ################
#pmac = p05.devices.PMACdict()  ################
#currScript = os.path.basename(__file__)  ################
from sys import argv  ################
import sys  ################
from numpy import shape
###########################################################
#### end initialization ###################################
###########################################################

#example of input
#python alignment_sample_stage.py nanoXTM_117032 1.5 180 5.8 -9 1

# scriptname, foldername, exptime, rotangle, rotCenter, sampleOut, alignNo= argv
# 
# exptime = float(exptime)
# rotangle = float(rotangle)
# rotCenter = float(rotCenter)
# sampleOut = float(sampleOut)
# alignNo = int(alignNo)

# if rotangle == 180.0:
#     rotstart = 0.0
# elif rotangle == 90.0:
#     rotstart = -90.0
# else:
#     print """
#     Input angle not allowed for alignment.
#     Only 180 or 90 are allowed input angles for alignment.
#     Exiting program"""
#     sys.exit()
#     #return None
# 
# print """
# Starting alignment procedure!
# start: %r
# end: %r """ % (rotstart, rotangle)
# 
# nanoScript = p05.nano.NanoScriptHelper(pmac, currScript, 'hzg', str(foldername), 'alignment', exptime, \
#                                   rotangle, 2, rotCenter, sampleOut, scriptname, \
#                                   closeShutter=True, \
#                                   useSmarAct=True, \
#                                   useStatusServer=True, \
#                                   usePCO=False, \
#                                   useASAP=True, \
#                                   exptime=exptime, \
#                                   useHamamatsu=True,\
#                                   disableSideBunchReacquisition = False)
# 
# # only 2 projections needed for alignment
# i1Array = numpy.linspace(rotstart, rotangle, num=2)
# 
# # nanoScript.TakeDarkImages()
# # nanoScript.tBeamShutter.command_inout('CloseOpen_BS_2', 1)
# # time.sleep(30)
# 
# for i1 in xrange(i1Array.size):
#     print p05.tools.GetTimeString() + ': Rotation position no. %i' % i1
# 
#     beamlost = nanoScript.WaitForBeam(PETRAcurrent=100., valreturn=True)
# 
#     pmac.Move('Sample_Rot', i1Array[i1])
#     time.sleep(0.5)
# 
#     # make flat corrected images
#     nanoScript.SetCurrentName('align', iNumber="%04d" % (alignNo,), iNumber2=i1Array)
#     nanoScript.TakeFlatfieldCorrectedImage(pmac, inpos=rotCenter, refpos=sampleOut, motor='SampleStage_x')
#     # nanoScript.TakeImage()
#     #settling time for rot stage movement
#     time.sleep(0.2)
# 
# ######################################################
# #### Finishing routines  --- do not change  ##########
# ######################################################
# nanoScript.FinishScan()  ##########
# ######################################################

path = r'T:\current\raw\nano1205_Camera_Focus_X2Z2'
file_name = r'\nano1205_Camera_Focus_X2Z2_img_0003.raw' 
a = numpy.fromfile(path+file_name)
tmp = numpy.fromstring(a, dtype=numpy.uint16).byteswap()
            
image = (tmp).reshape(2048, 2048)
imagesize = (2048, 2048)
print numpy.shape(image)

pylab.imshow(image,cmap='Greys',vmin=0,vmax=40000)
pylab.colorbar()
pylab.show()
