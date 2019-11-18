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
            'tango://hzgpp05eh2vme:10000/p05/register/eh2.out01')

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            'shutter': [self.tTTL, ['Value', {'ismotor': False}]],
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def Open(self, verbose=True):
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
        self.tTTL.write_attribute('Value', 0)
        time.sleep(0.8)  # wait for the shutter to actually open
        return 0

    def Close(self, verbose=True):
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
        self.tTTL.write_attribute('Value', 1)
        return 0

    def Status(self, verbose=True):
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
            if xrshStatus == 1:
                print("x-ray shutter closed.")
            if xrshStatus == 0:
                print("x-ray shutter opened.")
        return xrshStatus
