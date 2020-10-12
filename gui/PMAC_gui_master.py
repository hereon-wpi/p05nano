import os
import sys
import time

import numpy
from PyQt5 import QtCore, QtGui, uic as QtUic
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

import p05.tools.misc as misc
from p05.devices.PMACcomm import PMACcomm
from p05.devices.PMACdict import PMACdict
from p05.gui.PMAC_generic_motors import getPMACmotorList, getPMACmotorGroups
from p05.gui.PMAC_generic_motors import getPMACmotorUserList, getPMACmotorUserGroups
from p05.gui.PMAC_motorForm import cPMACmotor
from p05.gui.PMAC_sliderForm import cPMACair, cPMACslider


class cPMACgui(QtWidgets.QMainWindow):
    jobFinished = pyqtSignal(object)  #object is [self.p80, self.p89, self.p91, self.p92, self.isPos, self.setPos, self.airsignals]

    def __init__(self, parent = None, blockdirectmovements=True, devices=[], groups=[], name='PMAC motor GUI',user=False):
        super(cPMACgui, self).__init__()
        try:
            QtUic.loadUi('h:/_data/programming_python/p05/gui/PMAC_ui.ui', self)
            self.setWindowIcon(QtGui.QIcon('h:/_data/programming_python/p05/gui/images/gear.png'))
        except:
            _path = misc.GetPath('PMAC_ui.ui')
            QtUic.loadUi(_path, self)
            self.setWindowIcon(QtGui.QIcon(os.path.split(_path)[0] + os.sep + 'gear.png'))
        self.setWindowTitle(name)
        # self.setWindowIcon(QtGui.QIcon('h:/_data/programming_python/p05/gui/images/gear.png'))
        self.groupBox_PMAC.raise_()
        self.setGeometry(10, 25, 1825, 1110)
        
        self.main = parent
        self._initialize(devices, groups,user)
        
        self.io_pmac_polling.setValidator(self.floatValidator)
        self.controllers = numpy.empty(8, dtype=object)
        self.controllers[1:8] = [PMACcomm(controller=i1, ioconsole=False, silentmode=True) for i1 in range(1, 8)]
        self.controllerFaultA = numpy.empty(8, dtype=bool)
        self.controllerFaultA[:] = False
        self.controllerFaultB = numpy.empty(8, dtype=bool)
        self.controllerFaultB[:] = False
        self.controllerStatus = numpy.zeros((8))
        
        # QtCore.QObject.connect(self.updater, QtCore.SIGNAL("timeout()"), self.updatePMACs)
        self.updater.timeout.connect(self.updatePMACs)
        # QtCore.QObject.connect(self.but_pmac_polling, QtCore.SIGNAL('clicked()'), self.clickButtonPolling)
        self.but_pmac_polling.clicked.connect(self.clickButtonPolling)
        # (self.but_pmac_connection, QtCore.SIGNAL('clicked()'), self.clickButtonConnectPMACs)
        self.but_pmac_connection.clicked.connect(self.clickButtonConnectPMACs)

        # QtCore.QObject.connect(self.but_pmac01_stopmove, QtCore.SIGNAL('clicked()'), self.clickButtonStopMove01)
        self.but_pmac01_stopmove.clicked.connect(self.clickButtonStopMove01)
        # QtCore.QObject.connect(self.but_pmac02_stopmove, QtCore.SIGNAL('clicked()'), self.clickButtonStopMove02)
        self.but_pmac02_stopmove.clicked.connect(self.clickButtonStopMove02)
        # QtCore.QObject.connect(self.but_pmac03_stopmove, QtCore.SIGNAL('clicked()'), self.clickButtonStopMove03)
        self.but_pmac03_stopmove.clicked.connect(self.clickButtonStopMove03)
        # QtCore.QObject.connect(self.but_pmac04_stopmove, QtCore.SIGNAL('clicked()'), self.clickButtonStopMove04)
        self.but_pmac04_stopmove.clicked.connect(self.clickButtonStopMove04)
        # QtCore.QObject.connect(self.but_pmac05_stopmove, QtCore.SIGNAL('clicked()'), self.clickButtonStopMove05)
        self.but_pmac05_stopmove.clicked.connect(self.clickButtonStopMove05)
        # QtCore.QObject.connect(self.but_pmac06_stopmove, QtCore.SIGNAL('clicked()'), self.clickButtonStopMove06)
        self.but_pmac06_stopmove.clicked.connect(self.clickButtonStopMove06)
        # QtCore.QObject.connect(self.but_pmac07_stopmove, QtCore.SIGNAL('clicked()'), self.clickButtonStopMove07)
        self.but_pmac07_stopmove.clicked.connect(self.clickButtonStopMove07)

        # QtCore.QObject.connect(self.but_pmac01_reseterrors, QtCore.SIGNAL('clicked()'), self.clickButtonResetErrors01)
        self.but_pmac01_reseterrors.clicked.connect(self.clickButtonResetErrors01)
        # QtCore.QObject.connect(self.but_pmac02_reseterrors, QtCore.SIGNAL('clicked()'), self.clickButtonResetErrors02)
        self.but_pmac02_reseterrors.clicked.connect(self.clickButtonResetErrors02)
        # QtCore.QObject.connect(self.but_pmac03_reseterrors, QtCore.SIGNAL('clicked()'), self.clickButtonResetErrors03)
        self.but_pmac03_reseterrors.clicked.connect(self.clickButtonResetErrors03)
        # QtCore.QObject.connect(self.but_pmac04_reseterrors, QtCore.SIGNAL('clicked()'), self.clickButtonResetErrors04)
        self.but_pmac04_reseterrors.clicked.connect(self.clickButtonResetErrors04)
        # QtCore.QObject.connect(self.but_pmac05_reseterrors, QtCore.SIGNAL('clicked()'), self.clickButtonResetErrors05)
        self.but_pmac05_reseterrors.clicked.connect(self.clickButtonResetErrors05)
        # QtCore.QObject.connect(self.but_pmac06_reseterrors, QtCore.SIGNAL('clicked()'), self.clickButtonResetErrors06)
        self.but_pmac06_reseterrors.clicked.connect(self.clickButtonResetErrors06)
        # QtCore.QObject.connect(self.but_pmac07_reseterrors, QtCore.SIGNAL('clicked()'), self.clickButtonResetErrors07)
        self.but_pmac07_reseterrors.clicked.connect(self.clickButtonResetErrors07)

        # QtCore.QObject.connect(self.but_pmac01_sendcmd, QtCore.SIGNAL('clicked()'), self.clickButtonSendCommand01)
        self.but_pmac01_sendcmd.clicked.connect(self.clickButtonSendCommand01)
        # QtCore.QObject.connect(self.but_pmac02_sendcmd, QtCore.SIGNAL('clicked()'), self.clickButtonSendCommand02)
        self.but_pmac02_sendcmd.clicked.connect(self.clickButtonSendCommand02)
        # QtCore.QObject.connect(self.but_pmac03_sendcmd, QtCore.SIGNAL('clicked()'), self.clickButtonSendCommand03)
        self.but_pmac03_sendcmd.clicked.connect(self.clickButtonSendCommand03)
        # QtCore.QObject.connect(self.but_pmac04_sendcmd, QtCore.SIGNAL('clicked()'), self.clickButtonSendCommand04)
        self.but_pmac04_sendcmd.clicked.connect(self.clickButtonSendCommand04)
        # QtCore.QObject.connect(self.but_pmac05_sendcmd, QtCore.SIGNAL('clicked()'), self.clickButtonSendCommand05)
        self.but_pmac05_sendcmd.clicked.connect(self.clickButtonSendCommand05)
        # QtCore.QObject.connect(self.but_pmac06_sendcmd, QtCore.SIGNAL('clicked()'), self.clickButtonSendCommand06)
        self.but_pmac06_sendcmd.clicked.connect(self.clickButtonSendCommand06)
        # QtCore.QObject.connect(self.but_pmac07_sendcmd, QtCore.SIGNAL('clicked()'), self.clickButtonSendCommand07)
        self.but_pmac07_sendcmd.clicked.connect(self.clickButtonSendCommand07)
        
        
        
        self.show()
        return None
    
    def _initialize(self, devices, groups,user):
        self.button_style = """QPushButton{border: solid; border-bottom-color: #777777; border-bottom-width: 2px; border-right-color:#777777;\
                       border-right-width: 2px; border-top-color:#AAAAAA; border-top-width: 1px; border-left-color:#AAAAAA;\
                       border-left-width: 1px; border-radius: 3px; padding: 1px;  background: qlineargradient(x1: 0, y1: \
                       0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}\
                       QPushButton:pressed{background:qlineargradient(x1: 0, y1: \
                       0, x2: 0, y2: 1, stop: 0 #dadada, stop: 0.4 #d4d4d4, stop: 0.5 #c7c7c7, stop: 1.0 #dadada) }"""
        self.button_style_red = """QPushButton{border: solid; border-bottom-color: #777777; border-bottom-width: 2px; border-right-color:#777777;\
                       border-right-width: 2px; border-top-color:#AAAAAA; border-top-width: 1px; border-left-color:#AAAAAA;\
                       border-left-width: 1px; border-radius: 3px; padding: 1px;   background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                       stop: 0 #F8EBEB, stop: 0.4 #F8EBEB, stop: 0.5 #E6D0D0, stop: 1.0 #F8EBEB);}\
                       QPushButton:pressed{ background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #D8CBCB, stop: 0.4 #D8CBCB,
                                 stop: 0.5 #C6B0B0, stop: 1.0 #D8CBCB);}"""
        self.button_style_yellow = """QPushButton{border: solid; border-bottom-color: #777777; border-bottom-width: 2px; border-right-color:#777777;\
                       border-right-width: 2px; border-top-color:#AAAAAA; border-top-width: 1px; border-left-color:#AAAAAA;\
                       border-left-width: 1px; border-radius: 3px; padding: 1px;   background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                       stop: 0 #FAFAEA, stop: 0.4 #FAFAEA, stop: 0.5 #E7E7E7, stop: 1.0 #FAFAEA);}\
                       QPushButton:pressed{ background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #EAEACA, stop: 0.4 #D8CBCB,
                                 stop: 0.5 #EAEACA, stop: 1.0 #D8CBCB);}"""
        self.spin_style = """QDoubleSpinBox{border: solid;  border-bottom-color: #AAAAAA; border-bottom-width: 1px; border-right-color:#AAAAAA;\
                                 border-right-width: 1px;  border-top-color:#777777; border-top-width: 1px; border-left-color:#777777; 
                                 border-left-width: 1px;  border-radius: 3px; padding: 1px;  background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                 stop: 0 #ECECEC, stop: 0.4 #ECECEC, stop: 0.5 #DCDCDC, stop: 1.0 #ECECEC)};"""
        self.textbox_style = """QLineEdit{border: solid;  border-bottom-color: #AAAAAA; border-bottom-width: 1px; border-right-color:#AAAAAA;\
                                 border-right-width: 1px;  border-top-color:#777777; border-top-width: 1px; border-left-color:#777777; 
                                 border-left-width: 1px;  border-radius: 3px; padding: 1px;  background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\
                                 stop: 0 #ECECEC, stop: 0.4 #ECECEC, stop: 0.5 #DCDCDC, stop: 1.0 #ECECEC)};"""
        self.palette_red = QtGui.QPalette()
        self.palette_red.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
        
        self.palette_green = QtGui.QPalette()
        self.palette_green.setColor(QtGui.QPalette.Foreground, QtCore.Qt.green)
        
        self.palette_blk = QtGui.QPalette()
        self.palette_blk.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)

        self.palette_yellow = QtGui.QPalette()
        self.palette_yellow.setColor(QtGui.QPalette.Foreground, QtCore.Qt.yellow)

        self.but_pmac_polling.setStyleSheet(self.button_style)
        self.but_pmac_connection.setStyleSheet(self.button_style)
        
        self.but_pmac01_stopmove.setStyleSheet(self.button_style_red)
        self.but_pmac02_stopmove.setStyleSheet(self.button_style_red)
        self.but_pmac03_stopmove.setStyleSheet(self.button_style_red)
        self.but_pmac04_stopmove.setStyleSheet(self.button_style_red)
        self.but_pmac05_stopmove.setStyleSheet(self.button_style_red)
        self.but_pmac06_stopmove.setStyleSheet(self.button_style_red)
        self.but_pmac07_stopmove.setStyleSheet(self.button_style_red)
        
        self.but_pmac01_reseterrors.setStyleSheet(self.button_style)
        self.but_pmac02_reseterrors.setStyleSheet(self.button_style)
        self.but_pmac03_reseterrors.setStyleSheet(self.button_style)
        self.but_pmac04_reseterrors.setStyleSheet(self.button_style)
        self.but_pmac05_reseterrors.setStyleSheet(self.button_style)
        self.but_pmac06_reseterrors.setStyleSheet(self.button_style)
        self.but_pmac07_reseterrors.setStyleSheet(self.button_style)
        
        self.but_pmac01_sendcmd.setStyleSheet(self.button_style_yellow)
        self.but_pmac02_sendcmd.setStyleSheet(self.button_style_yellow)
        self.but_pmac03_sendcmd.setStyleSheet(self.button_style_yellow)
        self.but_pmac04_sendcmd.setStyleSheet(self.button_style_yellow)
        self.but_pmac05_sendcmd.setStyleSheet(self.button_style_yellow)
        self.but_pmac06_sendcmd.setStyleSheet(self.button_style_yellow)
        self.but_pmac07_sendcmd.setStyleSheet(self.button_style_yellow)

        
        self.io_pmac_polling.setStyleSheet(self.textbox_style)
        self.label_pmac_connection.setPalette(self.palette_red)
        self.label_pmac_connection.setText('disconnected')

        self.global_pmacsconnected = False
        self.global_delay = 250
        
        self.floatValidator = QtGui.QDoubleValidator(self)
        self.floatValidator.setRange(-360.00000, 360.00000, decimals = 5)
        
        self.stdfont = QtGui.QFont()
        self.stdfont.setFamily("Arial")
        self.stdfont.setPointSize(11)

        self.stdfontsmall = QtGui.QFont()
        self.stdfontsmall.setFamily("Arial")
        self.stdfontsmall.setPointSize(8)
        
        self.stdfontbold = QtGui.QFont()
        self.stdfontbold.setFamily("Arial")
        self.stdfontbold.setPointSize(11)
        self.stdfontbold.setBold(True)
        self.stdfontbold.setWeight(75)

        self.motors = numpy.empty(len(devices) + 4, dtype=object)
        self.motor_bgcolor = numpy.empty(len(devices) + 4, dtype=object)
        self.motor_posx = numpy.zeros((len(devices) + 4))
        self.motor_posy = numpy.zeros((len(devices) + 4))
        
        self.pmacdict = PMACdict(dummy = True).Dict
        self.pmacdict[-4] = self.pmacdict['GraniteSlab_1']
        self.pmacdict[-3] = self.pmacdict['GraniteSlab_2']
        self.pmacdict[-2] = self.pmacdict['GraniteSlab_3']
        self.pmacdict[-1] = self.pmacdict['GraniteSlab_4']

        self.groups = groups
        self.groups_mvr = numpy.r_[[QtWidgets.QGroupBox() for i1 in range(len(groups) + 1)]]
        self.groups_pos = numpy.r_[[QtWidgets.QGroupBox() for i1 in range(len(groups) + 1)]]
        self.group_stylesheet = numpy.empty(len(groups), dtype=object)
        self.status_labels = [None, self.label_pmac01_status, self.label_pmac02_status, self.label_pmac03_status, self.label_pmac04_status,
                           self.label_pmac05_status, self.label_pmac06_status, self.label_pmac07_status]
        self.p80_labels = [None, self.label_pmac01_p80, self.label_pmac02_p80, self.label_pmac03_p80, self.label_pmac04_p80,
                           self.label_pmac05_p80, self.label_pmac06_p80, self.label_pmac07_p80]
        self.p80b_labels = [None, self.label_pmac01_p80b, self.label_pmac02_p80b, self.label_pmac03_p80b, self.label_pmac04_p80b,
                           self.label_pmac05_p80b, self.label_pmac06_p80b, self.label_pmac07_p80b]
        self.p89_labels = [None, self.label_pmac01_p89, self.label_pmac02_p89, self.label_pmac03_p89, self.label_pmac04_p89,
                           self.label_pmac05_p89, self.label_pmac06_p89, self.label_pmac07_p89]
        self.p91_labels = [None, self.label_pmac01_p91, self.label_pmac02_p91, self.label_pmac03_p91, self.label_pmac04_p91,
                           self.label_pmac05_p91, self.label_pmac06_p91, self.label_pmac07_p91]
        self.p92_labels = [None, self.label_pmac01_p92, self.label_pmac02_p92, self.label_pmac03_p92, self.label_pmac04_p92,
                           self.label_pmac05_p92, self.label_pmac06_p92, self.label_pmac07_p92]
        if user:
            self.but_pmac01_stopmove.hide()
            self.but_pmac02_stopmove.hide()
            self.but_pmac03_stopmove.hide()
            self.but_pmac04_stopmove.hide()
            self.but_pmac05_stopmove.hide()
            self.but_pmac06_stopmove.hide()
            self.but_pmac07_stopmove.hide()
            self.label_pmac01_p80.hide()

            self.but_pmac01_reseterrors.hide()
            self.but_pmac02_reseterrors.hide()
            self.but_pmac03_reseterrors.hide()
            self.but_pmac04_reseterrors.hide()
            self.but_pmac05_reseterrors.hide()
            self.but_pmac06_reseterrors.hide()
            self.but_pmac07_reseterrors.hide()
            
            self.but_pmac01_sendcmd.hide()
            self.but_pmac02_sendcmd.hide()
            self.but_pmac03_sendcmd.hide()
            self.but_pmac04_sendcmd.hide()
            self.but_pmac05_sendcmd.hide()
            self.but_pmac06_sendcmd.hide()
            self.but_pmac07_sendcmd.hide()
            
            for i in self.p80_labels[1:]:
                i.hide()
        
        
        x0, y0 = 5, 5
        im = 0
        # initialize normal groups
        for i1 in range(self.groups_pos.size - 1):
            group = self.groups[i1]
            dy = 18 + group[1] * 65
            if y0 + dy >= 900: 
                y0, x0 = 5, x0 + 430
            self.group_stylesheet[i1] = """QGroupBox{background-color:%s}""" % group[2]
            self.groups_mvr[i1] = (QtWidgets.QGroupBox(self.tab_relativemovement))
            self.groups_pos[i1] = (QtWidgets.QGroupBox(self.tab_positions))
                
            for item in [self.groups_mvr[i1], self.groups_pos[i1]]:
                item.setFlat(True)
                item.setFont(self.stdfont)
                item.setTitle(group[0])
                item.setGeometry(QtCore.QRect(x0, y0, 425, dy))
                item.setStyleSheet(self.group_stylesheet[i1])
            self.motor_posy[im:im + group[1]] = 18 + y0 + numpy.arange(group[1]) * 65
            self.motor_posx[im:im + group[1]] = 20 + x0
            self.motor_bgcolor[im:im + group[1]] = group[2]
            
            y0 += dy + 10
            im += group[1]
        # initialize slider group
        dy = 600
        if y0 + dy >= 900: 
            y0, x0 = 5, x0 + 430
        self.group_stylesheet[-1] = """QGroupBox{background-color:#CCEECC}"""
        self.groups_mvr[-1] = (QtWidgets.QGroupBox(self.tab_relativemovement))
        self.groups_pos[-1] = (QtWidgets.QGroupBox(self.tab_positions))
        for item in [self.groups_mvr[-1], self.groups_pos[-1]]:
                item.setFlat(True)
                item.setFont(self.stdfont)
                item.setTitle('In-beam translations (sliders)')
                item.setGeometry(QtCore.QRect(x0, y0, 425, dy))
                item.setStyleSheet(self.group_stylesheet[-1])
        self.motor_posy[-4:] = 88 + y0 + numpy.arange(4) * 127
        self.motor_posx[-4:] = 20 + x0
        self.motor_bgcolor[-4:] = '#CCEECC'

        for i1 in range(self.motors.size - 4):
            dev = devices[i1]
            if len(dev) == 7:
                self.motors[i1] = cPMACmotor(self, self.motor_posx[i1], self.motor_posy[i1], alias=dev[0], \
                                            controllerID=dev[1], setCommand=dev[2], setPosVar=dev[3], \
                                            isPosVar=dev[4], bgcolor=self.motor_bgcolor[i1], \
                                            lowerlimit=dev[5], upperlimit=dev[6], motorindex=i1) 
            else:
                self.motors[i1] = cPMACmotor(self, self.motor_posx[i1], self.motor_posy[i1], alias=dev[0], \
                                            controllerID=dev[1], setCommand=dev[2], setPosVar=dev[3], \
                                            isPosVar=dev[4], bgcolor=self.motor_bgcolor[i1], motorindex=i1)


        for i1 in [-4, -3, -2, -1]:
            ul = min(self.pmacdict[i1]['upperLim'], self.pmacdict[i1]['upperSoftLim'])
            ll = max(self.pmacdict[i1]['lowerLim'], self.pmacdict[i1]['lowerSoftLim'])  
            self.motors[i1] = cPMACslider(self, self.motor_posx[i1], self.motor_posy[i1], alias='Slider #%i' % (i1 + 5), \
                                         controllerID=3, sliderID=i1 + 5, \
                                         bgcolor=self.motor_bgcolor[i1], motorindex=self.motors.size + i1, \
                                         lowerlimit = ll, upperlimit= ul)
            
        self.AirUpdater = cPMACair(self, xoffset=x0, yoffset=18 + y0, bgcolor='#CCEECC')
        return None
    #end _initialize

    
    def updatePMACs(self):
        # index = self.tabs.currentIndex()
        self.t0 = time.time()
        for i1 in range(1, 8):
            if self.controllers[i1] != None:
                tmp = self.controllers[i1].ReadVariable('P80')
                self.controllerStatus[i1] = tmp
                self.p80_labels[i1].setText('$' + hex(int(tmp))[2:].upper())
                self.p80b_labels[i1].setText(str(int(tmp)))
                if tmp == 0:
                    self.controllerFaultA[i1] = False
                    self.status_labels[i1].setText('moving')
                    self.status_labels[i1].setPalette(self.palette_green)
                elif tmp == 1:
                    self.controllerFaultA[i1] = False
                    self.status_labels[i1].setText('idle')
                    self.status_labels[i1].setPalette(self.palette_blk)
                elif tmp not in [0, 1]:
                    if self.controllerFaultA[i1] == False:
                        self.controllerFaultB[i1] = True
                    self.controllerFaultA[i1] = True
                    self.status_labels[i1].setText('error')
                    self.status_labels[i1].setPalette(self.palette_red)
        self.label_timeedit.setTime(QtCore.QTime.currentTime())
        # print index, time.time() - self.t0
        return None
            
    def clickButtonPolling(self):
        """Set the self.global_delay variable (in ms) """
        try: 
            _txt = self.io_pmac_polling.text()
            _val = float(_txt)
            self.global_pmacpolling = float(_val)
            self.label_pmac_pollingvalue.setText(_txt + ' ms')
            self.global_delay = _val 
            self.PollingThread.set_delay(_val * 1e-3)
            if self.global_pmacsconnected:
                self.updater.setInterval(self.global_delay)
                self.PollingThread.stop()
                self.PollingThread.restart()
        except:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Could not convert the string "%s" to a number.' % _txt,
                                          buttons=QtWidgets.QMessageBox.Ok)
        return None
    
    def clickButtonConnectPMACs(self):
        if self.global_pmacsconnected:
            self.label_pmac_connection.setPalette(self.palette_red)
            self.label_pmac_connection.setText('inactive')
            self.but_pmac_connection.setText('Start PMAC update')
            self.global_pmacsconnected = False
            self.updater.stop()
            self.PollingThread.stop()
            #for controller in self.controllers[1:8]:
            #    controller.CloseConnection()
            for motor in self.motors:
                motor.ActivateMotor(False)
                motor.pos_window.label_status.setText('disconnected')
                motor.pos_window.label_status.setPalette(self.palette_blk)
                motor.mvr_window.label_status.setText('disconnected')
                motor.mvr_window.label_status.setPalette(self.palette_blk)
        elif self.global_pmacsconnected == False:
            self.label_pmac_connection.setPalette(self.palette_green)
            self.label_pmac_connection.setText('active update')
            self.but_pmac_connection.setText('Stop PMAC update')
            #for controller in self.controllers[1:8]:
            #    controller.OpenConnection()
            self.global_pmacsconnected = True
            for motor in self.motors:
                motor.ActivateMotor(True)
            self.updater.start(self.global_delay)
            self.PollingThread.restart()
        return None
    
    def clickButtonStopMove01(self):
        self.EventStopPMACmovement(1)
        return None
    def clickButtonStopMove02(self):
        self.EventStopPMACmovement(2)
        return None
    def clickButtonStopMove03(self):
        self.EventStopPMACmovement(3)
        return None
    def clickButtonStopMove04(self):
        self.EventStopPMACmovement(4)
        return None
    def clickButtonStopMove05(self):
        self.EventStopPMACmovement(5)
        return None
    def clickButtonStopMove06(self):
        self.EventStopPMACmovement(6)
        return None
    def clickButtonStopMove07(self):
        self.EventStopPMACmovement(7)
        return None
    
    def clickButtonResetErrors01(self):
        self.EventResetErrors(1)
        return None
    def clickButtonResetErrors02(self):
        self.EventResetErrors(2)
        return None
    def clickButtonResetErrors03(self):
        self.EventResetErrors(3)
        return None
    def clickButtonResetErrors04(self):
        self.EventResetErrors(4)
        return None
    def clickButtonResetErrors05(self):
        self.EventResetErrors(5)
        return None
    def clickButtonResetErrors06(self):
        self.EventResetErrors(6)
        return None
    def clickButtonResetErrors07(self):
        self.EventResetErrors(7)
        return None

    def clickButtonSendCommand01(self):
        self.EventSendCommand(1, self.io_cmd_pmac01, self.label_pmac01_cmdresponse)
        return None
    def clickButtonSendCommand02(self):
        self.EventSendCommand(2, self.io_cmd_pmac02, self.label_pmac02_cmdresponse)
        return None
    def clickButtonSendCommand03(self):
        self.EventSendCommand(3, self.io_cmd_pmac03, self.label_pmac03_cmdresponse)
        return None
    def clickButtonSendCommand04(self):
        self.EventSendCommand(4, self.io_cmd_pmac04, self.label_pmac04_cmdresponse)
        return None
    def clickButtonSendCommand05(self):
        self.EventSendCommand(5, self.io_cmd_pmac05, self.label_pmac05_cmdresponse)
        return None
    def clickButtonSendCommand06(self):
        self.EventSendCommand(6, self.io_cmd_pmac06, self.label_pmac06_cmdresponse)
        return None
    def clickButtonSendCommand07(self):
        self.EventSendCommand(7, self.io_cmd_pmac07, self.label_pmac07_cmdresponse)
        return None

    def EventStopPMACmovement(self, controller):
        self.controllers[controller].GetResponse('Q70 = 16')
        return None

    def EventResetErrors(self, controller):
        self.controllers[controller].GetResponse('Q70 = 16')
        self.controllerFaultB[controller] = False
        return None

    def EventSendCommand(self, controllerID, io_input, text_output):
        _input = str(io_input.text())
        if self.controllers[controllerID].IsReady():
            _response = self.controllers[controllerID].GetResponse(_input)
            text_output.setText(_response)
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', "Controller is not ready for command. Request ignored",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        return None

    
        
    def NewUpdate(self, signal):
        index = self.tabs.currentIndex()
        self.p80, self.p89, self.p91, self.p92, self.isPos, self.setPos, self.airStatus = signal
        t0 = time.time()
        for i1 in range(1, 8):
            self.p89_labels[i1].setText('$' + hex(int(self.p89[i1]))[2:].upper())
            self.p91_labels[i1].setText('$' + hex(int(self.p91[i1]))[2:].upper())
            self.p92_labels[i1].setText('$' + hex(int(self.p92[i1]))[2:].upper())
        for i1 in range(self.motors.size - 4):
            self.motors[i1].eventLoopUpdate(index=index, pos=self.isPos[i1], targetpos=self.setPos[i1])
        for i1 in [-4, -3, -2, -1]:
            self.motors[i1].eventLoopUpdate(index=index, pos=self.isPos[i1], targetpos=self.setPos[i1], \
                                            airstatus=self.airStatus[0][i1 + 4], vacstatus=self.airStatus[1][i1 + 4])
        self.AirUpdater.Update(index=index)
        # print 'gui update', time.time() - t0
        return None
    
    def closeEvent(self, event):
        """Safety check for closing of window."""
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               "Are you sure to quit?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.PollingThread.terminate_signal = True
            event.accept()
        else:
            event.ignore()
        return None   


class  PMACpolling(QtCore.QThread):
    def __init__(self, parentThread, controllers, motors, airstatus, cur_delay = 0.25):
        QtCore.QThread.__init__(self, parentThread)
        self.controllers = controllers
        self.motors = motors
        self.AirUpdater = airstatus
        self.motorsize = self.motors.size 
        self.setPos = numpy.zeros((self.motorsize))
        self.isPos = numpy.zeros((self.motorsize))
        self.p80 = numpy.zeros((8))
        self.p89 = numpy.zeros((8))
        self.p91 = numpy.zeros((8))
        self.p92 = numpy.zeros((8))
        self.running = False
        self.cur_delay = cur_delay
        self.terminate_signal = False
        return None
    
    def set_delay(self, value):
        self.cur_delay = value
        return None
    
    def stop(self):
        self.running = False
        return None
    
    def restart(self):
        self.running = True
        return None
    
    def run(self):
        self.running = False
        self.updateControllers()
        return None
    
    def cleanUp(self):
        return None
    
    def getUpdate(self):
        return True
#class PMACpolling


class UpdateThread(PMACpolling):
    def __init__(self, parentThread, controllers, motors, airstatus, cur_delay = 0.25):
        PMACpolling.__init__(self, parentThread, controllers, motors, airstatus, cur_delay = cur_delay)
        return None
            
    def updateControllers(self):
        while True:
            if self.running:
                self.t0 = time.time()
                for i1 in range(1, 8):
                    tmp = self.controllers[i1].ReadVariable('P80')
                    self.p80[i1] = tmp
                    tmp = self.controllers[i1].ReadVariable('P89')
                    self.p89[i1] = tmp
                    tmp = self.controllers[i1].ReadVariable('P91')
                    self.p91[i1] = tmp
                    tmp = self.controllers[i1].ReadVariable('P92')
                    self.p92[i1] = tmp
                
                self.airsignals = self.AirUpdater.GetVarUpdate()

                for i1 in range(self.motorsize):
                    motor = self.motors[i1]
                    self.isPos[i1] = self.controllers[motor.controllerID].ReadVariable(motor.isPosVar)
                    self.setPos[i1] = self.controllers[motor.controllerID].ReadVariable(motor.setPosVar)

                time.sleep(max(0, self.cur_delay - (time.time() - self.t0)))
                # self.emit(QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), [self.p80, self.p89, self.p91, self.p92, self.isPos, self.setPos, self.airsignals])
                self.jobFinished.emit([self.p80, self.p89, self.p91, self.p92, self.isPos, self.setPos, self.airsignals])
            elif self.running == False:
                time.sleep(1.0 * self.cur_delay)
            if self.terminate_signal:
                break
        return None
# class UpdateThread




def PMACgui():
    app = QtWidgets.QApplication(sys.argv)
    gui = cPMACgui(parent=QtWidgets.QMainWindow(), devices=getPMACmotorList(), groups=getPMACmotorGroups(),user=False)
    gui.PollingThread = UpdateThread(gui.main, gui.controllers, gui.motors, gui.AirUpdater, cur_delay = 0.25)

    gui.PollingThread.jobFinished.connect(gui.NewUpdate)
    gui.PollingThread.start()
    gui.show()
    if sys.platform == 'win32' or sys.platform == 'win64':
        sys.exit(app.exec_())
    else:
        app.exec_()


def PMACUsergui():
    app = QtWidgets.QApplication(sys.argv)
    gui = cPMACgui(parent=QtWidgets.QMainWindow(), devices=getPMACmotorUserList(), groups=getPMACmotorUserGroups(),user=True)
    gui.PollingThread = UpdateThread(gui.main, gui.controllers, gui.motors, gui.AirUpdater, cur_delay = 0.25)
    gui.PollingThread.jobFinished.connect(gui.NewUpdate)
    gui.PollingThread.start()
    gui.show()
    if sys.platform == 'win32' or sys.platform == 'win64':
        sys.exit(app.exec_())
    else:
        app.exec_()

  
  
if __name__ == "__main__":
    PMACgui()