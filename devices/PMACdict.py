import numpy
import time

import p05.tools.misc as misc
from p05.devices.PMACcomm import PMACcomm


class PMACdict():
    def __init__(self, dummy=False):
        if dummy == True:
            self.Controller1, self.Controller2, self.Controller3, self.Controller4, self.Controller5, self.Controller6, self.Controller7 = 1, 2, 3, 4, 5, 6, 7
        else:
            self.Controller1 = PMACcomm(controller=1)
            self.Controller2 = PMACcomm(controller=2)
            self.Controller3 = PMACcomm(controller=3)
            self.Controller4 = PMACcomm(controller=4)
            self.Controller5 = PMACcomm(controller=5)
            self.Controller6 = PMACcomm(controller=6)
            self.Controller7 = PMACcomm(controller=7)
        self.__CreateDict()
    
    def __CreateDict(self):
        """Method used in initialization for creation of dictionary"""
        self.Dict = {}
        self.Dict['VacuumSF_x'] = {'Controller': self.Controller1, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q77', 'CurVariable': 'Q87', \
                                       'lowerLim':-25.0, 'upperLim': 25.0, 'lowerSoftLim':-25.0, 'upperSoftLim': 25.0}
        self.Dict['VacuumSF_y'] = {'Controller': self.Controller1, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q78', 'CurVariable': 'Q88', \
                                       'lowerLim':-5.0, 'upperLim': 5.0, 'lowerSoftLim':-5.0, 'upperSoftLim': 5.0}
        self.Dict['VacuumSF_z'] = {'Controller': self.Controller1, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q79', 'CurVariable': 'Q89', \
                                       'lowerLim':-10.0, 'upperLim':100.0, 'lowerSoftLim': 80.0, 'upperSoftLim': 100.0}
        self.Dict['VacuumSF_Rx'] = {'Controller': self.Controller1, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q71', 'CurVariable': 'Q81', \
                                       'lowerLim':-2.0, 'upperLim': 2.0, 'lowerSoftLim':-2.0, 'upperSoftLim': 2.0}
        self.Dict['VacuumSF_Ry'] = {'Controller': self.Controller1, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q72', 'CurVariable': 'Q82', \
                                       'lowerLim':-2.0, 'upperLim': 2.0, 'lowerSoftLim':-2.0, 'upperSoftLim': 2.0}
        self.Dict['VacuumSF_Rz'] = {'Controller': self.Controller1, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q73', 'CurVariable': 'Q83', \
                                       'lowerLim':-2.0, 'upperLim': 2.0, 'lowerSoftLim':-2.0, 'upperSoftLim': 2.0}
        self.Dict['VacuumTrans_y'] = {'Controller': self.Controller2, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q77', 'CurVariable': 'Q87', \
                                       'lowerLim': 0.0, 'upperLim': 500.0, 'lowerSoftLim': 0.0, 'upperSoftLim': 500.0}
        self.Dict['GraniteSlab_1'] = {'Controller': self.Controller3, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q77', 'CurVariable': 'Q87', \
                                       'lowerLim': 0.0, 'upperLim': 4263.0, 'lowerSoftLim': 0.0, 'upperSoftLim': 4263.0}
        self.Dict['GraniteSlab_2'] = {'Controller': self.Controller3, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q78', 'CurVariable': 'Q88', \
                                       'lowerLim': 670.0, 'upperLim': 5163.0, 'lowerSoftLim': 670.0, 'upperSoftLim': 5000.0}
        self.Dict['GraniteSlab_3'] = {'Controller': self.Controller3, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q79', 'CurVariable': 'Q89', \
                                      'lowerLim': 1300.0, 'upperLim': 5800.0, 'lowerSoftLim': 1400.0,
                                      'upperSoftLim': 5600.0}
        self.Dict['GraniteSlab_4'] = {'Controller': self.Controller3, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q71', 'CurVariable': 'Q81', \
                                       'lowerLim': 1900.0, 'upperLim': 6105.0, 'lowerSoftLim': 1900.0, 'upperSoftLim': 6105.0}
        self.Dict['Aperture_x'] = {'Controller': self.Controller3, 'SetCommand':  'Q70=8', 'TargetVariable': 'P73', 'CurVariable': 'P83', \
                                       'lowerLim':-5.0, 'upperLim': 5.0, 'lowerSoftLim':-5.0, 'upperSoftLim': 5.0}
        self.Dict['Aperture_y'] = {'Controller': self.Controller3, 'SetCommand':  'Q70=8', 'TargetVariable': 'P71', 'CurVariable': 'P81', \
                                       'lowerLim':-255.0, 'upperLim': 0.0, 'lowerSoftLim':-255.0, 'upperSoftLim': 0.0}
        self.Dict['Aperture_z'] = {'Controller': self.Controller3, 'SetCommand':  'Q70=8', 'TargetVariable': 'P72', 'CurVariable': 'P82', \
                                       'lowerLim':-26.0, 'upperLim': 0.0, 'lowerSoftLim':-26.0, 'upperSoftLim': 0.0}
        self.Dict['OpticsSF2_x'] = {'Controller': self.Controller4, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q77', 'CurVariable': 'Q87', \
                                       'lowerLim':-25.0, 'upperLim': 25.0, 'lowerSoftLim': -25.0, 'upperSoftLim': 25.0}
        self.Dict['OpticsSF2_y'] = {'Controller': self.Controller4, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q78', 'CurVariable': 'Q88', \
                                       'lowerLim':-5.0, 'upperLim': 5.0, 'lowerSoftLim':-3.0, 'upperSoftLim': 5.0}
        self.Dict['OpticsSF2_z'] = {'Controller': self.Controller4, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q79', 'CurVariable': 'Q89', \
                                       'lowerLim':-10.0, 'upperLim': 15.0, 'lowerSoftLim':-6.0, 'upperSoftLim': 8.0}
        self.Dict['OpticsSF2_Rx'] = {'Controller': self.Controller4, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q71', 'CurVariable': 'Q81', \
                                       'lowerLim':-2.5, 'upperLim': 2.5, 'lowerSoftLim':-2.5, 'upperSoftLim': 2.5}
        self.Dict['OpticsSF2_Ry'] = {'Controller': self.Controller4, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q72', 'CurVariable': 'Q82', \
                                       'lowerLim':-2.5, 'upperLim': 2.5, 'lowerSoftLim':-2.5, 'upperSoftLim': 2.5}
        self.Dict['OpticsSF2_Rz'] = {'Controller': self.Controller4, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q73', 'CurVariable': 'Q83', \
                                       'lowerLim':-2.5, 'upperLim': 2.5, 'lowerSoftLim':-2.5, 'upperSoftLim': 2.5}
        self.Dict['Diode1_z'] = {'Controller': self.Controller4, 'SetCommand':  'Q70=8', 'TargetVariable': 'P71', 'CurVariable': 'P81', \
                                       'lowerLim':-50.0, 'upperLim': 0.0, 'lowerSoftLim':-50.0, 'upperSoftLim': 0.0}
        self.Dict['Diode2_z'] = {'Controller': self.Controller4, 'SetCommand':  'Q70=8', 'TargetVariable': 'P72', 'CurVariable': 'P82', \
                                       'lowerLim':-50.0, 'upperLim': 0.0, 'lowerSoftLim':-50.0, 'upperSoftLim': 0.0}
        self.Dict['SampleStage_x'] = {'Controller': self.Controller5, 'SetCommand':  'Q70=8', 'TargetVariable': 'P71', 'CurVariable': 'P81', \
                                       'lowerLim':-20.0, 'upperLim': 0.0, 'lowerSoftLim':-20.0, 'upperSoftLim': 0.0}
        self.Dict['SampleStage_z'] = {'Controller': self.Controller5, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q79', 'CurVariable': 'Q89', \
                                       'lowerLim':-35.0, 'upperLim': 5.0, 'lowerSoftLim':-35.0, 'upperSoftLim': 0.0}
        self.Dict['SampleStage_Rx'] = {'Controller': self.Controller5, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q77', 'CurVariable': 'Q87', \
                                       'lowerLim':-0.5, 'upperLim': 0.5, 'lowerSoftLim':-0.5, 'upperSoftLim': 0.5}
        self.Dict['SampleStage_Ry'] = {'Controller': self.Controller5, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q78', 'CurVariable': 'Q88', \
                                       'lowerLim':-0.5, 'upperLim': 0.5, 'lowerSoftLim':-0.5, 'upperSoftLim': 0.5}
        self.Dict['Sample_Rot'] = {'Controller': self.Controller5, 'SetCommand':  'Q70=8', 'TargetVariable': 'P72', 'CurVariable': 'P82', \
                                   'lowerLim': -185.0, 'upperLim': 185.0, 'lowerSoftLim': -185.0, 'upperSoftLim': 185.0}
        self.Dict['Detector_x'] = {'Controller': self.Controller5, 'SetCommand':  'Q70=28', 'TargetVariable': 'P77', 'CurVariable': 'P87', \
                                       'lowerLim':-25.0, 'upperLim': 25.0, 'lowerSoftLim':-25.0, 'upperSoftLim': 25.0}
        self.Dict['Detector_z'] = {'Controller': self.Controller5, 'SetCommand':  'Q70=28', 'TargetVariable': 'P78', 'CurVariable': 'P88', \
                                       'lowerLim':-10.0, 'upperLim': 10.0, 'lowerSoftLim':-10.0, 'upperSoftLim': 10.0}
        self.Dict['Sample_x'] = {'Controller': self.Controller6, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q77', 'CurVariable': 'Q87', \
                                       'lowerLim':-5.0, 'upperLim': 5.0, 'lowerSoftLim':-5.0, 'upperSoftLim': 5.0}
        self.Dict['Sample_y'] = {'Controller': self.Controller6, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q78', 'CurVariable': 'Q88', \
                                       'lowerLim':-5.0, 'upperLim': 5.0, 'lowerSoftLim':-5.0, 'upperSoftLim': 5.0}
        self.Dict['Sample_z'] = {'Controller': self.Controller6, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q79', 'CurVariable': 'Q89', \
                                       'lowerLim':-5.0, 'upperLim': 5.0, 'lowerSoftLim':-5.0, 'upperSoftLim': 5.0}
        self.Dict['Sample_Rx'] = {'Controller': self.Controller6, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q71', 'CurVariable': 'Q81', \
                                       'lowerLim':-2.5, 'upperLim': 2.5, 'lowerSoftLim':-2.5, 'upperSoftLim': 2.5}
        self.Dict['Sample_Ry'] = {'Controller': self.Controller6, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q72', 'CurVariable': 'Q82', \
                                       'lowerLim':-2.5, 'upperLim': 2.5, 'lowerSoftLim':-2.5, 'upperSoftLim': 2.5}
        self.Dict['Sample_Rz'] = {'Controller': self.Controller6, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q73', 'CurVariable': 'Q83', \
                                       'lowerLim':-2.5, 'upperLim': 2.5, 'lowerSoftLim':-2.5, 'upperSoftLim': 2.5}
        self.Dict['OpticsSF1_x'] = {'Controller': self.Controller7, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q77', 'CurVariable': 'Q87', \
                                       'lowerLim':-20.0, 'upperLim': 20.0, 'lowerSoftLim':-20.0, 'upperSoftLim': 20.0}
        self.Dict['OpticsSF1_y'] = {'Controller': self.Controller7, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q78', 'CurVariable': 'Q88', \
                                       'lowerLim':-5.0, 'upperLim': 5.0, 'lowerSoftLim':-5.0, 'upperSoftLim': 5.0}
        self.Dict['OpticsSF1_z'] = {'Controller': self.Controller7, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q79', 'CurVariable': 'Q89', \
                                       'lowerLim':-10.0, 'upperLim': 15.0, 'lowerSoftLim':-10.0, 'upperSoftLim': 15.0}
        self.Dict['OpticsSF1_Rx'] = {'Controller': self.Controller7, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q71', 'CurVariable': 'Q81', \
                                       'lowerLim':-2.5, 'upperLim': 2.5, 'lowerSoftLim':-2.5, 'upperSoftLim': 2.5}
        self.Dict['OpticsSF1_Ry'] = {'Controller': self.Controller7, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q72', 'CurVariable': 'Q82', \
                                       'lowerLim':-2.5, 'upperLim': 2.5, 'lowerSoftLim':-2.5, 'upperSoftLim': 2.5}
        self.Dict['OpticsSF1_Rz'] = {'Controller': self.Controller7, 'SetCommand':  'Q70=4', 'TargetVariable': 'Q73', 'CurVariable': 'Q83', \
                                       'lowerLim':-2.5, 'upperLim': 2.5, 'lowerSoftLim':-2.5, 'upperSoftLim': 2.5}
        self.Dict['OpticsStage1_y'] = {'Controller': self.Controller7, 'SetCommand':  'Q70=8', 'TargetVariable': 'P71', 'CurVariable': 'P81', \
                                       'lowerLim': 0.0, 'upperLim': 300.0, 'lowerSoftLim': 0.0, 'upperSoftLim': 300.0}
        self.Dict['GraniteSlab_1single'] = {'Controller': self.Controller3, 'SetCommand':  'Q70=114', 'TargetVariable': 'Q77', 'CurVariable': 'Q87'}
        self.Dict['GraniteSlab_2single'] = {'Controller': self.Controller3, 'SetCommand':  'Q70=124', 'TargetVariable': 'Q78', 'CurVariable': 'Q88'}
        self.Dict['GraniteSlab_3single'] = {'Controller': self.Controller3, 'SetCommand':  'Q70=134', 'TargetVariable': 'Q79', 'CurVariable': 'Q89'}
        self.Dict['GraniteSlab_4single'] = {'Controller': self.Controller3, 'SetCommand':  'Q70=144', 'TargetVariable': 'Q71', 'CurVariable': 'Q81'}
        self.Dict['GraniteSlab_1single']['lowerLim'] = self.Dict['GraniteSlab_1']['lowerLim']
        self.Dict['GraniteSlab_1single']['upperLim'] = self.Dict['GraniteSlab_1']['upperLim']
        self.Dict['GraniteSlab_1single']['lowerSoftLim'] = self.Dict['GraniteSlab_1']['lowerSoftLim']
        self.Dict['GraniteSlab_1single']['upperSoftLim'] = self.Dict['GraniteSlab_1']['upperSoftLim']
        self.Dict['GraniteSlab_2single']['lowerLim'] = self.Dict['GraniteSlab_2']['lowerLim']
        self.Dict['GraniteSlab_2single']['upperLim'] = self.Dict['GraniteSlab_2']['upperLim']
        self.Dict['GraniteSlab_2single']['lowerSoftLim'] = self.Dict['GraniteSlab_2']['lowerSoftLim']
        self.Dict['GraniteSlab_2single']['upperSoftLim'] = self.Dict['GraniteSlab_2']['upperSoftLim']
        self.Dict['GraniteSlab_3single']['lowerLim'] = self.Dict['GraniteSlab_3']['lowerLim']
        self.Dict['GraniteSlab_3single']['upperLim'] = self.Dict['GraniteSlab_3']['upperLim']
        self.Dict['GraniteSlab_3single']['lowerSoftLim'] = self.Dict['GraniteSlab_3']['lowerSoftLim']
        self.Dict['GraniteSlab_3single']['upperSoftLim'] = self.Dict['GraniteSlab_3']['upperSoftLim']
        self.Dict['GraniteSlab_4single']['lowerLim'] = self.Dict['GraniteSlab_4']['lowerLim']
        self.Dict['GraniteSlab_4single']['upperLim'] = self.Dict['GraniteSlab_4']['upperLim']
        self.Dict['GraniteSlab_4single']['lowerSoftLim'] = self.Dict['GraniteSlab_4']['lowerSoftLim']
        self.Dict['GraniteSlab_4single']['upperSoftLim'] = self.Dict['GraniteSlab_4']['upperSoftLim']
 
        self.MotorList = ['VacuumSF_x', 'VacuumSF_y', 'VacuumSF_z', 'VacuumSF_Rx', 'VacuumSF_Ry', 'VacuumSF_Rz', 'VacuumTrans_y', \
                  'GraniteSlab_1', 'GraniteSlab_2', 'GraniteSlab_3', 'GraniteSlab_4', 'Aperture_x', 'Aperture_y', \
                  'Aperture_z', 'OpticsSF1_x', 'OpticsSF1_y', 'OpticsSF1_z', 'OpticsSF1_Rx', 'OpticsSF1_Ry', 'OpticsSF1_Rz', \
                  'OpticsStage1_y', 'OpticsSF2_x', 'OpticsSF2_y', 'OpticsSF2_z', 'OpticsSF2_Rx', 'OpticsSF2_Ry', 'OpticsSF2_Rz', \
                  'Diode1_z', 'Diode2_z', 'SampleStage_x', 'SampleStage_z', 'SampleStage_Rx', 'SampleStage_Ry', \
                  'Sample_Rot', 'Sample_x', 'Sample_y', 'Sample_z', 'Sample_Rx', 'Sample_Ry', 'Sample_Rz', \
                  'Detector_x', 'Detector_z']
        
        return None

    def SampleSF_mvrX(self, _value, WaitForMove=True):
        try:
            __delta = float(_value)
            __currentx = float(self.Controller6.GetVarValue('Q87', silent=True, valreturn=True))
            __currenty = float(self.Controller6.GetVarValue('Q88', silent=True, valreturn=True))
            __currentRot = float(self.Controller5.GetVarValue('P82', silent=True, valreturn=True))
            __valx = __currentx + numpy.cos(__currentRot * numpy.pi / 180) * __delta
            __valy = __currenty - numpy.sin(__currentRot * numpy.pi / 180) * __delta
        except:
            print(misc.GetTimeString() + ': Error: Could not convert %s to a number!' % str(_value))
            return None
        try:
            _state = self.Controller6.GetVarValue('P80', valreturn=True, silent=True)
        except:
            print(misc.GetTimeString() + ': Error: Could not communicate with controller.')
            return None
        if _state == 1.0:
            if (-4.5 < __valx < 4.5) and (-4.5 < __valy < 4.5):
                try:
                    self.Controller6.WriteVariable('Q77', '%.5f' % __valx)
                    self.Controller6.WriteVariable('Q78', '%.5f' % __valy)
                    time.sleep(0.05)
                    tmp = self.Controller6.GetResponse('Q70 = 4', silent=True)
                    if WaitForMove:
                        time0 = time.time()
                        while True:
                            time.sleep(0.05)
                            _state = self.Controller6.GetVarValue('P80', valreturn=True, silent=True)
                            if time.time() > time0 + 200:
                                print(misc.GetTimeString() + ': Error: Response timeout')
                                __error = True
                                break
                            if _state == 1:
                                break
                except:
                    print(misc.GetTimeString() + ': Error: Error while sending move command.')
        return None
    
    def SampleSF_mvrY(self, _value, WaitForMove=True):
        try:
            __delta = float(_value)
            __currentx = float(self.Controller6.GetVarValue('Q87', silent=True, valreturn=True))
            __currenty = float(self.Controller6.GetVarValue('Q88', silent=True, valreturn=True))
            __currentRot = float(self.Controller5.GetVarValue('P82', silent=True, valreturn=True))
            __valx = __currentx + numpy.sin(__currentRot * numpy.pi / 180) * __delta
            __valy = __currenty + numpy.cos(__currentRot * numpy.pi / 180) * __delta
        except:
            print(misc.GetTimeString() + ': Error: Could not convert %s to a number!' % str(_value))
            return None
        try:
            _state = self.Controller6.GetVarValue('P80', valreturn=True, silent=True)
        except:
            print(misc.GetTimeString() + ': Error: Could not communicate with controller.')
            return None
        if _state == 1.0:
            try:
                self.Controller6.WriteVariable('Q77', '%.5f' % __valx)
                self.Controller6.WriteVariable('Q78', '%.5f' % __valy)
                time.sleep(0.05)
                tmp = self.Controller6.GetResponse('Q70 = 4', silent=True)
                if WaitForMove:
                    time0 = time.time()
                    while True:
                        time.sleep(0.05)
                        _state = self.Controller6.GetVarValue('P80', valreturn=True, silent=True)
                        if time.time() > time0 + 200:
                            print(misc.GetTimeString() + ': Error: Response timeout')
                            __error = True
                            break
                        if _state == 1:
                            break
            except:
                print(misc.GetTimeString() + ': Error: Error while sending move command.')
        return None
    
    def Move(self, motorstring, position, WaitForMove=True, ReturnFeedback=False, ForceMove=False):
        """Move the motor <motorstring> to the position <position>"""
        __error = False
        if motorstring not in self.Dict.keys():
            print(misc.GetTimeString() + ': Error: Motor %s unknown!' % motorstring)
        try:
            _val = float(position)
        except:
            print(misc.GetTimeString() + ': Error: Could not convert %s to a number!' % str(position))
            return None
        try:
            _state = self.Dict[motorstring]['Controller'].GetVarValue('P80', valreturn=True, silent=True)
        except:
            print(misc.GetTimeString() + ': Error: Could not communicate with controller.')
            return None

        if (position < max(self.Dict[motorstring]['lowerLim'], self.Dict[motorstring]['lowerSoftLim'])) or \
           (min(self.Dict[motorstring]['upperLim'], self.Dict[motorstring]['upperSoftLim']) < position):
            print(misc.GetTimeString() + ': Error: Requested position %f outside of limits for motor %s. Move aborted....' %(position, motorstring))
            return None
        
        
        if _state == 1.0 or ForceMove:
            try:
                self.Dict[motorstring]['Controller'].WriteVariable(self.Dict[motorstring]['TargetVariable'], '%.5f' % _val)
                time.sleep(0.05)
                tmp = self.Dict[motorstring]['Controller'].GetResponse(self.Dict[motorstring]['SetCommand'], silent=True)
                if WaitForMove:
                    time0 = time.time()
                    while True:
                        time.sleep(0.01)
                        _state = self.Dict[motorstring]['Controller'].GetVarValue('P80', valreturn=True, silent=True)
                        if time.time() > time0 + 200:
                            print(misc.GetTimeString() + ': Error: Response timeout')
                            __error = True
                            break
                        if _state == 1:
                            break
            except:
                print(misc.GetTimeString() + ': Error: Error while sending move command.')
        else:
            print(misc.GetTimeString() + ': Error: Controller not ready. Move not started.')
        if __error:
            return None
        if ReturnFeedback:
            return True
        return None
    # end Move

    def MoveRel(self, motorstring, delta, WaitForMove=True, ReturnFeedback=False, ForceMove=False):
        """Move the motor <motorstring> relative the value <delta>"""
        __error = False
        if motorstring not in self.Dict.keys():
            print(misc.GetTimeString() + ': Error: Motor %s unknown!' % motorstring)
        try:
            __delta = float(delta)
            __current = float(self.Dict[motorstring]['Controller'].GetVarValue(self.Dict[motorstring]['TargetVariable'], silent=True, valreturn=True))
            __val = __delta + __current
        except:
            print(misc.GetTimeString() + ': Error: Could not convert %s to a number!' % str(delta))
            return None
        try:
            _state = self.Dict[motorstring]['Controller'].GetVarValue('P80', valreturn=True, silent=True)
        except:
            print(misc.GetTimeString() + ': Error: Could not communicate with controller.')
            return None

        if (__val < max(self.Dict[motorstring]['lowerLim'], self.Dict[motorstring]['lowerSoftLim'])) or \
           (min(self.Dict[motorstring]['upperLim'], self.Dict[motorstring]['upperSoftLim']) < __val):
            print(misc.GetTimeString() + ': Error: Requested position %f outside of limits for motor %s. Move aborted....' %(__val, motorstring))
            return None

        if _state == 1.0 or ForceMove:
            try:
                self.Dict[motorstring]['Controller'].WriteVariable(self.Dict[motorstring]['TargetVariable'], '%.5f' % __val)
                time.sleep(0.05)
                tmp = self.Dict[motorstring]['Controller'].GetResponse(self.Dict[motorstring]['SetCommand'], silent=True)
                if WaitForMove:
                    time0 = time.time()
                    while True:
                        time.sleep(0.05)
                        _state = self.Dict[motorstring]['Controller'].GetVarValue('P80', valreturn=True, silent=True)
                        if time.time() > time0 + 200:
                            print(misc.GetTimeString() + ': Error: Response timeout')
                            __error = True
                            break
                        if _state == 1:
                            break
            except:
                print(misc.GetTimeString() + ': Error: Error while sending move command.')
        else:
            print(misc.GetTimeString() + ': Error: Controller not ready. Move not started.')
        if __error:
            return None
        if ReturnFeedback:
            return True
        return None
    # end MoveRel
    
    def ShowMotors(self):
        """Method to show all motorstrings from dictionary"""
        for motor in self.Dict.keys():
            print('Motor: %s' % motor)
        return None
    # end ShowMotors
    
    def ReadMotorPos(self, motorstring, valreturn=True):
        """Method to read the position of motor <motorstring>.
        If <valreturn> == True, return value is the float motor position,
        else, the current position is printed on screen."""
        __error = False
        if motorstring not in self.Dict.keys():
            print(misc.GetTimeString() + ': Error: Motor %s unknown!' % motorstring)
            return None
        try:
            __current = float(self.Dict[motorstring]['Controller'].GetVarValue(self.Dict[motorstring]['CurVariable'], silent=True, valreturn=True))
        except:
            print(misc.GetTimeString() + ': Error: could not read motor position')
            return None
        if valreturn:
            return __current
        else:
            print('%s = %f' % (motorstring, __current))
            return None

    def ReadAllMotorPos(self, valreturn=True, silent=True):
        """Method to return a formatted string with the values of all motor positions."""
        __string = ''
        for __item in self.MotorList:
            __current = self.ReadMotorPos(__item, valreturn=True)
            if __current != None:
                if not silent: print('%s = \t%e' % (__item, __current))
                __string += '%e\t' % (__current)
            else:
                if not silent: print('%s = \tNone' % (__item))
                __string += 'NaN\t\t'    
            
        if valreturn:
            return __string
        else:
            return None
    # end ReadAllMotorPos
    
    def ReturnMotorPositionString(self):
        """Method to return a string of motor names and positions."""
        __string = ''
        for __item in self.MotorList:
            __current = self.ReadMotorPos(__item, valreturn=True)
            __string += '%s =\t%e\n' % (__item, __current)
        return __string
    # end ReturnMotorPositionString
    
    def SetRotSpeed(self,speed):
        self.EventSendCommandManual(self.Controller5, 'P97='+str(speed))


    ## function for reading in manually defined parameters, e.g. for initilizing the beamline
    def EventSendCommandManual(self, controllerID, _input):
        if controllerID.IsReady():
            _response = controllerID.GetResponse(_input)
            print("Response: ")
            print(_response)
        else:
            print("Warning! Controller is not ready for command. Request ignored")
            #QtGui.QMessageBox.warning(self, 'Warning', "Controller is not ready for command. Request ignored", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        return None

    def StopPMACmoveC5(self):
        self.Controller5.GetResponse('Q70 = 16')
        return None

    def ResetErrorsC5(self):
        self.Controller5.GetResponse('Q70 = 16')
        return None

    def checkInit(self,controllerID):
        count = 1
        _input = 'P80'
        busy = True
        while busy:
            count += 1
            print("Waiting!")
            time.sleep(0.5)
            if controllerID.IsReady():
                _response = controllerID.GetResponse(_input)
                busy = False
                
        return None
    
    
    def checkInitController5(self):
        while self.Controller5.GetResponse('P80', silent=True) != 1:
            time.sleep(0.1)
        return None
        
    def Exit(self):
        self.Controller1.CloseConnection()
        self.Controller2.CloseConnection()
        self.Controller3.CloseConnection()
        self.Controller4.CloseConnection()
        self.Controller5.CloseConnection()
        self.Controller6.CloseConnection()

# if __name__ == "__main__":
#     print "hej"
#     PMACdict.SampleSF_mvrY(1)