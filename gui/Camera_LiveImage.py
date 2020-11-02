import gc
import os
import sys
import time

import PIL
import PyTango
import numpy
import pyqtgraph
from PyQt5 import QtCore, QtGui, uic as QtUic, QtWidgets
from PyQt5.QtCore import pyqtSignal

import p05.common.PyTangoProxyConstants as proxies
import p05.nano
import p05.tools.misc as misc
from p05.devices.PMACdict import PMACdict

gc.enable()

# TODO Split file - too long
class cCamera_LiveImage(QtWidgets.QMainWindow):
    def __init__(self, parent=None, name='Camera live image'):
        super(cCamera_LiveImage, self).__init__()

        _path = misc.GetPath('Cameralive_ui_tab_NewDesign_2.ui')
        QtUic.loadUi(_path, self)
        self.setWindowIcon(QtGui.QIcon(os.path.split(_path)[0] + os.sep + 'images/images.jpg'))
        self.setWindowTitle(name)
        # self.setWindowIcon(QtGui.QIcon('h:/_data/programming_python/p05/gui/images/images.jpg'))
        self.setGeometry(10, 25, 1500, 965)
        self.HamaHutch = 'eh2'  # ALSO CHANGE BELOW if HAMA!!!For hama trigger in eh2 or eh1!
        self.Camera = 'PixelLink'  # !!!GUI ONLY STARTS WHEN THIS KAMERA IS ON!!! CHANGE IF NEEDED!
        # self.Camera = 'PCO'
        self.pid = os.getpid()

        self.tBeamShutter = PyTango.DeviceProxy(proxies.tBeam_shutter)
        
        if self.Camera == 'Hamamatsu':
            self.tCamera = PyTango.DeviceProxy(proxies.camera_hama)
            if self.HamaHutch == 'eh1':
                self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_01)
            elif self.HamaHutch == 'eh2':
                print("eh2")
                self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out03)
            self.cB_Cameras.setCurrentIndex(0)
            self.command_exptime = 'EXPOSURE_TIME'
            self.command_start = 'StartAcq'
            self.command_stop = 'AbortAcq'
            self.command_image = 'IMAGE'
            self.imagesize = (2048, 2048)
            
        if self.Camera == 'PCO':
            self.tCamera = PyTango.DeviceProxy(proxies.camera_pco)
            # self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out01)
            self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_01)

            self.cB_Cameras.setCurrentIndex(1)
            self.command_exptime = 'ExposureTime'
            self.command_start = 'StartAcq'
            self.command_stop = 'StopAcq'
            self.command_image = 'LiveImage'
            self.imagesize = (2048, 2048)
            self.tCamera.write_attribute('TriggerMode',1)
            
        if self.Camera == 'PixelLink':
            self.tCamera = PyTango.DeviceProxy(proxies.camera_pixlink)
            # self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out01)
            self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_01)
            self.cB_Cameras.setCurrentIndex(2)
            self.command_exptime = 'SHUTTER'
            self.command_start = 'StartAcq'
            self.command_stop = 'AbortAcq'
            self.command_image = 'IMAGE'
            self.rotate = 2
            self.imagesize = (2208, 3000)
                
        if self.Camera == 'Zyla':
            self.tCamera = PyTango.DeviceProxy(proxies.camera_zyla)
            # self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out01)
            self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out03)
            self.cB_Cameras.setCurrentIndex(3)
            self.command_exptime = 'acq_expo_time'
            self.command_start = 'startAcq'
            self.command_stop = 'abortAcq'
            self.command_image = 'IMAGE'
            self.tCamera.write_attribute('acq_trigger_mode','INTERNAL_TRIGGER')
            self.tCamera.write_attribute('saving_mode','MANUAL')
            self.imagesize = (2160,2560)


        if self.Camera == 'KIT':
            self.tCamera = PyTango.DeviceProxy(proxies.tCamera_p05)
            # self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out01)
            self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_03)
            self.cB_Cameras.setCurrentIndex(3)
            self.command_exptime = 'acq_expo_time'
            self.command_start = 'startAcq'
            self.command_stop = 'abortAcq'
            self.command_image = 'IMAGE'
            self.tCamera.write_attribute('acq_trigger_mode', 'INTERNAL_TRIGGER')
            self.tCamera.write_attribute('saving_mode', 'MANUAL')
            self.imagesize = (2160, 2560)

        # TODO minor do we really need real value here?
        # if self.tCamera.read_attribute(self.command_exptime).value == None
        #   self.exptime = 30

        # self.exptime = self.tCamera.read_attribute(self.command_exptime).value
        self.exptime = 30
        self.label_currentexptime.setText('%i ms' % (self.exptime * 1e3))

        self.main = parent

        self.bgcolor = '#0097d4'
        self.imageView.ui.graphicsView.setBackground(self.bgcolor)

        self.rulery = pyqtgraph.ROI((0, 0), size=(2048, 1))
        self.rulerx = pyqtgraph.ROI((0, 0), size=(1, 2048))
        self.imageView.getView().addItem(self.rulery)
        self.imageView.getView().addItem(self.rulerx)

        self.upper_right_corner_x = 0
        self.upper_right_corner_y = 0
        self.rotate = 0
        self.HistWidget = self.imageView.getHistogramWidget()
        self.HistWidget.setBackground('#eeeeee')
        # TODO !!! check if Correct
        self.path_scanscripts = 'scanscripts\\'
        # for some reason, a path in nanoXTM does not work
        self._initialize()
        self.activeUpdate = False
        self.global_delay = 30

        self.roi_x1 = 0
        self.roi_x2 = self.imagesize[0]
        self.roidx = self.imagesize[0]
        self.roi_y1 = 0
        self.roi_y2 = self.imagesize[1]
        self.roidy = self.imagesize[1]
        self.roi = (slice(self.roi_x1, self.roi_x2), slice(self.roi_y1, self.roi_y2))
        self.io_roixlow.setText('%i' % self.roi_x1)
        self.io_roixhigh.setText('%i' % self.roi_x2)
        self.io_roiylow.setText('%i' % self.roi_y1)
        self.io_roiyhigh.setText('%i' % self.roi_y2)
        self.histmin = 1
        self.histmax = 65000
        self.hist_autorange = True
        self.viewModeXRM = False
        #self.box1 = None
        self.PixelLinkIn = None

        self.currdir = None
        self.updater = QtCore.QTimer()
        self.but_SetExptime.clicked.connect(self.clickButtonSetExptime)
        self.but_SetPolling.clicked.connect(self.clickButtonStartLive)
        # QtCore.QObject.connect(self.but_SetPolling, QtCore.SIGNAL('clicked()'), self.clickButtonStartLive)
        self.but_GetImageData.clicked.connect(self.clickButtonGetImageData)
        # QtCore.QObject.connect(self.but_GetImageData, QtCore.SIGNAL('clicked()'), self.clickButtonGetImageData)
        self.but_GetImageData.clicked.connect(self.clickButtonGetImageData)
        # QtCore.QObject.connect(self.but_Snapshot, QtCore.SIGNAL('clicked()'), self.clickButtonSnapshop)
        self.but_Snapshot.clicked.connect(self.clickButtonSnapshop)
        #QtCore.QObject.connect(self.but_SetRoi, QtCore.SIGNAL('clicked()'), self.clickButtonSetRoi)    
        # QtCore.QObject.connect(self.but_ResetRoi, QtCore.SIGNAL('clicked()'), self.clickButtonResetRoi)
        self.but_ResetRoi.clicked.connect(self.clickButtonResetRoi)
        # QtCore.QObject.connect(self.but_SetHist, QtCore.SIGNAL('clicked()'), self.clickButtonSetHist)
        self.but_SetHist.clicked.connect(self.clickButtonSetHist)
        # QtCore.QObject.connect(self.but_SetHistAutoRange, QtCore.SIGNAL('clicked()'), self.clickButtonSetHistAutoRange)
        self.but_SetHistAutoRange.clicked.connect(self.clickButtonSetHistAutoRange)
        # QtCore.QObject.connect(self.but_RefreshHist, QtCore.SIGNAL('clicked()'), self.clickButtonRefreshHist)
        self.but_RefreshHist.clicked.connect(self.clickButtonRefreshHist)
        # QtCore.QObject.connect(self.but_SaveImage, QtCore.SIGNAL('clicked()'), self.clickButtonSaveImage)
        self.but_SaveImage.clicked.connect(self.clickButtonSaveImage)
        # QtCore.QObject.connect(self.but_SwitchView, QtCore.SIGNAL('clicked()'), self.clickButtonSwitchView)
        self.but_SwitchView.clicked.connect(self.clickButtonSwitchView)
        # QtCore.QObject.connect(self.but_SetFlat, QtCore.SIGNAL('clicked()'), self.clickButtonFlat)
        self.but_SetFlat.clicked.connect(self.clickButtonFlat)
        # QtCore.QObject.connect(self.cB_Cameras, QtCore.SIGNAL('currentIndexChanged(const QString&)'),self.selectCamera)
        self.cB_Cameras.currentIndexChanged.connect(self.selectCamera)
        # QtCore.QObject.connect(self.but_SetCrossPos, QtCore.SIGNAL('clicked()'), self.clickButtonSetCrossPos)
        self.but_SetCrossPos.clicked.connect(self.clickButtonSetCrossPos)
        # QtCore.QObject.connect(self.but_Rotate, QtCore.SIGNAL('clicked()'), self.clickButtonRotate)
        self.but_Rotate.clicked.connect(self.clickButtonRotate)
        
        # QtCore.QObject.connect(self.but_SetWorkingPos, QtCore.SIGNAL('clicked()'), self.clickButtonSetWorkingPos)
        self.but_SetWorkingPos.clicked.connect(self.clickButtonSetWorkingPos)
        # QtCore.QObject.connect(self.but_SetAlignmentPos, QtCore.SIGNAL('clicked()'), self.clickButtonSetAlignmentPos)
        self.but_SetAlignmentPos.clicked.connect(self.clickButtonSetAlignmentPos)
        # QtCore.QObject.connect(self.but_GotoWorkingPos, QtCore.SIGNAL('clicked()'), self.clickButtonGotoWorkingPos)
        self.but_GotoWorkingPos.clicked.connect(self.clickButtonGotoWorkingPos)
        # QtCore.QObject.connect(self.but_GotoAlignmentPos, QtCore.SIGNAL('clicked()'), self.clickButtonGotoAlignmentPos)
        self.but_GotoAlignmentPos.clicked.connect(self.clickButtonGotoAlignmentPos)
        
        # QtCore.QObject.connect(self.but_MvrX, QtCore.SIGNAL('clicked()'), self.clickButtonMvrX)
        self.but_MvrX.clicked.connect(self.clickButtonMvrX)
        #QtCore.QObject.connect(self.but_MvrY, QtCore.SIGNAL('clicked()'), self.clickButtonMvrY)
        # QtCore.QObject.connect(self.but_MvrZ, QtCore.SIGNAL('clicked()'), self.clickButtonMvrZ)
        self.but_MvrZ.clicked.connect(self.clickButtonMvrZ)
        # QtCore.QObject.connect(self.but_gotoRot, QtCore.SIGNAL('clicked()'), self.clickButtonGotoRot)
        self.but_gotoRot.clicked.connect(self.clickButtonGotoRot)
        # QtCore.QObject.connect(self.but_LoadAlignmentPos, QtCore.SIGNAL('clicked()'), self.clickButtonLoadAlignmentPos)
        self.but_LoadAlignmentPos.clicked.connect(self.clickButtonLoadAlignmentPos)
        # QtCore.QObject.connect(self.but_SaveAlignmentPos, QtCore.SIGNAL('clicked()'), self.clickButtonSaveAlignmentPos)
        self.but_SaveAlignmentPos.clicked.connect(self.clickButtonSaveAlignmentPos)
        # QtCore.QObject.connect(self.but_LoadWorkingPos, QtCore.SIGNAL('clicked()'), self.clickButtonLoadWorkingPos)
        self.but_LoadWorkingPos.clicked.connect(self.clickButtonLoadWorkingPos)
        # QtCore.QObject.connect(self.but_SaveWorkingPos, QtCore.SIGNAL('clicked()'), self.clickButtonSaveWorkingPos)
        self.but_SaveWorkingPos.clicked.connect(self.clickButtonSaveWorkingPos)
        # QtCore.QObject.connect(self.but_MovePixLinkOut, QtCore.SIGNAL('clicked()'), self.clickButtonMovePiXLinkOut)
        self.but_MovePixLinkOut.clicked.connect(self.clickButtonMovePiXLinkOut)
        # QtCore.QObject.connect(self.but_MovePixLinkIn, QtCore.SIGNAL('clicked()'), self.clickButtonMovePiXLinkIn)
        self.but_MovePixLinkIn.clicked.connect(self.clickButtonMovePiXLinkIn)
        # QtCore.QObject.connect(self.but_OpenShutter1, QtCore.SIGNAL('clicked()'), self.clickButtonOpenShutter1)
        self.but_OpenShutter1.clicked.connect(self.clickButtonOpenShutter1)
        # QtCore.QObject.connect(self.but_OpenShutter2, QtCore.SIGNAL('clicked()'), self.clickButtonOpenShutter2)
        self.but_OpenShutter2.clicked.connect(self.clickButtonOpenShutter2)
        # QtCore.QObject.connect(self.but_CloseShutter2, QtCore.SIGNAL('clicked()'), self.clickButtonCloseShutter2)
        self.but_CloseShutter2.clicked.connect(self.clickButtonCloseShutter2)
        
        # QtCore.QObject.connect(self.but_StartStandardScan, QtCore.SIGNAL('clicked()'), self.clickButtonStartStandardScan)
        self.but_StartStandardScan.clicked.connect(self.clickButtonStartStandardScan)
        # QtCore.QObject.connect(self.but_ResetScan, QtCore.SIGNAL('clicked()'), self.clickButtonResetScan)
        self.but_ResetScan.clicked.connect(self.clickButtonResetScan)
        # QtCore.QObject.connect(self.cB_Scan, QtCore.SIGNAL('currentIndexChanged(const QString&)'),self.selectScan)
        self.cB_Scan.currentIndexChanged.connect(self.selectScan)
        # QtCore.QObject.connect(self.but_AddItem, QtCore.SIGNAL('clicked()'), self.clickButtonAddItem)
        self.but_AddItem.clicked.connect(self.clickButtonAddItem)
        # QtCore.QObject.connect(self.but_RemoveItem, QtCore.SIGNAL('clicked()'), self.clickButtonRemoveItem)
        self.but_RemoveItem.clicked.connect(self.clickButtonRemoveItem)
        # QtCore.QObject.connect(self.but_MoveUp, QtCore.SIGNAL('clicked()'), self.clickButtonMoveUp)
        self.but_MoveUp.clicked.connect(self.clickButtonMoveUp)
        # QtCore.QObject.connect(self.but_MoveDown, QtCore.SIGNAL('clicked()'), self.clickButtonMoveDown)
        self.but_MoveDown.clicked.connect(self.clickButtonMoveDown)
        # QtCore.QObject.connect(self.but_StartScanList, QtCore.SIGNAL('clicked()'), self.clickButtonStartScanList)
        self.but_StartScanList.clicked.connect(self.clickButtonStartScanList)
        # QtCore.QObject.connect(self.checkBox_smearing, QtCore.SIGNAL('clicked()'), self.checkBoxSmearing)
        self.checkBox_smearing.clicked.connect(self.checkBoxSmearing)
        # QtCore.QObject.connect(self.checkBox_exptime, QtCore.SIGNAL('clicked()'), self.checkBoxExptime)
        self.checkBox_exptime.clicked.connect(self.checkBoxExptime)
        # QtCore.QObject.connect(self.checkBox_speed, QtCore.SIGNAL('clicked()'), self.checkBoxSpeed)
        self.checkBox_speed.clicked.connect(self.checkBoxSpeed)
        # QtCore.QObject.connect(self.io_exptime2,  QtCore.SIGNAL('returnPressed()'),self.updateParams)
        self.io_exptime2.returnPressed.connect(self.updateParams)
        # QtCore.QObject.connect(self.io_speed,  QtCore.SIGNAL('returnPressed()'),self.updateParams)
        self.io_speed.returnPressed.connect(self.updateParams)
        # QtCore.QObject.connect(self.io_smearing,  QtCore.SIGNAL('returnPressed()'),self.updateParams)
        self.io_smearing.returnPressed.connect(self.updateParams)
        
        self.show()
        return None
    
    def _initialize(self):
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

        self.palette_blue = QtGui.QPalette()
        self.palette_blue.setColor(QtGui.QPalette.Foreground, QtCore.Qt.blue)


        self.palette_orange = QtGui.QPalette()
        self.palette_orange.setColor(QtGui.QPalette.Foreground, QtGui.QColor(255, 127, 49))
        
        self.palette_lightblue = QtGui.QPalette()
        self.palette_lightblue.setColor(QtGui.QPalette.Foreground, QtGui.QColor(105, 138, 229))

        self.palette_hzgblue = QtGui.QPalette()
        self.palette_hzgblue.setColor(QtGui.QPalette.Foreground, QtGui.QColor(0, 152, 212))


        self.but_SetExptime.setStyleSheet(self.button_style)
        self.but_SetPolling.setStyleSheet(self.button_style)
        self.but_Snapshot.setStyleSheet(self.button_style)
        self.but_ResetRoi.setStyleSheet(self.button_style)
        self.but_SetHistAutoRange.setStyleSheet(self.button_style)
        self.but_SetHist.setStyleSheet(self.button_style)
        self.but_RefreshHist.setStyleSheet(self.button_style)
        self.but_SaveImage.setStyleSheet(self.button_style)
        self.but_GetImageData.setStyleSheet(self.button_style)
        self.but_SetFlat.setStyleSheet(self.button_style)
        self.but_SetCrossPos.setStyleSheet(self.button_style)
        self.but_Rotate.setStyleSheet(self.button_style)
        self.but_SetWorkingPos.setStyleSheet(self.button_style)
        self.but_SetAlignmentPos.setStyleSheet(self.button_style)
        self.but_GotoWorkingPos.setStyleSheet(self.button_style)
        self.but_GotoAlignmentPos.setStyleSheet(self.button_style)
        self.but_MvrX.setStyleSheet(self.button_style)
        self.but_MvrZ.setStyleSheet(self.button_style)
        self.but_gotoRot.setStyleSheet(self.button_style)
        self.but_LoadAlignmentPos.setStyleSheet(self.button_style)
        self.but_SaveAlignmentPos.setStyleSheet(self.button_style)
        self.but_LoadWorkingPos.setStyleSheet(self.button_style)
        self.but_SaveWorkingPos.setStyleSheet(self.button_style)
        self.but_MovePixLinkOut.setStyleSheet(self.button_style)
        self.but_MovePixLinkIn.setStyleSheet(self.button_style)
        self.but_StartStandardScan.setStyleSheet(self.button_style)
        self.but_AddItem.setStyleSheet(self.button_style)
        self.but_RemoveItem.setStyleSheet(self.button_style)
        self.but_MoveUp.setStyleSheet(self.button_style)
        self.but_MoveDown.setStyleSheet(self.button_style)
        self.but_StartScanList.setStyleSheet(self.button_style)
        
        

        self.label_currentpolling.setPalette(self.palette_red)
        self.label_currentpolling.setText('inactive')
        
        self.io_currentPosX.setText('0')
        self.io_currentPosY.setText('0')
        
        self.io_exptime.setStyleSheet(self.textbox_style)
        self.label_currenthistautorange.setPalette(self.palette_green)
        
        self.floatValidator = QtGui.QDoubleValidator(self)
        self.floatValidator.setRange(-360., 360.)
        
        self.checkBox_Normalize.setChecked(False)
        self.checkBox_Normalize.setEnabled(False)
        
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
        
        try:
            self.SM = numpy.zeros(4, dtype = object)
            self.SM[0] = PyTango.DeviceProxy(proxies.smaract_eh1_cha0)
            self.SM[1] = PyTango.DeviceProxy(proxies.smaract_eh1_cha1)
            self.SM[2] = PyTango.DeviceProxy(proxies.smaract_eh1_cha3)
            self.SM[3] = PyTango.DeviceProxy(proxies.smaract_eh1_cha4)
        except:
            self.SM = None
        try:
            self.pmac = PMACdict()
        except:
            self.pmac = None
            
        try:
            self.nano = p05.nano.NanoPositions()
        except:
            self.nano = None

        self.tPitch = PyTango.DeviceProxy(proxies.motor_mono_01_tPitch)
        self.tRoll = PyTango.DeviceProxy(proxies.motor_mono_02_tRoll)
        self.tUndulator = PyTango.DeviceProxy(proxies.tUndulator_1)
        self.tScintiY = PyTango.DeviceProxy(proxies.motor_eh1_05_tScintiY)
        self.tLensY = PyTango.DeviceProxy(proxies.motor_eh1_06_tLensY)
        self.tCamRot = PyTango.DeviceProxy(proxies.motor_eh1_07_tCamRot)
        self.tDCM = PyTango.DeviceProxy(proxies.dcmener_s01_01_tDCMenergy)
        self.tPixLinkMotorX = PyTango.DeviceProxy(proxies.motor_eh1_16_tPixLinkMotorX)
        self.tBeamShutter = PyTango.DeviceProxy(proxies.tBeam_shutter)
        print(self.Camera)
        return None

    # Buttons Tab 1

    def selectCamera(self):
        if self.activeUpdate:
            self.label_currentpolling.setPalette(self.palette_red)
            self.label_currentpolling.setText('inactive')
            self.but_SetPolling.setText('Start live acquisition')
            self.activeUpdate = False
            self.PollingThread.stop()
            if self.tCamera.state() == PyTango.DevState.EXTRACT:
                self.tCamera.command_inout(self.command_stop)
                time.sleep(0.1)
            if self.Camera == 'PixelLink' or self.Camera == 'PCO':
                self.tTrigger.write_attribute('Voltage', 0)
            if self.Camera == 'Hamamatsu':
                self.tTrigger.write_attribute('Value', 0)
                #self.tTrigger.write_attribute('Voltage', 0)
        print(self.cB_Cameras.currentText())
        self.Camera = self.cB_Cameras.currentText()
        print(self.Camera)
        if self.Camera == 'Hamamatsu':
            self.tCamera = PyTango.DeviceProxy(proxies.camera_hama)
            #self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out01)
            if self.HamaHutch == 'eh1':
                self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_01)
            elif self.HamaHutch == 'eh2':
                print("eh2")
                self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out03)
            self.command_exptime = 'EXPOSURE_TIME'
            self.command_start = 'StartAcq'
            self.command_stop = 'AbortAcq'
            self.command_image = 'IMAGE'
            self.tCamera.write_attribute('SaveImageFlag', False)
            self.tCamera.write_attribute('TRIGGER_SOURCE', 'INTERNAL')
            self.imagesize = (2048, 2048)
            self.rotate = 0
            print('ok')
        if self.Camera == 'PCO':
            self.tCamera = PyTango.DeviceProxy(proxies.camera_pco)
            self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_01)
            self.command_exptime = 'ExposureTime'
            self.command_start = 'StartAcq'
            self.command_stop = 'StopAcq'
            self.command_image = 'LiveImage'
            self.tCamera.write_attribute('TriggerMode',1)
            self.imagesize = (2048, 2048)
            print('Pco')
        if self.Camera == 'PixelLink':
            self.tCamera = PyTango.DeviceProxy(proxies.camera_pixlink)
            self.command_exptime = 'SHUTTER'
            self.command_start = 'StartAcq'
            self.command_stop = 'AbortAcq'
            self.command_image = 'Image'
            self.imagesize = (2208, 3000)
            self.rotate = 2
            print('PixelLink')
            
        if self.Camera == 'Zyla':
            self.tCamera = PyTango.DeviceProxy(proxies.camera_zyla)
            # self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out01)
            self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out03)
            self.command_exptime = 'acq_expo_time'
            self.command_start = 'startAcq'
            self.command_stop = 'abortAcq'
            self.command_image = 'IMAGE'
            self.tCamera.write_attribute('acq_trigger_mode','INTERNAL_TRIGGER')
            self.tCamera.write_attribute('saving_mode','MANUAL')    

            self.imagesize = (2560, 2160)

        if self.Camera == 'KIT':
            self.tCamera = PyTango.DeviceProxy(proxies.camera_kit)
            # self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out01)
            self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_03)
            self.command_exptime = 'exposure_time'
            self.command_start = 'Start'
            self.command_stop = 'Stop'
            self.command_image = 'image'
            self.tCamera.write_attribute('trigger_source','1')  # 0: auto, 1: software, 2: Hardware
            self.tCamera.write_attribute('writeInMemory','false')
            self.tCamera.write_attribute('number_of_frames','1')
            self.imagesize = (2560, 2160)

        if self.Camera == 'Lambda':
            self.tCamera = PyTango.DeviceProxy(proxies.camera_lambda)
            self.command_exptime = 'ShutterTime'
            self.command_start = 'StartAcq'
            self.command_stop = 'StopAcq'
            self.command_image = 'LiveLatestImageData'
            self.tCamera.write_attribute('TriggerMode', 0)
            time.sleep(0.2)
            self.tCamera.write_attribute('SaveAllImages', False)
            self.imagesize = (1556, 516)
            self.rotate = 1
            print('Lambda')

        # Reset ROI after changing Camera
        self.clickButtonResetRoi()
        self.rulerx.setPos((0, 0))
        self.rulerx.setSize((1, self.roidx))
        self.rulery.setPos((0, 0))
        self.rulery.setSize((self.roidy, 1))
        if self.rotate % 2 == 1:
            self.rulerx.setSize((1, self.roidy))
            self.rulery.setSize((self.roidx, 1))
        # Reset Hist
        self.hist_autorange = True
        self.label_currenthistautorange.setPalette(self.palette_green)
        self.label_currenthistautorange.setText('active')

        self.PollingThread.cameraChanged = True

        return


    def clickButtonSetExptime(self):
        """Set the self.global_delay variable (in ms) """
        #try: 
        _old_exp = self.exptime
        _txt = self.io_exptime.text()
        _val = float(_txt)
        self.exptime = _val * 1e-3
        self.label_currentexptime.setText(_txt + ' ms')
        if self.Camera == 'Lambda':
            self.exptime = self.exptime * 1000
        if self.activeUpdate:
            self.activeUpdate = False
            self.PollingThread.stop()
            # waiting for last image to be read out in update Camera
            time.sleep(_old_exp + 0.3)
            
            if self.tCamera.state() != PyTango.DevState.ON:
                self.tCamera.command_inout(self.command_stop)
            while self.tCamera.state() != PyTango.DevState.ON:
                time.sleep(0.01)
            self.tCamera.write_attribute(self.command_exptime, self.exptime)
            time.sleep(1)
            if self.tCamera.state() != PyTango.DevState.ON:
                QtWidgets.QMessageBox.warning(self, 'Warning', 'Camera Tango server not in on state!',
                                              buttons=QtWidgets.QMessageBox.Ok)
                return None

            print('Succsessfully set new exposure time: %.2f ms' % self.exptime * 1000)
            self.activeUpdate = True
            self.PollingThread.restart()   
        elif self.activeUpdate == False:
            print(self.command_exptime)
            print(self.exptime)
            while not self.tCamera.state() == PyTango.DevState.ON:
                time.sleep(0.01) 
            self.tCamera.write_attribute(self.command_exptime, self.exptime)
            #print('Succsessfully set new exposure time %.2f ms' %self.exptime*1000)
            #self.PollingThread.set_delay(self.exptime)
        #except:
            #print Exception
        
            #QtGui.QMessageBox.warning(self, 'Warning', 'Could not set a new exposure time.', buttons=QtGui.QMessageBox.Ok)
        return None
    
    def clickButtonGetImageData(self):
        try:
            self.exptime = self.tCamera.read_attribute(self.command_exptime).value
            if self.tCamera == 'PCO_old':
                tmp = numpy.fromstring(self.tPCO.read_attribute('LiveImage').value[1], dtype=numpy.uint16).byteswap()
            
                self.image = (tmp[2:]).reshape(tmp[0], tmp[1])
            else: 
                self.image = self.tCamera.read_attribute(self.command_image).value
            self.imagesize = numpy.shape(self.tCamera.read_attribute(self.command_image).value)
            self.NewUpdate([self.image, self.exptime, self.imagesize])
        except:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Could not acquire individual image.',
                                          buttons=QtWidgets.QMessageBox.Ok)
        return None
    #end clickButtonGetImageData
    
    def clickButtonSnapshop(self):
        try: 
            while not self.tCamera.state() == PyTango.DevState.ON:
                time.sleep(0.01) 
            #self.tCamera.write_attribute('SaveImageFlag',False)
            if self.activeUpdate:
                self.PollingThread.stop()
                self.label_currentpolling.setPalette(self.palette_red)
                self.label_currentpolling.setText('inactive')
                self.but_SetPolling.setText('Start live acquisition')
                self.activeUpdate = False
                if self.tCamera.state() == PyTango.DevState.EXTRACT:
                    self.tCamera.command_inout(self.command_stop)
                    if self.Camera == 'PixelLink'or self.Camera == 'PCO':
                        self.tTrigger.write_attribute('Voltage', 0)
                    if self.Camera == 'Hamamatsu':
                        if self.HamaHutch == 'eh1':
                            self.tTrigger.write_attribute('Voltage', 0)
                        elif self.HamaHutch == 'eh2':
                            self.tTrigger.write_attribute('Value', 0)
                    time.sleep(0.1 + self.exptime)
            self.exptime = self.tCamera.read_attribute(self.command_exptime).value
            self.label_currentexptime.setText('%i' %(self.exptime* 1e3) + ' ms')
            
            while not self.tCamera.state() == PyTango.DevState.ON:
                time.sleep(0.01)
            self.tCamera.command_inout(self.command_start)
            if self.Camera == 'Hamamatsu':
                while not self.tCamera.state() == PyTango.DevState.EXTRACT:
                    time.sleep(0.01)
            if self.Camera == 'Hamamatsu':
                if self.HamaHutch == 'eh1':
                    self.tTrigger.write_attribute('Voltage', 3.5)
                elif self.HamaHutch == 'eh2':
                    self.tTrigger.write_attribute('Value', 1)
            
            time.sleep(0.01)
            if self.Camera == 'PixelLink' or self.Camera == 'PCO':
                self.tTrigger.write_attribute('Voltage', 0)
            if self.Camera == 'Hamamatsu':
                if self.HamaHutch == 'eh1':
                    self.tTrigger.write_attribute('Voltage', 0)
                elif self.HamaHutch == 'eh2':
                    self.tTrigger.write_attribute('Value', 0)
            
            while not self.tCamera.state() == PyTango.DevState.ON:
                time.sleep(0.01)
            if self.Camera == 'PCO_old':
                tmp = numpy.fromstring(self.tCamera.read_attribute('LiveImage').value[1], dtype=numpy.uint16).byteswap()
            
                self.image = (tmp[2:]).reshape(tmp[0], tmp[1])
            else: 
                self.image = self.tCamera.read_attribute(self.command_image).value
            self.imagesize = numpy.shape(self.tCamera.read_attribute(self.command_image).value)
            self.NewUpdate([self.image, self.exptime, self.imagesize])
        except:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Could not acquire individual image.',
                                          buttons=QtWidgets.QMessageBox.Ok)
            raise
        return None

    def clickButtonSetRoi(self):
        try:
            roi_x1 = int(self.io_roixlow.text())
            roi_x2 = int(self.io_roixhigh.text())
            roidx = roi_x2 - roi_x1
            roi_y1 = int(self.io_roiylow.text())
            roi_y2 = int(self.io_roiyhigh.text())
            roidy = roi_y2 - roi_y1
        except:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Could not convert ROI values to numbers.',
                                          buttons=QtWidgets.QMessageBox.Ok)
        if roidx > self.imagesize[0] or roidy > self.imagesize[1]:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'ROI larger than image size. Please adapt.',
                                          buttons=QtWidgets.QMessageBox.Ok)
            return None
        self.roi_x1 = roi_x1
        self.roi_x2 = roi_x2
        self.roidx = roidx
        self.roi_y1 = roi_y1
        self.roi_y2 = roi_y2
        self.roidy = roidy
        self.roi = (slice(self.roi_x1, self.roi_x2), slice(self.roi_y1, self.roi_y2))
        self.label_currentroixlow.setText('%i' % self.roi_x1)
        self.label_currentroixhigh.setText('%i' % self.roi_x2)
        self.label_currentroiylow.setText('%i' % self.roi_y1)
        self.label_currentroiyhigh.setText('%i' % self.roi_y2)
        return None
    # end clickButtonSetRoi

    def clickButtonResetRoi(self):
        self.roi_x1 = 0
        self.roi_x2 =self.imagesize[0]
        self.roidx = self.imagesize[0]
        self.roi_y1 = 0
        self.roi_y2 = self.imagesize[1]
        self.roidy = self.imagesize[1]
        self.roi = (slice(self.roi_y1, self.roi_y2), slice(self.roi_x1, self.roi_x2))
        self.io_roixlow.setText('%i' % self.roi_x1)
        self.io_roixhigh.setText('%i' % self.roi_x2)
        self.io_roiylow.setText('%i' % self.roi_y1)
        self.io_roiyhigh.setText('%i' % self.roi_y2)
        self.label_currentroixlow.setText('%i' % self.roi_x1)
        self.label_currentroixhigh.setText('%i' % self.roi_x2)
        self.label_currentroiylow.setText('%i' % self.roi_y1)
        self.label_currentroiyhigh.setText('%i' % self.roi_y2)
        self.upper_right_corner_x = 0
        self.upper_right_corner_y = 0
        return None
    # end clickButtonSetRoi
        
    def clickButtonSetHist(self):
        try:
            histmin = int(self.io_histmin.text())
            histmax = int(self.io_histmax.text())
        except:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Could not convert histogram boundaries to numbers.',
                                          buttons=QtWidgets.QMessageBox.Ok)
            return None
        if histmin < 0 or histmax > 65565:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Histogram values outside 16bit dynamic range..',
                                          buttons=QtWidgets.QMessageBox.Ok)
            return None
        self.histmin = histmin
        self.histmax = histmax
        self.label_currenthistmin.setText('%i' % self.histmin)
        self.label_currenthistmax.setText('%i' % self.histmax)
        return None
    #end clickButtonSetHist

    def clickButtonSetHistAutoRange(self):
        if self.hist_autorange:
            self.hist_autorange = False
            self.label_currenthistautorange.setPalette(self.palette_blue)
            self.label_currenthistautorange.setText('manual')
        elif self.hist_autorange == False:
            self.hist_autorange = True
            self.label_currenthistautorange.setPalette(self.palette_green)
            self.label_currenthistautorange.setText('active')
        return None
    #end clickButtonSetHistAutoRange
    
    def clickButtonRefreshHist(self):
        try:
            roi_x1 = int(self.io_roixlow.text())
            roi_x2 = int(self.io_roixhigh.text())
            roidx = roi_x2 - roi_x1 + 1
            roi_y1 = int(self.io_roiylow.text())
            roi_y2 = int(self.io_roiyhigh.text())
            roidy = roi_y2 - roi_y1 + 1
        except:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Could not convert ROI values to numbers.',
                                          buttons=QtWidgets.QMessageBox.Ok)
        if roidx > self.imagesize[0] or roidy > self.imagesize[1]:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'ROI larger than image size. Please adapt.',
                                          buttons=QtWidgets.QMessageBox.Ok)
            return None
        self.roi_x1 = roi_x1
        self.roi_x2 = roi_x2
        self.roidx = roidx
        self.roi_y1 = roi_y1
        self.roi_y2 = roi_y2
        self.roidy = roidy
        self.roi = ((slice(self.roi_y1, self.roi_y2), slice(self.roi_x1, self.roi_x2)))
        self.label_currentroixlow.setText('%i' % self.roi_x1)
        self.label_currentroixhigh.setText('%i' % self.roi_x2)
        self.label_currentroiylow.setText('%i' % self.roi_y1)
        self.label_currentroiyhigh.setText('%i' % self.roi_y2)
        
        if hasattr(self, 'box1'):
            self.imageView.getView().removeItem(self.box1)
        self.rulerx.setPos((0,0))
        self.rulerx.setSize((1,self.roidy))
        self.rulery.setPos((0,0),)
        self.rulery.setSize((self.roidx,1))
        self.upper_right_corner_x += self.roi_x1
        self.upper_right_corner_y += self.roi_y1
        if self.hist_autorange:
            self.HistWidget.autoHistogramRange()
            self.imageView.setImage(self.image[self.roi])
        elif self.hist_autorange == False:
            self.HistWidget.setHistogramRange(self.histmin, self.histmax)
            self.imageView.setImage(self.image[self.roi],\
                                    levels = (self.histmin, self.histmax), autoHistogramRange = False)

        #end clickButtonRefreshHist
    
    def clickButtonSetCrossPos(self):
        print
        self.rulerx.setPos((int(self.io_currentPosX.text()),0))
        self.rulerx.setSize((1,self.roidy))
        self.rulery.setPos((0,int(self.io_currentPosY.text())))
        self.rulery.setSize((self.roidx,1))
    
    def clickButtonSaveImage(self):
        if self.activeUpdate:
            self.PollingThread.stop()
        if self.currdir == None:
            fname = QtWidgets.QFileDialog.getSaveFileName(parent=None, caption='Save name for image file',
                                                          filter="Tiff Image (*.tiff);; Images (*.png *.jpg *.tif)")
        elif self.currdir != None:
            fname = QtWidgets.QFileDialog.getSaveFileName(parent=None, caption='Save name for image file',
                                                          directory=self.currdir, \
                                                          filter = "Tiff Image (*.tiff);; Images (*.png *.jpg *.tif)")
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        _filename = os.path.basename(fname)
        _ftype = _filename.split('.')[1]
        print(fname, _ftype)
        if _ftype == 'raw':
            (self.image.transpose()).tofile(fname)
        elif _ftype in ['png', 'jpg', 'tif','tiff']:
            self.image = numpy.float32(self.image)
            #pylab.matplotlib.image.imsave(fname, self.image.transpose(), cmap = 'gray')
            #print (numpy.dtype(self.image.transpose()))
            im = PIL.Image.fromarray(self.image.transpose(), mode="F" ) # float32
            im.save(fname, "TIFF")
        
        if self.activeUpdate:
            self.PollingThread.restart()
        _log = 'Warning: Motor positions could have been moved by another process! \n'
        _log += 'Timestamp = ' + misc.GetTimeString()+ '\n'
        _log += 'Exposure time = \t%e (s)\n' %self.exptime
        _log += 'Undulator gap =\t%e\n' %self.tUndulator.read_attribute('Gap').value
        _log += 'DCM energy =   \t%e\n' %self.tDCM.read_attribute('Position').value
        _log += 'DCM pitch =    \t%e\n' %self.tPitch.read_attribute('Position').value
        if self.pmac != None:
            _log += self.pmac.ReturnMotorPositionString()
        _log += 'Scinillator y =\t%e\n' %self.tScintiY.read_attribute('Position').value
        _log += 'Lens y        =\t%e\n' %self.tLensY.read_attribute('Position').value
        _log += 'Camera rot    =\t%e\n' %self.tCamRot.read_attribute('Position').value
        if self.SM != None:
            try:
                _log += 'SmarAct Ch. 0 (x left) =\t%e\n' %self.SM[0].read_attribute('Position').value
                _log += 'SmarAct Ch. 1 (z top)=\t%e\n' %self.SM[1].read_attribute('Position').value
                _log += 'SmarAct Ch. 3 (x right) =\t%e\n' %self.SM[2].read_attribute('Position').value
                _log += 'SmarAct Ch. 4 (z bottom)=\t%e\n' %self.SM[3].read_attribute('Position').value
            except:
                _log += 'SmarAct communication error'
            
        with open(fname+'.log', 'w') as f:
            f.write(_log)
        return None
    
    def clickButtonStartLive(self):
        try:
            while not self.tCamera.state() == PyTango.DevState.ON:
                time.sleep(0.01)
        except:
            print("TANGO Error :(")
            return
        if self.activeUpdate:  # Stop Live Aquisition
            self.label_currentpolling.setPalette(self.palette_red)
            self.label_currentpolling.setText('inactive')
            self.but_SetPolling.setText('Start live acquisition')
            self.activeUpdate = False
            self.PollingThread.stop()
            if self.tCamera.state() == PyTango.DevState.EXTRACT:
                self.tCamera.command_inout(self.command_stop)
                time.sleep(0.1)

        else:  # Start Live Aquisition
            self.label_currentpolling.setPalette(self.palette_green)
            self.label_currentpolling.setText('active')
            self.but_SetPolling.setText('Stop live acquisition')
            
            if self.tCamera.state() == PyTango.DevState.EXTRACT:
                self.tCamera.command_inout(self.command_stop)
                time.sleep(0.01)
            if self.tCamera.state() != PyTango.DevState.ON:
                QtWidgets.QMessageBox.warning(self, 'Warning', 'Camera Tango server not in on state!',
                                              buttons=QtWidgets.QMessageBox.Ok)
                return None
            if self.Camera == 'Hamamatsu':
                while self.tCamera.state() != PyTango.DevState.ON:
                    time.sleep(0.1)
                self.tCamera.write_attribute('TRIGGER_SOURCE', 'INTERNAL')
                time.sleep(0.1)
                self.tCamera.write_attribute('SaveImageFlag',False)
            time.sleep(0.01)
            self.activeUpdate = True
            print("1")
            self.PollingThread.restart()
        return None
    #end clickButtonStartLive
    
    def clickButtonSwitchView(self):
        if self.viewModeXRM == False:
            self.imageView.ui.graphicsView.setBackground('#FF7E31')
            #self.HistWidget.setBackground('#FF7E31')
            self.label_currentview.setPalette(self.palette_orange)
            self.label_currentview.setText('Microscopy mode')
            
            self.viewModeXRM = True
        elif self.viewModeXRM == True:
            self.imageView.ui.graphicsView.setBackground('#0097d4')
            #self.HistWidget.setBackground('#698aE5')
            self.label_currentview.setPalette(self.palette_hzgblue)
            self.label_currentview.setText('Direct beam mode')
            self.viewModeXRM = False
            
        return None
    #end ClickButtonSwitchView
    
    def clickButtonFlat(self):
        try:
            self.flat = self.image
            print(self.flat)
            self.flat = numpy.rot90(self.flat, (4-self.rotate)%4)
            if self.viewModeXRM:
                self.flat = numpy.rot90(self.flat, 2)
            if self.Camera == 'PixelLink':
                self.flat = numpy.fliplr(self.flat)
            self.checkBox_Normalize.setEnabled(True)
        except:
            return
        return None
    
    def clickButtonRotate(self):
        self.rotate+=1
        return None
        
    # Buttons on Tab 2    
        
    def clickButtonSetWorkingPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        if self.cb_Mode.currentText() == 'TXM Mode':
            self.nano.SetWorkingPos()
        elif self.cb_Mode.currentText() == 'Holotomo Mode':
            self.nano.SetWorkingPos_h()
        #self.PollingThread.restart()
        return None
    
    def clickButtonSetAlignmentPos(self):
        self.PixelLinkIn = self.tPixLinkMotorX.read_attribute('Position')
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        if self.cb_Mode.currentText() == 'TXM Mode':
            self.nano.SetAlignmentPos()
        elif self.cb_Mode.currentText() == 'Holotomo Mode':
            self.nano.SetAlignmentPos_h()
        #self.PollingThread.restart()
        return None
    
    def clickButtonMovePiXLinkOut(self):
        self.tPixLinkMotorX.write_attribute('Position', 2)
        self.label_PixLinkInOut.setText('PixelLink Out')
        
    def clickButtonMovePiXLinkIn(self):
        self.PixelLinkIn = 86.4
        self.tPixLinkMotorX.write_attribute('Position', self.PixelLinkIn )
#         if posin < 0:
#             print("Warning, In position should be > 0")
#         elif posin >= 0:
#             self.tPixLinkMotorX.write_attribute('Position', 87.15)
#             self.label_PixLinkInOut.setText('PixelLink In')
    
    def clickButtonGotoWorkingPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        if self.cb_Mode.currentText() == 'TXM Mode':
            self.nano.GotoWorkingPos(mode ="TXM")
        elif self.cb_Mode.currentText() == 'Holotomo Mode':
            self.nano.GotoWorkingPos(mode ="holo")
        self.label_workingalignment.setText('Working Position')
        return None
    
    def clickButtonGotoAlignmentPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        #self.tBeamShutter.command_inout('CloseOpen_BS_1', 0)
        #print("closing shutter")
        self.tBeamShutter.command_inout('CloseOpen_BS_2', 0)
        time.sleep(4)
#        self.tPixLinkMotorX.write_attribute('Position',self.PixelLinkIn)
#        while self.tPixLinkMotorX.read_attribute('Position')< self.PixelLinkIn:
#            time.sleep(0.2)
        if self.cb_Mode.currentText() == 'TXM Mode':
            self.nano.GotoAlignmentPos(mode ="TXM")
        elif self.cb_Mode.currentText() == 'Holotomo Mode':
            self.nano.GotoAlignmentPos(mode ="holo")
        self.label_workingalignment.setText('Alignment Position')
        return None
    
    def clickButtonOpenShutter1(self):
        self.tBeamShutter.command_inout('CloseOpen_BS_1', 1)

    def clickButtonOpenShutter2(self):
        sys.stdout.write(misc.GetShortTimeString() + ': ATTENTION!!! Are you in working position? Open Shutter 2? [open, no]: ')
        sys.stdout.flush()
        tmp = sys.stdin.readline()[:-1]
        if tmp not in ['open', 'Open']:
            print('Aborting...')
            return None
        self.tBeamShutter.command_inout('CloseOpen_BS_2', 1)

    def clickButtonCloseShutter2(self):
        self.tBeamShutter.command_inout('CloseOpen_BS_2', 0)

    def clickButtonMvrX(self):
        self.pmac.SampleSF_mvrX(float(self.io_mvrx.text()),WaitForMove=False)
        return None
    
    def clickButtonMvrY(self):
        self.nano.MvrSampleY(float(self.io_mvry.text()))
        return None
    
    def clickButtonMvrZ(self):
        self.pmac.MoveRel('Sample_z', float(self.io_mvrz.text()),WaitForMove=False)
        #self.nano.MvrSampleZ(float(self.io_mvrz.text()))
        return None
    
    def clickButtonGotoRot(self):
        value = float(self.io_gotorot.text())
        if not (-180 <= value <= 180):
            print(
                misc.GetShortTimeString() + ': Warning - requested rotation position outside allowed limits.\nAborting...')
            return None
        self.pmac.Move('Sample_Rot', value,WaitForMove = False)
        return None
    
    def clickButtonSaveAlignmentPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        if self.currdir == None:
            fname = QtWidgets.QFileDialog.getExistingDirectory(parent=None, caption='Select folder')
        elif self.currdir != None:
            fname = QtWidgets.QFileDialog.getExistingDirectory(parent=None, caption='Select folder',
                                                               directory=self.currdir)
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        if self.cb_Mode.currentText() == 'TXM Mode':
            self.nano.SaveAlignmentPos(fname, mode ="TXM")
        elif self.cb_Mode.currentText() == 'Holotomo Mode':
            self.nano.SaveAlignmentPos(fname, mode ="holo")

    def clickButtonLoadAlignmentPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        if self.currdir == None:
            fname = QtWidgets.QFileDialog.getOpenFileName(parent=None, caption='Load file', filter="Text (*.txt)")
        elif self.currdir != None:
            fname = QtWidgets.QFileDialog.getOpenFileName(parent=None, caption='Load file', directory=self.currdir, \
                                                          filter = "Text (*.txt)")
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        if self.cb_Mode.currentText() == 'TXM Mode':
            self.nano.LoadAlignmentPos(fname, mode ="TXM")
        elif self.cb_Mode.currentText() == 'Holotomo Mode':
            self.nano.LoadAlignmentPos(fname, mode ="holo")
    
    def clickButtonSaveWorkingPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        if self.currdir == None:
            fname = QtWidgets.QFileDialog.getExistingDirectory(parent=None, caption='Select folder')
        elif self.currdir != None:
            fname = QtWidgets.QFileDialog.getExistingDirectory(parent=None, caption='Select folder',
                                                               directory=self.currdir)
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        print(fname)
        if self.cb_Mode.currentText() == 'TXM Mode':
            self.nano.SaveWorkingPos(fname, mode ="TXM")
        elif self.cb_Mode.currentText() == 'Holotomo Mode':
            self.nano.SaveWorkingPos(fname, mode ="holo")
        
    def clickButtonLoadWorkingPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        if self.currdir == None:
            fname = QtWidgets.QFileDialog.getOpenFileName(parent=None, caption='Load File', filter="Text (*.txt)")
        elif self.currdir != None:
            fname = QtWidgets.QFileDialog.getOpenFileName(parent=None, caption='Load File', directory=self.currdir, \
                                                          filter = "Text (*.txt)")
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        print(fname)
        if self.cb_Mode.currentText() == 'TXM Mode':
            self.nano.LoadWorkingPos(fname, mode ="TXM")
        elif self.cb_Mode.currentText() == 'Holotomo Mode':
            self.nano.LoadWorkingPos(fname, mode ="holo")

    # Buttons Tab 3

    def selectScan(self):
        self.Scan = self.cB_Scan.currentText()
        if self.Scan == 'Take Image Series':
            self.io_speed.setDisabled(True)
            self.checkBox_speed.setDisabled(True)
            self.io_smearing.setDisabled(True)
            self.checkBox_smearing.setDisabled(True)
            self.io_noimages.setDisabled(False)
            self.io_noref.setDisabled(False)
            self.io_nodistances.setDisabled(True)
            self.io_stepsize.setDisabled(True)
        if self.Scan == 'Fly Scan':
            self.io_speed.setDisabled(False)
            self.checkBox_speed.setDisabled(False)
            self.io_smearing.setDisabled(False)
            self.checkBox_smearing.setDisabled(False)
            self.io_noimages.setDisabled(True)
            self.io_noref.setDisabled(False)
            self.io_nodistances.setDisabled(True)
            self.io_stepsize.setDisabled(True)
        if self.Scan == 'Holotomo Fly':
            self.io_speed.setDisabled(False)
            self.checkBox_speed.setDisabled(False)
            self.io_smearing.setDisabled(False)
            self.checkBox_smearing.setDisabled(False)
            self.io_noimages.setDisabled(True)
            self.io_noref.setDisabled(False)
            self.io_nodistances.setDisabled(False)
            self.io_stepsize.setDisabled(False)
        if self.Scan == 'Holotomo Step':
            self.io_speed.setDisabled(True)
            self.checkBox_speed.setDisabled(True)
            self.io_smearing.setDisabled(True)
            self.checkBox_smearing.setDisabled(True)
            self.io_noimages.setDisabled(False)
            self.io_noref.setDisabled(False)
            self.io_nodistances.setDisabled(False)
            self.io_stepsize.setDisabled(False)


    def checkBoxExptime(self):
        if self.checkBox_exptime.isChecked():
            self.io_exptime2.setDisabled(False)
            if self.checkBox_speed.isChecked():
                self.checkBox_smearing.setChecked(False)
                self.io_smearing.setDisabled(True)
        else:
            self.io_exptime2.setDisabled(True)
            self.checkBox_smearing.setChecked(True)
            self.io_smearing.setDisabled(False)
            self.checkBox_speed.setChecked(True)
            self.io_speed.setDisabled(False)

    def checkBoxSmearing(self):
        if self.checkBox_smearing.isChecked():
            self.io_smearing.setDisabled(False)
            if self.checkBox_exptime.isChecked():
                self.checkBox_speed.setChecked(False)
                self.io_speed.setDisabled(True)
        else:
            self.io_smearing.setDisabled(True)
            self.checkBox_exptime.setChecked(True)
            self.io_exptime2.setDisabled(False)
            self.checkBox_speed.setChecked(True)
            self.io_speed.setDisabled(False)

    def checkBoxSpeed(self):
        if self.checkBox_speed.isChecked():
            self.io_speed.setDisabled(False)
            if self.checkBox_exptime.isChecked():
                self.checkBox_smearing.setChecked(False)
                self.io_smearing.setDisabled(True)
        else:
            self.io_speed.setDisabled(True)
            self.checkBox_exptime.setChecked(True)
            self.io_exptime2.setDisabled(False)
            self.checkBox_smearing.setChecked(True)
            self.io_smearing.setDisabled(False)

    def updateParams(self):
        if self.checkBox_exptime.isChecked():
            if self.checkBox_speed.isChecked():
                smearing = float(self.io_speed.text())*float(self.io_exptime2.text())*numpy.pi *2048/2 /180
                self.io_smearing.setText(str(smearing))
            elif self.checkBox_smearing.isChecked():
                speed = float(self.io_smearing.text()) *180./ (numpy.pi *2048/2*float(self.io_exptime2.text()))
                self.io_speed.setText(str(speed))
        else:
             exptime = float(self.io_smearing.text()) *180./ (numpy.pi *2048/2*float(self.io_speed.text()))
             self.io_exptime2.setText(str(exptime))
        num_img = int (180. /(float(self.io_speed.text())*(float(self.io_exptime2.text())+0.015 )))
        self.io_noimages.setText(str(num_img))
        scantime = (180/float(self.io_speed.text())/60)
        self.label_scantime.setText('%.2f min' % scantime)


    def clickButtonStartStandardScan(self):
        if self.activeUpdate:
            self.PollingThread.stop()
        while not self.tCamera.state() == PyTango.DevState.ON:
            time.sleep(0.01) 
        #self.tCamera.write_attribute('SaveImageFlag',True)
        self.Scan = self.cB_Scan.currentText()
        beamtime = self.io_beamtime.text()
        prefix = self.io_prefix.text()
        #rotangle = int(self.io_rotangle.text())
        #nop = int(self.io_nop.text())
        num_flat = int(self.io_noref.text())
        exptime = self.io_exptime2.text()
        rotcenter = float(self.io_cor.text())
        sampleout = float(self.io_sampleoutrel.text())
        num_images = int(self.io_noimages.text())
        num_dist = self.io_nodistances.text()
        stepsize = self.io_stepsize.text()
        speed = self.io_speed.text()
        smearing = self.io_smearing.text()
        CS = self.checkBox_CloseShutter.isChecked()
        if self.Scan == 'Holotomo Fly Ref':
            os.system('python ' + self.path_scanscripts + '05_Holotomo_Fly_RefInBetween.py %s %s %s %s %s %s %s %s %s %s %s' %(beamtime, prefix, rotcenter,sampleout, exptime,  speed, smearing, stepsize,num_dist,num_flat,CS))
        if self.Scan == 'Holotomo Step':
            os.system('python ' + self.path_scanscripts + '04_Holotomo_Step.py %s %s %s %s %s %s %s %s %s %s' %(beamtime, prefix, rotcenter,sampleout, exptime,  num_images, stepsize,num_dist,num_flat,CS))
        if self.Scan == 'Holotomo Fly':
            os.system('python ' + self.path_scanscripts + '03_Holotomo_Fly.py %s %s %s %s %s %s %s %s %s %s %s' %(beamtime, prefix, rotcenter,sampleout, exptime,  speed, smearing, stepsize,num_dist,num_flat,CS))
        if self.Scan == 'Take Image Series':
            os.system('python ' + self.path_scanscripts + '02_ImageSeries.py %s %s %s %s %s %s %s %s' %(beamtime, prefix, rotcenter,sampleout, exptime, num_images, num_flat, CS))
        if self.Scan == 'Fly Scan':
            os.system('python ' + self.path_scanscripts + '01_standard_flyScan.py %s %s %s %s %s %s %s %s %s' % (beamtime, prefix, rotcenter,sampleout, exptime, speed, smearing, num_flat, CS))
        if self.Scan == 'Fly Scan 360':
            os.system('python ' + self.path_scanscripts + '07_flyScan_360.py %s %s %s %s %s %s %s %s %s' % (
            beamtime, prefix, rotcenter, sampleout, exptime, speed, smearing, num_flat, CS))

    def clickButtonResetScan(self):
        sys.stdout.write(misc.GetShortTimeString() + ': RESET SCAN? [reset, no]: ')
        sys.stdout.flush()
        tmp = sys.stdin.readline()[:-1]
        if tmp not in ['reset', 'Reset']:
            print('Aborting...')
            return None
        self.tCamera.command_inout('AbortAcq')
        self.pmac.StopPMACmoveC5()
        self.pmac.ResetErrorsC5()
        self.pmac.SetRotSpeed(30)
        self.pmac.Move("SampleRot", 0)
        self.pmac.Move("SampleStage", float(self.io_cor.text()))


    
    
    def clickButtonAddItem(self):
        beamtime = self.io_beamtime.text()
        prefix = self.io_prefix.text()
        rotangle = int(self.io_rotangle.text())
        nop = int(self.io_nop.text())
        noref = int(self.io_noref.text())
        exptime = float(self.io_exptime2.text())
        rotcenter = float(self.io_cor.text())
        sampleout = float(self.io_sampleoutrel.text())
        scriptname = '..\scripts\Camera_helper.py'
        integNo = int(self.io_an.text())
        if self.Scan == 'Standard Scan':
            #self.list_Scan.addItem('print("'+beamtime+'")')
            self.list_Scan.addItem('ch.StartScanStandard("..\scripts\Camera_helper.py",'+ str(beamtime) +','+ str(prefix) + ','+ str(nop) +','+ str(exptime) +','+ str(rotcenter) +',' + str(sampleout) +',' + 'rotangle='+str(rotangle)+')' )
        if self.Scan == 'Close Shutter':
            self.list_Scan.addItem('ch.closeShutter()')
        if self.Scan == 'Take Image Series':
            self.list_Scan.addItem('ch.TakeImageSeries("'+str(scriptname)+'",'+str(beamtime)+','+ str(prefix)+','+ str(integNo)+','+ str(exptime)+','+ str(rotcenter)+','+ str(sampleout)+','+ str(noref)+')')
        
        
    def clickButtonStartScanList(self):
        #print(self.list_Scan.item(0).text())
        for i in range(self.list_Scan.count()):
            #print(self.list_Scan.item(i).text())
            exec(str(self.list_Scan.item(i).text()))
    
    def clickButtonRemoveItem(self):
        ItemSelect = self.list_Scan.currentRow()
        self.list_Scan.takeItem(ItemSelect)
    
    
    def clickButtonMoveUp(self):
        ItemSelect = self.list_Scan.currentRow()
        if ItemSelect > 0:
            Item = self.list_Scan.takeItem(ItemSelect)
            self.list_Scan.insertItem(ItemSelect-1,Item)
        
    def clickButtonMoveDown(self):
        ItemSelect = self.list_Scan.currentRow()
        if ItemSelect < self.list_Scan.count():
            Item = self.list_Scan.takeItem(ItemSelect)
            self.list_Scan.insertItem(ItemSelect+1,Item)
    
    
    # New Commands for Click and Mouse Drag in ImageView for ruler and 

    def click(self,event):
        event.accept()  
        pos = event.pos()
        self.io_currentPosX.setText(str(int(pos.x()+self.upper_right_corner_x)))
        self.io_currentPosY.setText(str(int(pos.y()+self.upper_right_corner_y)))
        currValue = self.image[(int(pos.x()),int(pos.y()))]
        print(currValue)
        self.label_currentvalue.setText(str(currValue))
        self.rulerx.setPos((pos.x(),0))
        self.rulerx.setSize((1, self.roidx))
        self.rulery.setPos((0, pos.y()))
        self.rulery.setSize((self.roidy, 1))
        if self.rotate % 2 == 1:
            self.rulerx.setSize((1,self.roidy))
            self.rulery.setSize((self.roidx,1))
        #item1 = pyqtgraph.LineROI((0,0),(10,10), width=1,  pen=QtGui.QPen(QtCore.Qt.red, 1), movable=True)
        #self.imageView.getView().addItem(item1)
        self.io_roixlow.setText('%i' % self.roi_x1)
        self.io_roixhigh.setText('%i' % self.roi_x2)
        self.io_roiylow.setText('%i' % self.roi_y1)
        self.io_roiyhigh.setText('%i' % self.roi_y2)

        try:
            self.imageView.getView().removeItem(self.box1)
        except:
            pass
        return None


    def mouseDrag(self,event):
        event.accept()
        pos1 = event.pos()
        pos2 = event.buttonDownPos()

        try:
            if pos1.x()< pos2.y():
                roi_x1 = int(pos1.x())
                roi_x2 = int(pos2.x())
            else:
                roi_x1 = int(pos2.x())
                roi_x2 = int(pos1.x())
            roidx = roi_x2 - roi_x1 + 1
            if pos1.y()< pos2.y():
                roi_y1 = int(pos1.y())
                roi_y2 = int(pos2.y())
            else:
                roi_y1 = int(pos2.y())
                roi_y2 = int(pos1.y())
            roidy = roi_y2 - roi_y1 + 1
        except:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Could not convert ROI values to numbers.',
                                          buttons=QtWidgets.QMessageBox.Ok)
        if roidx > self.imagesize[0] or roidy > self.imagesize[1]:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'ROI larger than image size. Please adapt.',
                                          buttons=QtWidgets.QMessageBox.Ok)
            return None
#         self.roi_x1 = roi_x1
#         self.roi_x2 = roi_x2
#         self.roidx = roidx
#         self.roi_y1 = roi_y1
#         self.roi_y2 = roi_y2
#         self.roidy = roidy
#         print (self.roi_x1)

        self.io_roixlow.setText('%i' % roi_x1)
        self.io_roixhigh.setText('%i' % roi_x2)
        self.io_roiylow.setText('%i' % roi_y1)
        self.io_roiyhigh.setText('%i' % roi_y2)
        self.box = pyqtgraph.ROI((roi_x1,roi_y1), size=(roidx,roidy))
        self.imageView.getView().addItem(self.box)
        if hasattr(self, 'box1'):
            self.imageView.getView().removeItem(self.box1)
            del(self.box1)
        self.box1 = self.box

#        try:
#            self.imageView.getView().removeItem(self.box1)
#            del(self.box1)
#        finally:
        
    
    def NewUpdate(self, _data):
        # Rotation of Image
        if hasattr(self, 'image'):
            del(self.image)
            gc.collect()
        if self.Camera == 'Zyla':
            a = _data[0]
            #print(a)
            lowerbit = a[0:len(a):2]
            upperbit = a[1:len(a):2]
            self.image = lowerbit+ 256*upperbit
            self.image = self.image.reshape(2160,2560)
        else:
            self.exptime = _data[1]
            self.imagesize = _data[2]
            self.image = _data[0]

        if self.checkBox_Normalize.isChecked():
            self.image = numpy.float32(self.image)
            #self.flat = numpy.rot90(self.flat, self.rotate)
            self.image = numpy.divide(self.image, self.flat, out=numpy.zeros_like(self.image), where=self.flat!=0)
        self.image = self.image[self.roi]
        self.image = numpy.rot90(self.image, self.rotate)

        self.imagesize = self.image.shape

        del(_data)
        gc.collect()
        if self.Camera == 'PixelLink':
            self.image = numpy.fliplr(self.image)
            #self.image = numpy.rot90(self.image)
            #self.image = numpy.rot90(self.image)
            #self.image = numpy.rot90(self.image)
            self.viewModeXRM = True
        #if self.Camera == 'Hamamatsu':
            # self.viewModeXRM = True
            #if self.checkBox_Normalize.isChecked():
                #self.flat = numpy.rot90(self.flat, 1)
            #self.image = numpy.rot90(self.image, 1)
        if self.viewModeXRM == True:  
            self.image = numpy.rot90(self.image, 2)
#            if self.checkBox_Normalize.isChecked():
#                self.flat = numpy.rot90(self.flat, 2)


        self.label_currentexptime.setText('%i ms' % (1e3 * self.exptime))
        self.imageView.getImageItem().mouseClickEvent = self.click
        self.imageView.getImageItem().mouseDragEvent = self.mouseDrag
        self.imageView.clear()
        if self.hist_autorange:
            self.HistWidget.autoHistogramRange()
            self.imageView.setImage(self.image)
        elif self.hist_autorange == False:
            self.HistWidget.setHistogramRange(self.histmin, self.histmax)
            self.imageView.setImage(self.image,\
                                    levels = (self.histmin, self.histmax), autoHistogramRange = False)
        self.label_timeedit.setTime(QtCore.QTime.currentTime())
        
        #print (self.pmac.ReadMotorPos('Sample_Rot'))
        self.label_posx.setText('%.4f'% self.pmac.ReadMotorPos('Sample_x'))
        self.label_posy.setText('%.4f'%self.pmac.ReadMotorPos('Sample_y'))
        self.label_posz.setText('%.4f'%self.pmac.ReadMotorPos('Sample_z'))
        self.label_posrot.setText('%.4f'%self.pmac.ReadMotorPos('Sample_Rot'))
        
        
        if self.PixelLinkIn == None:
            self.label_PixLinkInOut.setText('PixelLink position not set')
        elif self.tPixLinkMotorX.read_attribute('Position').value == self.PixelLinkIn:
            self.label_PixLinkInOut.setText('PixelLink In')
        elif self.tPixLinkMotorX.read_attribute('Position').value == 2:
            self.label_PixLinkInOut.setText('PixelLink Out')
        else:
            self.label_PixLinkInOut.setText('PixelLink Moving')
        return None
    # end NewUpdate
    
    
    def closeEvent(self, event):
        """Safety check for closing of window."""
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               "Are you sure to quit?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            if self.tCamera.state() == PyTango.DevState.EXTRACT:
                self.tCamera.command_inout(self.command_stop)
            self.PollingThread.terminate_signal = True
            
            event.accept()
        else:
            event.ignore()
        return None   


class  Camerapolling(QtCore.QThread):
    def __init__(self, parentThread, Camera, trigger,cB_Cameras, cur_delay = 0.25):
        QtCore.QThread.__init__(self, parentThread)
        self.parent = parentThread
        self.Image = None
        self.tCamera = Camera
        self.cB_Cameras = cB_Cameras
        self.tTrigger = trigger
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
        self.updateCamera()
        return None
    
    def cleanUp(self):
        return None
    
    def getUpdate(self):
        return True

    def __del__(self):
        self.exiting = True
        self.wait()
        return None
#end Camerapolling


class UpdateThread(Camerapolling):
    jobFinished = pyqtSignal(object)#object is [self.image, self.exptime, self.imagesize]

    def __init__(self, parentThread, Camera, trigger, cB_Cameras, cur_delay = 0.25):
        Camerapolling.__init__(self, parentThread, Camera, trigger, cB_Cameras, cur_delay = cur_delay)
        self.HamaHutch = 'eh2'
        self.cameraChanged = True
        self.pid = os.getpid()
        return None
            
    def updateCamera(self):

        while True:
            #PythonMemoryUsage(pid = self.pid, checkpoint = 0)
            self.CameraName = self.cB_Cameras.currentText()
            if self.running:
                if self.CameraName == 'Hamamatsu' and self.cameraChanged:
                    self.tCamera = PyTango.DeviceProxy(proxies.camera_hama)
                    
                    if self.HamaHutch == 'eh1':
                        self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_01)
                    elif self.HamaHutch == 'eh2':
                        self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out03)
                    self.command_exptime = 'EXPOSURE_TIME'
                    self.command_start = 'StartAcq'
                    self.command_stop = 'AbortAcq'
                    self.command_image = 'IMAGE'
                    self.imagesize = (2048, 2048)
                    self.cameraChanged = False
                    #print ('ok')
                if self.CameraName == 'PCO' and self.cameraChanged:
                    self.tCamera = PyTango.DeviceProxy(proxies.camera_pco)
                    self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_01)
                    self.command_exptime = 'ExposureTime'
                    self.command_start = 'StartAcq'
                    self.command_stop = 'StopAcq'
                    self.command_image = 'LiveImage'
                    self.imagesize = (2048, 2048)
                    self.cameraChanged = False
                if self.CameraName == 'PixelLink' and self.cameraChanged:
                    self.tCamera = PyTango.DeviceProxy(proxies.camera_pixlink)
                    self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_01)
                    self.command_exptime = 'SHUTTER'
                    self.command_start = 'StartAcq'
                    self.command_stop = 'AbortAcq'
                    self.command_image = 'Image'
                    self.imagesize = (2208, 3000)
                    self.cameraChanged = False
                if self.CameraName == 'Zyla' and self.cameraChanged:
                    self.tCamera = PyTango.DeviceProxy(proxies.camera_zyla)
                    # self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out01)
                    self.tTrigger = PyTango.DeviceProxy(proxies.register_eh2_out03)
                    self.command_exptime = 'acq_expo_time'
                    self.command_start = 'startAcq'
                    self.command_stop = 'abortAcq'
                    self.command_image = 'IMAGE'
                    self.tCamera.write_attribute('acq_trigger_mode','INTERNAL_TRIGGER')
                    self.tCamera.write_attribute('saving_mode','MANUAL')
                    self.imagesize = (2560, 2160)
                    self.cameraChanged = False

                if self.CameraName == 'KIT' and self.cameraChanged:
                    self.tCamera = PyTango.DeviceProxy(proxies.camera_kit)
                    self.tTrigger = PyTango.DeviceProxy(proxies.dac_eh1_01)
                    self.command_exptime = 'exposure_time'
                    self.command_start = 'Start'
                    self.command_stop = 'Stop'
                    self.command_image = 'image'
                    self.tCamera.write_attribute('trigger_source','1')  # 0: auto, 1: software, 2: Hardware
                    self.tCamera.write_attribute('writeInMemory','false')
                    self.imagesize = (2560, 2160)
                    self.cameraChanged = False

                if self.CameraName == 'Lambda' and self.cameraChanged:
                    self.tCamera = PyTango.DeviceProxy(proxies.camera_lambda)
                    self.command_exptime = 'ShutterTime'
                    self.command_start = 'StartAcq'
                    self.command_stop = 'StopAcq'
                    self.command_image = 'LiveLastImageData'
                    self.tCamera.write_attribute('TriggerMode', 0)
                    time.sleep(0.3)
                    self.tCamera.write_attribute('SaveAllImages', False)
                    time.sleep(0.3)
                    self.tCamera.write_attribute('FrameNumbers', 1)
                    self.imagesize = (1556, 516)
                    self.cameraChanged = False

                #print (self.CameraName)
                self.t0 = time.time()
                if self.CameraName =='Zyla':
                    self.tCamera.command_inout('prepareAcq')
                # Wait for ON state
                while not self.tCamera.state() == PyTango.DevState.ON:
                    time.sleep(0.02)
                # Start Aquisition
                self.tCamera.command_inout(self.command_start)
                # Wait for finishing Aquisition
                while not self.tCamera.state() == PyTango.DevState.ON:
                    time.sleep(0.02)
                # Read exptime and image from Tango server
                self.exptime = self.tCamera.read_attribute(self.command_exptime).value
                if self.CameraName == 'PCO_old':
                    tmp = numpy.fromstring(self.tCamera.read_attribute('LiveImage').value[1], dtype=numpy.uint16).byteswap()
                    self.image = (tmp[2:]).reshape(tmp[0], tmp[1])
                elif self.CameraName == 'Zyla':
                    time.sleep(self.exptime+1)
                    a = self.tCamera.read_attribute('saving_next_number')
                    tmp = self.tCamera.command_inout('getImage',a.value)
                    self.image = tmp
                    del(tmp)
                else:
                    self.image = self.tCamera.read_attribute(self.command_image).value
                # Set imagesize ? NEEDED?
                if self.CameraName == 'Zyla' or 'Lambda':
                    self.imagesize = self.imagesize
                else:          
                    self.imagesize = self.image.shape #numpy.shape(self.tCamera.read_attribute(self.command_image).value) #(self.tCamera.read_attribute('IMAGE_WIDTH'), self.tCamera.read_attribute('IMAGE_WIDTH'))
                #time.sleep(max(0, self.cur_delay - (time.time() - self.t0)))
                # self.emit(QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), [self.image, self.exptime, self.imagesize])
                self.jobFinished.emit([self.image, self.exptime, self.imagesize])
            elif self.running == False:
                time.sleep(0.1)
            if self.terminate_signal:
                    break
            #PythonMemoryUsage(pid = self.pid, checkpoint = 1)
        return None
# class UpdateThread



def Camera_LiveImage(parent=None, devices=None, groups=None, name='Camera live image'):
    app = QtWidgets.QApplication(sys.argv)
    
    gui = cCamera_LiveImage(name=name, parent=QtWidgets.QMainWindow())
    gui.PollingThread = UpdateThread(gui.main, gui.tCamera, gui.tTrigger,gui.cB_Cameras)
    gui.PollingThread.jobFinished.connect(gui.NewUpdate) #jobFinished is a future event and we subscribe (connect) to event before it may be emited.
    gui.PollingThread.start()
    gui.show()
    if sys.platform == 'win32' or sys.platform == 'win64':
        sys.exit(app.exec_())
    else:
        app.exec_()


if __name__ == "__main__":
    Camera_LiveImage()
