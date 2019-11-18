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


class cPCO_LiveImage(QtGui.QMainWindow):
    def __init__(self, parent=None, name='PCO live image'):
        super(cPCO_LiveImage, self).__init__()
        try:
            QtUic.loadUi('h:/_data/programming_python/p05/gui/PCOlive_ui.ui', self)
            self.setWindowIcon(QtGui.QIcon('h:/_data/programming_python/p05/gui/pco.png'))
        except:
            _path = misc.GetPath('PCOlive_ui.ui')
            QtUic.loadUi(_path, self)
            self.setWindowIcon(QtGui.QIcon(os.path.split(_path)[0] + os.sep + 'pco.png'))
        self.setWindowTitle(name)
        self.setWindowIcon(QtGui.QIcon('h:/_data/programming_python/p05/gui/pco.png'))
        self.setGeometry(10, 25, 1500, 965)

	self.tBeamShutter = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/shutter/all')        

        self.tPCO = PyTango.DeviceProxy('//hzgpp05vme1:10000/eh1/pco/edge')
        self.tTrigger = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/dac/eh1.01')
        self.exptime = self.tPCO.read_attribute('ExposureTime').value
        self.label_currentexptime.setText('%i ms' %(self.exptime* 1e3))
            
        self.main = parent
        
        self.bgcolor = '#698aE5'
        self.imageView.ui.graphicsView.setBackground(self.bgcolor)
        
        
        self.HistWidget = self.imageView.getHistogramWidget()
        self.HistWidget.setBackground('#EEEEEE')
        
    
        self._initialize()
        self.activeUpdate = False
        self.global_delay = 300
        self.imagesize = (2048, 2048)
        self.roi_x1 = 1
        self.roi_x2 = self.imagesize[0]
        self.roidx = self.imagesize[0]
        self.roi_y1 = 1
        self.roi_y2 = self.imagesize[1]
        self.roidy = self.imagesize[1]
        self.histmin = 1
        self.histmax = 65000
        self.hist_autorange = True
        self.viewModeXRM = False

        self.currdir = None
        self.updater = QtCore.QTimer()
        
        QtCore.QObject.connect(self.but_SetExptime, QtCore.SIGNAL('clicked()'), self.clickButtonSetExptime)    
        QtCore.QObject.connect(self.but_SetPolling, QtCore.SIGNAL('clicked()'), self.clickButtonStartLive)
        QtCore.QObject.connect(self.but_GetImageData, QtCore.SIGNAL('clicked()'), self.clickButtonGetImageData)
        QtCore.QObject.connect(self.but_Snapshot, QtCore.SIGNAL('clicked()'), self.clickButtonSnapshop)
        QtCore.QObject.connect(self.but_SetRoi, QtCore.SIGNAL('clicked()'), self.clickButtonSetRoi)    
        QtCore.QObject.connect(self.but_ResetRoi, QtCore.SIGNAL('clicked()'), self.clickButtonResetRoi)
        QtCore.QObject.connect(self.but_SetHist, QtCore.SIGNAL('clicked()'), self.clickButtonSetHist)    
        QtCore.QObject.connect(self.but_SetHistAutoRange, QtCore.SIGNAL('clicked()'), self.clickButtonSetHistAutoRange)
        QtCore.QObject.connect(self.but_RefreshHist, QtCore.SIGNAL('clicked()'), self.clickButtonRefreshHist)
        QtCore.QObject.connect(self.but_SaveImage, QtCore.SIGNAL('clicked()'), self.clickButtonSaveImage)
        QtCore.QObject.connect(self.but_SwitchView, QtCore.SIGNAL('clicked()'), self.clickButtonSwitchView)
        
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


        self.but_SetExptime.setStyleSheet(self.button_style)
        self.but_SetPolling.setStyleSheet(self.button_style)
        self.but_Snapshot.setStyleSheet(self.button_style)
        self.but_SetRoi.setStyleSheet(self.button_style)
        self.but_ResetRoi.setStyleSheet(self.button_style)
        self.but_SetHistAutoRange.setStyleSheet(self.button_style)
        self.but_SetHist.setStyleSheet(self.button_style)
        self.but_RefreshHist.setStyleSheet(self.button_style)
        self.but_SaveImage.setStyleSheet(self.button_style)
        self.but_GetImageData.setStyleSheet(self.button_style)
        

        self.label_currentpolling.setPalette(self.palette_red)
        self.label_currentpolling.setText('inactive')

        
        self.io_exptime.setStyleSheet(self.textbox_style)
        self.label_currenthistautorange.setPalette(self.palette_green)
        
        self.floatValidator = QtGui.QDoubleValidator(self)
        self.floatValidator.setRange(-360., 360.)
        
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

        self.tPitch =  PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/motor/mono.01')
        self.tRoll  =  PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/motor/mono.02')
        self.tUndulator = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/undulator/1')
        self.tScintiY = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.05')
        self.tLensY = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.06')
        self.tCamRot = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.07')
        self.tDCM = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/dcmener/s01.01')
        return None
            
            
    def initializeUpdater(self):
        QtCore.QObject.connect(self.PollingThread, QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), self.NewUpdate)
        return None
    #end initializeUpdater

    def clickButtonSetExptime(self):
        """Set the self.global_delay variable (in ms) """
        try: 
            _txt = self.io_exptime.text()
            _val = float(_txt)
            self.exptime = _val * 1e-3
            self.label_currentexptime.setText(_txt + ' ms')
            if self.activeUpdate:
                self.PollingThread.stop()
                time.sleep(0.1)
                self.t0 = time.time()
                self.tPCO.command_inout('STOP')
                while True:
                    if self.tPCO.state() == PyTango.DevState.RUNNING: time.sleep(0.1)
                    else:
                        break
                    if time.time() - self.t0 > 60: break
                self.PollingThread.set_delay(self.exptime)
                self.tPCO.write_attribute('ExposureTime', self.exptime)
                time.sleep(0.1)
                self.tPCO.command_inout('Live')
                self.PollingThread.restart()
            elif self.activeUpdate == False:
                self.tPCO.write_attribute('ExposureTime', self.exptime)
                self.PollingThread.set_delay(self.exptime)
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not set a new exposure time.', buttons=QtGui.QMessageBox.Ok)
        return None
    
    def clickButtonGetImageData(self):
        try:
            self.exptime = self.tPCO.read_attribute('ExposureTime').value
            tmp = numpy.fromstring(self.tPCO.read_attribute('Image').value[1], dtype=numpy.uint16).byteswap()
            
            self.image = (tmp[2:]).reshape(tmp[0], tmp[1])
            self.imagesize = (tmp[0], tmp[1])
            self.NewUpdate([self.image, self.exptime, self.imagesize])
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not acquire individual image.', buttons=QtGui.QMessageBox.Ok)
        return None
    #end clickButtonGetImageData
    
    def clickButtonSnapshop(self):
        try: 
            if self.activeUpdate:
                self.PollingThread.stop()
                self.label_currentpolling.setPalette(self.palette_red)
                self.label_currentpolling.setText('inactive')
                self.but_SetPolling.setText('Start live acquisition')
                self.activeUpdate = False
                if self.tPCO.state() == PyTango.DevState.RUNNING:
                    self.tPCO.command_inout('STOP')
                    self.tTrigger.write_attribute('Voltage', 0)
                    time.sleep(0.1 + self.exptime)
            self.exptime = self.tPCO.read_attribute('ExposureTime').value
            self.label_currentexptime.setText('%i' %(self.exptime* 1e3) + ' ms')
            self.tPCO.command_inout('StartStandardAcq')
            time.sleep(1)
            self.tTrigger.write_attribute('Voltage', 5)
            time.sleep(self.exptime + 0.4)
            self.tTrigger.write_attribute('Voltage', 0)
            tmp = numpy.fromstring(self.tPCO.read_attribute('Image').value[1], dtype=numpy.uint16).byteswap()
            self.image = (tmp[2:]).reshape(tmp[0], tmp[1])
            self.imagesize = (tmp[0], tmp[1])
            self.NewUpdate([self.image, self.exptime, self.imagesize])
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not acquire individual image.', buttons=QtGui.QMessageBox.Ok)
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
        self.roi_x2 = self.imagesize[0]
        self.roidx = self.imagesize[0]
        self.roi_y1 = 1
        self.roi_y2 = self.imagesize[1]
        self.roidy = self.imagesize[1]
        self.label_currentroixlow.setText('%i' % self.roi_x1)
        self.label_currentroixhigh.setText('%i' % self.roi_x2)
        self.label_currentroiylow.setText('%i' % self.roi_y1)
        self.label_currentroiyhigh.setText('%i' % self.roi_y2)
        return None
    # end clickButtonSetRoi
        
    def clickButtonSetHist(self):
        try:
            histmin = int(self.io_histmin.text())
            histmax = int(self.io_histmax.text())
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
        if self.hist_autorange:
            self.HistWidget.autoHistogramRange()
            self.imageView.setImage(self.image[self.roi_x1-1:self.roi_x2, self.roi_y1-1:self.roi_y2])
        elif self.hist_autorange == False:
            self.HistWidget.setHistogramRange(self.histmin, self.histmax)
            self.imageView.setImage(self.image[self.roi_x1-1:self.roi_x2, self.roi_y1-1:self.roi_y2],\
                                    levels = (self.histmin, self.histmax), autoHistogramRange = False)
        #end clickButtonRefreshHist
    
    
    def clickButtonSaveImage(self):
        if self.activeUpdate:
            self.PollingThread.stop()
        if self.currdir == None:
            fname = QtGui.QFileDialog.getSaveFileName(parent=None, caption='Save name for image file', filter = "Raw data (*.raw);; Images (*.png *.jpg *.tif)")
        elif self.currdir != None:
            fname = QtGui.QFileDialog.getSaveFileName(parent=None, caption='Save name for image file', directory = self.currdir, \
                                                      filter = "Raw data (*.raw);; Images (*.png *.jpg *.tif)")
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        _filename = os.path.basename(fname)
        _ftype = _filename.split('.')[1]
        print fname, _ftype
        if _ftype == 'raw':
            (self.image.transpose()).tofile(fname)
        elif _ftype in ['png', 'jpg', 'tif']:
            pylab.matplotlib.image.imsave(fname, self.image.transpose(), cmap = 'gray')
        
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
        if self.activeUpdate:
            self.label_currentpolling.setPalette(self.palette_red)
            self.label_currentpolling.setText('inactive')
            self.but_SetPolling.setText('Start live acquisition')
            self.activeUpdate = False
            self.PollingThread.stop()
            if self.tPCO.state() == PyTango.DevState.RUNNING:
                self.tPCO.command_inout('Stop')
                time.sleep(0.1)
            self.tTrigger.write_attribute('Voltage', 0)
        else:
            self.label_currentpolling.setPalette(self.palette_green)
            self.label_currentpolling.setText('active')
            self.but_SetPolling.setText('Stop live acquisition')
            self.activeUpdate = True
            if self.tPCO.state() == PyTango.DevState.RUNNING:
                self.tPCO.command_inout('Stop')
                time.sleep(0.1)
            if self.tPCO.state() != PyTango.DevState.ON:
                QtGui.QMessageBox.warning(self, 'Warning', 'PCO Tango server not in on state!', buttons=QtGui.QMessageBox.Ok)
                return None
            self.tPCO.command_inout('Live')
            time.sleep(2)
            self.tTrigger.write_attribute('Voltage', 0)
            time.sleep(0.1)
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
            self.imageView.ui.graphicsView.setBackground('#698aE5')
            #self.HistWidget.setBackground('#698aE5')
            self.label_currentview.setPalette(self.palette_lightblue)
            self.label_currentview.setText('Direct beam mode')
            self.viewModeXRM = False
            
        return None
    #end ClickButtonSwitchView
    
    def NewUpdate(self, _data):
        self.exptime = _data[1]
        self.imagesize = _data[2]
        self.image = numpy.rot90(_data[0])
        if self.viewModeXRM == True:  self.image = numpy.rot90(self.image, 2)
        self.label_currentimagexsize.setText('%i' % self.imagesize[0])
        self.label_currentimageysize.setText('%i' % self.imagesize[1])
        
        self.label_currentexptime.setText('%i ms' % (1e3 * self.exptime))
        if self.hist_autorange:
            self.HistWidget.autoHistogramRange()
            self.imageView.setImage(self.image[self.roi_x1-1:self.roi_x2, self.roi_y1-1:self.roi_y2])
        elif self.hist_autorange == False:
            self.HistWidget.setHistogramRange(self.histmin, self.histmax)
            self.imageView.setImage(self.image[self.roi_x1-1:self.roi_x2, self.roi_y1-1:self.roi_y2],\
                                    levels = (self.histmin, self.histmax), autoHistogramRange = False)
        self.label_timeedit.setTime(QtCore.QTime.currentTime())
        return None
    # end NewUpdate
    
    
    def closeEvent(self, event):
        """Safety check for closing of window."""
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            if self.tPCO.state() == PyTango.DevState.RUNNING:
                self.tPCO.command_inout('Stop')
                self.tTrigger.write_attribute('Voltage', 0)
            self.PollingThread.terminate_signal = True
            
            event.accept()
        else:
            event.ignore()
        return None   


class  PCOpolling(QtCore.QThread):
    def __init__(self, parentThread, pco, trigger, cur_delay = 0.25):
        QtCore.QThread.__init__(self, parentThread)
        self.parent = parentThread
        self.Image = None
        self.tPCO = pco
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
        self.updatePCO()
        return None
    
    def cleanUp(self):
        return None
    
    def getUpdate(self):
        return True

    def __del__(self):
        self.exiting = True
        self.wait()
        return None
#end PCOpolling


class UpdateThread(PCOpolling):
    def __init__(self, parentThread, pco, trigger, cur_delay = 0.25):
        PCOpolling.__init__(self, parentThread, pco, trigger, cur_delay = cur_delay)
        return None
            
    def updatePCO(self):
        while True:
            if self.running:
                self.t0 = time.time()
                self.exptime = self.tPCO.read_attribute('ExposureTime').value
                self.tTrigger.write_attribute('Voltage', 5)
                time.sleep(self.exptime + 0.1)
                self.tTrigger.write_attribute('Voltage', 0)
                tmp = numpy.fromstring(self.tPCO.read_attribute('Image').value[1], dtype=numpy.uint16).byteswap()
                self.Image = (tmp[2:]).reshape(tmp[0], tmp[1])
                self.imagesize = (tmp[0], tmp[1])
                time.sleep(max(0, self.cur_delay - (time.time() - self.t0)))
                self.emit(QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), [self.Image, self.exptime, self.imagesize])
            elif self.running == False:
                time.sleep(0.1)
            if self.terminate_signal:
                break
        return None
# class UpdateThread



def PCO_LiveImage(parent=None, devices=None, groups=None, name='PCO live image'):
    app = QtGui.QApplication(sys.argv)
    gui = cPCO_LiveImage(name=name, parent=QtGui.QMainWindow())
    gui.PollingThread = UpdateThread(gui.main, gui.tPCO, gui.tTrigger)
    gui.PollingThread.start()
    gui.initializeUpdater()
    gui.show()
    if sys.platform == 'win32' or sys.platform == 'win64':
        sys.exit(app.exec_())
    else:
        app.exec_()

