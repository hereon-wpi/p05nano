###########################################################
#### Initialization --- do not change #####################
###########################################################
import p05.devices, p05.nano, p05.tools  ################
import numpy, time, os, PyTango  ################

from sys import argv  ################
from p05.nano.Cameras import PCO_nanoCam, FLIeh2_nanoCam, Hamamatsu_nanoCam
###########################################################
#### end initialization ###################################
###########################################################
pmac = p05.devices.PMACdict()  ################
currScript = os.path.basename(__file__)  ################

sPrefix = "hama_test"
sGroup = 'hzg'
sBeamtime = 'test'
exptime = 1

hamamatsu = Hamamatsu_nanoCam(imageDir = 'e:/%s/%s/%s/' %(sGroup, sBeamtime, sPrefix), exptime = exptime)

for i in range(10):
    hamamatsu.acquireImage()
    print (i)