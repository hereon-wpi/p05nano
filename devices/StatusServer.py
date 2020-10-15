import time
from p05.common import TangoServerMap
import re
import time

from p05.common import TangoServerMap


# TODO not used, want to make it work
class StatusServer():
    """
    The StatusServer class provides methods to interact with the p05 StatusServer.
    """
    def __init__(self):
        self._tProxyStatusserver = TangoServerMap.getProxy('statusserver')

        self.lastReadOut = None
        self.valDictList = None

    def status(self, verbose=True):
        """
        Determines the activity of the StatusServer. It can be one of:
        IDLE: no data collection
        LIGHT_POLLING: Polling at a fixed intervall, no value history
        HEAVY_DUTY: Polling with intervals determined by the configuration file. Data history kept
        """
        retVal = self._tProxyStatusserver.read_attribute('crtActivity').value
        if verbose is True:
            print('StatusServer is %s' % retVal)
        return retVal

    def startCollectData(self):
        self._tProxyStatusserver.startCollectData()

    def stopCollectData(self):
        self._tProxyStatusserver.stopCollectData()

    def startPoll(self):
        self._tProxyStatusserver.startLightPolling()

    def startPollInterval(self, pollTime=1000):
        self._tProxyStatusserver.startPollingAtFixedRate(pollTime)

    def eraseData(self):
        self._tProxyStatusserver.eraseData()

    def getLatestData(self, verbose=True):
        retVal = self._tProxyStatusserver.getLatestSnapshot()
        retList = self.__generateSTSList(retVal)
        self.lastReadOut = retList
        if verbose:
            print('Snapshot: ', retList)
        return retList

    def getSingleValue(self, name, verbose=True):
        status = self.status(verbose=False)
        # if the STS is IDLE return -1
        if status == "IDLE":
            self.startCollectData()
            time.sleep(0.3)
            if verbose:
                print('The status server is IDLE. Starting statusserver')

        retList = self.getLatestData(verbose=False)
        singleValList = None
        for item in retList:
            if item["name"] == name:
                singleValList = item
        if singleValList is None:
            singleValList = 'No entry ' + name + ' found.'
        if verbose:
            print("Values: ", singleValList)

        if status == "IDLE":
            self.stopCollectData()
            if verbose:
                print('Stopping statusserver.')

        return singleValList

    # def getLatestDataGroup(self):

    def __generateSTSList(self, stsReadOut):
        """
        Generates a list with dictionaries with all STS data.
        """
        for item in sorted(stsReadOut):
            SS_values = re.findall(r"[\w.]+", item)
            t_SS = (datetime.datetime.fromtimestamp(float(SS_values[1]) / 1e3))
            try:
                t_p3I = (float(SS_values[2]))
            except:
                t_p3I = (None)
            t_tine = (datetime.datetime.fromtimestamp(float(SS_values[3]) / 1e3))

            return {"tColl": t_SS, "value": t_p3I, "tVal": t_tine}
