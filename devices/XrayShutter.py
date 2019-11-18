import PyTango
import time
from p05.devices.DeviceCommon import DeviceCommon


class XRayShutter(DeviceCommon):
    """
    Motion class for the tripod controller in P05/EH2.

    tripod class inherits from p05devices. Common function for all devices
    can be found there.
    """

    def __init__(self):

        # Aerotech Axis
        self.tTTL = PyTango.DeviceProxy(
            'tango://hzgpp05vme2:10000/p05/register/eh2.out01')

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            'shutter': [self.tTTL, ['Value', {'ismotor': False}]],
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def open(self, verbose=True):
        """
        DESCRIPTION:
            Open X-Ray shutter.
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if verbose is True:
            print("Opening x-ray shutter")
        self.tTTL.write_attribute('Value', 1)
        time.sleep(0.8)  # wait for the shutter to actually open
        return 0

    def close(self, verbose=True):
        """
        DESCRIPTION:
            Close X-Ray shutter.
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        if verbose is True:
            print("Closing x-ray shutter")
        self.tTTL.write_attribute('Value', 0)
        return 0

    def status(self, verbose=True):
        """
        DESCRIPTION:
            Returns status of the X-Ray shutter.
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        xrshStatus = self.tTTL.read_attribute('Value').value
        if verbose is True:
            if xrshStatus == 0:
                print("x-ray shutter closed.")
            if xrshStatus == 1:
                print("x-ray shutter opened.")
        return xrshStatus
