import p05.devices
import p05.common
from p05.scripts import Aperture

class p05instEH2():
    def __init__(self):
        self.tObjectDict = {
            'aperture1': [True, 'Aperture behind DCM'],
            'aperture2': [True, 'first Aperture JJ X-Ray in EH2'],
            'aperture3': [False, 'second Aperture JJ X-Ray in EH2'],
            'DCM': [True, 'Double Crystal Monochromator'],
            'camerastage': [True, 'Camera Stage (Micos Five Axis)'],
            'basestage': [True, 'Base Stage (Tripod)'],
            'microscope': [True, 'Microscope Optics'],
            'rotationstage': [True, 'Rotation Stage (Aerotech)'],
            'undulator': [True, 'Undulator'],
            'samplestage': [True, 'Sample Stage (Attocube)'],
            'ehdcamera': [True, 'EHD camera'],
            'xrayshutter': [True, 'Uniblitz X-Ray Shutter'],
            'qbpm1': [True, 'first Quadrupol Beamposition Monitor in OH'],
            'qbpm4': [True, 'Quadrupol Beamposition Monitor in EH2'],
            'statusserver': [True, 'P05 StatusServer'],
            'sample': [True, 'Sample manipulation'],
            'optics': [True, 'Optics manipulation'],
        }
        self.__strOk = '[\033[1;32mok\033[1;m]'
        self.__strErr = '[\033[1;31m!!\033[1;m]'

    def instanciate(self):
        if self.tObjectDict['aperture1'][0]:
            try:
                #instanciate aperture behind mono
                s1x = '//hasgksspp05s01:10000/p05/motor/mono.09'
                s2x = '//hasgksspp05s01:10000/p05/motor/mono.13'
                s1z = '//hasgksspp05s01:10000/p05/motor/mono.14'
                s2z = '//hasgksspp05s01:10000/p05/motor/mono.10'
                global aperture1
                aperture1 = Aperture(x1=s1x, x2=s2x, z1=s1z, z2=s2z)
                aperture1.checkmaxwidth = True
                print('%s Created DCM aperture object: aperture1.' %
                      self.__strOk)
            except:
                self.tObjectDict['aperture1'][0] = False
                print(' % s Could not instanciate DCM aperture1' %
                      self.__strErr)

        if self.tObjectDict['aperture2'][0]:
            try:
                #instanciate aperture in EH2
                sx1 = '//hzgpp05eh2vme:10000/p05/motor/eh2.01'
                sx2 = '//hzgpp05eh2vme:10000/p05/motor/eh2.02'
                sz1 = '//hzgpp05eh2vme:10000/p05/motor/eh2.03'
                sz2 = '//hzgpp05eh2vme:10000/p05/motor/eh2.04'
                global aperture2
                aperture2 = Aperture(x1=sx1, x2=sx2, z1=sz1, z2=sz2)
                aperture2.checkmaxwidth = False
                print('%s Created JJ X-ray aperture object in EH2:\
                      aperture2.' % self.__strOk)
            except:
                self.tObjectDict['aperture2'][0] = False
                print('%s Could not instanciate DCM aperture2' % self.__strErr)

        if self.tObjectDict['aperture3'][0]:
            try:
                #instanciate aperture in EH2
                s1x = '//hzgpp05eh2vme:10000/p05/motor/eh2.06'
                s2x = '//hzgpp05eh2vme:10000/p05/motor/eh2.05'
                s1z = '//hzgpp05eh2vme:10000/p05/motor/eh2.07'
                s2z = '//hzgpp05eh2vme:10000/p05/motor/eh2.08'
                global aperture3
                aperture3 = Aperture(x1=s1x, x2=s2x, z1=s1z, z2=s2z)
                aperture3.checkmaxwidth = False
                print('%s Created JJ X-ray aperture object in EH2: aperture3.'
                      % self.__strOk)
            except:
                self.tObjectDict['aperture2'][0] = False
                print('%s Could not instanciate DCM aperture3' % self.__strErr)

        if self.tObjectDict['DCM'][0]:
            try:
                #instanciate DCM
                global DCM
                DCM = p05.devices.CDCM()
                print('%s Created DCM object: DCM.' % self.__strOk)
            except:
                self.tObjectDict['DCM'][0] = False
                print('%s Could not instanciate DCM object.' % self.__strErr)

        if self.tObjectDict['camerastage'][0]:
            try:
                #instanciate micos five axis
                global camerastage
                camerastage = p05.devices.MicosFiveAxis()
                print('%s Created Visible Light Optics Stage object:\
                      camerastage.' % self.__strOk)
            except:
                self.tObjectDict['camerastage'][0] = False
                print('%s Could not instanciate camerastage object.' %
                      self.__strErr)

        if self.tObjectDict['basestage'][0]:
            try:
                #instanciate Tripod
                global basestage
                basestage = p05.devices.Tripod()
                print('%s Created Base Stage object: basestage.' %
                      self.__strOk)
            except:
                self.tObjectDict['basestage'][0] = False
                print('%s Could not instanciate basestage object.' %
                      self.__strErr)

        if self.tObjectDict['microscope'][0]:
            try:
                #instanciate microscope optics
                global microscope
                microscope = p05.devices.MicroscopeOptics()
                print('%s Created microscope optics object: microscope.' %
                      self.__strOk)
            except:
                self.tObjectDict['microscope'][0] = False
                print('%s Could not instanciate microscope object.' %
                      self.__strErr)

        if self.tObjectDict['rotationstage'][0]:
            try:
                #instanciate Aerotech
                global rotationstage
                rotationstage = p05.devices.Aerotech()
                print('%s Created Rotation Stage object: rotationstage.' %
                      self.__strOk)
            except:
                self.tObjectDict['rotationstage'][0] = False
                print('%s Could not instanciate microscope object.' %
                      self.__strErr)

        if self.tObjectDict['undulator'][0]:
            try:
                #instanciate undulator
                global undulator
                undulator = p05.devices.Undulator()
                print('%s Created undulator object: undulator.' % self.__strOk)
            except:
                self.tObjectDict['undulator'][0] = False
                print('%s Could not instanciate undulator object.' %
                      self.__strErr)

        if self.tObjectDict['samplestage'][0]:
            try:
                #instanciate attocubes
                global samplestage
                samplestage = p05.devices.Attocube()
                print('%s Created Sample Positioner Stage object: samplestage.'
                      % self.__strOk)
            except:
                self.tObjectDict['samplestage'][0] = False
                print('%s Could not instanciate samplestage object.' %
                      self.__strErr)

        if self.tObjectDict['ehdcamera'][0]:
            try:
                #instanciate ehdcamera camera
                global ehdcamera
                ehdcamera = p05.devices.FLIcamera()
                print('%s Created EHD camera object: ehdcamera.' %
                      self.__strOk)
            except:
                self.tObjectDict['ehdcamera'][0] = False
                print('%s Could not instanciate ehdcamera object.' %
                      self.__strErr)

        if self.tObjectDict['xrayshutter'][0]:
            try:
                #instanciate x-ray shutter
                global xrayshutter
                xrayshutter = p05.devices.XRayShutter()
                print('%s Created x-ray shutter object: xrayshutter.' %
                      self.__strOk)
            except:
                self.tObjectDict['xrayshutter'][0] = False
                print('%s Could not instanciate xrayshutter object.' %
                      self.__strErr)

        if self.tObjectDict['qbpm1'][0]:
            try:
                #instanciate qbpm1
                global qbpm1
                qbpm1 = p05.devices.QBPM('qbpm1')
                print('%s Created QBPM object: qbpm1.' % self.__strOk)
            except:
                self.tObjectDict['qbpm1'][0] = False
                print('%s Could not instanciate qbpm1 object.' % self.__strErr)

        if self.tObjectDict['qbpm4'][0]:
            try:
                #instanciate qbpm4
                global qbpm4
                qbpm4 = p05.devices.QBPM('qbpm4')
                print('%s Created QBPM object: qbpm4.' % self.__strOk)
            except:
                self.tObjectDict['qbpm4'][0] = False
                print('%s Could not instanciate qbpm4 object.' % self.__strErr)

        if self.tObjectDict['statusserver'][0]:
            try:
                #instanciate p05 StatusServer
                global statusserver
                statusserver = p05.devices.StatusServer()
                print('%s Created StatusServer object: statusserver.' %
                      self.__strOk)
            except:
                self.tObjectDict['statusserver'][0] = False
                print('%s Could not instanciate statusserver object.' %
                      self.__strErr)

        if self.tObjectDict['sample'][0]:
            try:
                #instanciate sample manipulation class
                global sample
                sample = p05.devices.Sample()
                print('%s Created sample manipulation object: sample.' %
                      self.__strOk)
            except:
                self.tObjectDict['sample'][0] = False
                print('%s Could not instanciate sample object.' %
                      self.__strErr)

        if self.tObjectDict['optics'][0]:
            try:
                #instanciate optics manipulation class
                global optics
                optics = p05.devices.Optics()
                print('%s Created optics manipulation object: optics.' %
                      self.__strOk)
            except:
                self.tObjectDict['optics'][0] = False
                print('%s Could not instanciate optics object.' %
                      self.__strErr)

    def show(self):
        for tObject in self.tObjectDict:
            if self.tObjectDict[tObject][0]:
                print('object %s: %s' % (tObject,
                                         self.tObjectDict[tObject][1]))


def initEH2():
    p05.common.TangoServerMap.initAllProxies()
    p05EH2Instance = p05instEH2()
    p05EH2Instance.instanciate()
