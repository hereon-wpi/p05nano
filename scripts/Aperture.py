import PyTango
import time


class Aperture():
    """
    Class to move the apertures consistently.
    The standard cosy is used for this script.
    """
    
    def __init__(self, **kwargs):

        self.aperture_x1 = PyTango.DeviceProxy(kwargs['x1'])
        self.aperture_z1 = PyTango.DeviceProxy(kwargs['z1'])
        self.aperture_x2 = PyTango.DeviceProxy(kwargs['x2'])
        self.aperture_z2 = PyTango.DeviceProxy(kwargs['z2'])
        
        self.curr_pos_x1 = 0.0
        self.curr_pos_z1 = 0.0
        self.curr_pos_x2 = 0.0
        self.curr_pos_z2 = 0.0
        
        self.xcenter = 0.0
        self.zcenter = 0.0
        self.xwidth = 0.0
        self.zwidth = 0.0
        self.xmaxwidth = 6.0
        self.zmaxwidth = 6.0

        self.checkmaxwidth = True
        
        self.__update_positions()

        self.__target_pos_x1 = self.curr_pos_x1
        self.__target_pos_z1 = self.curr_pos_z1
        self.__target_pos_x2 = self.curr_pos_x2
        self.__target_pos_z2 = self.curr_pos_z2

    def pos(self):
        """
        Prints current absolute motor positions and aperture dimensions to the screen.
        """
        print('\nAbsolute positions:')
        self.__update_positions()
        print('motor x1 = '+str(self.curr_pos_x1))   # display absolute positions
        print('motor z1 = '+str(self.curr_pos_z1))
        print('motor x2 = '+str(self.curr_pos_x2))
        print('motor z2 = '+str(self.curr_pos_z2))

        print('\nRelative positions:')
        print('aperture center x from base position = ' + str(self.xcenter))
        print('aperture center z from base position = ' + str(self.zcenter))
        print('delta x = ' + str(self.xwidth))
        print('delta z = ' + str(self.zwidth) + '\n')
        
    def x(self, x):
        """
        Move center of aperture to an absolute value x [mm].
        Usage: object.z(z)
        """
        x = float(x)
        self.__update_positions()
        self.__target_pos_x1 = x+self.xwidth/2
        self.__target_pos_x2 = x-self.xwidth/2
        self.__target_pos_z1 = self.curr_pos_z1 
        self.__target_pos_z2 = self.curr_pos_z2 
        print('moving aperture center from x=' + str(self.xcenter) + ' to x=' + str(x))
        self.__do_move()
        
        
    def z(self, z):
        """
        Move center of aperture to an absolute value z [mm].
        Usage: object.z(z)
        """
        z = float(z)
        self.__update_positions()
        self.__target_pos_x1 = self.curr_pos_x1 
        self.__target_pos_x2 = self.curr_pos_x2 
        self.__target_pos_z1 = z-self.zwidth/2
        self.__target_pos_z2 = z+self.zwidth/2
        print('moving aperture center from z=' + str(self.zcenter) + ' to z=' + str(z))
        self.__do_move()
                
    def rx(self, rx):
        """
        Move center of aperture about x [mm] relative to current position.
        Usage: object.rx(x)
        """
        rx = float(rx)
        self.__update_positions()
        self.__target_pos_x1 = self.xcenter+rx-self.xwidth/2
        self.__target_pos_x2 = self.xcenter+rx+self.xwidth/2
        self.__target_pos_z1 = self.curr_pos_z1 
        self.__target_pos_z2 = self.curr_pos_z2 
        print('moving aperture center from x='+str(self.xcenter)+' to x='+str(self.xcenter+rx))
        self.__do_move()
        
    def rz(self, rz):
        """
        Move center of aperture about z [mm] relative to current position.
        Usage: object.rz(z)
        """
        rz = float(rz)
        self.__update_positions()
        self.__target_pos_x1 = self.curr_pos_x1 
        self.__target_pos_x2 = self.curr_pos_x2 
        self.__target_pos_z1 = self.zcenter+rz-self.zwidth/2
        self.__target_pos_z2 = self.zcenter+rz+self.zwidth/2
        print('moving aperture center from z='+str(self.zcenter)+' to z='+str(self.zcenter+rz))
        self.__do_move()

    def dx(self, dx):
        """
        Change aperture x-width to dx [mm].
        Usage: object.dx[dx]
        """
        dx = float(dx)
        self.__update_positions()
        self.__target_pos_x1 = self.xcenter-dx/2
        self.__target_pos_x2 = self.xcenter+dx/2
        self.__target_pos_z1 = self.curr_pos_z1 
        self.__target_pos_z2 = self.curr_pos_z2 
        print('change aperture x-width from dx='+str(self.xwidth)+' to dx='+str(dx))
        self.__do_move()

    def dz(self, dz):
        """
        Change aperture z-width to dz [mm].
        Usage: object.dz[dz]
        """
        dz = float(dz)
        self.__update_positions()
        self.__target_pos_x1 = self.curr_pos_x1 
        self.__target_pos_x2 = self.curr_pos_x2 
        self.__target_pos_z1 = self.zcenter-dz/2
        self.__target_pos_z2 = self.zcenter+dz/2
        print('change aperture z-width from dz='+str(self.zwidth)+' to dz='+str(dz))
        self.__do_move()
        
    def rdx(self, rdx):
        """
        Change aperture x-width relative to current width by dx [mm].
        Usage: object.rdx[dx]
        """
        rdx = float(rdx)
        self.__update_positions()
        self.__target_pos_x1 = self.xcenter-self.xwidth/2-rdx/2
        self.__target_pos_x2 = self.xcenter+self.xwidth/2+rdx/2
        self.__target_pos_z1 = self.curr_pos_z1 
        self.__target_pos_z2 = self.curr_pos_z2 
        print('change aperture x-width from dx='+str(self.xwidth)+' to dx='+str(self.xwidth+rdx))
        self.__do_move()
        
    def rdz(self, rdz):
        """
        Change aperture z-width relative to current width by dz [mm].
        Usage: object.rdz[dz]
        """
        rdz = float(rdz)
        self.__update_positions()
        self.__target_pos_x1 = self.curr_pos_x1 
        self.__target_pos_x2 = self.curr_pos_x2 
        self.__target_pos_z1 = self.zcenter-self.zwidth/2-rdz/2
        self.__target_pos_z2 = self.zcenter+self.zwidth/2+rdz/2
        print('change aperture z-width from dz='+str(self.zwidth)+' to dz='+str(self.zwidth+rdz))
        self.__do_move()

    def __checkwidth(self):
        """
        Check if the slitwidth is below the maximum allowed values.
        """
        self.__update_positions()
        if self.checkmaxwidth == True:
            if (self.__target_pos_x1 - self.__target_pos_x2) > self.xmaxwidth:
                return -1
            elif (self.__target_pos_z2 - self.__target_pos_z1) > self.zmaxwidth:
                return -1
            else:
                return 0
        else:
            return 0
    
    def __do_move(self):
        """
        Perform move to the set positions.
        """
        width_ok = self.__checkwidth()
        if width_ok == 0:
            print(self.__target_pos_x1,self.__target_pos_x2,self.__target_pos_z1,self.__target_pos_z1)
            self.aperture_x1.write_attribute('Position',self.__target_pos_x1)
            self.aperture_z1.write_attribute('Position',self.__target_pos_z1)
            self.aperture_x2.write_attribute('Position',self.__target_pos_x2)
            self.aperture_z2.write_attribute('Position',self.__target_pos_z2)
            self.__wait_motion_complete()
        elif width_ok == -1:
            print('width out of allowed range of dx='+str(self.xmaxwidth)+', dz='+str(self.zmaxwidth)+'. Move aborted.')
            
    def __wait_motion_complete(self):
        state_x1 = self.aperture_x1.State()
        state_z1 = self.aperture_z1.State()
        state_x2 = self.aperture_x2.State()
        state_z2 = self.aperture_z2.State()
            
        while state_x1==PyTango.DevState.MOVING or state_z1==PyTango.DevState.MOVING or state_x2==PyTango.DevState.MOVING or state_z2 ==PyTango.DevState.MOVING:
            time.sleep(0.05)
            state_x1 = self.aperture_x1.State()
            state_z1 = self.aperture_z1.State()
            state_x2 = self.aperture_x2.State()
            state_z2 = self.aperture_z2.State()
            
    def __update_positions(self):
        """
        Update current motor positions and aperture dimensions.
        """
        self.curr_pos_x1=self.aperture_x1.read_attribute('Position').value
        self.curr_pos_z1=self.aperture_z1.read_attribute('Position').value
        self.curr_pos_x2=self.aperture_x2.read_attribute('Position').value
        self.curr_pos_z2=self.aperture_z2.read_attribute('Position').value
        
        self.xwidth = self.curr_pos_x2 - self.curr_pos_x1
        self.zwidth = self.curr_pos_z2 - self.curr_pos_z1
        self.xcenter = self.xwidth/2 + self.curr_pos_x1
        self.zcenter = self.zwidth/2 + self.curr_pos_z1

    def calibrate(self):
        self.aperture_x1.SetStepPosition(0)
        self.aperture_x2.SetStepPosition(0)
        self.aperture_z1.SetStepPosition(0)
        self.aperture_z2.SetStepPosition(0)

        self.aperture_x1.write_attribute('UnitCalibration',0)
        self.aperture_z1.write_attribute('UnitCalibration',0)
        self.aperture_x2.write_attribute('UnitCalibration',0)
        self.aperture_z2.write_attribute('UnitCalibration',0)
