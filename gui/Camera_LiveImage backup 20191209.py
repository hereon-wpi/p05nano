import numpy
from PyQt4 import uic as QtUic
from PyQt4 import QtGui
from PyQt4 import QtCore
import PyTango
import sys
import time
import pyqtgraph
import os
import p05.tools.misc as misc
import pylab
from p05.devices.PMACdict import PMACdict
import p05.nano
import pylab as plt
import PIL
import p05.scripts.Camera_helper as ch

from msilib.schema import CheckBox
from matplotlib.backend_bases import MouseEvent


class cCamera_LiveImage(QtGui.QMainWindow):
    def __init__(self, parent=None, name='Camera live image'):
        super(cCamera_LiveImage, self).__init__()
        try:
            QtUic.loadUi('h:/_data/programming_python/p05/gui/Cameralive_ui_tab_NewDesign.ui', self)
            self.setWindowIcon(QtGui.QIcon('h:/_data/programming_python/p05/gui/images.jpg'))
        except:
            _path = misc.GetPath('Cameralive_ui_tab_NewDesign.ui')
            QtUic.loadUi(_path, self)
            self.setWindowIcon(QtGui.QIcon(os.path.split(_path)[0] + os.sep + 'images.jpg'))
        self.setWindowTitle(name)
        #self.setWindowIcon(QtGui.QIcon('h:/_data/programming_python/p05/gui/images.jpg'))
        self.setGeometry(10, 25, 1500, 965)
        self.HamaHutch = 'eh2'  # ALSO CHANGE BELOW!
        self.Camera = 'PixelLink'
        #self.Camera = 'PCO'
        
        self.tBeamShutter = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/shutter/all')
        
        if self.Camera == 'Hamamatsu':
            self.tCamera = PyTango.DeviceProxy('//hzgpp05vme1.desy.de:10000/p05/camera/hama')
            if self.HamaHutch == 'eh1':
                self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
            #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
            elif self.HamaHutch == 'eh2':
                print("eh2")
                self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out03')
            self.cB_Cameras.setCurrentIndex(0)
            self.command_exptime = 'EXPOSURE_TIME'
            self.command_start = 'StartAcq'
            self.command_stop = 'AbortAcq'
            self.command_image = 'IMAGE'
            self.imagesize = (2048, 2048)
            
        if self.Camera == 'PCO':
            self.tCamera = PyTango.DeviceProxy('//hzgpp05vme1:10000/eh1/pco/edge')
            #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out01')
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')

            self.cB_Cameras.setCurrentIndex(1)
            self.command_exptime = 'ExposureTime'
            self.command_start = 'StartStandardAcq'
            self.command_stop = 'Stop'
            self.command_image = 'Image'
            self.imagesize = (2048, 2048)
            self.tCamera.write_attribute('TriggerMode',1)
            
        if self.Camera == 'PixelLink':
            self.tCamera = PyTango.DeviceProxy('//hzgpp05vme1.desy.de:10000/p05/camera/pixlink')
            #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out01')
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
            self.cB_Cameras.setCurrentIndex(2)
            self.command_exptime = 'SHUTTER'
            self.command_start = 'StartAcq'
            self.command_stop = 'AbortAcq'
            self.command_image = 'IMAGE'
            self.imagesize = (2208, 3000)
                
        if self.Camera == 'Zyla':
            self.tCamera = PyTango.DeviceProxy('hzgpp05ct09:10000/p05/limaccds/ct09.01')
            #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out01')
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out03')
            self.cB_Cameras.setCurrentIndex(3)
            self.command_exptime = 'acq_expo_time'
            self.command_start = 'startAcq'
            self.command_stop = 'abortAcq'
            self.command_image = 'IMAGE'
            self.tCamera.write_attribute('acq_trigger_mode','INTERNAL_TRIGGER')
            self.tCamera.write_attribute('saving_mode','MANUAL')
            self.imagesize = (2160,2560)
            
            
        if self.Camera == 'KIT':
            self.tCamera = PyTango.DeviceProxy('hzgpp05ct09:10000/p05/')
            #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out01')
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.03')
            self.cB_Cameras.setCurrentIndex(3)
            self.command_exptime = 'acq_expo_time'
            self.command_start = 'startAcq'
            self.command_stop = 'abortAcq'
            self.command_image = 'IMAGE'
            self.tCamera.write_attribute('acq_trigger_mode','INTERNAL_TRIGGER')
            self.tCamera.write_attribute('saving_mode','MANUAL')
            self.imagesize = (2160,2560)
            
        self.exptime = self.tCamera.read_attribute(self.command_exptime).value
        self.label_currentexptime.setText('%i ms' %(self.exptime* 1e3))
            
        self.main = parent
        
        self.bgcolor = '#0097d4'
        self.imageView.ui.graphicsView.setBackground(self.bgcolor)
        
        self.rulery = pyqtgraph.ROI((0,0), size=(2048, 1))
        self.rulerx = pyqtgraph.ROI((0,0), size=(1, 2048))
        self.imageView.getView().addItem(self.rulery)
        self.imageView.getView().addItem(self.rulerx)
        
        self.upper_right_corner_x = 0
        self.upper_right_corner_y = 0
        self.rotate = 0
        self.HistWidget = self.imageView.getHistogramWidget()
        self.HistWidget.setBackground('#eeeeee')
        
    
        self._initialize()
        self.activeUpdate = False
        self.global_delay = 30
        
        
        self.roi_x1 = 1
        self.roi_x2 = self.imagesize[0]
        self.roidx = self.imagesize[0]
        self.roi_y1 = 1
        self.roi_y2 = self.imagesize[1]
        self.roidy = self.imagesize[1]
        self.io_roixlow.setText('%i' % self.roi_x1)
        self.io_roixhigh.setText('%i' % self.roi_x2)
        self.io_roiylow.setText('%i' % self.roi_y1)
        self.io_roiyhigh.setText('%i' % self.roi_y2)
        self.histmin = 1
        self.histmax = 65000
        self.hist_autorange = True
        self.viewModeXRM = False
        self.box1 = None
        self.PixelLinkIn = None

        self.currdir = None
        self.updater = QtCore.QTimer()
        
        QtCore.QObject.connect(self.but_SetExptime, QtCore.SIGNAL('clicked()'), self.clickButtonSetExptime)    
        QtCore.QObject.connect(self.but_SetPolling, QtCore.SIGNAL('clicked()'), self.clickButtonStartLive)
        QtCore.QObject.connect(self.but_GetImageData, QtCore.SIGNAL('clicked()'), self.clickButtonGetImageData)
        QtCore.QObject.connect(self.but_Snapshot, QtCore.SIGNAL('clicked()'), self.clickButtonSnapshop)
        #QtCore.QObject.connect(self.but_SetRoi, QtCore.SIGNAL('clicked()'), self.clickButtonSetRoi)    
        QtCore.QObject.connect(self.but_ResetRoi, QtCore.SIGNAL('clicked()'), self.clickButtonResetRoi)
        QtCore.QObject.connect(self.but_SetHist, QtCore.SIGNAL('clicked()'), self.clickButtonSetHist)    
        QtCore.QObject.connect(self.but_SetHistAutoRange, QtCore.SIGNAL('clicked()'), self.clickButtonSetHistAutoRange)
        QtCore.QObject.connect(self.but_RefreshHist, QtCore.SIGNAL('clicked()'), self.clickButtonRefreshHist)
        QtCore.QObject.connect(self.but_SaveImage, QtCore.SIGNAL('clicked()'), self.clickButtonSaveImage)
        QtCore.QObject.connect(self.but_SwitchView, QtCore.SIGNAL('clicked()'), self.clickButtonSwitchView)
        QtCore.QObject.connect(self.but_SetFlat, QtCore.SIGNAL('clicked()'), self.clickButtonFlat)
        QtCore.QObject.connect(self.cB_Cameras, QtCore.SIGNAL('currentIndexChanged(const QString&)'),self.selectCamera)
        QtCore.QObject.connect(self.but_SetCrossPos, QtCore.SIGNAL('clicked()'), self.clickButtonSetCrossPos)
        QtCore.QObject.connect(self.but_Rotate, QtCore.SIGNAL('clicked()'), self.clickButtonRotate)
        
        QtCore.QObject.connect(self.but_SetWorkingPos, QtCore.SIGNAL('clicked()'), self.clickButtonSetWorkingPos)
        QtCore.QObject.connect(self.but_SetAlignmentPos, QtCore.SIGNAL('clicked()'), self.clickButtonSetAlignmentPos)
        QtCore.QObject.connect(self.but_GotoWorkingPos, QtCore.SIGNAL('clicked()'), self.clickButtonGotoWorkingPos)
        QtCore.QObject.connect(self.but_GotoAlignmentPos, QtCore.SIGNAL('clicked()'), self.clickButtonGotoAlignmentPos)
        
        QtCore.QObject.connect(self.but_MvrX, QtCore.SIGNAL('clicked()'), self.clickButtonMvrX)
        #QtCore.QObject.connect(self.but_MvrY, QtCore.SIGNAL('clicked()'), self.clickButtonMvrY)
        QtCore.QObject.connect(self.but_MvrZ, QtCore.SIGNAL('clicked()'), self.clickButtonMvrZ)
        QtCore.QObject.connect(self.but_gotoRot, QtCore.SIGNAL('clicked()'), self.clickButtonGotoRot)
        QtCore.QObject.connect(self.but_LoadAlignmentPos, QtCore.SIGNAL('clicked()'), self.clickButtonLoadAlignmentPos)
        QtCore.QObject.connect(self.but_SaveAlignmentPos, QtCore.SIGNAL('clicked()'), self.clickButtonSaveAlignmentPos)
        QtCore.QObject.connect(self.but_LoadWorkingPos, QtCore.SIGNAL('clicked()'), self.clickButtonLoadWorkingPos)
        QtCore.QObject.connect(self.but_SaveWorkingPos, QtCore.SIGNAL('clicked()'), self.clickButtonSaveWorkingPos)
        QtCore.QObject.connect(self.but_MovePixLinkOut, QtCore.SIGNAL('clicked()'), self.clickButtonMovePiXLinkOut)
        QtCore.QObject.connect(self.but_MovePixLinkIn, QtCore.SIGNAL('clicked()'), self.clickButtonMovePiXLinkIn)

        
        QtCore.QObject.connect(self.but_StartStandardScan, QtCore.SIGNAL('clicked()'), self.clickButtonStartStandardScan)
        QtCore.QObject.connect(self.cB_Scan, QtCore.SIGNAL('currentIndexChanged(const QString&)'),self.selectScan)
        QtCore.QObject.connect(self.but_AddItem, QtCore.SIGNAL('clicked()'), self.clickButtonAddItem)
        QtCore.QObject.connect(self.but_RemoveItem, QtCore.SIGNAL('clicked()'), self.clickButtonRemoveItem)
        QtCore.QObject.connect(self.but_MoveUp, QtCore.SIGNAL('clicked()'), self.clickButtonMoveUp)
        QtCore.QObject.connect(self.but_MoveDown, QtCore.SIGNAL('clicked()'), self.clickButtonMoveDown)
        QtCore.QObject.connect(self.but_StartScanList, QtCore.SIGNAL('clicked()'), self.clickButtonStartScanList)
        #QtCore.QObject.connect(self.but_Take0180, QtCore.SIGNAL('clicked()'), self.clickButtonTake0180)
        
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
            self.SM[0] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha0')
            self.SM[1] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha1')
            self.SM[2] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha3')
            self.SM[3] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/smaract/eh1.cha4')
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
        
        self.tPitch =  PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/motor/mono.01')
        self.tRoll  =  PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/motor/mono.02')
        self.tUndulator = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/undulator/1')
        self.tScintiY = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.05')
        self.tLensY = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.06')
        self.tCamRot = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.07')
        self.tDCM = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/dcmener/s01.01')
        self.tPixLinkMotorX = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.16')
        self.tBeamShutter = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/shutter/all')
        print(self.Camera)
        return None
            
            
    def initializeUpdater(self):
        QtCore.QObject.connect(self.PollingThread, QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), self.NewUpdate)
        return None
    #end initializeUpdater

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
            #self.tCamera = PyTango.DeviceProxy('//hzgpp05vme1.desy.de:10000/p05/camera/hama')
            self.tCamera = PyTango.DeviceProxy('//hzgpp07eh4.desy.de:10000/p07/hama/eh4')
            #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out01')
            if self.HamaHutch == 'eh1':
                self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
            elif self.HamaHutch == 'eh2':
                print("eh2")
                self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out03')
            self.command_exptime = 'EXPOSURE_TIME'
            self.command_start = 'StartAcq'
            self.command_stop = 'AbortAcq'
            self.command_image = 'IMAGE'
            self.imagesize = (2048, 2048)
            self.rotate = 0
            self.roi_x1 = 1
            self.roi_x2 = self.imagesize[0]
            self.roidx = self.imagesize[0]
            self.roi_y1 = 1
            self.roi_y2 = self.imagesize[1]
            self.roidy = self.imagesize[1]
            print ('ok')
        if self.Camera == 'PCO':
            self.tCamera = PyTango.DeviceProxy('//hzgpp05vme1:10000/eh1/pco/edge')
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
            self.command_exptime = 'ExposureTime'
            self.command_start = 'StartStandardAcq'
            self.command_stop = 'Stop'
            self.command_image = 'Image'
            self.tCamera.write_attribute('TriggerMode',1)
            self.imagesize = (2048, 2048)
            self.roi_x1 = 1
            self.roi_x2 = self.imagesize[1]
            self.roidx = self.imagesize[1]
            self.roi_y1 = 1
            self.roi_y2 = self.imagesize[0]
            self.roidy = self.imagesize[0]
            print('Pco')
        if self.Camera == 'PixelLink':
            self.tCamera = PyTango.DeviceProxy('//hzgpp05vme1.desy.de:10000/p05/camera/pixlink')
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
            self.command_exptime = 'SHUTTER'
            self.command_start = 'StartAcq'
            self.command_stop = 'AbortAcq'
            self.command_image = 'Image'
            self.imagesize = (2208, 3000)
            self.roi_x1 = 1
            self.roi_x2 = self.imagesize[1]
            self.roidx = self.imagesize[1]
            self.roi_y1 = 1
            self.roi_y2 = self.imagesize[0]
            self.roidy = self.imagesize[0]
            self.rotate = 1
            print ('PixelLink')
            
        if self.Camera == 'Zyla':
            self.tCamera = PyTango.DeviceProxy('hzgpp05ct09:10000/p05/limaccds/ct09.01')
            #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out01')
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out03')
            self.command_exptime = 'acq_expo_time'
            self.command_start = 'startAcq'
            self.command_stop = 'abortAcq'
            self.command_image = 'IMAGE'
            self.tCamera.write_attribute('acq_trigger_mode','INTERNAL_TRIGGER')
            self.tCamera.write_attribute('saving_mode','MANUAL')    
            
            self.imagesize = (2560, 2160)
            self.roi_x1 = 1
            self.roi_x2 = self.imagesize[1]
            self.roidx = self.imagesize[1]
            self.roi_y1 = 1
            self.roi_y2 = self.imagesize[0]
            self.roidy = self.imagesize[0]
        
        if self.Camera == 'KIT':
            self.tCamera = PyTango.DeviceProxy('hzgpp05ctcam1:10000/p05/hzguca/kit')
            #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out01')
            self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.03')
            self.command_exptime = 'exposure_time'
            self.command_start = 'Start'
            self.command_stop = 'Stop'
            self.command_image = 'image'
            self.tCamera.write_attribute('trigger_source','1')  # 0: auto, 1: software, 2: Hardware
            self.tCamera.write_attribute('writeInMemory','false')
            self.tCamera.write_attribute('number_of_frames','1')
            self.imagesize = (2560, 2160)
            self.roi_x1 = 1
            self.roi_x2 = self.imagesize[1]
            self.roidx = self.imagesize[1]
            self.roi_y1 = 1
            self.roi_y2 = self.imagesize[0]
            self.roidy = self.imagesize[0]
    

    def clickButtonSetExptime(self):
        """Set the self.global_delay variable (in ms) """
        #try: 
        _old_exp = self.exptime
        _txt = self.io_exptime.text()
        _val = float(_txt)
        self.exptime = _val * 1e-3
        self.label_currentexptime.setText(_txt + ' ms')
        if self.activeUpdate:
            self.activeUpdate = False
            self.PollingThread.stop()
            # waiting for last image to be read out in update Camera
            time.sleep(_old_exp + 0.3)
            
            if self.tCamera.state() != PyTango.DevState.ON:
                self.tCamera.command_inout(self.command_stop)
            while self.tCamera.state() != PyTango.DevState.ON:
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
            self.tCamera.write_attribute(self.command_exptime, self.exptime)
            time.sleep(1)
            self.activeUpdate = True
#                 if self.tCamera.state() == PyTango.DevState.EXTRACT:
#                     self.tCamera.command_inout(self.command_stop)
#                     time.sleep(0.1)
            if self.tCamera.state() != PyTango.DevState.ON:
                QtGui.QMessageBox.warning(self, 'Warning', 'Camera Tango server not in on state!', buttons=QtGui.QMessageBox.Ok)
                return None
            #self.tCamera.command_inout(self.command_start)
            time.sleep(2)
            self.PollingThread.restart()   
        elif self.activeUpdate == False:
            print(self.command_exptime)
            print(self.exptime)
            while not self.tCamera.state() == PyTango.DevState.ON:
                time.sleep(0.01) 
            self.tCamera.write_attribute(self.command_exptime,self.exptime )
            #self.PollingThread.set_delay(self.exptime)
        #except:
            #print Exception
        
            #QtGui.QMessageBox.warning(self, 'Warning', 'Could not set a new exposure time.', buttons=QtGui.QMessageBox.Ok)
        return None
    
    def clickButtonGetImageData(self):
        try:
            self.exptime = self.tCamera.read_attribute(self.command_exptime).value
            if self.tCamera == 'PCO':
                tmp = numpy.fromstring(self.tPCO.read_attribute('Image').value[1], dtype=numpy.uint16).byteswap()
            
                self.image = (tmp[2:]).reshape(tmp[0], tmp[1])
            else: 
                self.image = self.tCamera.read_attribute(self.command_image).value
            self.imagesize = numpy.shape(self.tCamera.read_attribute(self.command_image).value)
            self.NewUpdate([self.image, self.exptime, self.imagesize])
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not acquire individual image.', buttons=QtGui.QMessageBox.Ok)
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
            if self.Camera == 'PixelLink' or self.Camera == 'PCO':
                self.tTrigger.write_attribute('Voltage', 3.5)
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
            if self.Camera == 'PCO':
                tmp = numpy.fromstring(self.tCamera.read_attribute('Image').value[1], dtype=numpy.uint16).byteswap()
            
                self.image = (tmp[2:]).reshape(tmp[0], tmp[1])
            else: 
                self.image = self.tCamera.read_attribute(self.command_image).value
            self.imagesize = numpy.shape(self.tCamera.read_attribute(self.command_image).value)
            self.NewUpdate([self.image, self.exptime, self.imagesize])
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not acquire individual image.', buttons=QtGui.QMessageBox.Ok)
            raise
        return None

    def clickButtonSetRoi(self):
        try:
            roi_x1 = int(self.io_roixlow.text())
            roi_x2 = int(self.io_roixhigh.text())
            roidx = roi_x2 - roi_x1 + 1
            roi_y1 = int(self.io_roiylow.text())
            roi_y2 = int(self.io_roiyhigh.text())
            roidy = roi_y2 - roi_y1 + 1
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not convert ROI values to numbers.', buttons=QtGui.QMessageBox.Ok)
        if roidx > self.imagesize[0] or roidy > self.imagesize[1]:
            QtGui.QMessageBox.warning(self, 'Warning', 'ROI larger than image size. Please adapt.', buttons=QtGui.QMessageBox.Ok)
            return None
        self.roi_x1 = roi_x1
        self.roi_x2 = roi_x2
        self.roidx = roidx
        self.roi_y1 = roi_y1
        self.roi_y2 = roi_y2
        self.roidy = roidy
        self.label_currentroixlow.setText('%i' % self.roi_x1)
        self.label_currentroixhigh.setText('%i' % self.roi_x2)
        self.label_currentroiylow.setText('%i' % self.roi_y1)
        self.label_currentroiyhigh.setText('%i' % self.roi_y2)
        return None
    # end clickButtonSetRoi

    def clickButtonResetRoi(self):
        self.roi_x1 = 1
        self.roi_x2 =self.imagesize[0]
        self.roidx = self.imagesize[0]
        self.roi_y1 = 1
        self.roi_y2 = self.imagesize[1]
        self.roidy = self.imagesize[1]
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
            histmin = float(self.io_histmin.text())
            histmax = float(self.io_histmax.text())
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not convert histogram boundaries to numbers.', buttons=QtGui.QMessageBox.Ok)
            return None
        if histmin < 0 or histmax > 65565:
            QtGui.QMessageBox.warning(self, 'Warning', 'Histogram values outside 16bit dynamic range..', buttons=QtGui.QMessageBox.Ok)
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
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not convert ROI values to numbers.', buttons=QtGui.QMessageBox.Ok)
        if roidx > self.imagesize[0] or roidy > self.imagesize[1]:
            QtGui.QMessageBox.warning(self, 'Warning', 'ROI larger than image size. Please adapt.', buttons=QtGui.QMessageBox.Ok)
            return None
        self.roi_x1 = roi_x1
        self.roi_x2 = roi_x2
        self.roidx = roidx
        self.roi_y1 = roi_y1
        self.roi_y2 = roi_y2
        self.roidy = roidy
        self.label_currentroixlow.setText('%i' % self.roi_x1)
        self.label_currentroixhigh.setText('%i' % self.roi_x2)
        self.label_currentroiylow.setText('%i' % self.roi_y1)
        self.label_currentroiyhigh.setText('%i' % self.roi_y2)
        
        self.imageView.getView().removeItem(self.box1)
        self.rulerx.setPos((0,0))
        self.rulerx.setSize((1,self.roidy))
        self.rulery.setPos((0,0),)
        self.rulery.setSize((self.roidx,1))
        self.upper_right_corner_x += self.roi_x1
        self.upper_right_corner_y += self.roi_y1
        if self.hist_autorange:
            self.HistWidget.autoHistogramRange()
            self.imageView.setImage(self.image[self.roi_x1-1:self.roi_x2, self.roi_y1-1:self.roi_y2])
        elif self.hist_autorange == False:
            self.HistWidget.setHistogramRange(self.histmin, self.histmax)
            self.imageView.setImage(self.image[self.roi_x1-1:self.roi_x2, self.roi_y1-1:self.roi_y2],\
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
            fname = QtGui.QFileDialog.getSaveFileName(parent=None, caption='Save name for image file', filter = "Tiff Image (*.tiff);; Images (*.png *.jpg *.tif)")
        elif self.currdir != None:
            fname = QtGui.QFileDialog.getSaveFileName(parent=None, caption='Save name for image file', directory = self.currdir, \
                                                      filter = "Tiff Image (*.tiff);; Images (*.png *.jpg *.tif)")
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        _filename = os.path.basename(fname)
        _ftype = _filename.split('.')[1]
        print fname, _ftype
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
            #self.tCamera.write_attribute('SaveImageFlag',False)
        except:
            pass
        if self.activeUpdate:
            self.label_currentpolling.setPalette(self.palette_red)
            self.label_currentpolling.setText('inactive')
            self.but_SetPolling.setText('Start live acquisition')
            self.activeUpdate = False
            self.PollingThread.stop()
            if self.tCamera.state() == PyTango.DevState.EXTRACT:
                self.tCamera.command_inout(self.command_stop)
                time.sleep(0.1)
            if self.Camera == 'PixelLink'or self.Camera == 'PCO':
                self.tTrigger.write_attribute('Voltage', 0)
            if self.Camera == 'Hamamatsu':
                #self.tCamera.write_attribute('TRIGGER_SOURCE', 'INTERNAL')
                if self.HamaHutch == 'eh1':
                    self.tTrigger.write_attribute('Voltage', 0)
                elif self.HamaHutch == 'eh2':
                    self.tTrigger.write_attribute('Value', 0)
        else:
            self.label_currentpolling.setPalette(self.palette_green)
            self.label_currentpolling.setText('active')
            self.but_SetPolling.setText('Stop live acquisition')
            self.activeUpdate = True
            
            if self.tCamera.state() == PyTango.DevState.EXTRACT:
                self.tCamera.command_inout(self.command_stop)
                time.sleep(0.01)
            if self.tCamera.state() != PyTango.DevState.ON:
                QtGui.QMessageBox.warning(self, 'Warning', 'Camera Tango server not in on state!', buttons=QtGui.QMessageBox.Ok)
                return None
            #self.tCamera.command_inout(self.command_start)
            #time.sleep(2)
            #self.tTrigger.write_attribute('Voltage', 0)
            if self.Camera == 'PixelLink' or self.Camera == 'PCO':
                self.tTrigger.write_attribute('Voltage', 0)
            if self.Camera == 'Hamamatsu':
                #self.tCamera.write_attribute('TRIGGER_SOURCE', 'INTERNAL')
                if self.HamaHutch == 'eh1':
                    self.tTrigger.write_attribute('Voltage', 0)
                elif self.HamaHutch == 'eh2':
                    self.tTrigger.write_attribute('Value', 0)
            time.sleep(0.01)
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
        self.nano.SetWorkingPos()
        #self.PollingThread.restart()
        return None
    
    def clickButtonSetAlignmentPos(self):
        self.PixelLinkIn = self.tPixLinkMotorX.read_attribute('Position')
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        self.nano.SetAlignmentPos()
        #self.PollingThread.restart()
        return None
    
    def clickButtonMovePiXLinkOut(self):
        self.tPixLinkMotorX.write_attribute('Position', 2)
        self.label_PixLinkInOut.setText('PixelLink Out')
        
    def clickButtonMovePiXLinkIn(self):
        self.tPixLinkMotorX.write_attribute('Position', self.PixelLinkIn )
#         if posin < 0:
#             print("Warning, In position should be > 0")
#         elif posin >= 0:
#             self.tPixLinkMotorX.write_attribute('Position', 87.15)
#             self.label_PixLinkInOut.setText('PixelLink In')
    
    def clickButtonTake0180(self):
        if self.activeUpdate:
            self.PollingThread.stop()    
        #scan.take0180(self.io_beamtime.text(), self.io_prefix.text(),plot= True)
        ch.alignment_sample_stage('..\scripts\Camera_helper.py', self.io_beamtime.text(), self.io_prefix.text(), int(self.io_rotangle.text()),float(self.io_exptime2.text()), float(self.io_cor.text()), float(self.io_sampleoutrel.text()),float(self.io_rotstartangle.text()),int(self.io_an.text()))
    

    def clickButtonGotoWorkingPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        self.nano.GotoWorkingPos()
        self.label_workingalignment.setText('Working Position')
        return None
    
    def clickButtonGotoAlignmentPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        #self.tBeamShutter.command_inout('CloseOpen_BS_1', 0)
        #print("closing shutter")
        self.tBeamShutter.command_inout('CloseOpen_BS_2', 0)
        time.sleep(4)
        self.tPixLinkMotorX.write_attribute('Position',self.PixelLinkIn)
        while self.tPixLinkMotorX.read_attribute('Position')< self.PixelLinkIn:
            time.sleep(0.2)
        self.nano.GotoAlignmentPos()
        self.label_workingalignment.setText('Alignment Position')
        return None
    
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
            print misc.GetShortTimeString() + ': Warning - requested rotation position outside allowed limits.\nAborting...'
            return None
        self.pmac.Move('Sample_Rot', value,WaitForMove = False)
        return None
    
    def clickButtonSaveAlignmentPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        if self.currdir == None:
            fname = QtGui.QFileDialog.getExistingDirectory(parent=None, caption='Select folder')
        elif self.currdir != None:
            fname = QtGui.QFileDialog.getExistingDirectory(parent=None, caption='Select folder',directory = self.currdir)
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        self.nano.SaveAlignmentPos(fname)
        
    def clickButtonLoadAlignmentPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        if self.currdir == None:
            fname = QtGui.QFileDialog.getOpenFileName(parent=None, caption='Load file', filter = "Text (*.txt)")
        elif self.currdir != None:
            fname = QtGui.QFileDialog.getOpenFileName(parent=None, caption='Load file', directory = self.currdir, \
                                                      filter = "Text (*.txt)")
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        self.nano.LoadAlignmentPos(fname)
    
    def clickButtonSaveWorkingPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        if self.currdir == None:
            fname = QtGui.QFileDialog.getExistingDirectory(parent=None, caption='Select folder')
        elif self.currdir != None:
            fname = QtGui.QFileDialog.getExistingDirectory(parent=None, caption='Select folder',directory = self.currdir)
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        print(fname)
        self.nano.SaveWorkingPos(fname)
        
    def clickButtonLoadWorkingPos(self):
        #if self.activeUpdate:
        #    self.PollingThread.stop()
        if self.currdir == None:
            fname = QtGui.QFileDialog.getOpenFileName(parent=None, caption='Load File', filter = "Text (*.txt)")
        elif self.currdir != None:
            fname = QtGui.QFileDialog.getOpenFileName(parent=None, caption='Load File', directory = self.currdir, \
                                                      filter = "Text (*.txt)")
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        print(fname)
        self.nano.LoadWorkingPos(fname)

    # Buttons Tab 3

    def selectScan(self):
        self.Scan = self.cB_Scan.currentText()
        if self.Scan == 'Take Image Series':
            self.io_rotangle.setDisabled(True)
            self.io_nop.setDisabled(True)
            self.io_rotstartangle.setDisabled(True)
            self.io_refpos.setDisabled(True)
        if self.Scan == 'Standard Scan':
            self.io_rotangle.setDisabled(False)
            self.io_nop.setDisabled(False)
            self.io_rotstartangle.setDisabled(False)
            self.io_refpos.setDisabled(True)
    
    
    def clickButtonStartStandardScan(self):
        if self.activeUpdate:
            self.PollingThread.stop()
        while not self.tCamera.state() == PyTango.DevState.ON:
            time.sleep(0.01) 
        self.tCamera.write_attribute('SaveImageFlag',True)
        self.Scan = self.cB_Scan.currentText()
        beamtime = self.io_beamtime.text()
        prefix = self.io_prefix.text()
        rotangle = int(self.io_rotangle.text())
        nop = int(self.io_nop.text())
        noref = int(self.io_noref.text())
        exptime = float(self.io_exptime2.text())
        rotcenter = float(self.io_cor.text())
        sampleout = float(self.io_sampleoutrel.text())
        integNo = int(self.io_an.text())
        refpos = int(self.io_refpos.text())
        scriptname = '..\scripts\Camera_helper.py'
        if self.Scan == 'Standard Scan':
            ch.StartScanStandard('..\scripts\Camera_helper.py', beamtime, prefix, nop, exptime, rotcenter, sampleout ,rotangle=rotangle)
        if self.Scan == 'Tomo, Ref at start and end':
            ch.StartScan_RefEnd('..\scripts\Camera_helper.py', beamtime, prefix, rotangle, nop, exptime, rotcenter, sampleout)
        if self.Scan == 'Close Shutter':
            ch.closeShutter()
        if self.Scan == 'Take Image Series':
            ch.TakeImageSeries(scriptname,beamtime ,prefix ,integNo,exptime,rotcenter,sampleout,noref)
        if self.Scan == 'Tomo Integrated':
            ch.StartScanIntegrated(scriptname, beamtime, prefix, rotangle, nop, exptime, rotcenter, sampleout, integNo,noref=noref,refpos=refpos)
    
    
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
        currValue = self.image[pos.x(),pos.y()]
        print currValue
        self.label_currentvalue.setText(str(currValue))
        self.rulerx.setPos((pos.x(),0))
        self.rulerx.setSize((1,self.roidy))
        self.rulery.setPos((0,pos.y()),)
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
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not convert ROI values to numbers.', buttons=QtGui.QMessageBox.Ok)
        if roidx > self.imagesize[0] or roidy > self.imagesize[1]:
            QtGui.QMessageBox.warning(self, 'Warning', 'ROI larger than image size. Please adapt.', buttons=QtGui.QMessageBox.Ok)
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
        try:
            self.imageView.getView().removeItem(self.box1)
        finally: 
            self.box1 = self.box
        
    
    def NewUpdate(self, _data):

        # Rotation of Image
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
            self.image = numpy.rot90(_data[0])
        for i in range(self.rotate):
            self.image = numpy.rot90(self.image)
        if self.checkBox_Normalize.isChecked():
            self.image = numpy.float32(self.image)
            for i in range(self.rotate):
                self.flat = numpy.rot90(self.flat)
            self.image = numpy.divide(self.image, self.flat, out=numpy.zeros_like(self.image), where=self.flat!=0)
        
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
            if self.checkBox_Normalize.isChecked():
                self.flat = numpy.rot90(self.flat, 2)
        
        
        self.label_currentexptime.setText('%i ms' % (1e3 * self.exptime))
        self.imageView.getImageItem().mouseClickEvent = self.click
        self.imageView.getImageItem().mouseDragEvent = self.mouseDrag
        if self.hist_autorange:
            self.HistWidget.autoHistogramRange()
            self.imageView.setImage(self.image[self.roi_x1-1:self.roi_x2, self.roi_y1-1:self.roi_y2])
        elif self.hist_autorange == False:
            self.HistWidget.setHistogramRange(self.histmin, self.histmax)
            self.imageView.setImage(self.image[self.roi_x1-1:self.roi_x2, self.roi_y1-1:self.roi_y2],\
                                    levels = (self.histmin, self.histmax), autoHistogramRange = False)
        self.label_timeedit.setTime(QtCore.QTime.currentTime())
        
        #print (self.pmac.ReadMotorPos('Sample_Rot'))
        self.label_posx.setText(str(self.pmac.ReadMotorPos('Sample_x')))
        self.label_posy.setText(str(self.pmac.ReadMotorPos('Sample_y')))
        self.label_posz.setText(str(self.pmac.ReadMotorPos('Sample_z')))
        self.label_posrot.setText(str(self.pmac.ReadMotorPos('Sample_Rot')))
        
        
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
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            if self.tCamera.state() == PyTango.DevState.EXTRACT:
                self.tCamera.command_inout(self.command_stop)
                if self.Camera == 'PixelLink' or self.Camera == 'PCO':
                    self.tTrigger.write_attribute('Voltage', 0)
                if self.Camera == 'Hamamatsu':
                    if self.HamaHutch == 'eh1':
                        self.tTrigger.write_attribute('Voltage', 0)
                    elif self.HamaHutch == 'eh2':
                        self.tTrigger.write_attribute('Value', 0)
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
    def __init__(self, parentThread, Camera, trigger, cB_Cameras, cur_delay = 0.25):
        Camerapolling.__init__(self, parentThread, Camera, trigger, cB_Cameras, cur_delay = cur_delay)
        self.HamaHutch = 'eh2'
        return None
            
    def updateCamera(self):

        while True:
            self.CameraName = self.cB_Cameras.currentText()
            if self.running:
                
                if self.CameraName == 'Hamamatsu':
                    #self.tCamera = PyTango.DeviceProxy('//hzgpp05vme1.desy.de:10000/p05/camera/hama')
                    self.tCamera = PyTango.DeviceProxy('//hzgpp07eh4.desy.de:10000/p07/hama/eh4')
                    
                    if self.HamaHutch == 'eh1':
                        self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
                    elif self.HamaHutch == 'eh2':
                        self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out03')
                    self.command_exptime = 'EXPOSURE_TIME'
                    self.command_start = 'StartAcq'
                    self.command_stop = 'AbortAcq'
                    self.command_image = 'IMAGE'
                    #print ('ok')
                if self.CameraName == 'PCO':
                    self.tCamera = PyTango.DeviceProxy('//hzgpp05vme1:10000/eh1/pco/edge')
                    self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
                    self.command_exptime = 'ExposureTime'
                    self.command_start = 'StartStandardAcq'
                    self.command_stop = 'STOP'
                    self.command_image = 'Image'
                if self.CameraName == 'PixelLink':
                    self.tCamera = PyTango.DeviceProxy('//hzgpp05vme1.desy.de:10000/p05/camera/pixlink')
                    self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
                    self.command_exptime = 'SHUTTER'
                    self.command_start = 'StartAcq'
                    self.command_stop = 'AbortAcq'
                    self.command_image = 'Image'
                if self.CameraName == 'Zyla':
                    self.tCamera = PyTango.DeviceProxy('hzgpp05ct09:10000/p05/limaccds/ct09.01')
                    #self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out01')
                    self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme2:10000/p05/register/eh2.out03')
                    self.command_exptime = 'acq_expo_time'
                    self.command_start = 'startAcq'
                    self.command_stop = 'abortAcq'
                    self.command_image = 'IMAGE'
                    self.tCamera.write_attribute('acq_trigger_mode','INTERNAL_TRIGGER')
                    self.tCamera.write_attribute('saving_mode','MANUAL')
                    self.imagesize = (2560, 2160)
                    
                if self.CameraName == 'KIT':
                    self.tCamera = PyTango.DeviceProxy('hzgpp05ctcam1:10000/p05/hzguca/kit')
                    self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
                    self.command_exptime = 'exposure_time'
                    self.command_start = 'Start'
                    self.command_stop = 'Stop'
                    self.command_image = 'image'
                    self.tCamera.write_attribute('trigger_source','1')  # 0: auto, 1: software, 2: Hardware
                    self.tCamera.write_attribute('writeInMemory','false')    
                    self.imagesize = (2560, 2160)

                
                #print (self.CameraName)
                self.t0 = time.time()
                if self.CameraName =='Zyla':
                    self.tCamera.command_inout('prepareAcq')
                while not self.tCamera.state() == PyTango.DevState.ON:
                    time.sleep(0.001)
                self.tCamera.command_inout(self.command_start)
                
                if self.CameraName == 'Hamamatsu':
                    while not self.tCamera.state() == PyTango.DevState.EXTRACT:
                        time.sleep(0.001)
                        #print('wait for extract')
                        
                if self.CameraName == 'PixelLink' or self.CameraName == 'PCO':
                    self.tTrigger.write_attribute('Voltage', 3.5)
                if self.CameraName == 'Hamamatsu':
                    if self.HamaHutch == 'eh1':
                        self.tTrigger.write_attribute('Voltage', 3.5)
                    elif self.HamaHutch == 'eh2':
                        self.tTrigger.write_attribute('Value', 1)
                time.sleep(0.01)
                if self.CameraName == 'PixelLink' or self.CameraName == 'PCO':
                    self.tTrigger.write_attribute('Voltage', 0)
                if self.CameraName == 'Hamamatsu':
                    if self.HamaHutch == 'eh1':
                        self.tTrigger.write_attribute('Voltage', 0)
                    elif self.HamaHutch == 'eh2':
                        self.tTrigger.write_attribute('Value', 0)
                while not self.tCamera.state() == PyTango.DevState.ON:
                    time.sleep(0.001)
                self.exptime = self.tCamera.read_attribute(self.command_exptime).value
                
                if self.CameraName == 'PCO':
                    tmp = numpy.fromstring(self.tCamera.read_attribute('Image').value[1], dtype=numpy.uint16).byteswap()
                    self.image = (tmp[2:]).reshape(tmp[0], tmp[1])
                elif self.CameraName == 'Zyla':
                    time.sleep(self.exptime+1)
                    a = self.tCamera.read_attribute('saving_next_number')
                    tmp = self.tCamera.command_inout('getImage',a.value)
                    self.image = tmp
                else:
                    self.image = self.tCamera.read_attribute(self.command_image).value
                if self.CameraName == 'Zyla':
                    self.imagesize = (2160,2560)
                else:          
                    self.imagesize = numpy.shape(self.tCamera.read_attribute(self.command_image).value) #(self.tCamera.read_attribute('IMAGE_WIDTH'), self.tCamera.read_attribute('IMAGE_WIDTH'))
                #time.sleep(max(0, self.cur_delay - (time.time() - self.t0)))
                self.emit(QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), [self.image, self.exptime, self.imagesize])
                
            elif self.running == False:
                time.sleep(0.1)
            if self.terminate_signal:
                    break
        return None
# class UpdateThread



def Camera_LiveImage(parent=None, devices=None, groups=None, name='Camera live image'):
    app = QtGui.QApplication(sys.argv)
    
    gui = cCamera_LiveImage(name=name, parent=QtGui.QMainWindow())
    gui.PollingThread = UpdateThread(gui.main, gui.tCamera, gui.tTrigger,gui.cB_Cameras)
    gui.PollingThread.start()
    gui.initializeUpdater()
    gui.show()
    if sys.platform == 'win32' or sys.platform == 'win64':
        sys.exit(app.exec_())
    else:
        app.exec_()


if __name__ == "__main__":
    Camera_LiveImage()
