import numpy
from PyQt4 import uic as QtUic
from PyQt4 import QtGui
from PyQt4 import QtCore
import PyTango
import sys
import time
import os
import p05.tools.misc as misc
import pylab
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class cQBPMmonitor(QtGui.QMainWindow):
    def __init__(self, parent, name='QBPM monitor', counter = None, dualMode = False):
        super(cQBPMmonitor, self).__init__()
        try:
            QtUic.loadUi('h:/_data/programming_python/p05/gui/QBPM_ui.ui', self)
            self.setWindowIcon(QtGui.QIcon('h:/_data/programming_python/p05/gui/qbpm.png'))
        except:
            _path = misc.GetPath('QBPM_ui.ui')
            QtUic.loadUi(_path, self)
            self.setWindowIcon(QtGui.QIcon(os.path.split(_path)[0] + os.sep + 'qbpm.png'))
        self.setWindowTitle(name)
        self.setGeometry(25, 35, 881, 666)
        
        try:
            self.tQBPM = PyTango.DeviceProxy(counter)
            if dualMode:
                self.tQBPM2 = PyTango.DeviceProxy('//hzgpp05vme0:10000/p05/i404/exp.02')
        except Exception, e:
            QtGui.QMessageBox.critical(self.parent, 'Error', "TANGO exception. Could not connect to the TANGO server at the address %s\n%s" % (counter, e), buttons=QtGui.QMessageBox.Ok)
        self.tPETRA = PyTango.DeviceProxy('//hzgpp05vme1:10000/PETRA/GLOBALS/keyword')
        self.main = parent
        self.dualMode = dualMode
        self.figure = pylab.figure(1, figsize=(11, 8), dpi=80)
        self.figureCanvas = FigureCanvas(self.figure)
        self.figureCanvas.setParent(self)
        self.figureCanvas.setGeometry(10, 100, 861, 551)
        self.axes = self.figure.add_axes([0.08, 0.07, 0.85, 0.9])
        self.axespetra = self.axes.twinx()
        self.axespetra.set_ylim([-2, 105])
        self.axes.hold(True)
        self.axespetra.hold(True)
        
        
        self.updater = QtCore.QTimer()
        self.cur_averaging = 2
        self.cur_frequency = 5
        self.cur_numdata = 400
        self.update_active = False
        self.autoScale = True
        self.data_i = 2
        self.cur_upperlim = 'auto'
        self.cur_lowerlim = 'auto'
        
        self.yarr = numpy.zeros(1000) + 1e-12
        self.yarr2 = numpy.zeros(1000) + 1e-12
        self.ypetra = numpy.zeros(1000)
        self.xarr = numpy.zeros(1000)
        

        QtCore.QObject.connect(self.but_StartStop, QtCore.SIGNAL('clicked()'), self.clickButtonStartStop)    
        QtCore.QObject.connect(self.comboBox_UpdateFrequency, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_UpdateFrequency)
        QtCore.QObject.connect(self.comboBox_Averaging, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_Averaging)
        QtCore.QObject.connect(self.comboBox_NumDatapoints, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_NumDatapoints)
        QtCore.QObject.connect(self.comboBox_UpperLimit, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_UpperLimit)
        QtCore.QObject.connect(self.comboBox_LowerLimit, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_LowerLimit)
        
        return None
    
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

        self.but_StartStop.setStyleSheet(self.button_style)

        self.label_update.setPalette(self.palette_red)
        self.label_update.setText('inactive')

        self.comboBox_Averaging.setStyleSheet(self.textbox_style)
        
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

        QtCore.QObject.connect(self.PollingThread, QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), self.NewUpdate)
        self.show()

        return None
            
    def clickButtonStartStop(self):
        if self.update_active:
            self.label_update.setPalette(self.palette_red)
            self.label_update.setText('inactive')
            self.label_p3current.setPalette(self.palette_red)
            self.label_p3current.setText('inactive')
            self.PollingThread.stop()
            self.update_active = False
        elif self.update_active == False:
            self.label_update.setPalette(self.palette_green)
            self.label_update.setText('active')
            self.label_p3current.setPalette(self.palette_blk)
            ('inactive')
            self.PollingThread.running = True
            self.PollingThread.restart()
            self.update_active = True
        return None
    # end clickButtonStartStop
    
    def changeCombo_Averaging(self):
        self.cur_averaging = int(self.comboBox_Averaging.currentText())
        self.PollingThread.set_averaging(self.cur_averaging)
        return None
    # end changeCombo_Averaging
    
    def changeCombo_NumDatapoints(self):
        self.cur_numdata = int(self.comboBox_NumDatapoints.currentText())
        return None
    # end changeCombo_NumDatapoints
    
    def changeCombo_UpperLimit(self):
        self.cur_upperlim = self.comboBox_UpperLimit.currentText()
        if self.cur_lowerlim != 'auto' and self.cur_upperlim != 'auto':
            if float(self.cur_lowerlim) >= float(self.cur_upperlim):
                self.cur_lowerlim = 'auto'
                self.comboBox_LowerLimit.setCurrentIndex(0)
        return None
    # end changeCombo_UpperLimit
    
    def changeCombo_LowerLimit(self):
        self.cur_lowerlim = self.comboBox_LowerLimit.currentText()
        if self.cur_lowerlim != 'auto' and self.cur_upperlim != 'auto':
            if float(self.cur_lowerlim) >= float(self.cur_upperlim):
                self.cur_upperlim = 'auto'
                self.comboBox_UpperLimit.setCurrentIndex(0)
        return None
    # end changeCombo_LowerLimit

    def changeCombo_UpdateFrequency(self):
        self.cur_frequency = int(self.comboBox_UpdateFrequency.currentText())
        self.PollingThread.set_frequency(self.cur_frequency)
        return None
    # end changeCombo_UpdateFrequency

    def NewUpdate(self, _data):
        if self.update_active:
            self.label_p3current.setText('%3.1f mA' % _data[1])
        if _data[0] < 1e-10: _data[0] = 1.01e-10
        self.yarr = numpy.roll(self.yarr, -1)
        
        self.ypetra = numpy.roll(self.ypetra, -1)
        self.xarr = numpy.roll(self.xarr, -1)
        self.xarr[-1] = time.time()
        self.yarr[-1] = _data[0]
        self.ypetra[-1] = _data[1] 

        if self.data_i == 2:
            self.xarr[-2] = self.xarr[-1] - 1e-6
            self.yarr[-2] = self.yarr[-1]
            self.ypetra[-2] = self.ypetra[-1]

        self.limit = min(self.data_i, self.cur_numdata)
        curx, cury, curypetra = self.xarr[-self.limit:] - self.xarr[-1], self.yarr[-self.limit:], self.ypetra[-self.limit:]
        if self.dualMode:
            self.yarr2 = numpy.roll(self.yarr2, -1)
            self.yarr2[-1] = max(_data[2], 1.01e-10)
            if self.data_i == 2: self.yarr2[-2] = self.yarr2[-1]
            cury2 = self.yarr2[-self.limit:]
            
        self.data_i += 1

        self.axes.semilogy(curx, cury, markeredgewidth=0.1, markersize=4, color='#2222FF', linewidth=1.5, marker='o')
        if self.dualMode:
            self.axes.semilogy(curx, cury2, markeredgewidth=0.1, markersize=4, color='#698aE5', linewidth=1.5, marker='o')
            cury = [cury, cury2]
        self.axespetra.plot(curx, (curypetra), markeredgewidth=0.1, color='#BB1111', linewidth=2)
        
        if self.cur_upperlim == 'auto':
            self.axlimtop = numpy.exp(numpy.log(10) * (int(numpy.log10(numpy.max(cury)))))
        else:
            self.axlimtop = float(self.cur_upperlim)    
        if self.cur_lowerlim == 'auto':
            self.axlimbot = numpy.exp(numpy.log(10) * (int(numpy.log10(numpy.min(cury))) - 1))
        else:
            self.axlimbot = float(self.cur_lowerlim)

        if self.axlimtop <= self.axlimbot:
            self.axlimtop = numpy.exp(numpy.log(10) * (int(numpy.log10(numpy.max(cury)))))
            self.axlimbot = numpy.exp(numpy.log(10) * (int(numpy.log10(numpy.min(cury))) - 1))
            self.cur_lowerlim = 'auto'
            self.comboBox_LowerLimit.setCurrentIndex(0)
            self.cur_upperlim = 'auto'
            self.comboBox_UpperLimit.setCurrentIndex(0)

        self.axes.set_xlim([curx[0], curx[-1]])
        self.axes.set_ylim([self.axlimbot, self.axlimtop])
        self.axes.set_xlabel('time / s')
        self.axes.set_ylabel('QBPM current', color = '#2222FF')
        self.axespetra.set_ylim([-2, 105])
        self.axespetra.set_ylabel('PETRA III current / mA', color = '#BB1111')
        self.figureCanvas.draw()
        self.axespetra.lines.pop(0)        
        self.axes.lines.pop(0)
        if self.dualMode: self.axes.lines.pop(0)
        return None
    # end NewUpdate
    
    
    def closeEvent(self, event):
        """Safety check for closing of window."""
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.PollingThread.terminate_signal = True
            self.PollingThread.quit()
            time.sleep(1.0 * self.cur_averaging / self.cur_frequency)
            event.accept()
        else:
            event.ignore()
        return None   


class  QBPMpolling(QtCore.QThread):
    def __init__(self, parentThread, tQBPM=None, tQBPM2 = None, tPETRA=None, start_avg=2, start_freq=5):
        QtCore.QThread.__init__(self, parentThread)
        self.running = False
        self.changeAvg = False
        self.cur_averaging = start_avg
        self.cur_frequency = start_freq
        self.qbpm_val = 0.
        self.qbpm_val2 = 0.
        self.tQBPM = tQBPM
        self.tQBPM2 = tQBPM2
        self.tPETRA = tPETRA
        self.petra_val = 0.
        self.counter = 0
        self.dualMode = False
        self.terminate_signal = False
        return None
    
    def set_averaging(self, value):
        self.changeAvg = True
        self.newAvg = value
        return None

    def set_frequency(self, value):
        self.cur_frequency = value
        return None
    
    def stop(self):
        self.running = False
        return None
    
    def restart(self):
        self.running = True
        return None
    
    def run(self):
        self.running = False
        self.getUpdate()
        return None
    
    def cleanUp(self):
        return None
    
    def getUpdate(self):
        return True

class CounterThread(QBPMpolling):
    def __init__(self, parentThread, tQBPM=None, tQBPM2 = None, tPETRA=None):
        QBPMpolling.__init__(self, parentThread, tQBPM=tQBPM, tQBPM2=tQBPM2, tPETRA=tPETRA)
        return None
    
    def getUpdate(self):
        while True:
            if self.changeAvg:
                self.cur_averaging = self.newAvg
                self.changeAvg = False
            if self.running:
                for i1 in xrange(self.cur_averaging):
                    self.t0 = time.time()
                    self.qbpm_val += self.tQBPM.read_attribute('PosAndAvgCurr').value[2] / self.cur_averaging
                    if self.dualMode:
                        self.qbpm_val2 += self.tQBPM2.read_attribute('PosAndAvgCurr').value[2] / self.cur_averaging
                    time.sleep(max(0, 1.0 / self.cur_frequency - (time.time() - self.t0)))
                self.petra_val = self.tPETRA.read_attribute('BeamCurrent').value
                if self.dualMode:
                    self.emit(QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), [self.qbpm_val, self.petra_val, self.qbpm_val2])
                else:
                    self.emit(QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), [self.qbpm_val, self.petra_val])
                self.qbpm_val = 0.
                self.qbpm_val2 = 0.
            elif self.running == False:
                time.sleep(1.0 / self.cur_frequency)
            if self.terminate_signal:
                break
        return None        



def QBPMmonitor(parent=None, name='QBPM monitor', counter = '//hzgpp05vme0:10000/p05/i404/exp.01', dualMode = False):
    app = QtGui.QApplication(sys.argv)
    gui = cQBPMmonitor(QtGui.QMainWindow(), name=name, counter = '//hzgpp05vme0:10000/p05/i404/exp.01', dualMode = dualMode)
    if gui.dualMode: 
        gui.PollingThread = CounterThread(gui.main, tQBPM=gui.tQBPM, tQBPM2 = gui.tQBPM2, tPETRA=gui.tPETRA)
        gui.PollingThread.dualMode = True
    else:
        gui.PollingThread = CounterThread(gui.main, tQBPM=gui.tQBPM, tPETRA=gui.tPETRA)
    gui.PollingThread.start()
    gui._initialize()
    gui.show()
    if sys.platform == 'win32' or sys.platform == 'win64':
        sys.exit(app.exec_())
    else:
        app.exec_()

