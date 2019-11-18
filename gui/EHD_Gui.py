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
from p05.devices.XrayShutter import XRayShutter



class cEHD_Gui(QtGui.QMainWindow):
    def __init__(self, parent=None, name='EHD image GUI'):
        super(cEHD_Gui, self).__init__()
        try:
            QtUic.loadUi('h:/_data/programming_python/p05/gui/EHD_ui.ui', self)
            self.setWindowIcon(QtGui.QIcon('h:/_data/programming_python/p05/gui/ehd.png'))
        except:
            _path = misc.GetPath('PCOlive_ui.ui')
            QtUic.loadUi(_path, self)
            self.setWindowIcon(QtGui.QIcon(os.path.split(_path)[0] + os.sep + 'ehd.png'))
        self.setWindowTitle(name)
        self.setGeometry(10, 25, 1500, 965)
        
        self.tEHD = PyTango.DeviceProxy('//hzgpp05ct1:10000/p05/eh2/smc0900')
        self.Shutter = XRayShutter
        self.exptime = self.tEHD.read_attribute('ExposureTime').value
        
        self.bgcolor = '#000088'
        self.imageView.ui.graphicsView.setBackground(self.bgcolor)
        
        self.HistWidget = self.imageView.getHistogramWidget()
        self.HistWidget.setBackground(self.bgcolor)
        
        self.currdir = None
        self.updater = QtCore.QTimer()
        self._initialize()
        
        QtCore.QObject.connect(self.but_SetExptime, QtCore.SIGNAL('clicked()'), self.clickButtonSetExptime)    
        QtCore.QObject.connect(self.but_GetImageData, QtCore.SIGNAL('clicked()'), self.clickButtonGetImageData)
        QtCore.QObject.connect(self.but_Snapshot, QtCore.SIGNAL('clicked()'), self.clickButtonSnapshop)
        QtCore.QObject.connect(self.but_SetCameraRoi, QtCore.SIGNAL('clicked()'), self.clickButtonSetCameraRoi)    
        QtCore.QObject.connect(self.but_ResetCameraRoi, QtCore.SIGNAL('clicked()'), self.clickButtonResetCameraRoi)
        QtCore.QObject.connect(self.but_SetHist, QtCore.SIGNAL('clicked()'), self.clickButtonSetHist)    
        QtCore.QObject.connect(self.but_SetHistAutoRange, QtCore.SIGNAL('clicked()'), self.clickButtonSetHistAutoRange)
        QtCore.QObject.connect(self.but_RefreshHist, QtCore.SIGNAL('clicked()'), self.clickButtonRefreshHist)
        QtCore.QObject.connect(self.but_SaveImage, QtCore.SIGNAL('clicked()'), self.clickButtonSaveImage)
        QtCore.QObject.connect(self.but_SetImageRoi, QtCore.SIGNAL('clicked()'), self.clickButtonSetImageRoi)    
        QtCore.QObject.connect(self.but_SetBinning, QtCore.SIGNAL('clicked()'), self.clickButtonSetBinning)    
        QtCore.QObject.connect(self.but_ResetImageRoi, QtCore.SIGNAL('clicked()'), self.clickButtonResetImageRoi)
        QtCore.QObject.connect(self.combo_Binning, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeBinningCombo)
        QtCore.QObject.connect(self.but_SetUpdateDelay, QtCore.SIGNAL('clicked()'), self.clickButtonSetUpdateDelay)    
        QtCore.QObject.connect(self.but_ContinuousUpdate, QtCore.SIGNAL('clicked()'), self.clickButtonContinuousUpdate)
        
        self.PollingThread = EHDpolling(self, camera =self.tEHD)
        QtCore.QObject.connect(self.PollingThread, QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), self.RecievedNewImage)

        self.CameraReadSettings()
        self.show()
        return None
    
    def _initialize(self):
        ##############################################
        ############## Button styles: ################
        ##############################################
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

        self.but_SetExptime.setStyleSheet(self.button_style)
        self.but_Snapshot.setStyleSheet(self.button_style)
        self.but_GetImageData.setStyleSheet(self.button_style)
        self.but_SetCameraRoi.setStyleSheet(self.button_style)
        self.but_ResetCameraRoi.setStyleSheet(self.button_style)
        self.but_SetHistAutoRange.setStyleSheet(self.button_style)
        self.but_SetHist.setStyleSheet(self.button_style)
        self.but_RefreshHist.setStyleSheet(self.button_style)
        self.but_SaveImage.setStyleSheet(self.button_style)
        self.but_SetImageRoi.setStyleSheet(self.button_style)
        self.but_ResetImageRoi.setStyleSheet(self.button_style)
        self.but_SetBinning.setStyleSheet(self.button_style)
        self.but_ContinuousUpdate.setStyleSheet(self.button_style)
        self.but_SetUpdateDelay.setStyleSheet(self.button_style)
        self.io_exptime.setStyleSheet(self.textbox_style)
        self.label_currenthistautorange.setPalette(self.palette_green)
        
        
        ##############################################
        ############## Text styles: ##################
        ##############################################
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
        
        ##############################################
        ############## TANGO connections: ############
        ##############################################
        try:
            self.SM = numpy.zeros(4, dtype=object)
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

        self.tPitch = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/motor/mono.01')
        self.tRoll = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/motor/mono.02')
        self.tUndulator = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/undulator/1')
        self.tScintiY = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.05')
        self.tLensY = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.06')
        self.tCamRot = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/motor/eh1.07')
        self.tDCM = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/dcmener/s01.01')
        
        ##############################################
        ############## Camera initialization: ########
        ##############################################
        self.CAM_FlipLR = False
        self.CAM_PosX_FromPix = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array((Ytotal - Ymin, Ytotal - Ymax))
        self.CAM_PixY_FromPos = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array((Xtotal - Xmin, Xtotal - Xmax))
        self.CAM_FlipUD = False
        self.CAM_PosY_FromPix = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array((Xtotal - Xmin, Xtotal - Xmax))
        self.CAM_PixX_FromPos = lambda Xmin, Xmax, Xtotal, Ymin, Ymax, Ytotal: numpy.array((Ytotal - Ymin, Ytotal - Ymax))

        self.bool_ZoomActive = False
        
        self.label_currentexptime.setText('%i ms' % (self.tEHD.read_attribute('ExposureTime').value))
        self.selected_binning = 1
        
        self.imagesize = (3056, 3056)
        self.visroi_x1 = 1
        self.visroi_x2 = self.imagesize[0]
        self.visroidx = self.imagesize[0]
        self.visroi_y1 = 1
        self.visroi_y2 = self.imagesize[1]
        self.visroidy = self.imagesize[1]
        
        self.camroi_x1 = 1
        self.camroi_x2 = self.imagesize[0]
        self.camroidx = self.imagesize[0]
        self.camroi_y1 = 1
        self.camroi_y2 = self.imagesize[1]
        self.camroidy = self.imagesize[1]
        self.CAM_NumPixX = 3056
        self.CAM_NumPixY = 3056

        self.updatedelay = 1000                
        self.histmin = 1
        self.histmax = 65000
        self.hist_autorange = True
        self.hist_log = False
        self.continuousupdate = False
        self.CameraReadSettings()
        
        ##############################################
        ############## Colormaps: ####################
        ##############################################
        
        
        _hot_data = {'red':   ((0., 0.0416, 0.0416), (0.365079, 1.000000, 1.000000), (1.0, 1.0, 1.0)), \
                     'green': ((0., 0., 0.), (0.365079, 0.000000, 0.000000), (0.746032, 1.000000, 1.000000), (1.0, 1.0, 1.0)), \
                     'blue':  ((0., 0., 0.), (0.746032, 0.000000, 0.000000), (1.0, 1.0, 1.0))}
        
        pos = numpy.array([0, 0.365, 0.746, 1.])
        val = numpy.array([[0.0416, 0., 0., 1.], [1., 0., 0., 1.], [1., 1., 0., 1.], [1., 1., 1., 1.]])
        cmap = pyqtgraph.ColorMap(pos, val)
        self.lut_hot = cmap.getLookupTable(0.0, 1.0, 256)
        
        pos = numpy.array([0., 1.])
        val = numpy.array([[0.0, 0., 0., 1.], [1., 1., 1., 1.]])
        cmap = pyqtgraph.ColorMap(pos, val)
        self.lut_gray = cmap.getLookupTable(0.0, 1.0, 256)
        
        self.cmap = True
        # self.label
        
        return None
            
    
    def changeBinningCombo(self):
        self.selected_binning = int(self.combo_Binning.currentText())
    # end changeBinningCombo
    
    def clickButtonSetExptime(self):
        """Set the self.global_delay variable (in ms) """
        try: 
            _txt = self.io_exptime.text()
            _val = float(_txt)
            self.exptime = _val
            self.label_currentexptime.setText(_txt + ' ms')
            self.tEHD.write_attribute('ExposureTime', self.exptime)
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not set a new exposure time.', buttons=QtGui.QMessageBox.Ok)
        return None
    
    def clickButtonGetImageData(self):
        try:
            self.exptime = self.tEHD.read_attribute('ExposureTime').value
            self.CameraReadSettings()
            self.image = 1.0 * numpy.flipud(self.tEHD.read_attribute('Image').value)
            self.imagesize = self.image.shape
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not acquire individual image.', buttons=QtGui.QMessageBox.Ok)
        self.NewUpdate()
        return None
    # end clickButtonGetImageData
    
    def clickButtonSnapshop(self):
        t0 = time.time()
        try: 
            self.exptime = self.tEHD.read_attribute('ExposureTime').value * 1e-3
            self.CameraReadSettings()
            self.label_currentexptime.setText('%i' % (self.exptime * 1e3) + ' ms')
            self.tEHD.command_inout('ExposeFrame')
            time.sleep(self.exptime)
            while self.tEHD.state() != PyTango.DevState.EXTRACT:
                time.sleep(0.05)
            self.tEHD.command_inout('GrabFrame')
            time.sleep(0.05)
            timeout = 10
            while self.tEHD.state() != PyTango.DevState.ON:
                time.sleep(0.1)
                timeout -= 0.1
                if timeout < 0: 
                    QtGui.QMessageBox.warning(self, 'Warning', 'Camera timeout.', buttons=QtGui.QMessageBox.Ok)
                    break
    
            self.image = numpy.flipud(self.tEHD.read_attribute('Image').value)
            self.imagesize = self.image.shape
            self.NewUpdate()
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not acquire individual image.', buttons=QtGui.QMessageBox.Ok)
        print time.time() - t0
        return None
        
    
    def clickButtonSetCameraRoi(self):
        try:
            tmp_x1 = int(self.io_roixlow.text())
            tmp_x2 = int(self.io_roixhigh.text())
            tmp_y1 = int(self.io_roiylow.text())
            tmp_y2 = int(self.io_roiyhigh.text())
            tmp_x = self.CAM_PixX_FromPos(tmp_x1, tmp_x2, self.CAM_NumPixX / self.CAM_Binning, tmp_y1, tmp_y2, self.CAM_NumPixY / self.CAM_Binning)
            tmp_y = self.CAM_PixY_FromPos(tmp_x1, tmp_x2, self.CAM_NumPixX / self.CAM_Binning, tmp_y1, tmp_y2, self.CAM_NumPixY / self.CAM_Binning)
            self.CAM_xlow, self.CAM_xhigh = min(tmp_x), max(tmp_x)
            self.CAM_ylow, self.CAM_yhigh = min(tmp_y), max(tmp_y)
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not convert ROI values to numbers.', buttons=QtGui.QMessageBox.Ok)
        self.tEHD.write_attribute('Roi_ul_x', long(self.CAM_xlow))
        self.tEHD.write_attribute('Roi_ul_y', long(self.CAM_ylow))
        self.tEHD.write_attribute('Roi_lr_x', long(self.CAM_xhigh - self.CAM_xlow))
        self.tEHD.write_attribute('Roi_lr_y', long(self.CAM_yhigh - self.CAM_ylow))
            
        self.label_cameraroixlow.setText('%i' % self.CAM_xlow)
        self.label_cameraroixhigh.setText('%i' % self.CAM_xhigh)
        self.label_cameraroiylow.setText('%i' % self.CAM_ylow)
        self.label_cameraroiyhigh.setText('%i' % self.CAM_yhigh)
        return None
    # end clickButtonSetRoi

    def clickButtonResetCameraRoi(self):
        self.tEHD.write_attribute('Roi_ul_x', long(0))
        self.tEHD.write_attribute('Roi_ul_y', long(0))
        self.tEHD.write_attribute('Roi_lr_y', long(3056))
        self.tEHD.write_attribute('Roi_lr_x', long(3056))
        self.label_cameraroixlow.setText('%i' % 0)
        self.label_cameraroixhigh.setText('%i' % 3056)
        self.label_cameraroiylow.setText('%i' % 0)
        self.label_cameraroiyhigh.setText('%i' % 3056)
        return None
    # end clickButtonResetCameraRoi
    
    
    def clickButtonSetImageRoi(self):
        try:
            tmp_x1 = int(self.io_imageroixlow.text())
            tmp_x2 = int(self.io_imageroixhigh.text())
            tmp_y1 = int(self.io_imageroiylow.text())
            tmp_y2 = int(self.io_imageroiyhigh.text())
            self.visroi_x1, self.visroi_x2 = min(tmp_x1, tmp_x2), max(tmp_x1, tmp_x2)
            self.visroi_y1, self.visroi_y2 = min(tmp_y1, tmp_y2), max(tmp_y1, tmp_y2)
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not convert ROI values to numbers.', buttons=QtGui.QMessageBox.Ok)
            
        self.label_imageroixlow.setText('%i' % self.visroi_x1)
        self.label_imageroixhigh.setText('%i' % self.visroi_x2)
        self.label_imageroiylow.setText('%i' % self.visroi_y1)
        self.label_imageroiyhigh.setText('%i' % self.visroi_y2)
        self.NewUpdate()
        return None
    # end clickButtonSetRoi

    def clickButtonResetImageRoi(self):
        self.visroi_x1 = 0
        self.visroi_x2 = self.imagesize[0]
        self.visroidx = self.imagesize[0]
        self.visroi_y1 = 0
        self.visroi_y2 = self.imagesize[1]
        self.visroidy = self.imagesize[1]
        self.label_imageroixlow.setText('%i' % self.visroi_x1)
        self.label_imageroixhigh.setText('%i' % self.visroi_x2)
        self.label_imageroiylow.setText('%i' % self.visroi_y1)
        self.label_imageroiyhigh.setText('%i' % self.visroi_y2)
        self.NewUpdate()
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
    # end clickButtonSetHist

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
    # end clickButtonSetHistAutoRange
    
    def clickButtonSetBinning(self):
        try:
            self.tEHD.write_attribute('VBin', self.selected_binning)
            self.tEHD.write_attribute('HBin', self.selected_binning)
            self.label_currentbinning.setText('%i' % self.selected_binning)
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not set new binning.', buttons=QtGui.QMessageBox.Ok)
            return None
        return None
    # end clickButtonSetBinning
        
    
    def clickButtonRefreshHist(self):
        if self.hist_autorange:
            self.HistWidget.autoHistogramRange()
            self.imageView.setImage(self.image[self.visroi_x1:self.visroi_x2, self.visroi_y1:self.visroi_y2])
        elif self.hist_autorange == False:
            self.HistWidget.setHistogramRange(self.histmin, self.histmax)
            self.imageView.setImage(self.image[self.visroi_x1:self.visroi_x2, self.visroi_y1:self.visroi_y2], \
                                    levels=(self.histmin, self.histmax), autoHistogramRange=False)
        # end clickButtonRefreshHist
    
    
    def clickButtonSaveImage(self):
        if self.currdir == None:
            fname = QtGui.QFileDialog.getSaveFileName(parent=None, caption='Save name for image file', filter="Raw data (*.raw);; Images (*.png *.jpg *.tif)")
        elif self.currdir != None:
            fname = QtGui.QFileDialog.getSaveFileName(parent=None, caption='Save name for image file', directory=self.currdir, \
                                                      filter="Raw data (*.raw);; Images (*.png *.jpg *.tif)")
        fname = str(fname)
        self.currdir = os.path.dirname(fname)
        _filename = os.path.basename(fname)
        _ftype = _filename.split('.')[1]
        print fname, _ftype
        if _ftype == 'raw':
            (self.image.transpose()).tofile(fname)
        elif _ftype in ['png', 'jpg', 'tif']:
            pylab.matplotlib.image.imsave(fname, self.image.transpose(), cmap='gray')
            
        _log = 'Warning: Motor positions could have been moved by another process! \n'
        _log += 'Timestamp = ' + misc.GetTimeString() + '\n'
        _log += 'ExposureTime =\t%e\n' % (self.tEHD.read_attribute('ExposureTime').value * 1e-3)
        _log += 'Undulator gap =\t%e\n' % self.tUndulator.read_attribute('Gap').value
        _log += 'DCM energy =   \t%e\n' % self.tDCM.read_attribute('Position').value
        _log += 'DCM pitch =    \t%e\n' % self.tPitch.read_attribute('Position').value
        if self.pmac != None:
            _log += self.pmac.ReturnMotorPositionString()
        _log += 'Scinillator y =\t%e\n' % self.tScintiY.read_attribute('Position').value
        _log += 'Lens y        =\t%e\n' % self.tLensY.read_attribute('Position').value
        _log += 'Camera rot    =\t%e\n' % self.tCamRot.read_attribute('Position').value
        if self.SM != None:
            try:
                _log += 'SmarAct Ch. 0 =\t%e\n' % self.SM[0].read_attribute('Position').value
                _log += 'SmarAct Ch. 1 =\t%e\n' % self.SM[1].read_attribute('Position').value
                _log += 'SmarAct Ch. 3 =\t%e\n' % self.SM[2].read_attribute('Position').value
                _log += 'SmarAct Ch. 4 =\t%e\n' % self.SM[3].read_attribute('Position').value
            except:
                _log += 'SmarAct communication error'
            
        with open(fname + '.log', 'w') as f:
            f.write(_log)
        return None
    #clickButtonSaveImage
    
    def clickButtonSetUpdateDelay(self):
        try: 
            _txt = self.io_updatedelay.text()
            _val = float(_txt)
            self.updatedelay = _val
            self.PollingThread.stop()
            self.PollingThread.restart(self.updatedelay)
            self.label_currentupdatedelay.setText(_txt + ' ms')
            
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Could not set a new update delay time.', buttons=QtGui.QMessageBox.Ok)
        return None
        #end clickButtonSetUpdateDelay
        
    def clickButtonContinuousUpdate(self):
        if self.continuousupdate == False:
            self.PollingThread.restart(self.updatedelay)
            self.continuousupdate = True
            self.but_ContinuousUpdate.setText('Stop continuous update')
        elif self.continuousupdate:
            self.PollingThread.stop()
            self.continuousupdate = False
            self.but_ContinuousUpdate.setText('Get image data (continuous update)')
            
        return None
    #end clickButtonContinuousUpdate

    def NewUpdate(self):
        self.label_currentimagexsize.setText('%i' % self.imagesize[0])
        self.label_currentimageysize.setText('%i' % self.imagesize[1])
        self.CameraReadSettings()
        if self.hist_autorange:
            self.HistWidget.autoHistogramRange()
            self.imageView.setImage(self.image[self.visroi_x1:self.visroi_x2, self.visroi_y1:self.visroi_y2])
        elif self.hist_autorange == False:
            self.HistWidget.setHistogramRange(self.histmin, self.histmax)
            self.imageView.setImage(self.image[self.visroi_x1:self.visroi_x2, self.visroi_y1:self.visroi_y2], \
                                    levels=(self.histmin, self.histmax), autoHistogramRange=False)
        self.label_timeedit.setTime(QtCore.QTime.currentTime())
        return None
    # end NewUpdate
    
    def CameraReadSettings(self):
        try:
            self.CAM_Binning = self.tEHD.read_attribute('VBin').value
            tmp_x1 = self.tEHD.read_attribute('Roi_ul_x').value / self.CAM_Binning
            tmp_x2 = self.tEHD.read_attribute('Roi_lr_x').value + tmp_x1
            tmp_y1 = self.tEHD.read_attribute('Roi_ul_y').value / self.CAM_Binning
            tmp_y2 = self.tEHD.read_attribute('Roi_lr_y').value + tmp_y1
        except:
            QtGui.QMessageBox.warning(self, 'Warning', 'Error reading ROI from camera.!', buttons=QtGui.QMessageBox.Ok)
            return None
        tmp_x = self.CAM_PosX_FromPix(tmp_x1, tmp_x2, self.CAM_NumPixX / self.CAM_Binning, tmp_y1, tmp_y2, self.CAM_NumPixY / self.CAM_Binning)
        tmp_y = self.CAM_PosY_FromPix(tmp_x1, tmp_x2, self.CAM_NumPixX / self.CAM_Binning, tmp_y1, tmp_y2, self.CAM_NumPixY / self.CAM_Binning)
        self.CAM_xlow = min(tmp_x)
        self.CAM_xhigh = max(tmp_x)
        self.CAM_ylow = min(tmp_y)
        self.CAM_yhigh = max(tmp_y)
        if not self.bool_ZoomActive:
            self.Image_xlow = 0
            self.Image_xhigh = self.CAM_xhigh - self.CAM_xlow
            self.Image_ylow = 0
            self.Image_yhigh = self.CAM_yhigh - self.CAM_ylow
        self.label_cameraroixlow.setText('%i' % self.CAM_xlow)            
        self.label_cameraroixhigh.setText('%i' % self.CAM_xhigh)
        self.label_cameraroiylow.setText('%i' % self.CAM_ylow)            
        self.label_cameraroiyhigh.setText('%i' % self.CAM_yhigh)
        self.label_currentbinning.setText('%i' % self.CAM_Binning)
        return None

    def RecievedNewImage(self, image):
        self.image = image
        self.NewUpdate()
        return None
    #end RecievedNewImage
        
    def closeEvent(self, event):
        """Safety check for closing of window."""
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        return None   


class  EHDpolling(QtCore.QThread):
    def __init__(self, parentThread=None, camera = None):
        QtCore.QThread.__init__(self, parentThread)
        self.Image = None
        self.updater = QtCore.QTimer()
        self.tEHD= camera
        QtCore.QObject.connect(self.updater, QtCore.SIGNAL("timeout()"), self.updateImage)
        return None
    
    def restart(self, interval):
        self.updater.setInterval(interval)
        self.updater.start()
    
    def stop(self):
        self.updater.stop()
        return None
    
    def __del__(self):
        self.exiting = True
        self.wait()
        
    def updateImage(self):
        self.Image = self.tEHD.read_attribute('Image').value
        self.emit(QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), self.Image)
        return None



def EHD_Gui(parent=None, devices=None, groups=None, name='EHD image'):
    app = QtGui.QApplication(sys.argv)
    gui = cEHD_Gui(name=name)
    gui.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = EHD_Gui()
    gui.show()
    sys.exit(app.exec_())
