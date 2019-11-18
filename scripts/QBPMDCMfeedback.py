import time
from p05.devices.QBPM import QBPM
from p05.devices.DCM import CDCM
from p05.tools.PIDcontroller import PID


class QBPMDCMfeedback():

    def __init__(self, qbpm):
        # Instanciate PID,QBPM and DCM classes
        self.Xpid = PID()
        self.Zpid = PID()
        self.Ipid = PID()
        self.qbpm = QBPM(qbpm)
        self.dcm = CDCM()

        # Feedback parameter
        # feedback status: 'IDLE', 'RUNNING', 'ERROR'
        self.status = 'IDLE'
        # in s how often the dcm is adjusted
        self.updateInterval = 5
        # the qbpms right behind the DCM do not deliver useful x/z position and
        # must use Iavg
        self.feedbackSensor = qbpm
        # in which direction should the x2pitch correct (if Iavg is used)
        self.corrSign = 1
        # Iavg tolerance (should be a bit larger than the noise on the signal)
        self.Itolerance = 4e-9
        # Ithreshold is the threshold at which feedback loop stops (closed
        # shutter, lost beam)
        self.Ithreshold = 1e-7

        self.logfile = '~/feedback.log'

    def startFeedback(self):
        if self.status is 'RUNNING':
            return
        self.feedbackLoop()

    def feedbackLoop(self, integrate=True):
        try:
            print('disabeling backlash on 2xtal pitch an roll.')
            self.dcm._tWrite(self.dcm._tProxyDCMX2Pitch, 'UnitBacklash', 0)
            self.dcm._tWrite(self.dcm._tProxyDCMX2Roll, 'UnitBacklash', 0)
            self.setPoint()
            print('initial values pitch/roll/intensity %f/%f/%f' %
                  (self.Xpid.getPoint(), self.Zpid.getPoint(),
                   self.Ipid.getPoint()))
            if self.feedbackSensor in ['qbpm1', 'qbpm2']:
                    self.feedbackIavg(integrate=integrate)
            if self.feedbackSensor == 'qbpm4':
                while True:
                    self.feedbackPos(integrate=integrate)
        except (KeyboardInterrupt, SystemExit):
            print('Caught Interrupt signal - exiting')
            print('Setting backlash back to default values \
                  (5e-5 pitch, 2e-3 roll) .')
            self.dcm._tWrite(self.dcm._tProxyDCMX2Pitch, 'UnitBacklash', 5e-5)
            self.dcm._tWrite(self.dcm._tProxyDCMX2Roll, 'UnitBacklash', 2e-3)
            return None

    def feedbackPos(self, integrate=True):
        # read QBPM values
        if integrate is True:
            X, Z, I = self.__readAvgQBPMxzi()
        else:
            X, Z, I = self.__readQBPMxzi()

        beamOk = self._checkIntensity(I)

        if beamOk:
            Xpid = self.Xpid.update(X)
            Zpid = self.Zpid.update(Z)

            print('X/pid=%f/%f,  Z/pid=%f/%f' % (X, Xpid, Z, Zpid))
            self.dcm.x2Pitch(Zpid, relative=True)
            self.dcm.x2Roll(Xpid, relative=True)
        else:
            print('Skip feedback cycle due to low intensity.')

    def feedbackIavg(self, integrate=True, act=False):
        # read QBPM values
        if integrate is True:
            X, Z, I = self.__readAvgQBPMxzi()
        else:
            X, Z, I = self.__readQBPMxzi()

        # feed values to PID algorithm
        Xpid = self.Xpid.update(X)
        Zpid = self.Zpid.update(Z)
        Ipid = self.Ipid.update(I)

        if abs(I-self.Ipid.getPoint()) > self.Itolerance:
            print('Set: %e Ipid=%e/%e' % (self.Ipid.getPoint(), I,
                                          Ipid*self.corrSign))
            # correct DCM with PID and cpnversion values
            self.dcm.x2Pitch(Zpid * self.corrSign, relative=True,
                             verbose=False)

            # check QBPM again
            if integrate is True:
                XavgCheck, ZavgCheck, IavgCheck = self.__readAvgQBPMxzi()
            else:
                XavgCheck, ZavgCheck, IavgCheck = self.__readQBPMxzi()

            if IavgCheck < I + I * self.Itolerance:
                self.corrSign *= -1
        else:
            print('Set: %e I=%e,  Idiff=%e' % (self.Ipid.getPoint(), I,
                                               I-self.Ipid.getPoint()))

    def feedbackIavg2(self, integrate=True):
        if integrate is True:
            X, Z, I = self.__readAvgQBPMxzi()  # read QBPM values
        else:
            X, Z, I = self.__readQBPMxzi()  # read QBPM values

        Xpid = self.Xpid.update(X)     # feed values to PID algorithm
        Xerror = self.Xpid.error
        Zpid = self.Zpid.update(Z)
        Zerror = self.Zpid.error
        Ipid = self.Ipid.update(I)
        Ierror = self.Ipid.error

        print('Set: %e Ipid=%e/%e' % (self.Ipid.getPoint(), I, Ipid *
                                      self.corrSign))
        # correct DCM with PID and cpnversion values
        self.dcm.x2Pitch(Zpid * self.corrSign, relative=True, verbose=False)

        # check QBPM again
        time.sleep(3)
        if integrate is True:
            XavgCheck, ZavgCheck, IavgCheck = self.__readAvgQBPMxzi()
        else:
            XavgCheck, ZavgCheck, IavgCheck = self.__readQBPMxzi()

        if IavgCheck < I + I * self.Itolerance:
            self.corrSign *= -1

    def stopFeedback(self):
        pass

    def setPoint(self):
        Xqbpm, Zqbpm, Iqbpm = self.__readAvgQBPMxzi()
        self.Xpid.setPoint(Xqbpm)
        self.Zpid.setPoint(Zqbpm)
        self.Ipid.setPoint(Iqbpm)

    def status(self):
        pass

    def __readAvgQBPMxzi(self):
        Xqbpm, Zqbpm = self.qbpm.readPosition(verbose=False)
        Iqbpm = self.qbpm.readAvgCurrent(verbose=False)
        t0 = time.time()
        tDelta = 0
        index = 0
        Xsum, Zsum, Isum = 0, 0, 0
        while tDelta < self.updateInterval:
            index += 1
            Xqbpm, Zqbpm = self.qbpm.readPosition(verbose=False)
            Iqbpm = self.qbpm.readAvgCurrent(verbose=False)
            Xsum, Zsum, Isum = Xsum+Xqbpm, Zsum+Zqbpm, Isum+Iqbpm
            tDelta = time.time()-t0
        index = float(index)
        Xavg, Zavg, Iavg = Xsum/index, Zsum/index, Isum/index
        return Xavg, Zavg, Iavg

    def __readQBPMxzi(self):
        Xqbpm, Zqbpm = self.qbpm.readPosition(verbose=False)
        Iqbpm = self.qbpm.readAvgCurrent(verbose=False)
        return Xqbpm, Zqbpm, Iqbpm

    def __checkStatus(self):
        pass

    def _checkIntensity(self, Iqbpm):
        if Iqbpm < self.Ithreshold:
            return False
        return True


