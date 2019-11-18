###########################################################
#### Initialization --- do not change #####################
###########################################################
import p05.devices, p05.nano, p05.tools  ################
import numpy, time, os, PyTango  ################

from sys import argv  ################
from p05.nano.Cameras import PCO_nanoCam, FLIeh2_nanoCam, Hamamatsu_nanoCam, Zyla_nanoCam
###########################################################
#### end initialization ###################################
###########################################################
pmac = p05.devices.PMACdict()  ################
currScript = os.path.basename(__file__)  ################

sPrefix = "hama_test"
sGroup = 'hzg'
sBeamtime = 'test'
exptime = 2

zyla = Zyla_nanoCam(imageDir = '/gpfs/commissioning/scratch_bl/camera_test/', exptime = exptime)

zyla.setExptime(exptime)
zyla.setImageName('ref')
zyla.setImgNumber(10)
for i in range(10):
    zyla.acquireImage()
    print (i)