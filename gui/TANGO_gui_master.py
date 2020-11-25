import os
import sys
import time

import numpy
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic as QtUic
from PyQt5.QtCore import pyqtSignal

import p05.tools.misc as misc
from p05.gui.TANGO_deviceForm import cTANGOdevice


class cTANGOgui(QtWidgets.QMainWindow):

    def __init__(self, parent, devices=[], groups=[], name='TANGO motor GUI', geometry=None):
        super(cTANGOgui, self).__init__()
        self.main = parent

        _path = misc.GetPath('TANGO_ui.ui')
        print(_path)
        QtUic.loadUi(_path, self)
        self.setWindowIcon(QtGui.QIcon(os.path.split(_path)[0] + os.sep + 'tango.png'))
        self.setWindowTitle(name)
        if geometry != None:
            self.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
            self.windowsize = geometry
        else:
            self.setGeometry(15, 35, 1790, 1110)
            self.windowsize = [15, 35, 1790, 1110]

        self._initialize(devices, groups)
        
        # QtCore.QObject.connect(self.but_TANGO_pollingDelay, QtCore.SIGNAL('clicked()'), self.clickButtonPollingDelay)
        self.but_TANGO_pollingDelay.clicked.connect(self.clickButtonPollingDelay)
        # QtCore.QObject.connect(self.but_TANGO_polling, QtCore.SIGNAL('clicked()'), self.clickButtonSwitchPolling)
        self.but_TANGO_polling.clicked.connect(self.clickButtonSwitchPolling)
        return None
    
    def _initialize(self, devices, groups):
        """
        Further initialization routines, for better readability not included in __init__
        """
        self.global_TANGOactive = False
        self.global_delay = 250
        
        self.button_style = """QPushButton{border: solid; border-bottom-color: #777777; border-bottom-width: 2px; border-right-color:#777777;\
                               border-right-width: 2px; border-top-color:#AAAAAA; border-top-width: 1px; border-left-color:#AAAAAA;\
                               border-left-width: 1px; border-radius: 3px; padding: 1px;  background: qlineargradient(x1: 0, y1: \
                               0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}\
                               QPushButton:pressed{background:qlineargradient(x1: 0, y1: \
                               0, x2: 0, y2: 1, stop: 0 #dadada, stop: 0.4 #d4d4d4, stop: 0.5 #c7c7c7, stop: 1.0 #dadada) }"""
        
        self.stdfontbold = QtGui.QFont()
        self.stdfontbold.setFamily("Arial")
        self.stdfontbold.setPointSize(11)
        self.stdfontbold.setBold(True)
        self.stdfontbold.setWeight(75)

        self.but_TANGO_polling.setStyleSheet(self.button_style)
        self.but_TANGO_pollingDelay.setStyleSheet(self.button_style)
        
        self.floatValidator = QtGui.QDoubleValidator(self)
        self.floatValidator.setRange(-360., 360.)
        self.palette_red = QtGui.QPalette()
        self.palette_red.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
        
        self.palette_green = QtGui.QPalette()
        self.palette_green.setColor(QtGui.QPalette.Foreground, QtCore.Qt.green)
        
        self.palette_blk = QtGui.QPalette()
        self.palette_blk.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)

        self.label_TANGO_polling.setPalette(self.palette_red)
        self.label_TANGO_polling.setText('inactive')
        
        self.stdfont = QtGui.QFont()
        self.stdfont.setFamily("Arial")
        self.stdfont.setPointSize(10)
        
        self.devices = numpy.empty(len(devices), dtype=object)
        self.motor_posx = numpy.zeros((len(devices)))
        self.motor_posy = numpy.zeros((len(devices)))
        self.motor_heights = numpy.zeros((len(devices)))
        self.motor_bgcolor = numpy.empty(len(devices), dtype=object)

        for i1 in range(self.devices.size):
            self.motor_heights[i1] = devices[i1].get('NumAttributes', 4) * 23 + 23
            if devices[i1].get('ShowRelMovementPanel', True) and not devices[i1].get('ReadOnly', False): self.motor_heights[i1] += 26
            if devices[i1].get('ShowCommands', True) and not devices[i1].get('ReadOnly', False): self.motor_heights[i1] += 52
            if 'ZMXdevice' in devices[i1].keys(): self.motor_heights[i1] += 23
                
        self.timer = QtCore.QTime()
        idev = len(devices)
        igrp = numpy.sum([group[1] for group in groups])
        if igrp < idev:
            groups.append(['undefined', idev - igrp, '#FAFAFA'])
            
        self.tmpgroups = []
        x0, y0 = 5, 30
        imotor = 0
        for i1 in range(len(groups)):
            group = groups[i1]
            _name = group[0]
            igroup = group[1]
            ngroup = 0
            newgroup = True
            while ngroup < group[1]:
                while True:
                    dy = 16 + self.motor_heights[imotor:imotor + igroup].sum() + igroup * 5
                    if y0 + dy > self.windowsize[3] - 30: 
                        igroup -= 1
                    else: 
                        break
                
                if igroup <= 0:
                    x0, y0 = x0 + 474, 30
                    igroup = group[1] - ngroup
                else:
                    if not newgroup:
                        _name = group[0] + ' (continued)' 
                    self.tmpgroups.append([_name, igroup, group[2]])
                    ngroup += igroup
                    imotor += igroup
                    igroup = group[1] - ngroup
                    y0 += dy + 10
                    newgroup = False

        self.groups = numpy.r_[[QtWidgets.QGroupBox() for i1 in range(len(self.tmpgroups))]]
        self.group_stylesheet = numpy.empty(len(self.tmpgroups), dtype=object)
        
        x0, y0 = 5, 30
        imotor = 0
        for i1 in range(self.groups.size):
            group = self.tmpgroups[i1]
            group[1] = int(group[1])
            self.groups[i1] = (QtWidgets.QGroupBox(self))
            self.groups[i1].setFlat(True)
             
            dy = 16 + self.motor_heights[imotor:imotor + group[1]].sum() + group[1] * 5
            if y0 + dy > self.windowsize[3] - 30: 
                y0, x0 = 30, x0 + 474
            self.groups[i1].setFont(self.stdfont)
            self.groups[i1].setTitle(group[0])
            self.groups[i1].setGeometry(QtCore.QRect(x0, y0, 469, dy))
            self.group_stylesheet[i1] = """QGroupBox{background-color:%s}""" % group[2]
            self.groups[i1].setStyleSheet(self.group_stylesheet[i1])
            self.motor_posy[imotor:imotor + group[1]] = 20 + y0 + numpy.r_[
                [[self.motor_heights[imotor:imotor + i1].sum() for i1 in range(group[1])]]] + numpy.arange(
                group[1]).astype(numpy.int) * 5
            self.motor_posx[imotor:imotor + group[1]] = 3 + x0
            self.motor_bgcolor[imotor:imotor + group[1]] = group[2]
            y0 += dy + 10
            imotor += group[1]

        for i1 in range(self.devices.size):
            dev = devices[i1]
            self.devices[i1] = cTANGOdevice(self, self.motor_posx[i1], self.motor_posy[i1], alias=dev.get('DeviceName'), \
                                            numrows=dev.get('NumAttributes', 4), allowmvr=dev.get('ShowRelMovementPanel', True), \
                                            bgcolor=self.motor_bgcolor[i1], mainatt=dev.get('MainAttribute', None), \
                                            readonly=dev.get('ReadOnly', False), showcmds=dev.get('ShowCommands', True), \
                                            serveraddress=dev.get('TangoAddress'), ZMXdevice=dev.get('ZMXdevice', None))
        
        for motor in self.devices:
                motor.enable(False)
        
        self.io_tango_polling.setValidator(self.floatValidator)
        self.TANGOobjects = numpy.r_[[self.devices[i1].TangoObject for i1 in range(self.devices.size)]]
        return None
    # end _initialize

    
    def clickButtonPollingDelay(self):
        """Set the self.global_delay variable (in ms) """
        try: 
            _txt = self.io_tango_polling.text()
            _val = float(_txt)
            self.label_pmac_pollingvalue.setText(_txt + ' ms')
            self.global_delay = _val
            self.PollingThread.set_delay(self.global_delay * 1e-3) 
        except:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Could not convert the string "%s" to a number.' % _txt,
                                          buttons=QtWidgets.QMessageBox.Ok)
        return None
    
    def clickButtonSwitchPolling(self):
        if self.global_TANGOactive:
            self.label_TANGO_polling.setPalette(self.palette_red)
            self.label_TANGO_polling.setText('inactive')
            self.but_TANGO_polling.setText('Start polling')
            self.global_TANGOactive = False
            self.PollingThread.stop()
            for motor in self.devices:
                motor.enable(False)
        elif self.global_TANGOactive == False:
            self.label_TANGO_polling.setPalette(self.palette_green)
            self.label_TANGO_polling.setText('active')
            self.but_TANGO_polling.setText('Stop polling')
            self.global_TANGOactive = True
            for motor in self.devices:
                motor.enable(True)
            self.PollingThread.restart()
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
    
    def NewUpdate(self, data):
        self.label_timeedit.setTime(QtCore.QTime.currentTime())
        _vals = data[0]
        _states = data[1]
        _zmx = data[2]
        for i1 in range(self.devices.size):
            self.devices[i1].attvalues = _vals[i1]
            self.devices[i1].state = _states[i1]
            if self.devices[i1].ZMXdevice != None:
                self.devices[i1].zmxerrorstatus = _zmx[i1]
        for device in self.devices:
            device.eventLoopUpdate()
        return None




class  TANGOpolling(QtCore.QThread):
    def __init__(self, parentThread, devices, cur_delay=0.25):
        QtCore.QThread.__init__(self, parentThread)
        self.devices = devices
        self.parent = parentThread
        self.devicesize = self.devices.size
        self.devicestates = numpy.empty(self.devicesize, dtype=object)
        self.zmxerrors = numpy.empty(self.devicesize, dtype=object)
        self.updater = QtCore.QTimer()
        self.attvalues = numpy.empty((self.devicesize, 5), dtype=object)
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
        self.readAttributes()
        return None
    
    def cleanUp(self):
        return None
    
    def getUpdate(self):
        return True

class ReadoutThread(TANGOpolling):
    jobFinished = pyqtSignal(object)  # object is [self.attvalues, self.devicestates, self.zmxerrors]

    def __init__(self, parentThread, devices):
        TANGOpolling.__init__(self, parentThread, devices)
        return None

    def readAttributes(self):
        while True:
            if self.running:
                self.t0 = time.time()
                attlist, attformatter = [], []
                for motor in self.devices:
                    attlist.append(motor.attnames)
                    attformatter.append(motor.attformatter)

                for i1 in range(self.devicesize):
                    self.devicestates[i1] = self.devices[i1].TangoObject.state()
                    for i2 in range(len(attlist[i1])):
                        if attlist[i1][i2] != 'None':
                            try:
                                self.attvalues[i1, i2] = self.devices[i1].TangoObject.read_attribute(str(attlist[i1][i2])).value
                            except Exception as e:
                                QtWidgets.QMessageBox.critical(self.parent, 'Error',
                                                               "TANGO exception. Error code:\n%s" % (e),
                                                               buttons=QtWidgets.QMessageBox.Ok)
                                attlist[i1][i2] = 'None'
                                self.devices[i1].window.att_select_buttons[i2].setCurrentIndex(0)
                                self.devices[i1].attnames[i2] = 'None'
                                self.devices[i1].window.num_attributevals[i2].setText('')
                    if self.devices[i1].ZMXdevice != None:
                        self.zmxerrors[i1] = self.devices[i1].ZMXtangoObject.read_attribute('Error').value
                        
                time.sleep(max(0, self.cur_delay - (time.time() - self.t0)))
                # self.emit(QtCore.SIGNAL("jobFinished( PyQt_PyObject )"), [self.attvalues, self.devicestates, self.zmxerrors])
                self.jobFinished.emit([self.attvalues, self.devicestates, self.zmxerrors])
            elif self.running == False:
                time.sleep(1.0 * self.cur_delay)
            if self.terminate_signal:
                break
        
        return None
# class ReadoutThread

    
def TANGOgui(parent=None, devices=None, groups=None, name='TANGO motor GUI', geometry=None):
    app = QtWidgets.QApplication(sys.argv)
    gui = cTANGOgui(parent=QtWidgets.QMainWindow(), devices=devices, groups=groups, name=name, geometry=geometry)
    gui.PollingThread = ReadoutThread(gui.main, gui.devices)
    gui.PollingThread.jobFinished.connect(gui.NewUpdate)
    gui.PollingThread.start()
    gui.show()
    if sys.platform == 'win32' or sys.platform == 'win64':
        sys.exit(app.exec_())
    else:
        app.exec_()




if __name__ == "__main__":
    TANGOgui()
