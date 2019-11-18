import PyTango
import time
import p05.tools.misc as misc
import p05.devices as dev
import numpy
import getpass
import os
import sys
import pickle

class NanoGrainMapping():
    def __init__(self, sampleOutDist = 0.2, writePosLog = True):
        self.__pmac = dev.PMACdict()
        
        self.__SP = numpy.zeros(6, dtype = object)
        self.__SP[0] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano.01')
        self.__SP[1] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano.02')
        self.__SP[2] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano.03')
        self.__SP[3] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano.04')
        self.__SP[4] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano.05')
        self.__SP[5] = PyTango.DeviceProxy('//haspp03nano:10000/p03/smarpodmotor/p03nano.06')
        
        self.__rotStage = PyTango.DeviceProxy('//haspp03nano:10000/p03nano/labmotion/exp.01')
        
        #Optics working position
        self.__wp_ok = False
        self.__wp_pos = {}
        #Optics alignment position
        self.__ap_ok = False
        self.__ap_pos = {}
        #Sample rotation center
        self.__rc_ok = False
        self.writePosLog = writePosLog
        try:
            self.__sampleOutDist = float(sampleOutDist)
        except:
            print misc.GetShortTimeString() + ': Warning - could not convert sampleOutDist = %s to a number.' %sampleOutDist
            self.__sampleOutDist = 0.2
        
        self.__currDir = os.path.dirname(__file__).replace('\\', '/')
        if os.path.exists(self.__currDir + os.sep + 'nanoPositioning.log'):
            self.__fLogStr = """open(self.__currDir + os.sep + 'nanoPositioning.log', 'a')"""
        else:
            self.__fLogStr = """open(self.__currDir + os.sep + 'nanoPositioning.log', 'w')"""
        return None
    #end __init__
    
    def MvrSampleX_NGM(self, value):
        __delta = float(value)
        __currentx = self.__SP[0].read_attribute('Position').value
        __currenty = self.__SP[0].read_attribute('Position').value
        __currentRot = self.__rotStage.read_attribute('Position').value
        __valx = __currentx + numpy.sin(__currentRot * numpy.pi / 180) * __delta
        __valy = __currenty + numpy.cos(__currentRot * numpy.pi / 180) * __delta
        self.__SP[0].write_attribute(__valx)
        self.__SP[1].write_attribute(__valy)

if __name__ == '__main__':
    test = NanoGrainMapping()