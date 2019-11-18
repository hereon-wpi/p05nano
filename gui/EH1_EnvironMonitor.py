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
import copy

class cEH1EnvMonitor(QtGui.QMainWindow):
    def __init__(self, parent, name='Counter', counter=None):
        super(cEH1EnvMonitor, self).__init__()
        try:
            QtUic.loadUi('h:/_data/programming_python/p05/gui/EH1_EnvironMonitor_ui.ui', self)
            self.setWindowIcon(QtGui.QIcon('h:/_data/programming_python/p05/gui/qbpm.png'))
        except:
            _path = misc.GetPath('EH1_EnvironMonitor_ui.ui')
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
        self.figureCanvas.setGeometry(10, 205, 841, 551)
        self.axesT = self.figure.add_axes([0.09, 0.1, 0.82, 0.88])
        self.axesRH = self.axesT.twinx()
        
        self.axesT.hold(False)
        self.axesRH.hold(False)
        
        self.cur_frequency = 1
        self.cur_numdata = 400
        self.update_active = False
        self.autoScale = True
        self.data_i = 2
        self.cur_upperlimT = 'auto'
        self.cur_lowerlimT = 'auto'
        self.cur_upperlimRH = 'auto'
        self.cur_lowerlimRH = 'auto'
        self.yarrT = numpy.zeros((3,5000)) + 1e-12
        self.yarrRH = numpy.zeros((3,5000)) + 1e-12
        self.xarr = numpy.zeros(5000)
        self.averaging = 1.
        self.active_sensors = numpy.ones((6), dtype = bool)
        self.sensors = [self.s1_Temp, self.s1_Humid, self.s2_Temp, self.s2_Humid, self.s3_Temp, self.s3_Humid]
        self.colors_T = ['#89BAE5', '#99D9EA', '#6444FB']
        self.colors_RH = ['#FF7E31', '#FFF317', '#DE5a1b']

        QtCore.QObject.connect(self.but_StartStop, QtCore.SIGNAL('clicked()'), self.clickButtonStartStop)    
        QtCore.QObject.connect(self.but_TempSetUpperLimit, QtCore.SIGNAL('clicked()'), self.clickButtonSetTempUpperLimit)    
        QtCore.QObject.connect(self.but_TempSetLowerLimit, QtCore.SIGNAL('clicked()'), self.clickButtonSetTempLowerLimit)    
        QtCore.QObject.connect(self.but_HumidSetUpperLimit, QtCore.SIGNAL('clicked()'), self.clickButtonSetHumidUpperLimit)    
        QtCore.QObject.connect(self.but_HumidSetLowerLimit, QtCore.SIGNAL('clicked()'), self.clickButtonSetHumidLowerLimit)    
        QtCore.QObject.connect(self.but_SetActiveSensors, QtCore.SIGNAL('clicked()'), self.clickButtonSetActiveSensors)
        QtCore.QObject.connect(self.but_ClearBuffer, QtCore.SIGNAL('clicked()'), self.clickButton_ClearBuffer)
        QtCore.QObject.connect(self.comboBox_UpdateFrequency, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_UpdateFrequency)
        QtCore.QObject.connect(self.comboBox_NumDatapoints, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_NumDatapoints)
        QtCore.QObject.connect(self.comboBox_TempUpperLimit, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_TempUpperLimit)
        QtCore.QObject.connect(self.comboBox_TempLowerLimit, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_TempLowerLimit)
        QtCore.QObject.connect(self.comboBox_HumidUpperLimit, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_HumidUpperLimit)
        QtCore.QObject.connect(self.comboBox_HumidLowerLimit, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo_HumidLowerLimit)
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
        self.but_TempSetLowerLimit.setStyleSheet(self.button_style)
        self.but_TempSetUpperLimit.setStyleSheet(self.button_style)
        self.but_HumidSetLowerLimit.setStyleSheet(self.button_style)
        self.but_HumidSetUpperLimit.setStyleSheet(self.button_style)

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

        self.edit_TempUpperLimit.setFont(self.stdfont)
        self.edit_TempLowerLimit.setFont(self.stdfont)
        self.edit_HumidUpperLimit.setFont(self.stdfont)
        self.edit_HumidLowerLimit.setFont(self.stdfont)

        self.edit_TempUpperLimit.setVisible(False)
        self.edit_TempLowerLimit.setVisible(False)
        self.but_TempSetLowerLimit.setVisible(False)
        self.but_TempSetUpperLimit.setVisible(False)
        self.edit_HumidUpperLimit.setVisible(False)
        self.edit_HumidLowerLimit.setVisible(False)
        self.but_HumidSetLowerLimit.setVisible(False)
        self.but_HumidSetUpperLimit.setVisible(False)

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
    
    
    def clickButtonSetTempUpperLimit(self):
        try:
            self.cur_upperlimT = float(self.edit_TempUpperLimit.text())
        except:
            QtGui.QMessageBox.warning(self.main, 'Warning', "%s could not be converted to a number." % self.edit_TempUpperLimit.text(), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            self.edit_TempUpperLimit.setText('')
            self.cur_upperlimT = 'auto'
        return None
    #end clickButtonSetTempUpperLimit
    
    
    def clickButtonSetTempLowerLimit(self):
        try:
            self.cur_lowerlimT = float(self.edit_TempLowerLimit.text())
        except:
            QtGui.QMessageBox.warning(self.main, 'Warning', "%s could not be converted to a number." % self.edit_TempUpperLimit.text(), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            self.edit_TempLowerLimit.setText('')
            self.cur_lowerlimT = 'auto'
        return None
    #end clickButtonSetTempLowerLimit

    def clickButtonSetHumidUpperLimit(self):
        try:
            self.cur_upperlimRH = float(self.edit_HumidUpperLimit.text())
        except:
            QtGui.QMessageBox.warning(self.main, 'Warning', "%s could not be converted to a number." % self.edit_HumidUpperLimit.text(), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            self.edit_HumidUpperLimit.setText('')
            self.cur_upperlimRH = 'auto'
        return None
    #end clickButtonSetHumidUpperLimit
    
    
    def clickButtonSetHumidLowerLimit(self):
        try:
            self.cur_lowerlimRH = float(self.edit_HumidLowerLimit.text())
        except:
            QtGui.QMessageBox.warning(self.main, 'Warning', "%s could not be converted to a number." % self.edit_HumidUpperLimit.text(), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            self.edit_HumidLowerLimit.setText('')
            self.cur_lowerlimRH = 'auto'
        return None
    #end clickButtonSetHumidLowerLimit
    
    def clickButtonSetActiveSensors(self):
        self.PollingThread.stop()
        time.sleep(0.5)
        self.label_update.setPalette(self.palette_red)
        self.label_update.setText('inactive')
        for i1 in xrange(6):
            self.active_sensors[i1] = self.sensors[i1].isChecked()
        self.PollingThread.setActiveState(self.active_sensors)
        self.update_active = False
        return None
    #end clickButtonSetTANGOaddress

    def clickButton_ClearBuffer(self):
        self.data_i = 2
        self.yarrT = numpy.zeros((3,5000)) + 1e-12
        self.yarrRH = numpy.zeros((3,5000)) + 1e-12
        self.xarr = numpy.zeros(5000)
        return None
    #end clickButton_ClearBuffer
        
    def changeCombo_NumDatapoints(self):
        self.cur_numdata = int(self.comboBox_NumDatapoints.currentText())
        return None
    # end changeCombo_NumDatapoints
    
    def changeCombo_TempUpperLimit(self):
        self.cur_upperlimT = self.comboBox_TempUpperLimit.currentText()
        if self.cur_upperlimT == 'manual':
            self.edit_TempUpperLimit.setVisible(True)
            self.but_TempSetUpperLimit.setVisible(True)
            self.cur_upperlimT = 'auto'
        elif self.cur_upperlimT == 'auto':
            self.edit_TempUpperLimit.setVisible(False)
            self.but_TempSetUpperLimit.setVisible(False)
        if self.cur_lowerlimT != 'auto' and self.cur_upperlimT != 'auto':
            if float(self.cur_lowerlimT) >= float(self.cur_upperlimT):
                self.cur_lowerlimT = 'auto'
                self.comboBox_TempLowerLimit.setCurrentIndex(0)
        return None
    # end changeCombo_TempUpperLimit
    
    def changeCombo_TempLowerLimit(self):
        self.cur_lowerlimT = self.comboBox_TempLowerLimit.currentText()
        if self.cur_lowerlimT == 'manual':
            self.edit_TempLowerLimit.setVisible(True)
            self.but_TempSetLowerLimit.setVisible(True)
            self.cur_lowerlimT = 'auto'
        elif self.cur_lowerlimT == 'auto':
            self.edit_TempLowerLimit.setVisible(False)
            self.but_TempSetLowerLimit.setVisible(False)
        if self.cur_lowerlimT != 'auto' and self.cur_upperlimT != 'auto':
            if float(self.cur_lowerlimT) >= float(self.cur_upperlimT):
                self.cur_upperlimT = 'auto'
                self.comboBox_TempUpperLimit.setCurrentIndex(0)
        return None
    # end changeCombo_TempLowerLimit

    def changeCombo_HumidUpperLimit(self):
        self.cur_upperlimRH = self.comboBox_HumidUpperLimit.currentText()
        if self.cur_upperlimRH == 'manual':
            self.edit_HumidUpperLimit.setVisible(True)
            self.but_HumidSetUpperLimit.setVisible(True)
            self.cur_upperlimRH = 'auto'
        elif self.cur_upperlimRH == 'auto':
            self.edit_HumidUpperLimit.setVisible(False)
            self.but_HumidSetUpperLimit.setVisible(False)
        if self.cur_lowerlimRH != 'auto' and self.cur_upperlimRH != 'auto':
            if float(self.cur_lowerlimRH) >= float(self.cur_upperlimRH):
                self.cur_lowerlimRH = 'auto'
                self.comboBox_HumidLowerLimit.setCurrentIndex(0)
        return None
    # end changeCombo_HumidUpperLimit
    
    def changeCombo_HumidLowerLimit(self):
        self.cur_lowerlimRH = self.comboBox_HumidLowerLimit.currentText()
        if self.cur_lowerlimRH == 'manual':
            self.edit_HumidLowerLimit.setVisible(True)
            self.but_HumidSetLowerLimit.setVisible(True)
            self.cur_lowerlimRH = 'auto'
        elif self.cur_lowerlimRH == 'auto':
            self.edit_HumidLowerLimit.setVisible(False)
            self.but_HumidSetLowerLimit.setVisible(False)
        if self.cur_lowerlimRH != 'auto' and self.cur_upperlimRH != 'auto':
            if float(self.cur_lowerlimRH) >= float(self.cur_upperlimRH):
                self.cur_upperlimRH = 'auto'
                self.comboBox_HumidUpperLimit.setCurrentIndex(0)
        return None
    # end changeCombo_HumidLowerLimit
    
    def changeCombo_UpdateFrequency(self):
        self.cur_frequency = float(self.comboBox_UpdateFrequency.currentText())
        self.PollingThread.set_frequency(self.cur_frequency)
        return None
    # end changeCombo_UpdateFrequency


    def changeCombo_Averaging(self):
        self.PollingThread.set_averaging(int(self.comboBox_Averaging.currentText()))
        return None
    #end changeCombo_Averaging

    def NewUpdate(self, _data):
        if self.update_active:
            self.label_timeedit.setTime(QtCore.QTime.currentTime())
        
        for i1 in xrange(3):
            self.yarrT[i1] = numpy.roll(self.yarrT[i1], -1)
            self.yarrRH[i1] = numpy.roll(self.yarrRH[i1], -1)
    
        self.xarr = numpy.roll(self.xarr, -1)
        
        self.xarr[-1] = time.time()
        self.yarrT[:, -1] = _data[0][[0,2,4]]
        self.yarrRH[:, -1] = _data[0][[1,3,5]]
        
        if self.data_i == 2:
            self.xarr[-2] = self.xarr[-1] - 1e-6
            self.yarrT[:,-2] = self.yarrT[:,-1]
            self.yarrRH[:,-2] = self.yarrRH[:,-1]
        self.limit = min(self.data_i, self.cur_numdata)
        curx,curyT, curyRH  = self.xarr[-self.limit:] - self.xarr[-1], 5 * self.yarrT[:, -self.limit:], 10 * self.yarrRH[:, -self.limit:]
        
        self.data_i += 1

        self.axesT.plot([0,0], [0,0])
        self.axesT.hold(True)
        #self.axesRH.plot([0,0], [0,0])
        #self.axesRH.hold(True)

        if self.cur_upperlimT == 'auto':
            self.axTlimtop = 1.05* curyT.max()
        else:
            self.axTlimtop = self.cur_upperlimT
        
        if self.cur_lowerlimT == 'auto':
            self.axTlimbot = max(0.95 * curyT.min(), 0)
        else:
            self.axTlimbot = self.cur_lowerlimT

        if self.axTlimtop <= self.axTlimbot:
            self.axTlimbot = min(curyT)
            self.axTlimtop = max(curyT)
            self.cur_lowerlimT = 'auto'
            self.comboBox_TempLowerLimit.setCurrentIndex(0)
            self.cur_upperlimT = 'auto'
            self.comboBox_TempUpperLimit.setCurrentIndex(0)

        if self.cur_upperlimRH == 'auto':
            self.axRHlimtop = 1.05* curyRH.max()
        else:
            self.axRHlimtop = self.cur_upperlimRH
        
        if self.cur_lowerlimRH == 'auto':
            self.axRHlimbot = max(0.95 * curyRH.min(), 0)
        else:
            self.axRHlimbot = self.cur_lowerlimRH

        if self.axRHlimtop <= self.axRHlimbot:
            self.axRHlimbot = min(curyRH)
            self.axRHlimtop =  max(curyRH)
            self.cur_lowerlimRH = 'auto'
            self.comboBox_HumidLowerLimit.setCurrentIndex(0)
            self.cur_upperlimRH = 'auto'
            self.comboBox_HumidUpperLimit.setCurrentIndex(0)

        tmpRH = (self.axTlimtop - self.axTlimbot) / ( self.axRHlimtop - self.axRHlimbot )* curyRH \
                + ( self.axTlimbot + self.axTlimtop ) /2 -  (self.axTlimtop - self.axTlimbot) / ( self.axRHlimtop - self.axRHlimbot ) * ( self.axRHlimtop + self.axRHlimbot ) / 2
        
        for i1 in xrange(3):
            if self.active_sensors[i1*2]:
                self.axesT.plot(curx, curyT[i1], markeredgewidth=0.1, markersize=4, color=self.colors_T[i1], linewidth=1.5, marker='o')
            if self.active_sensors[i1*2+1]:
                self.axesT.plot(curx, tmpRH[i1] , markeredgewidth=0.1, markersize=4, color=self.colors_RH[i1], linewidth=1.5, marker='o')
            

        

        
        self.axesT.set_xlim([curx[0], curx[-1]])
        self.axesT.set_ylim([self.axTlimbot, self.axTlimtop])
        self.axesRH.set_ylim([self.axRHlimbot, self.axRHlimtop])
        self.axesT.set_xlabel('time / s')
        self.axesT.set_ylabel('Temperature / Celsius', color='#2222FF')
        self.axesRH.set_ylabel('Relative humidity / percent', color='#FF7E31')
        self.figureCanvas.draw()
        self.axesT.hold(False)
        self.axesRH.hold(False)
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
            time.sleep(2.0 / self.cur_frequency)
            event.accept()
        else:
            event.ignore()
        return None   


class  CounterPolling(QtCore.QThread):
    def __init__(self, parentThread, tPETRA=None, start_freq=1):
        QtCore.QThread.__init__(self, parentThread)
        self.running = False
        self.changeAvg = False
        self.cur_frequency = start_freq
        
        self.counter_vals = numpy.zeros((6))
        self.tCounter = numpy.zeros((6), dtype ='object')
        self.active_states = numpy.ones((6), dtype = bool)
        for i1 in xrange(6):
            self.tCounter[i1] = PyTango.DeviceProxy('//hzgpp05vme1:10000/p05/adc/eh1.%02i' %(i1+1))
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
    
    def setActiveState(self, _active):
        self.active_states = _active
    
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

class EH1EnvThread(CounterPolling):
    def __init__(self, parentThread, tCounter=None):
        CounterPolling.__init__(self, parentThread)
        return None
    
    def getUpdate(self):
        while True:
            if self.changeAvg:
                self.cur_averaging = self.newAvg
                self.changeAvg = False
            if self.running:
                self.counter_vals[:] = 0.
                for i1 in xrange(self.cur_averaging):
                    self.t0 = time.time()
                    for i1 in xrange(6):
                        if self.active_states[i1]: self.counter_vals[i1] += self.tCounter[i1].read_attribute('Value').value
                    time.sleep(max(0, 1.0 / self.cur_frequency - (time.time() - self.t0)))
                self.counter_vals /= self.cur_averaging
                self.emit(QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), [copy.copy(self.counter_vals)])
            elif self.running == False:
                time.sleep(1.0 / self.cur_frequency)
            if self.terminate_signal:
                break
        return None        



def EH1_EnvironMonitor(parent=None, name='EH1 Environment monitor'):
    app = QtGui.QApplication(sys.argv)
    gui = cEH1EnvMonitor(QtGui.QMainWindow(), name=name)
    gui.PollingThread = EH1EnvThread(gui.main)
    gui.PollingThread.start()
    gui._initialize()
    gui.show()
    if sys.platform == 'win32' or sys.platform == 'win64':
        sys.exit(app.exec_())
    else:
        app.exec_()


if __name__ == "__main__":
    EH1_EnvironMonitor()
