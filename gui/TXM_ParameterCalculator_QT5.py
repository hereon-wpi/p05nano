import numpy
from PyQt5 import QtCore, QtGui, uic as QtUic, QtWidgets
import sys
import os
import pylab
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import zipfile

colors = ['#FFA500', '#1F45FC', '#4CC417', '#C11B17', '#4B0082', '#565051', '#43C6DB', '#43BFC7']
pylab.rcParams['font.size'] = 15


def GetPath(_file):
    """Function to get the path of the p05.gui module."""
    #t0 = time.time()
    for masterdir in sys.path:
        for dirname in os.walk(masterdir):
            #print dirname[0], os.path.join(dirname[0], _file)
            try:
                possible = os.path.join(dirname[0], _file)
                if os.path.isfile(possible):
                    #print time.time()- t0
                    return possible
            except:
                pass
    return None


def StringFill(_string, _len, fill_front = False, fill_spaces = False):
    """Function to fill the string _string up to length _len
    with dots. If len(_string) > _len, the string is cropped.
    **kwargs: fill_front = True to fill in front of the input string.
    (Preset fill_front = False)
    Examples:
    StringFill('test 123', 12) = 'test 123 ...'
    StringFill('test 123', 12, fill_front = True) = '... test 123'
    """
    tmp = len(_string)
    if tmp < _len:
        if fill_spaces == False:
            if fill_front == True:
                return (_len-tmp-1)*'.'+' '+_string
            else:
                return _string+' '+(_len-tmp-1)*'.'
        else:
            if fill_front == True:
                return (_len-tmp)*' '+_string
            else:
                return _string+(_len-tmp)*' '
    else:
        return _string[:_len]
#end Stringfill


class cTXMCalculator(QtWidgets.QWidget.QMainWindow):
    def __init__(self, parent, name='TXM parameter calculator', path=None, screensize = [1920, 1200]):
        super(cTXMCalculator, self).__init__()
        if path == None:
            try:
                if sys.platform == 'win32' or sys.platform == 'win64':
                    QtUic.loadUi('u:/_Programming_code/Python/I13/gui/TXM_ParameterCalculator.ui', self)
                    self.setWindowIcon(QtGui.QIcon('u:/_Programming_code/Python/I13/gui/txm.png'))
                else:
                    QtUic.loadUi('/dls_sw/i13/scripts/Malte/I13/gui/TXM_ParameterCalculator.ui', self)
                    self.setWindowIcon(QtGui.QIcon('/dls_sw/i13/scripts/Malte/I13/gui/period.png'))
            except:
                _path = GetPath('TXM_ParameterCalculator.ui')
                QtUic.loadUi(_path, self)
                self.setWindowIcon(QtGui.QIcon(os.path.split(_path)[0] + os.sep + 'txm.png'))
        else:        
            try:
                QtUic.loadUi(path + '/gui/TXM_ParameterCalculator.ui', self)
                self.setWindowIcon(QtGui.QIcon(path + '/gui/txm.png'))
            except:
                _path = GetPath('TXM_ParameterCalculator.ui')
                QtUic.loadUi(_path, self)
                self.setWindowIcon(QtGui.QIcon(os.path.split(_path)[0] + os.sep + 'txm.png'))
        
        self.setWindowTitle(name)
        self.widgetX = 1790
        self.widgetY = 1080
        self.setGeometry(10, 30, self.widgetX, self.widgetY)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.widgetX, self.widgetY)
        self.main = parent
        self.zip_basedir = None
        self.zip_filename = None
        
        self.colors = ['#FFA500', '#1F45FC', '#4CC417', '#C11B17', '#4B0082', '#565051', '#43C6DB', '#43BFC7']
        self.figure1 = pylab.figure(1, figsize=(11, 8), dpi=80)
        self.figure1Canvas = FigureCanvas(self.figure1)
        self.figure1Canvas.setParent(self)
        self.figure1Canvas.setGeometry(480, 200, self.widgetX - 480 - 10, self.widgetY - 200 - 10)
        self.f1ax1 = self.figure1.add_axes([0.085, 0.1, 0.84, 0.87])
        self.f1ax2 = self.f1ax1.twinx()
        self.plot1Type = 'linear'
        self.plot2Type = 'linear'
        self.plot1ylow = 0
        self.plot1yhigh = 1
        self.plot2ylow = 0
        self.plot2yhigh = 1
        self.plot1var = None
        self.plot2var = None
        self.plot1Autoscale = True
        self.plot2Autoscale = True
        self.ax1plotContent = False
        self.ax2plotContent = False
        self.f2plotContent = False
        self.activeVar = None
        self.figureExists = False
        self.ignoreUpdate = False
        
        self.figure2 = pylab.figure(2, figsize=(6, 4), dpi=80)
        self.figure2Canvas = FigureCanvas(self.figure2)
        self.figure2Canvas.setParent(self)
        self.figure2Canvas.setGeometry(920, 10, self.widgetX - 920 - 10, 200 - 10)
        self.figure2ax = self.figure2.add_axes([0.085, 0.34, 0.84, 0.6])
        
        self.figure3 = pylab.figure(3, figsize=(12, 10))
        self.f3ax = self.figure3.add_axes([0.1, 0.15, 0.84, 0.8])
        self.f3content = False
        self.f3ax.cla()
        
        # parameters 1 (beamline and FZP)
        self.energy = numpy.asarray(12)
        self.bandwidth = numpy.asarray(1e-3) 
        self.FZP_dr = numpy.asarray(50e-9)
        self.FZP_D = numpy.asarray(150e-6)

        self.but_SetEnergy.clicked.connect(self.clickButtonSetEnergy)
        self.but_SetBandwidth.clicked.connect(self.clickButtonSetBandwidth)
        self.but_SetFZP_dr.clicked.connect(self.clickButtonSetFZP_dr)
        self.but_SetFZP_D.clicked.connect(self.clickButtonSetFZP_D)

        self.edit_energy.returnPressed.connect(self.clickButtonSetEnergy)
        self.edit_bandwidth.returnPressed.connect(self.clickButtonSetBandwidth)
        self.edit_FZP_dr.returnPressed.connect(self.clickButtonSetFZP_dr)
        self.edit_FZP_D.returnPressed.connect(self.clickButtonSetFZP_D)
        
        # parameters 2 (detector)
        self.M_det = numpy.asarray(1)
        self.det_PixSize = numpy.asarray(6.5e-6)
        self.det_Nhor = numpy.asarray(2048)
        self.det_Nvert = numpy.asarray(2048)
        self.det_useEffPix = False
        self.det_eff_pix = numpy.asarray(50e-9)
        self.dist_sample_det = numpy.asarray(8.3)
        
        self.but_SetM_det.clicked.connect(self.clickButtonSetM_det)
        self.but_SetPixSize.clicked.connect(self.clickButtonSetDet_PixSize)
        self.but_SetDet_Nhor.clicked.connect(self.clickButtonSetDet_Nhor)
        self.but_SetDet_Nvert.clicked.connect(self.clickButtonSetDet_Nvert)
        self.comboBox_ParametersDet.currentIndexChanged.connect(self.selectParametersDet)
        self.but_SetDistSampleDet.clicked.connect(self.clickButtonSetDistSampleDet)
        self.but_SetEffPix.clicked.connect(self.clickButtonSetResolution)

        self.edit_M_det.returnPressed.connect(self.clickButtonSetM_det)
        self.edit_det_PixSize.returnPressed.connect(self.clickButtonSetDet_PixSize)
        self.edit_det_Nhor.returnPressed.connect(self.clickButtonSetDet_Nhor)
        self.edit_det_Nvert.returnPressed.connect(self.clickButtonSetDet_Nvert)
        self.edit_dist_sample_det.returnPressed.connect(self.clickButtonSetDistSampleDet)
        self.edit_eff_pix.returnPressed.connect(self.clickButtonSetResolution)
        
        # parameters 3 (beamshaper)
        self.BSC_D = numpy.asarray(2.9e-3)
        self.BSC_CS = numpy.asarray(1.5e-3)
        self.BSC_dr = numpy.asarray(50e-9)
        self.BSC_field = numpy.asarray(60e-6)

        self.BSC_useFullDet = False
        self.but_SetBSC_D.clicked.connect(self.clickButtonSetBSC_D)
        self.comboBox_ParametersCS.currentIndexChanged.connect(self.selectParametersCS)
        self.but_SetBSC_CS.clicked.connect(self.clickButtonSetBSC_CS)
        self.but_SetBSC_field.clicked.connect(self.clickButtonSetBSC_field)
        
        self.edit_BSC_D.returnPressed.connect(self.clickButtonSetBSC_D)
        self.edit_BSC_CS.returnPressed.connect(self.clickButtonSetBSC_CS)
        self.edit_BSC_field.returnPressed.connect(self.clickButtonSetBSC_field)
        
        self.but_SaveData.clicked.connect(self.writeData)
        self._updateParameters1()
#        self._updateParameters2()
        
        # plotting parameters:
        self.edit_plot1Low.valueChanged.connect(self.changePlot1LimitLow)
        self.edit_plot1High.valueChanged.connect(self.changePlot1LimitHigh)
        self.edit_plot2Low.valueChanged.connect(self.changePlot2LimitLow)
        self.edit_plot2High.valueChanged.connect(self.changePlot2LimitHigh)  
        self.comboBox_plot1.currentIndexChanged.connect(self.changePlot1Type)
        self.comboBox_plot1_autoscale.currentIndexChanged.connect(self.changePlot1Autoscale)
        self.comboBox_plot1_variable.currentIndexChanged.connect(self.changePlot1Variable)
        self.comboBox_plot2_variable.currentIndexChanged.connect(self.changePlot2Variable)
        self.comboBox_plot2.currentIndexChanged.connect(self.changePlot2Type)
        self.comboBox_plot2_autoscale.currentIndexChanged.connect(self.changePlot2Autoscale)
              
        self._initialize()
        return None
    # end __init__
    
    def _initialize(self):
        self.button_style = """QPushButton{border: solid; border-bottom-color: #777777; border-bottom-width: 2px; border-right-color:#777777;\
                       border-right-width: 2px; border-top-color:#AAAAAA; border-top-width: 1px; border-left-color:#AAAAAA;\
                       border-left-width: 1px; border-radius: 3px; padding: 1px;  background: qlineargradient(x1: 0, y1: \
                       0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}\
                       QPushButton:pressed{background:qlineargradient(x1: 0, y1: \
                       0, x2: 0, y2: 1, stop: 0 #dadada, stop: 0.4 #d4d4d4, stop: 0.5 #c7c7c7, stop: 1.0 #dadada) }"""
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

        for item in [self.label_21, self.edit_dist_sample_det, self.but_SetDistSampleDet, self.label_54, self.label_104]:
            item.setVisible(False)
        for item in [self.label_20, self.edit_eff_pix, self.but_SetEffPix, self.label_53, self.label_103]:
            item.setVisible(True)
        for item in [self.edit_BSC_CS, self.but_SetBSC_CS]:
            item.setVisible(False)

        self.DictPlotTitle = {'energy': 'Energy [keV]', 'bandwidth':'Bandwidth', 'FZP_dr':'FZP outer zone width [nm]', \
                              'FZP_D':'FZP diameter [um]', 'M_det':'Detector magnification', 'det_PixSize':'Detector pixel size [um]', \
                              'det_Nhor':'Detector number of pixels (hor.)', 'det_Nvert':'Detector number of pixels (vert.)', \
                              'det_eff_pix':'Detector effective pixel size [nm]', 'dist_sample_det':'Distance sample-detector [m]', \
                              'BSC_D': 'BSC diameter [mm]', 'BSC_CS':'BSC central stop diameter [mm]'}


        self.DictPlotVariables = {'None': None, 'X-ray wavelength': 'wavelength', 'FZP resolution':'FZP_resolution', \
                                  'FZP object numerical aperture (NA)': 'FZP_objectNA', 'FZP depth of focus':'FZP_DOF', 'FZP number of zones':'FZP_Nzones', \
                                  'Detector effective pixel size':'det_eff_pix', 'Distance sample-detector':'dist_sample_det', \
                                  'Distance sample-FZP':'dist_sample_FZP', 'Effective pixel size':'det_eff_pix', \
                                  'Geometric FOV (horizontal)': 'det_FOVhor', 'Geometric FOV (vertical)':'det_FOVvert', 'X-ray magnification':'M_xray', \
                                  'Total magnification': 'M_total', 'BSC central stop size':'BSC_CS', 'BSC focal length': 'BSC_f', \
                                  'BSC number of zones':'BSC_Nzones', 'BSC effective FOV':'BSC_effFOV', 'BSC free area': 'BSC_freeArea', \
                                  'Distance BSC-sample':'dist_BSC_sample', 'FZP theoretical FOV': 'FZP_FOV'}
     
        self.DictPlotLabels = {'wavelength':'X-ray wavelength [A]', 'FZP_resolution':'FZP resolution [nm]', \
                                  'FZP_objectNA': 'FZP object numerical aperture (NA)', 'FZP_DOF':'FZP depth of focus [um]', 'FZP_Nzones':'FZP number of zones', \
                                  'det_eff_pix':'Detector effective pixel size [nm]', 'dist_sample_det':'Distance sample-detector [m]', \
                                  'dist_sample_FZP':'Distance sample-FZP [mm]', 'dist_BSC_sample':'Distance BSC-sample [m]', \
                                  'det_FOVhor':'Geometric FOV (horizontal) [um]', 'det_FOVvert':'Geometric FOV (vertical) [um]', 'M_xray':'X-ray magnification', \
                                  'M_total':'Total magnification', 'BSC_CS':'Central stop size [mm]', 'BSC_f':'BSC focal length [m]', \
                                  'BSC_Nzones':'BSC number of zones', 'BSC_effFOV':'BSC effective FOV [um]', 'BSC_freeArea':'BSC free area [%]', \
                                  'FZP_FOV':'FZP theoretical FOV'}

        self.DictPlotFactors = {'wavelength':1e10, 'FZP_resolution':1e9, 'FZP_objectNA': 1, 'FZP_DOF':1e6, 'FZP_Nzones':1, \
                                  'det_eff_pix':1e9, 'dist_sample_det':1, 'dist_sample_FZP':1e3, \
                                  'det_FOVhor':1e6, 'det_FOVvert':1e6, 'M_xray':1, 'M_total':1, 'BSC_CS':1e3, 'BSC_f':1, \
                                  'BSC_Nzones':1, 'BSC_effFOV':1e6, 'BSC_freeArea':100, 'energy': 1, 'bandwidth':1, \
                                  'FZP_dr':1e9, 'FZP_D':1e6, 'M_det':1, 'det_PixSize': 1e6, 'det_Nhor':1, 'det_Nvert': 1, \
                                  'BSC_D':1e3, 'BSC_CS': 1e3, 'dist_BSC_sample': 1, 'FZP_FOV':1e6}
    
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

        tmp = str(self.comboBox_ParametersDet.currentText())
        if tmp == 'Set detector effective pixel size':
            self.det_useEffPix = True
            for item in [self.label_21, self.edit_dist_sample_det, self.but_SetDistSampleDet, self.label_54, self.label_104]:
                item.setVisible(False)
            for item in [self.label_20, self.edit_eff_pix, self.but_SetEffPix, self.label_53, self.label_103]:
                item.setVisible(True)
            self.edit_eff_pix.setText(str(self.det_eff_pix * 1e9))
        if tmp == 'Set target distance sample-det':
            self.det_useEffPix = False
            for item in [self.label_21, self.edit_dist_sample_det, self.but_SetDistSampleDet, self.label_54, self.label_104]:
                item.setVisible(True)
            for item in [self.label_20, self.edit_eff_pix, self.but_SetEffPix, self.label_53, self.label_103]:
                item.setVisible(False)
                self.edit_dist_sample_det.setText(str(self.dist_sample_det))

        tmp = str(self.comboBox_ParametersCS.currentText())
        if tmp == 'Use full detector FOV':
            self.BSC_useFullDet = True
            for item in [self.edit_BSC_CS, self.but_SetBSC_CS]:
                item.setVisible(False)
            self.label_200.setVisible(True)
        if tmp == 'Select central stop size':
            self.BSC_useFullDet = False
            for item in [self.edit_BSC_CS, self.but_SetBSC_CS]:
                item.setVisible(True)
            self.label_200.setVisible(False)
            
        self.RefreshPlot()
        self.show()
        return None
    # end _initialize
            
    def _updateParameters1(self):
        self.wavelength = numpy.asarray(12.398 / self.energy * 1e-10)
        self.FZP_resolution = numpy.asarray(1.22 * self.FZP_dr)
        self.FZP_objectNA = numpy.asarray(self.wavelength / (2 * self.FZP_dr))
        self.FZP_DOF = numpy.asarray(2 * self.FZP_dr ** 2 / self.wavelength)
        self.FZP_Nzones = numpy.asarray(self.FZP_D / (4 * self.FZP_dr))
        self.FZP_f = numpy.asarray(self.FZP_D * self.FZP_dr / self.wavelength)
       
        self.label_1.setText(str(self.wavelength * 1e10))
        self.label_2.setText(str(self.FZP_resolution * 1e9))
        self.label_3.setText(str(self.FZP_objectNA))
        self.label_4.setText(str(self.FZP_DOF * 1e6))
        self.label_5.setText(str(self.FZP_Nzones))
        self.label_6.setText(str(self.FZP_f * 1e3))
        self._updateParameters2()
        return None
    # end _updateParameters1

    def _updateParameters2(self):
        if self.det_useEffPix:
            self.M_total = numpy.asarray(self.det_PixSize / self.det_eff_pix)
            self.M_xray = numpy.asarray(self.M_total / self.M_det)
            self.dist_sample_FZP = numpy.asarray(self.FZP_f * (1.0 + self.M_xray) / self.M_xray)
            self.dist_FZP_det = numpy.asarray(self.FZP_f * (1.0 + self.M_xray))
            self.dist_sample_det = numpy.asarray(self.dist_FZP_det + self.dist_sample_FZP)
        else:  # i.e. use distance sample-det
            self.dist_sample_FZP = numpy.asarray(self.dist_sample_det / 2 - (self.dist_sample_det ** 2 / 4 - self.dist_sample_det * self.FZP_f) ** 0.5)
            self.dist_FZP_det = numpy.asarray(self.dist_sample_det - self.dist_sample_FZP)
            self.M_xray = numpy.asarray(self.dist_FZP_det / self.dist_sample_FZP)
            self.M_total = numpy.asarray(self.M_xray * self.M_det)
            self.det_eff_pix = numpy.asarray(self.det_PixSize / self.M_total)

        self.det_FOVhor = numpy.asarray(self.det_eff_pix * self.det_Nhor)
        self.det_FOVvert = numpy.asarray(self.det_eff_pix * self.det_Nvert)
        self.FZP_imageNA = self.FZP_D / 2 / self.dist_FZP_det
        self.FZP_angularFOV = 2 * (self.wavelength / (5 * self.FZP_imageNA ** 2) * 1 / (self.dist_FZP_det + self.M_xray ** 2 * self.dist_sample_FZP) + 1) ** 2 - 2
        self.FZP_FOV = self.FZP_angularFOV * 2 * self.dist_sample_FZP

        self.label_101.setText(str(self.det_FOVhor * 1e6))
        self.label_102.setText(str(self.det_FOVvert * 1e6))
        self.label_103.setText(str(self.dist_sample_det))
        self.label_104.setText(str(self.det_eff_pix * 1e9))
        self.label_105.setText(str(self.M_xray))
        self.label_106.setText(str(self.M_total))
        self.label_107.setText(str(self.dist_sample_FZP * 1e3))
        self.label_108.setText(str(self.FZP_angularFOV * 1e3))
        self.label_109.setText(str(self.FZP_FOV * 1e6))
        self._updateParameters3()
        return None
    # end _updateParameters2

    def _updateParameters3(self):
        self.BSC_f = numpy.asarray(self.BSC_D * self.FZP_dr / self.wavelength)
        self.dist_BSC_sample = numpy.asarray(240. / 2 - (240. ** 2 / 4 - 240. * self.BSC_f) ** 0.5)
        self.dist_source_BSC = numpy.asarray(240. - self.dist_BSC_sample)
        self.BSC_Nzones = self.BSC_D / (4 * self.BSC_dr)
        if self.BSC_useFullDet:
            self.BSC_CShor = numpy.asarray(self.det_PixSize * self.det_Nhor * self.dist_BSC_sample / self.dist_sample_det / self.M_det)
            self.BSC_CSvert = numpy.asarray(self.det_PixSize * self.det_Nvert * self.dist_BSC_sample / self.dist_sample_det / self.M_det)
            self.BSC_CS = numpy.where(self.BSC_CShor >= self.BSC_CSvert, self.BSC_CShor, self.BSC_CSvert)
        self.BSC_effFOV = self.BSC_CS / self.dist_BSC_sample * self.dist_sample_det / self.M_xray
        self.tmpval = 1 - self.BSC_CS ** 2 / (numpy.pi * (self.BSC_D / 2) ** 2)
        self.BSC_freeArea = numpy.where(self.tmpval > 0, self.tmpval, 0)
        
         
        if min(self.det_FOVhor, self.BSC_effFOV) <= self.BSC_field:
            tmp_fov_hor = min(self.det_FOVhor, self.BSC_effFOV) 
            eff_hor =  tmp_fov_hor / self.BSC_field
        else:
            tmp_fov_hor = self.BSC_field
            eff_hor = 1 
        
        if min(self.det_FOVvert, self.BSC_effFOV) <= self.BSC_field:
            tmp_fov_vert = min(self.det_FOVvert, self.BSC_effFOV) 
            eff_vert =  tmp_fov_vert / self.BSC_field
        else:
            tmp_fov_vert = self.BSC_field
            eff_vert = 1 
        
        self.total_eff =  eff_hor * eff_vert * self.BSC_freeArea
        self.label_200.setText(str(self.BSC_CS * 1e3))
        self.label_201.setText(str(self.BSC_f))
        self.label_203.setText(str(self.BSC_effFOV * 1e6))
        self.label_204.setText(str(self.BSC_freeArea * 100))
        self.label_205.setText(str(self.dist_BSC_sample))

        self.label_202.setText('%.1f' %(self.total_eff*100))
        self.label_206.setText('%.1f um %s %i px' %(tmp_fov_hor*1e6, u"\u2259".encode('utf-8'), tmp_fov_hor/self.det_eff_pix))
        self.label_207.setText('%.1f um %s %i px' %(tmp_fov_vert*1e6, u"\u2259".encode('utf-8'), tmp_fov_vert/self.det_eff_pix))
        
        self.check_NFZP = numpy.where((self.FZP_Nzones > 100), True, False) * numpy.where((self.FZP_Nzones < 1 / self.bandwidth), True, False)
        self.check_DOF = numpy.where(self.FZP_DOF >= self.BSC_effFOV, True, False)
        self.check_NBSC = numpy.where(self.BSC_Nzones < 1 / self.bandwidth, True, False)
        self.RefreshPlot()
        return None
    # end _updateParameters3

    def selectParametersDet(self):
        tmp = str(self.comboBox_ParametersDet.currentText())
        if tmp == 'Set detector effective pixel size':
            self.det_useEffPix = True
            for item in [self.label_21, self.edit_dist_sample_det, self.but_SetDistSampleDet, self.label_54, self.label_104]:
                item.setVisible(False)
            for item in [self.label_20, self.edit_eff_pix, self.but_SetEffPix, self.label_53, self.label_103]:
                item.setVisible(True)
            self.edit_eff_pix.setText(str(self.det_eff_pix * 1e9))
        if tmp == 'Set target distance sample-det':
            self.det_useEffPix = False
            for item in [self.label_21, self.edit_dist_sample_det, self.but_SetDistSampleDet, self.label_54, self.label_104]:
                item.setVisible(True)
            for item in [self.label_20, self.edit_eff_pix, self.but_SetEffPix, self.label_53, self.label_103]:
                item.setVisible(False)
                self.edit_dist_sample_det.setText(str(self.dist_sample_det))
        self._updateParameters2()
        return None
    # end selectParametersDet

    def selectParametersCS(self):
        tmp = str(self.comboBox_ParametersCS.currentText())
        if tmp == 'Use full detector FOV':
            self.BSC_useFullDet = True
            for item in [self.edit_BSC_CS, self.but_SetBSC_CS]:
                item.setVisible(False)
            self.label_200.setVisible(True)
        if tmp == 'Select central stop size':
            self.BSC_useFullDet = False
            for item in [self.edit_BSC_CS, self.but_SetBSC_CS]:
                item.setVisible(True)
            self.label_200.setVisible(False)
        self._updateParameters2()
        return None
    # end selectParametersDet

    def clickButtonSetEnergy(self):
        try:
            self.tmpval = self.energy.copy()
            self.energy = numpy.asarray(eval(str(self.edit_energy.text())))
        except Exception as e:
            self.energy = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse energy value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_energy.setText(str(self.energy))
            return None
        if self.energy.size > 1:     self.activeVar = 'energy'
        self._updateParameters1()
        return None
    # end clickButtonSetEnergy
    
    def clickButtonSetBandwidth(self):
        try:
            self.tmpval = self.bandwidth.copy()
            self.bandwidth = numpy.asarray(eval(str(self.edit_bandwidth.text())))
        except Exception as e:
            self.bandwidth = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse bandwidth value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_bandwidth.setText(str(self.bandwidth))
            return None
        if self.bandwidth.size > 1:     self.activeVar = 'bandwidth'
        self._updateParameters1()
        return None
    # end clickButtonSetBandwidth
    
    def clickButtonSetFZP_dr(self):
        try:
            self.tmpval = self.FZP_dr.copy()
            self.FZP_dr = numpy.asarray(eval(str(self.edit_FZP_dr.text())) * 1e-9)
        except Exception as e:
            self.FZP_dr = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse FZP_dr value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_FZP_dr.setText(str(self.FZP_dr))
            return None
        if self.FZP_dr.size > 1:     self.activeVar = 'FZP_dr'
        self.BSC_dr = self.FZP_dr
        self._updateParameters1()
        return None
    # end clickButtonSetFZP_dr

    def clickButtonSetFZP_D(self):
        try:
            self.tmpval = self.FZP_D.copy()
            self.FZP_D = numpy.asarray(eval(str(self.edit_FZP_D.text())) * 1e-6)
        except Exception as e:
            self.FZP_D = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse FZP_D value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_FZP_D.setText(str(self.FZP_D))
            return None
        if self.FZP_D.size > 1:     self.activeVar = 'FZP_D'
        self._updateParameters1()
        return None
    # end clickButtonSetFZP_D

    def clickButtonSetM_det(self):
        try:
            self.tmpval = self.M_det.copy()
            self.M_det = numpy.asarray(eval(str(self.edit_M_det.text())))
        except Exception as e:
            self.M_det = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse detector magnification value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_M_det.setText(str(self.M_det))
            return None
        if self.M_det.size > 1:     self.activeVar = 'M_det'
        self._updateParameters2()
        return None
    # end clickButtonSetM_det
    
    def clickButtonSetDet_PixSize(self):
        try:
            self.tmpval = self.det_PixSize.copy()
            self.det_PixSize = numpy.asarray(eval(str(self.edit_det_PixSize.text())) * 1e-6)
        except Exception as e:
            self.det_PixSize = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse detector pixel size value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_det_PixSize.setText(str(self.det_PixSize))
            return None
        if self.det_PixSize.size > 1:     self.activeVar = 'det_PixSize'
        self._updateParameters2()
        return None
    # end clickButtonSetdet_PixSize
        
    def clickButtonSetDet_Nhor(self):
        try:
            self.tmpval = self.det_Nhor.copy()
            self.det_Nhor = numpy.asarray(eval(str(self.edit_det_Nhor.text())))
        except Exception as e:
            self.det_Nhor = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse number of pixels (hor.) value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_det_Nhor.setText(str(self.det_Nhor))
            return None
        if self.det_Nhor.size > 1:     self.activeVar = 'det_Nhor'
        self._updateParameters2()
        return None
    # end clickButtonSetdet_Nhor
        
    def clickButtonSetDet_Nvert(self):
        try:
            self.tmpval = self.det_Nvert.copy()
            self.det_Nvert = numpy.asarray(eval(str(self.edit_det_Nvert.text())))
        except Exception as e:
            self.det_Nvert = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse number of pixels (vert.) value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_det_Nvert.setText(str(self.det_Nvert))
            return None
        if self.det_Nvert.size > 1:     self.activeVar = 'det_Nvert'
        self._updateParameters2()
        return None
    # end clickButtonSetdet_Nvert
    
    def clickButtonSetDistSampleDet(self):
        try:
            self.tmpval = self.dist_sample_det.copy()
            self.dist_sample_det = numpy.asarray(eval(str(self.edit_dist_sample_det.text())), dtype=numpy.float32)
        except Exception as e:
            self.dist_sample_det = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse distance sample-detector value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_dist_sample_det.setText(str(self.dist_sample_det))
            return None
        if self.dist_sample_det.size > 1:     self.activeVar = 'dist_sample_det'
        self._updateParameters2()
        return None
    # end clickButtonSetDistSampleDet
    
    def clickButtonSetResolution(self):
        try:
            self.tmpval = self.det_eff_pix.copy()
            self.det_eff_pix = numpy.asarray(eval(str(self.edit_eff_pix.text())) * 1e-9)
        except Exception as e:
            self.det_eff_pix = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse object resolution value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_eff_pix.setText(str(self.det_eff_pix))
            return None
        if self.det_eff_pix.size > 1:     self.activeVar = 'object_resolution'
        self._updateParameters2()
        return None
    # end clickButtonSetResolution

    def clickButtonSetBSC_D(self):
        try:
            self.tmpval = self.BSC_D.copy()
            self.BSC_D = numpy.asarray(eval(str(self.edit_BSC_D.text())) * 1e-3)
        except Exception as e:
            self.BSC_D = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parseBSC diameter value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_BSC_D.setText(str(self.BSC_D))
            return None
        if self.BSC_D.size > 1:     self.activeVar = 'BSC_D'
        self._updateParameters3()
        return None
    # end clickButtonSetBSC_D    

    def clickButtonSetBSC_field(self):
        try:
            self.tmpval = self.BSC_field.copy()
            self.BSC_field = numpy.asarray(eval(str(self.edit_BSC_field.text())) * 1e-6)
        except Exception as e:
            self.BSC_field = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse BSC field size value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_BSC_field.setText(str(self.BSC_field))
            return None
        self.activeVar = 'BSC_field'
        self._updateParameters3()
        return None
    # end clickButtonSetBSC_field  
    
    def clickButtonSetBSC_CS(self):
        try:
            self.tmpval = self.BSC_CS.copy()
            self.BSC_CS = numpy.asarray(eval(str(self.edit_BSC_CS.text())) * 1e-3)
        except Exception as e:
            self.BSC_CS = self.tmpval
            QtWidgets.QWidget.QMessageBox.critical(self, 'Error', 'Could not parse BSC central stop value or multiple input parameter arrays selected\n%s.' % e, buttons=QtWidgets.QWidget.QMessageBox.Ok)
            self.edit_BSC_CS.setText(str(self.BSC_CS))
            return None
        if self.BSC_CS.size > 1:     self.activeVar = 'BSC_CS'
        self._updateParameters3()
        return None
    # end clickButtonSetBSC_CS    
    
    def changePlot1Type(self):
        self.plot1Type = str(self.comboBox_plot1.currentText()) 
        self.RefreshPlot()
        return None
    # end changePlot1Type

    def changePlot2Type(self):
        self.plot2Type = str(self.comboBox_plot2.currentText()) 
        self.RefreshPlot()
        return None
    # end changePlot2Type

    def changePlot1Autoscale(self):
        self.plot1Autoscale = eval(str(self.comboBox_plot1_autoscale.currentText())) 
        self.RefreshPlot()
        return None
    # end changePlot1Autoscale

    def changePlot2Autoscale(self):
        self.plot2Autoscale = eval(str(self.comboBox_plot2_autoscale.currentText())) 
        self.RefreshPlot()
        return None
    # end changePlot2Autoscale

    def changePlot1LimitLow(self):
        self.plot1ylow = self.edit_plot1Low.value()
        if self.plot1ylow >= self.plot1yhigh:
            self.plot1ylow = self.plot1yhigh - 1
        if not self.ignoreUpdate:
            self.RefreshPlot()
        return None
    # end changePlot1LimitLow

    def changePlot1LimitHigh(self):
        self.plot1yhigh = self.edit_plot1High.value()
        if self.plot1ylow >= self.plot1yhigh:
            self.plot1yhigh = self.plot1ylow + 1
        if not self.ignoreUpdate:
            self.RefreshPlot()
        return None
    # end changePlot1LimitHigh

    def changePlot2LimitLow(self):
        self.plot2ylow = self.edit_plot2Low.value()
        if self.plot2ylow >= self.plot2yhigh:
            self.plot2ylow = self.plot2yhigh - 1
        if not self.ignoreUpdate:
            self.RefreshPlot()
        return None
    # end changePlot2LimitLow
    
    def changePlot2LimitHigh(self):
        self.plot2yhigh = self.edit_plot2High.value()
        if self.plot2ylow >= self.plot2yhigh:
            self.plot2yhigh = self.plot2ylow + 1
        if not self.ignoreUpdate:
            self.RefreshPlot()
        return None
    # end changePlot2LimitHigh
        
    def changePlot1Variable(self):
        self.plot1var = self.DictPlotVariables[str(self.comboBox_plot1_variable.currentText())]
        self.RefreshPlot()
        return None
    # end changePlot1Variable
        
    def changePlot2Variable(self):
        self.plot2var = self.DictPlotVariables[str(self.comboBox_plot2_variable.currentText())]
        self.RefreshPlot()
        return None
    # end changePlot2Variable

    def RefreshPlot(self):
        if self.activeVar == None or eval('self.'+self.activeVar).size == 1:
            return None
        if self.figureExists:
            self.figure2ax.lines.pop(0)
            self.figure2ax.lines.pop(0)
            self.figure2ax.lines.pop(0)
        if self.ax1plotContent:
            self.f1ax1.lines.pop(0)
            self.ax1plotContent = False
        if self.ax2plotContent:   
            self.f1ax2.lines.pop(0)
            self.ax2plotContent = False
        if eval('self.' + self.activeVar + '.size') == 1:
            return None
        self.plotTitle = self.DictPlotTitle[self.activeVar]
        self.plotx = eval('self.' + self.activeVar) * self.DictPlotFactors[self.activeVar]
                 
        if self.plot1var != None:
            self.tmpval = eval('self.' + self.plot1var) * self.DictPlotFactors[self.plot1var]
            if self.tmpval.size == 1:
                self.tmpval = numpy.array([self.tmpval] * self.plotx.size)
            if self.plot1Type == 'logarithmic':
                self.f1ax1.set_yscale('log')
                self.f1ax1.semilogy(self.plotx, self.tmpval, color=colors[3], linewidth=1.5, markeredgewidth=0, markersize=4, marker='o')
            elif self.plot1Type == 'linear':
                self.f1ax1.set_yscale('linear')
                self.f1ax1.plot(self.plotx, self.tmpval, color=colors[3], linewidth=1.5, markeredgewidth=0, markersize=4, marker='o')
            self.f1ax1.set_ylabel(self.DictPlotLabels[self.plot1var], color=colors[3])
            self.ax1plotContent = True
            self.f1ax1.set_xlabel(self.plotTitle)
            if self.plot1Autoscale:
                ylow, yhigh = numpy.amin(self.tmpval), numpy.amax(self.tmpval)
                ylow = min(0.995 * ylow, 1.01 * ylow)
                yhigh = max(0.995 * yhigh, 1.01 * yhigh)
                self.f1ax1.set_ylim([ylow, yhigh])
                self.ignoreUpdate = True
                self.edit_plot1Low.setValue(ylow)
                self.edit_plot1High.setValue(yhigh)
                self.edit_plot1Low.setValue(ylow)
                self.edit_plot1High.setValue(yhigh)
                self.ignoreUpdate = False
                # self.f1ax1.autoscale(True)
            else:
                self.f1ax1.set_ylim([self.plot1ylow, self.plot1yhigh])
            self.f1ax1.set_xlim([self.plotx[0], self.plotx[-1]])
        
        if self.plot2var != None:
            self.tmpval = eval('self.' + self.plot2var) * self.DictPlotFactors[self.plot2var]
            if self.tmpval.size == 1:
                self.tmpval = numpy.array([self.tmpval] * self.plotx.size)
            if self.plot2Type == 'logarithmic':
                self.f1ax2.set_yscale('log')
                self.f1ax2.semilogy(self.plotx, self.tmpval, color=colors[1], linewidth=1.5, markeredgewidth=0, markersize=4, marker='o')
            elif self.plot2Type == 'linear':
                self.f1ax2.set_yscale('linear')
                self.f1ax2.plot(self.plotx, self.tmpval, color=colors[1], linewidth=1.5, markeredgewidth=0, markersize=4, marker='o')
            self.f1ax2.set_ylabel(self.DictPlotLabels[self.plot2var], color=colors[1])
            self.f1ax1.set_xlabel(self.plotTitle)
            self.ax2plotContent = True
            if self.plot2Autoscale:
                ylow, yhigh = numpy.amin(self.tmpval), numpy.amax(self.tmpval)
                ylow = min(0.99 * ylow, 1.005 * ylow)
                yhigh = max(0.99 * yhigh, 1.005 * yhigh)
                self.f1ax2.set_ylim([ylow, yhigh])
                self.ignoreUpdate = True
                self.edit_plot2Low.setValue(ylow)
                self.edit_plot2High.setValue(yhigh)
                self.edit_plot2Low.setValue(ylow)
                self.edit_plot2High.setValue(yhigh)
                self.ignoreUpdate = False
            if not self.plot2Autoscale:
                self.f1ax2.set_ylim([self.plot2ylow, self.plot2yhigh])
            self.f1ax2.set_xlim([self.plotx[0], self.plotx[-1]])
                
        if not self.plot2Autoscale:
            self.f1ax2.set_ylim([self.plot2ylow, self.plot2yhigh])

                
        if self.check_NFZP.size == 1:   self.check_NFZP = numpy.array([self.check_NFZP] * self.plotx.size)
        if self.check_DOF.size == 1:   self.check_DOF = numpy.array([self.check_DOF] * self.plotx.size)
        if self.check_NBSC.size == 1:   self.check_NBSC = numpy.array([self.check_NBSC] * self.plotx.size)
        self.figure2ax.plot(self.plotx, self.check_NFZP + 0.05, color=colors[3], linewidth=1.5, markeredgewidth=0, markersize=4, marker='o')
        self.figure2ax.plot(self.plotx, self.check_DOF, color=colors[1], linewidth=1.5, markeredgewidth=0, markersize=4, marker='o')
        self.figure2ax.plot(self.plotx, self.check_NBSC - 0.05, color=colors[2], linewidth=1.5, markeredgewidth=0, markersize=4, marker='o')
        self.figure2ax.set_ylim(-0.5, 1.8)
        self.figure2ax.set_xlim([self.plotx[0], self.plotx[-1]])
        self.figure2ax.set_yticks([0, 1])
        self.figure2ax.set_yticklabels(['warning', 'OK'])
        self.figure2ax.set_xlabel(self.plotTitle)
        if not self.figureExists:
            x0, dx = self.plotx[0], self.plotx[-1] - self.plotx[0] 
            self.figure2.text(0.15, 0.79, 'Number of FZP zones', color=colors[3])
            self.figure2.text(0.425, 0.79, 'Depth of field', color=colors[1])
            self.figure2.text(0.65, 0.79, 'Number of BSC zones', color=colors[2])
            self.figureExists = True
            
        self.figure1Canvas.draw()
        self.figure2Canvas.draw()
        return None
    # end RefreshPlot

    def writeData(self):
        if self.zip_basedir == None:
            self.zip_fname = QtWidgets.QWidget.QFileDialog.getSaveFileName(self, 'Name of logfile', '', "Zip files (*.zip)")[0]
        elif self.zip_basedir != None:
            self.zip_fname = QtWidgets.QWidget.QFileDialog.getSaveFileName(self, 'Name of logfile', self.zip_basedir, "Zip files (*.zip)")[0]
        self.zip_basedir = os.path.dirname(self.zip_fname)
        self.zip_filename = os.path.basename(self.zip_fname)
        if self.zip_fname not in ['', None]:
            try:
                with zipfile.ZipFile(self.zip_fname, 'w') as zobject:
                    self.zip_fobject = True
            except:
                self.zip_fobject = None
                QtWidgets.QWidget.QMessageBox.critical(self, 'Error', "The selected file:\n\t%s\nis write-protected and cannot be opened." % (self.zip_fname), buttons=QtWidgets.QWidget.QMessageBox.Ok)
                return None
           
            if self.activeVar == None:
                return None
            if eval('self.' + self.activeVar + '.size') != 1:
                self.plotx = eval('self.' + self.activeVar) * self.DictPlotFactors[self.activeVar]
                for item in self.DictPlotLabels.keys():
        #             if self.f3content:
        #                 self.f3ax.lines.pop(0)
                    self.plotTitle = self.DictPlotTitle[self.activeVar]
                    self.tmpval = eval('self.' + item) * self.DictPlotFactors[item]
                    if self.tmpval.size == 1:
                        self.tmpval = numpy.array([self.tmpval] * self.plotx.size)
        
                    self.f3ax.plot(self.plotx, self.tmpval, color=colors[3], linewidth=1.5, markeredgewidth=0, markersize=4, marker='o')
                    self.f3ax.set_ylabel(self.DictPlotLabels[item], color=colors[3])
                    self.f3ax.set_xlabel(self.plotTitle)
                    ylow, yhigh = numpy.amin(self.tmpval), numpy.amax(self.tmpval)
                    ylow = min(0.995 * ylow, 1.01 * ylow)
                    yhigh = max(0.995 * yhigh, 1.01 * yhigh)
                    self.f3ax.set_ylim([ylow, yhigh])
                    self.f3ax.grid(True)
                    self.figure3.savefig(self.zip_basedir + os.sep + item + '_vs_%s.png' % self.activeVar)
                    numpy.savetxt(self.zip_basedir + os.sep + item + '_vs_%s.txt' % self.activeVar, numpy.asarray([self.plotx, self.tmpval]))
            self.txt_parameters = ''
            for item in self.DictPlotTitle.keys():
                writeItem = True
                if item == 'dist_sample_det' and self.det_useEffPix:   writeItem = False
                if item == 'det_eff_pix' and not self.det_useEffPix: writeItem = False
                if item == 'BSC_CS' and self.BSC_useFullDet:    writeItem = False
                if writeItem:
                    self.txt_parameters += StringFill(self.DictPlotTitle[item] + ':', 40) + ' ' + str(eval('self.' + item) * self.DictPlotFactors[item]) + '\n'
            with open(self.zip_basedir + os.sep + '_Input_Parameters.txt', 'w') as f:
                f.write(self.txt_parameters)
            try:
                with zipfile.ZipFile(self.zip_fname, 'w') as zobject:
                    for item in self.DictPlotLabels.keys():
                        zobject.write(self.zip_basedir + os.sep + item + '_vs_%s.png' % self.activeVar, item + '_vs_%s.png' % self.activeVar)
                        zobject.write(self.zip_basedir + os.sep + item + '_vs_%s.txt' % self.activeVar, item + '_vs_%s.txt' % self.activeVar)
                        os.remove(self.zip_basedir + os.sep + item + '_vs_%s.txt' % self.activeVar)
                        os.remove(self.zip_basedir + os.sep + item + '_vs_%s.png' % self.activeVar)
                    zobject.write(self.zip_basedir + os.sep + '_Input_Parameters.txt', '_Input_Parameters.txt')
                    os.remove(self.zip_basedir + os.sep + '_Input_Parameters.txt')
            except:
                self.zip_fobject = None
                QtWidgets.QWidget.QMessageBox.critical(self, 'Error', "Error writing zip file\n\t%s." % (self.zip_fname), buttons=QtWidgets.QWidget.QMessageBox.Ok)
                return None
        return None
    # end writeData
    
    def closeEvent(self, event, reply=None):
        """Safety check for closing of window."""
        if reply == None:
            reply = QtWidgets.QWidget.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtWidgets.QWidget.QMessageBox.Yes | QtWidgets.QWidget.QMessageBox.No, QtWidgets.QWidget.QMessageBox.No)
        if reply == QtWidgets.QWidget.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        return None   





def TXMCalculator(parent=None, name='TXM parameter calculator', fluxdata='c:/_data/I13-id-flux_newB.raw', path=None):
    app = QtWidgets.QWidget.QApplication(sys.argv)
    screensize = app.desktop().screenGeometry()
    gui = cTXMCalculator((), name=name, path=path, screensize = [screensize.width(), screensize.height()])
    if sys.platform == 'win32' or sys.platform == 'win64':
        sys.exit(app.exec_())
    else:
        app.exec_()



if __name__ == '__main__':
#     TXMCalculator(path = 'c:/_u_copy/_Programming_Code/Python/I13')
    TXMCalculator(path='C:/Users/flenners/Desktop/TXM Calculator') # ''u:/_Programming_Code/Python/I13')
