import PyTango
import time
import p05.tools.misc as misc

class JJslits():
    def __init__(self):
        self.tS1x1 = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.04')
        self.tS1x2 = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.03')
        self.tS1z1 = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.01')
        self.tS1z2 = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.02')


    def MoveRel(self, delta):
        """Move the JJ slits in the EH1 with the width <delta>. 
        Positive values correspond to closing the slits. """
        tS1x1pos = self.tS1x1.read_attribute('Position').value
        tS1x2pos = self.tS1x2.read_attribute('Position').value
        tS1z1pos = self.tS1z1.read_attribute('Position').value
        tS1z2pos = self.tS1z2.read_attribute('Position').value
        
        self.tS1x1.write_attribute('Position', tS1x1pos+delta)
        self.tS1x2.write_attribute('Position', tS1x2pos-delta)
        self.tS1z1.write_attribute('Position', tS1z1pos+delta)
        self.tS1z2.write_attribute('Position', tS1z2pos-delta)
        
        time.sleep(0.1)
        while self.tS1x1.state() == PyTango.DevState.MOVING or self.tS1x2.state() == PyTango.DevState.MOVING \
           or self.tS1z1.state() == PyTango.DevState.MOVING or self.tS1z2.state() == PyTango.DevState.MOVING: 
            time.sleep(0.1)
        return None
    #end SlitsMoveRel

    def MoveX(self, delta = 0.05):
        tS1x1pos = self.tS1x1.read_attribute('Position').value
        tS1x2pos = self.tS1x2.read_attribute('Position').value
        self.tS1x1.write_attribute('Position', tS1x1pos+delta)
        self.tS1x2.write_attribute('Position', tS1x2pos+delta)
        time.sleep(0.1)
        while self.tS1x1.state() == PyTango.DevState.MOVING or self.tS1x2.state() == PyTango.DevState.MOVING \
           or self.tS1z1.state() == PyTango.DevState.MOVING or self.tS1z2.state() == PyTango.DevState.MOVING: 
            time.sleep(0.1)
        return None
    #end SlitsMoveX

    def MoveZ(self, delta = 0.05):
        tS1z1pos = self.tS1z1.read_attribute('Position').value
        tS1z2pos = self.tS1z2.read_attribute('Position').value
        self.tS1z1.write_attribute('Position', tS1z1pos+delta)
        self.tS1z2.write_attribute('Position', tS1z2pos+delta)
        time.sleep(0.1)
        while self.tS1x1.state() == PyTango.DevState.MOVING or self.tS1x2.state() == PyTango.DevState.MOVING \
           or self.tS1z1.state() == PyTango.DevState.MOVING or self.tS1z2.state() == PyTango.DevState.MOVING: 
            time.sleep(0.1)
        return None
    #end SlitsMoveX

    def Close(self, delta = 1):
        """Wrapper for closing the slits and returning a print output. 
        Positive values correspond to closing the slits.
        <delta>:  width to move each slit (in mm), 
                  i.e. delta = 1 corresponds to 2 mm closure"""
        self.MoveRel(delta)
        print(misc.GetTimeString()+': Finished closing slits')
        return None
    #end SlitsClose

    def Open(self, delta = 1):
        """Wrapper for opening the slits and returning a print output. 
        Positive values correspond to opening the slits.
        <delta>:  width to move each slit (in mm), 
                  i.e. delta = 1 corresponds to 2 mm opening"""
        self.MoveRel(-delta)
        print(misc.GetTimeString()+': Finished opening slits')
        return None
    #end SlitsOpen

    def GetPos(self):
        """Method to return slit positions as formatted string."""
        tS1x1pos = self.tS1x1.read_attribute('Position').value
        tS1x2pos = self.tS1x2.read_attribute('Position').value
        tS1z1pos = self.tS1z1.read_attribute('Position').value
        tS1z2pos = self.tS1z2.read_attribute('Position').value
        return '%e\t%e\t%e\t%e\t' %(tS1x1pos, tS1x2pos, tS1z1pos, tS1z2pos)
    #end SlitsGetPos

