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

class cCounterMonitor(QtGui.QMainWindow):
    def __init__(self, parent, name='Counter', counter=None):
        super(cCounterMonitor, self).__init__()
        try:
            QtUic.loadUi('h:/_data/programming_python/p05/gui/Counter_ui.ui', self)
            self.setWindowIcon(QtGui.QIcon('h:/_data/programming_python/p05/gui/qbpm.png'))
        except:
            _path = misc.GetPath('Counter_ui.ui')
            QtUic.loadUi(_path, self)
            self.setWindowIcon(QtGui.QIcon(os.path.split(_path)[0] + os.sep + 'qbpm.png'))
        self.setWindowTitle(name)
        self.setGeometry(25, 35, 851, 740)
        self.PollingThread = None
        self.main = parent
        
        self.counter = counter

        self.figure = pylab.figure(1, figsize=(11, 8), dpi=80)
        self.figureCanvas = FigureCanvas(self.figure)
        self.figureCanvas.setParent(self)
        self.figureCanvas.setGeometry(10, 180, 841, 551)
        self.axes = self.figure.add_axes([0.09, 0.07, 0.89, 0.9])
        self.axes.hold(False)
        
        self.cur_frequency = 5
        self.cur_numdata = 400
        self.update_active = False
        self.autoScale = True
        self.data_i = 2
        self.cur_upperlim = 'auto'
        self.cur_lowerlim = 'auto'
        self.cur_plottype = 'linear'
        self.yarr = numpy.zeros(1000) + 1e-12
        self.xarr = numpy.zeros(1000)
        self.multiplicator = 1.
        self.averaging = 1.

        QtCore.QObject.connect(self.but_StartStop, QtCore.SIGNAL('clicked()'), self.clickButtonStartStop)    
        QtCore.QObject.connect(self.but_SetUpperLimit, QtCore.SIGNAL('clicked()'), self.clickButtonSetUpperLimit)    
        QtCore.QObject.connect(self.but_SetLowerLimit, QtCore.SIGNAL('clicked()'), self.clickButtonSetLowerLimit)    
        QtCore.QObject.connect(self.but_SetTANGOaddress, QtCore.SIGNAL('clicked()'), self.clickButtonSetTANGOaddress)
        QtCore.QObject.connect(self.but_ClearBuffer, QtCore.SIGNAL('clicked()'), self.clickButton_ClearBuffer)
        QtCore.QObject.connect(self.but_SetMultiplicator, QtCore.SIGNAL('clicked()'), self.clickButton_SetMultiplicator)
        QtCore.QObject.connect(self.comboBox_UpdateFrequency, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_UpdateFrequency)
        QtCore.QObject.connect(self.comboBox_NumDatapoints, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_NumDatapoints)
        QtCore.QObject.connect(self.comboBox_UpperLimit, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_UpperLimit)
        QtCore.QObject.connect(self.comboBox_LowerLimit, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_LowerLimit)
        QtCore.QObject.connect(self.comboBox_TANGOattributes, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_TANGOattributes)
        QtCore.QObject.connect(self.comboBox_PlotType, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_PlotType)
        QtCore.QObject.connect(self.comboBox_Averaging, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_Averaging)
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
        self.but_SetLowerLimit.setStyleSheet(self.button_style)
        self.but_SetUpperLimit.setStyleSheet(self.button_style)
        self.but_SetTANGOaddress.setStyleSheet(self.button_style)
        self.but_SetMultiplicator.setStyleSheet(self.button_style)

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

        self.edit_UpperLimit.setFont(self.stdfont)
        self.edit_LowerLimit.setFont(self.stdfont)
        self.edit_TANGOaddress.setFont(self.stdfont)

        self.edit_UpperLimit.setVisible(False)
        self.edit_LowerLimit.setVisible(False)
        self.but_SetLowerLimit.setVisible(False)
        self.but_SetUpperLimit.setVisible(False)
        self.comboBox_TANGOattributes.setVisible(False)

        QtCore.QObject.connect(self.PollingThread, QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), self.NewUpdate)
        if self.counter != None:
            self.edit_TANGOaddress.setText(self.counter)
            self.clickButtonSetTANGOaddress()

        self.show()

        return None
            
    def clickButtonStartStop(self):
        if self.update_active:
            self.label_update.setPalette(self.palette_red)
            self.label_update.setText('inactive')
            self.PollingThread.stop()
            self.update_active = False
        elif self.update_active == False:
            self.label_update.setPalette(self.palette_green)
            self.label_update.setText('active')
            self.PollingThread.restart()
            self.update_active = True
        return None
    # end clickButtonStartStop
    
    
    def clickButtonSetUpperLimit(self):
        try:
            self.cur_upperlim = float(self.edit_UpperLimit.text())
        except:
            QtGui.QMessageBox.warning(self.main, 'Warning', "%s could not be converted to a number." % self.edit_UpperLimit.text(), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            self.edit_UpperLimit.setText('')
            self.cur_upperlim = 'auto'
        return None
    #end clickButtonSetUpperLimit
    
    
    def clickButtonSetLowerLimit(self):
        try:
            self.cur_lowerlim = float(self.edit_LowerLimit.text())
        except:
            QtGui.QMessageBox.warning(self.main, 'Warning', "%s could not be converted to a number." % self.edit_UpperLimit.text(), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            self.edit_LowerLimit.setText('')
            self.cur_lowerlim = 'auto'
        return None
    #end clickButtonSetLowerLimit

    def clickButtonSetTANGOaddress(self):
        self.sCounter = str(self.edit_TANGOaddress.text())
        self.PollingThread.stop()
        time.sleep(0.5)
        self.label_update.setPalette(self.palette_red)
        self.label_update.setText('inactive')
        try:
            self.tCounter = PyTango.DeviceProxy(self.sCounter)
            self.PollingThread.setTANGOaddress(self.tCounter)
            self.select_mode = False
            for i in range(self.comboBox_TANGOattributes.count()):
                self.comboBox_TANGOattributes.removeItem(0)
            tmp = list(self.tCounter.get_attribute_list())
            tmp.sort()
            tmp.insert(0, 'None')
            self.TangoAttList = numpy.asarray(tmp, dtype = object)
            for att in self.TangoAttList:
                self.comboBox_TANGOattributes.addItem(att)
            self.comboBox_TANGOattributes.setVisible(True)
            self.data_i = 2
            self.cur_upperlim = 'auto'
            self.cur_lowerlim = 'auto'
        
            self.yarr = numpy.zeros(1000) + 1e-12
            self.xarr = numpy.zeros(1000)
            self.select_mode = True
        except Exception, e:
            QtGui.QMessageBox.critical(self.main, 'Error', "TANGO exception. Could not connect to the TANGO server at the address %s\n%s" % (self.sCounter, e), buttons=QtGui.QMessageBox.Ok)
            self.tCounter = None
            self.comboBox_TANGOattributes.setVisible(False)
            return None
        return None
    #end clickButtonSetTANGOaddress

    def clickButton_ClearBuffer(self):
        self.data_i = 2
        self.yarr = numpy.zeros(1000) + 1e-12
        self.xarr = numpy.zeros(1000)
        return None
    #end clickButton_ClearBuffer
        
    def clickButton_SetMultiplicator(self):
        try:
            self.multiplicator = float(self.edit_Factor.text())
        except:
            self.multiplicator = 1.
            self.edit_Factor.setText("")
            QtGui.QMessageBox.warning(self.main, 'Warning', "Multiplcation factor not a valid float number", buttons=QtGui.QMessageBox.Ok)
        return None
    #end clickButton_SetMultiplicator

    def changeCombo_NumDatapoints(self):
        self.cur_numdata = int(self.comboBox_NumDatapoints.currentText())
        return None
    # end changeCombo_NumDatapoints
    
    def changeCombo_UpperLimit(self):
        self.cur_upperlim = self.comboBox_UpperLimit.currentText()
        if self.cur_upperlim == 'manual':
            self.edit_UpperLimit.setVisible(True)
            self.but_SetUpperLimit.setVisible(True)
            self.cur_upperlim = 'auto'
        elif self.cur_upperlim == 'auto':
            self.edit_UpperLimit.setVisible(False)
            self.but_SetUpperLimit.setVisible(False)
        if self.cur_lowerlim != 'auto' and self.cur_upperlim != 'auto':
            if float(self.cur_lowerlim) >= float(self.cur_upperlim):
                self.cur_lowerlim = 'auto'
                self.comboBox_LowerLimit.setCurrentIndex(0)
        return None
    # end changeCombo_UpperLimit
    
    def changeCombo_LowerLimit(self):
        self.cur_lowerlim = self.comboBox_LowerLimit.currentText()
        if self.cur_lowerlim == 'manual':
            self.edit_LowerLimit.setVisible(True)
            self.but_SetLowerLimit.setVisible(True)
            self.cur_lowerlim = 'auto'
        elif self.cur_lowerlim == 'auto':
            self.edit_LowerLimit.setVisible(False)
            self.but_SetLowerLimit.setVisible(False)
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

    def changeCombo_TANGOattributes(self):
        if self.select_mode:
            self.cur_attribute = str(self.comboBox_TANGOattributes.currentText())
            if self.cur_attribute == 'None':
                self.cur_attribute = None
                self.PollingThread.setTANGOattribute(None)
            else:
                self.tmp = self.tCounter.read_attribute(self.cur_attribute)
                self.label_update.setPalette(self.palette_red)
                self.label_update.setText('inactive')
                self.PollingThread.stop()
                self.update_active = False
                if self.tmp.type not in [PyTango.CmdArgType.DevShort, PyTango.CmdArgType.DevLong, PyTango.CmdArgType.DevUShort, \
                                    PyTango.CmdArgType.DevULong, PyTango.CmdArgType.DevLong64, PyTango.CmdArgType.DevULong64, \
                                    PyTango.CmdArgType.DevInt, PyTango.CmdArgType.DevFloat, PyTango.CmdArgType.DevDouble]:
                    QtGui.QMessageBox.critical(self.main, 'Error', "The selected attribute is not a numerical value. Please select other attribute!", buttons=QtGui.QMessageBox.Ok)
                    self.cur_attribute = None
                    self.PollingThread.setTANGOattribute(None)
                    self.comboBox_TANGOattributes.setCurrentIndex(0)
                else:
                    self.PollingThread.setTANGOattribute(self.cur_attribute)
        return None
    #end self.changeCombo_TANGOattributes

    def changeCombo_PlotType(self):
        self.cur_plottype = self.comboBox_PlotType.currentText()
        return None
    #end self.changeCombo_PlotType

    def changeCombo_Averaging(self):
        self.PollingThread.set_averaging(int(self.comboBox_Averaging.currentText()))
        return None
    #end changeCombo_Averaging

    def NewUpdate(self, _data):
        if self.update_active:
            self.label_timeedit.setTime(QtCore.QTime.currentTime())
        if abs(_data[0]) < 1e-10: _data[0] = 1.01e-10
        self.yarr = numpy.roll(self.yarr, -1)
        self.xarr = numpy.roll(self.xarr, -1)
        self.xarr[-1] = time.time()
        self.yarr[-1] = _data[0] 
        
        if self.data_i == 2:
            self.xarr[-2] = self.xarr[-1] - 1e-6
            self.yarr[-2] = self.yarr[-1]
        self.limit = min(self.data_i, self.cur_numdata)
        curx, cury = self.xarr[-self.limit:] - self.xarr[-1], self.yarr[-self.limit:]* self.multiplicator
        self.data_i += 1

        if self.cur_plottype == 'linear':
            self.axes.plot(curx, cury, markeredgewidth=0.1, markersize=4, color='#2222FF', linewidth=1.5, marker='o')
            
            if self.cur_upperlim == 'auto':
                self.axlimtop = 1.05* cury.max()
            else:
                self.axlimtop = self.cur_upperlim
            
            if self.cur_lowerlim == 'auto':
                self.axlimbot = cury.min()
                if self.axlimbot <= 0:
                    self.axlimbot *= 1.05
                elif self.axlimbot > 0:
                    self.axlimbot *= 0.95
            else:
                self.axlimbot = self.cur_lowerlim
    
            if self.axlimtop <= self.axlimbot:
                self.axlimtop = max(cury)
                self.axlimbot = min(cury)
                self.cur_lowerlim = 'auto'
                self.comboBox_LowerLimit.setCurrentIndex(0)
                self.cur_upperlim = 'auto'
                self.comboBox_UpperLimit.setCurrentIndex(0)
        
        
        elif self.cur_plottype == 'log':
            self.axes.semilogy(curx, cury, markeredgewidth=0.1, markersize=4, color='#2222FF', linewidth=1.5, marker='o')
            if self.cur_upperlim == 'auto':
                self.axlimtop = numpy.exp(numpy.log(10) * (int(numpy.log10(max(cury)))))
                if numpy.log10(max(cury)) > 0.:
                    self.axlimtop *= 10
            else:
                self.axlimtop = self.cur_upperlim
            if self.cur_lowerlim == 'auto':
                self.axlimbot = numpy.exp(numpy.log(10) * (int(numpy.log10(min(cury))) - 1))
            else:
                self.axlimbot = self.cur_lowerlim
    
            if self.axlimtop <= self.axlimbot:
                self.axlimtop = numpy.exp(numpy.log(10) * (int(numpy.log10(max(cury)))))
                self.axlimbot = numpy.exp(numpy.log(10) * (int(numpy.log10(min(cury))) - 1))
                self.cur_lowerlim = 'auto'
                self.comboBox_LowerLimit.setCurrentIndex(0)
                self.cur_upperlim = 'auto'
                self.comboBox_UpperLimit.setCurrentIndex(0)

        self.axes.set_xlim([curx[0], curx[-1]])
        self.axes.set_ylim([self.axlimbot, self.axlimtop])
        self.axes.set_xlabel('time / s')
        self.axes.set_ylabel('Counter', color='#2222FF')
        self.figureCanvas.draw()
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
            time.sleep(1.0 / self.cur_frequency)
            event.accept()
        else:
            event.ignore()
        return None   


class  CounterPolling(QtCore.QThread):
    def __init__(self, parentThread, tCounter=None, tPETRA=None, start_freq=5):
        QtCore.QThread.__init__(self, parentThread)
        self.running = False
        self.cur_frequency = start_freq
        self.changeAvg = False
        self.counter_val = 0.
        self.tCounter = tCounter
        self.counterAttribute = None
        self.counter = 0
        self.terminate_signal = False
        self.cur_averaging = 1
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
    
    def setTANGOaddress(self, _address):
        self.running = False
        time.sleep(0.5)
        try:
            self.tCounter = PyTango.DeviceProxy(_address)
        except:
            self.tCounter = None
            self.counterAttribute = None
        return None
    
    def setTANGOattribute(self, _attribute):
        self.running = False
        self.counterAttribute = _attribute
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

class CounterThread(CounterPolling):
    def __init__(self, parentThread, tCounter=None):
        CounterPolling.__init__(self, parentThread, tCounter=tCounter)
        return None
    
    def getUpdate(self):
        while True:
            if self.changeAvg:
                self.cur_averaging = self.newAvg
                self.changeAvg = False
            if self.running:
                if self.tCounter != None and self.counterAttribute != None:
                    self.counter_val = 0
                    self.cur_n = self.cur_averaging
                    for i1 in xrange(self.cur_n):
                        self.t0 = time.time()
                        self.counter_val += self.tCounter.read_attribute(self.counterAttribute).value
                        time.sleep(max(0, 1.0 / self.cur_frequency - (time.time() - self.t0)))
                    self.counter_val /= self.cur_n
                    self.emit(QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), [self.counter_val])
            elif self.running == False:
                time.sleep(1.0 / self.cur_frequency)
            if self.terminate_signal:
                break
        return None        



def CounterMonitor(parent=None, name='Counter monitor', counter='//hzgpp05vme1:10000/p05/adc/eh1.01'):
    app = QtGui.QApplication(sys.argv)
    gui = cCounterMonitor(QtGui.QMainWindow(), name=name, counter=counter)
    gui.PollingThread = CounterThread(gui.main, tCounter=counter)
    gui.PollingThread.start()
    gui._initialize()
    gui.show()
    if sys.platform == 'win32' or sys.platform == 'win64':
        sys.exit(app.exec_())
    else:
        app.exec_()


if __name__ == "__main__":
    CounterMonitor()
