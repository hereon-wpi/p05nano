import time
from matplotlib import pyplot
from p05.common import TangoServerMap


class FlourescenceDetector:
    """
    P05 class to control the fluorescence detector in EH1.
    """
    def __init__(self):
        self._tFluorescenceDetector = TangoServerMap.getProxy('fluorescenceDetector')
        self.spectrum = None

    def get_spectrum(self, dwelltime):
        """
        DESCRIPTION:
            get_spectrum returns a fluorescence spectrum as numpy array.
            The array is also saved in the class variable self.spectrum.

        PARAMETERS:
            dwelltime:
                <Float>
                dwelltime of the flourescence measurement
        """
        self._tFluorescenceDetector.Clear()
        self._tFluorescenceDetector.Start()
        time.sleep(dwelltime)
        self._tFluorescenceDetector.Stop()
        self._tFluorescenceDetector.Read()
        self.spectrum = self._tFluorescenceDetector.read_attribute(
            'Data').value
        return self.spectrum

    def plot_spectrum(self, spectrum=None, log=False):
        """
        DESCRIPTION:
            plot_spectrum plots a spectrum of either the last taken spectrum or a given spectrum.

        KEYWORDS:
            spectrum:
                if ommitted, plot last spectrum. Otherwise spectrum must be a numpy array
                which is subsequently plotted
            log:
                <Boolean>
                plot with logarithmic y axis. Default: False.
        """
        fig = pyplot.figure()
        ax = fig.add_subplot(111)
        if spectrum is None:
            if log is True:
                ax.semilogy(self.spectrum)
            else:
                ax.plot(self.spectrum)
        else:
            if log is True:
                ax.semilogy(spectrum)
            else:
                ax.plot(spectrum)

        ax.set_xlabel('channel')
        ax.set_ylabel('counts')
        pyplot.show()
