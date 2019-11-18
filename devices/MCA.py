from p05.devices.DeviceCommon import DeviceCommon
from p05.common import TangoServerMap
from time import sleep
from numpy import arange


class MCA(DeviceCommon):
    """
    DESCRIPTION:
        MCA (Multi Channel Analyzer) Class. Enables readout of MCA.
    """
    def __init__(self):
        # MCA

        self._tProxyMCA = TangoServerMap.getProxy('mca')

        # Dictionary of all real world (printed) names and PyTango object names
        self.__devdict = {
            'mca': [self._tProxyMCA, ['Data', {'ismotor': False}]],
        }

        # Initialize methods from superclass
        DeviceCommon.__init__(self, self.__devdict)

    def __call__(self):
        self.Pos()
        self.State()
        return None

    def start(self, verbose=True):
        """
        DESCRIPTION:
            Starts the MCA measurement.
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        return self._tExec(self._tProxyMCA, 'Start')

    def stop(self, verbose=True):
        """
        DESCRIPTION:
            Stops the MCA measurement.
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        return self._tExec(self._tProxyMCA, 'Stop')

    def read(self, verbose=True):
        """
        DESCRIPTION:
            Read result of the MCA measurement.
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        self._tExec(self._tProxyMCA, 'Read')
        return self._tRead(self._tProxyMCA, 'Data')

    def clear(self, verbose=True):
        """
        DESCRIPTION:
            Clear MCA data buffer.
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        return self._tExec(self._tProxyMCA, 'Clear')

    def measure(self, time, verbose=True):
        """
        DESCRIPTION:
            Make a MCA measurement for a given time and return the result.
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
            time=<INTEGER>:
                Duration of the measurement in seconds.
        """
        self.clear()
        self.start()
        sleep(time)
        self.stop()
        data = self.read()
        energy = (arange(data.shape[0]) + 88.2405) / 66.6427

        return energy, data
