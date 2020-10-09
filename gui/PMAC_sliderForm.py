import numpy
from PyQt5 import QtCore, QtGui


class cPMACair(QtCore.QObject):
    def __init__(self, _parent, xoffset=0, yoffset=0, bgcolor='#ECECEC', controllerID=3):
        super(cPMACair, self).__init__()
        self.parent = _parent
        self.bgcolor = bgcolor
        self.controllerID = controllerID
        self.pos_window = cSliderAirForm(self, self.parent.tab_positions, _xoffset=xoffset, _yoffset=yoffset, bgcolor=self.bgcolor)
        self.mvr_window = cSliderAirForm(self, self.parent.tab_relativemovement, _xoffset=xoffset, _yoffset=yoffset, bgcolor=self.bgcolor)
        
        # QtCore.QObject.connect(self.pos_window.but_AirOn, QtCore.SIGNAL('clicked()'), self.clickButtonAirOn)
        self.pos_window.but_AirOn.clicked.connect(self.clickButtonAirOn)
        # QtCore.QObject.connect(self.pos_window.but_AirOff, QtCore.SIGNAL('clicked()'), self.clickButtonAirOff)
        self.pos_window.but_AirOff.clicked.connect(self.clickButtonAirOff)
        # QtCore.QObject.connect(self.mvr_window.but_AirOn, QtCore.SIGNAL('clicked()'), self.clickButtonAirOn)
        self.mvr_window.but_AirOn.clicked.connect(self.clickButtonAirOn)
        # QtCore.QObject.connect(self.mvr_window.but_AirOff, QtCore.SIGNAL('clicked()'), self.clickButtonAirOff)
        self.mvr_window.but_AirOff.clicked.connect(self.clickButtonAirOff)
        #QtCore.QObject.connect(self.mvr_window.but_Init, QtCore.SIGNAL('clicked()'), self.clickButtonInitilize())
        
        self.airvars = ['m32', 'm33', 'm34', 'm35']
        self.airvarvalues = numpy.zeros((4))
        self.vacvars = ['m40', 'm42', 'm44', 'm45']
        self.vacvarvalues = numpy.zeros((4))
        return None
    
    def clickButtonAirOn(self):
        print(self.controllerID)
        if self.parent.controllers[self.controllerID].IsReady():
            print(1, 0)
            self.parent.controllers[self.controllerID].GetResponse("Q70 = 18", silent = True)
        return None
    
    def clickButtonAirOff(self):
        if self.parent.controllers[self.controllerID].IsReady():
            print(1, 1)
            self.parent.controllers[self.controllerID].GetResponse("Q70 = 17", silent = True)
        #self.parent.controllers[self.controllerID].WriteVariable('Q70', '17')
        return None
    
    
    def GetVarUpdate(self):
        for i1 in range(4):
            self.airvarvalues[i1] = self.parent.controllers[self.controllerID].ReadVariable(self.airvars[i1])
            self.vacvarvalues[i1] = self.parent.controllers[self.controllerID].ReadVariable(self.vacvars[i1])
        return [self.airvarvalues, self.vacvarvalues]

    def Update(self, index):
        if index == 0: window = self.pos_window
        elif index == 1: window = self.mvr_window
        tmp = self.airvarvalues.sum()
        if tmp == 0:
            window.label_airstatus.setPalette(self.parent.palette_red)
            window.label_airstatus.setText('all off')
        elif 0 < tmp < 4:
            window.label_airstatus.setPalette(self.parent.palette_yellow)
            window.label_airstatus.setText('partially on')
        elif tmp == 4:
            window.label_airstatus.setPalette(self.parent.palette_green)
            window.label_airstatus.setText('all on')
        tmp = self.vacvarvalues.sum()
        if tmp == 0:
            window.label_vacstatus.setPalette(self.parent.palette_red)
            window.label_vacstatus.setText('all off')
        elif 0 < tmp < 4:
            window.label_vacstatus.setPalette(self.parent.palette_yellow)
            window.label_vacstatus.setText('partially on')
        elif tmp == 4:
            window.label_vacstatus.setPalette(self.parent.palette_green)
            window.label_vacstatus.setText('all on')
        return None


        
class cSliderAirForm(QtGui.QWidget):
    def __init__(self, _parent, _tab, _xoffset=0, _yoffset=0, alias='unknown', bgcolor='#ECECEC'):
        super(cSliderAirForm, self).__init__()
        
        self.stdsizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.stdsizePolicy.setHorizontalStretch(0)
        self.stdsizePolicy.setVerticalStretch(0)
        self.stdsizePolicy.setHeightForWidth(_parent.parent.sizePolicy().hasHeightForWidth())
        
        self.parent = _parent
        self.parent_widget = _tab
        self.alias = alias
        self.bg_color = bgcolor
        
        self.label_airname = QtGui.QLabel(self.parent_widget)
        self.label_airname.setObjectName("label_airname")
        self.label_airname.setText('global pressurized air status:')

        self.label_airstatus = QtGui.QLabel(self.parent_widget)
        self.label_airstatus.setObjectName("label_airstatus")
        self.label_airstatus.setText('unknown')
        
        self.label_vacname = QtGui.QLabel(self.parent_widget)
        self.label_vacname.setObjectName("label_vacname")
        self.label_vacname.setText('global low-pressure status:')

        self.label_vacstatus = QtGui.QLabel(self.parent_widget)
        self.label_vacstatus.setObjectName("label_vacstatus")
        self.label_vacstatus.setText('unknown')
        
        #self.label_Init = QtGui.QLabel(self.parent_widget)
        #self.label_Init.setObjectName("label_Init")
        #self.label_Init.setText('Initialization of the sliders:')

        self.labels = [self.label_airname, self.label_airstatus, self.label_vacname, self.label_vacstatus]
        for label in self.labels:
            label.setFont(self.parent.parent.stdfont)
            label.setStyleSheet("""QLabel{background-color:%s;}""" % self.bg_color)

        self.but_AirOn = QtGui.QPushButton(self.parent_widget)
        self.but_AirOn.setFont(self.parent.parent.stdfont)
        self.but_AirOn.setObjectName("but_AirOn")
        self.but_AirOn.setText("activate global air supply")
        self.but_AirOn.setStyleSheet(self.parent.parent.button_style)
        
        self.but_AirOff = QtGui.QPushButton(self.parent_widget)
        self.but_AirOff.setFont(self.parent.parent.stdfont)
        self.but_AirOff.setObjectName("but_AirOff")
        self.but_AirOff.setText("deactive global air supply")
        self.but_AirOff.setStyleSheet(self.parent.parent.button_style)        

        # QtCore.QMetaObject.connectSlotsByName(self.parent_widget)
        # button for initializing the granite slabs
#         self.but_Init = QtGui.QPushButton(self.parent_widget)
#         self.but_Init.setFont(self.parent.parent.stdfont)
#         self.but_Init.setObjectName("but_Init")
#         self.but_Init.setText("Initialize")
#         self.but_Init.setStyleSheet(self.parent.parent.button_style)  
        
        self.label_airname.setGeometry(QtCore.QRect(22 + _xoffset, 2 + _yoffset, 190, 21))
        self.label_airstatus.setGeometry(QtCore.QRect(213 + _xoffset, 2 + _yoffset, 101, 21))
        
        self.label_vacname.setGeometry(QtCore.QRect(22 + _xoffset, 22 + _yoffset, 190, 21))
        self.label_vacstatus.setGeometry(QtCore.QRect(213 + _xoffset, 22 + _yoffset, 71, 21))
        
        self.but_AirOn.setGeometry(QtCore.QRect(22 + _xoffset, 44 + _yoffset, 189, 21))
        self.but_AirOff.setGeometry(QtCore.QRect(213 + _xoffset, 44 + _yoffset, 193, 21))
        
        #self.label_Init.setGeometry(QtCore.QRect(22 + _xoffset, 66 + _yoffset, 193, 21))
        #self.but_Init.setGeometry(QtCore.QRect(213 + _xoffset, 66 + _yoffset, 193, 21))
        return None
# ##end class PMACair



class cPMACslider(QtCore.QObject):
    def __init__(self, _parent, _xoffset=0, _yoffset=0, alias='unknown', controllerID=None, sliderID=None, \
                 lowerlimit=-10000, upperlimit=10000, bgcolor='#ECECEC', motorindex=-1):
        
        super(cPMACslider, self).__init__()
        self.parent = _parent
        self.alias = alias
        self.controllerID = controllerID
        self.sliderID = sliderID
        if self.sliderID in [1,2,3,4]:
            self.setPosVar = ['Q77', 'Q78', 'Q79', 'Q71'][self.sliderID-1]
            self.isPosVar = ['Q87', 'Q88', 'Q89', 'Q81'][self.sliderID-1]
            self.cmdAirOn = ['Q70 = 118', 'Q70 = 128', 'Q70 = 138', 'Q70 = 148'][self.sliderID-1]
            self.cmdAirOff = ['Q70 = 117', 'Q70 = 127', 'Q70 = 137', 'Q70 = 147'][self.sliderID-1]
            self.cmdMoveSolo = ['Q70 = 114', 'Q70 = 124', 'Q70 = 134', 'Q70 = 144'][self.sliderID-1]
            self.cmdMoveAll = 'Q70 = 4'
            self.airVar = ['M32', 'M33', 'M34', 'M35'][self.sliderID-1]
            self.vacVar = ['M40', 'M42', 'M44', 'M45'][self.sliderID-1]
        elif self.sliderID not in [1, 2, 3, 4]:
            QtGui.QMessageBox.warning(self.parent, 'Warning', 'The slider number %i is unknown..' % self.sliderID, QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            return None
        
        self.lowerlimit = lowerlimit
        self.upperlimit = upperlimit
        self.bgcolor = bgcolor
        self.motorindex = motorindex

        self.pos_window = cSliderPositionForm(self, self.parent.tab_positions, _xoffset=_xoffset, _yoffset=_yoffset, alias=alias, bgcolor=self.bgcolor)
        self.mvr_window = cSliderRelMoveForm(self, self.parent.tab_relativemovement, _xoffset=_xoffset, _yoffset=_yoffset, alias=alias, bgcolor=self.bgcolor)
        
        # QtCore.QObject.connect(self.pos_window.but_moveSolo, QtCore.SIGNAL('clicked()'), self.clickButtonMoveSolo)
        self.pos_window.but_moveSolo.clicked.connect(self.clickButtonMoveSolo)
        # QtCore.QObject.connect(self.pos_window.but_moveAll, QtCore.SIGNAL('clicked()'), self.clickButtonMoveAll)
        self.pos_window.but_moveAll.clicked.connect(self.clickButtonMoveAll)
        # QtCore.QObject.connect(self.pos_window.but_setnewtarget, QtCore.SIGNAL('clicked()'), self.clickButtonSetNewTarget)
        self.pos_window.but_setnewtarget.clicked.connect(self.clickButtonSetNewTarget)
        # QtCore.QObject.connect(self.pos_window.but_activateAir, QtCore.SIGNAL('clicked()'), self.clickButtonAirOn)
        self.pos_window.but_activateAir.clicked.connect(self.clickButtonAirOn)
        # QtCore.QObject.connect(self.pos_window.but_deactivateAir, QtCore.SIGNAL('clicked()'), self.clickButtonAirOff)
        self.pos_window.but_deactivateAir.clicked.connect(self.clickButtonAirOff)
        # QtCore.QObject.connect(self.mvr_window.but_moverel_pos, QtCore.SIGNAL('clicked()'), self.clickButtonMoveRelPos)
        self.mvr_window.but_moverel_pos.clicked.connect(self.clickButtonMoveRelPos)
        # QtCore.QObject.connect(self.mvr_window.but_moverel_neg, QtCore.SIGNAL('clicked()'), self.clickButtonMoveRelNeg)
        self.mvr_window.but_moverel_neg.clicked.connect(self.clickButtonMoveRelNeg)
        # QtCore.QObject.connect(self.mvr_window.but_activateAir, QtCore.SIGNAL('clicked()'), self.clickButtonAirOn)
        self.mvr_window.but_activateAir.clicked.connect(self.clickButtonAirOn)
        # QtCore.QObject.connect(self.mvr_window.but_deactivateAir, QtCore.SIGNAL('clicked()'), self.clickButtonAirOff)
        self.mvr_window.but_deactivateAir.clicked.connect(self.clickButtonAirOff)
        
        self.ActivateMotor(False)
        
        self.statusPalette = [self.parent.palette_green, self.parent.palette_blk, self.parent.palette_red]
        self.statusText = ['moving', 'idle', 'error']
        self.airPalette = [self.parent.palette_red, self.parent.palette_green]
        self.airText = ['off', 'on']
        return None

    def ActivateMotor(self, activationState):
        self.pos_window.but_moveAll.setEnabled(activationState)
        self.pos_window.but_moveSolo.setEnabled(activationState)
        self.pos_window.but_setnewtarget.setEnabled(activationState)
        self.pos_window.but_activateAir.setEnabled(activationState)
        self.pos_window.but_deactivateAir.setEnabled(activationState)
        
        self.mvr_window.but_moverel_pos.setEnabled(activationState)
        self.mvr_window.but_moverel_neg.setEnabled(activationState)
        self.mvr_window.box_delta.setEnabled(activationState)
        self.mvr_window.but_activateAir.setEnabled(activationState)
        self.mvr_window.but_deactivateAir.setEnabled(activationState)
        return None

    def clickButtonMoveSolo(self):
        """Method to set the target variable from the input box and start the movement of the solo motor."""
        _txt= self.pos_window.io_newtarget.text()
        if self.parent.controllerFaultB[self.controllerID] == True:
            QtGui.QMessageBox.warning(self.parent, 'Warning', 'Cannot move the motor "%s" while PMAC in unacknowledged error state.' %self.alias, QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            return None
        if _txt not in ['', '.', ','] and self.parent.global_pmacsconnected:
            _val = float(_txt)
            if self.lowerlimit <= _val <= self.upperlimit:
                self.pos_window.num_targetpos.setText('%.4f' %_val)
                if self.parent.controllers[self.controllerID].IsReady():
                    self.parent.controllers[self.controllerID].WriteVariable(self.setPosVar, _val)
                    self.parent.controllers[self.controllerID].GetResponse(self.cmdMoveSolo, silent = True)
            else:
                QtGui.QMessageBox.warning(self.parent, 'Warning', "The number %.4f is out of bounds of the accessible position range." %_val, QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
                self.pos_window.io_newtarget.setText('')
                return None
        return None

    def clickButtonMoveAll(self):
        if self.parent.controllers[self.controllerID].IsReady():
            self.parent.controllers[self.controllerID].GetResponse(self.cmdMoveAll, silent = True)
        return None
        
    def clickButtonSetNewTarget(self):
        _txt = self.pos_window.io_newtarget.text().replace(',', '.')
        self.mvr_window.box_delta.setValue(0)
        if _txt not in ['', '.', ','] and self.parent.global_pmacsconnected:
            _val = float(_txt)
            if self.lowerlimit <= _val <= self.upperlimit:
                self.parent.controllers[self.controllerID].WriteVariable(self.setPosVar, _val)
                self.pos_window.num_targetpos.setText('%.4f' % _val)
            else:
                QtGui.QMessageBox.warning(self.parent, 'Warning', "The number %.4f is out of bounds of the accessible position range." % _val, QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
                self.pos_window.io_newtarget.setText('')
                return None
        return None

    def clickButtonAirOn(self):
        self.parent.controllers[self.controllerID].GetResponse(self.cmdAirOn, silent = True)
        return None

    def clickButtonAirOff(self):
        self.parent.controllers[self.controllerID].GetResponse(self.cmdAirOff, silent = True)
        return None
    
    def clickButtonMoveRelPos(self):
        self.moveRel(1.0)
        return None
    
    def clickButtonMoveRelNeg(self):
        self.moveRel(-1.0)
        return None
    
    
    
    def moveRel(self, factor):
        if self.parent.controllerFaultB[self.controllerID] == True:
            QtGui.QMessageBox.warning(self.parent, 'Warning', 'Cannot move the motor "%s" while PMAC in unacknowledged error state.' % self.alias, QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            return None
        self.dpos = float(self.mvr_window.box_delta.text().replace(',', '.'))
        if self.parent.controllers[self.controllerID].IsReady():
            self.pos = self.parent.controllers[self.controllerID].ReadVariable(self.isPosVar)
            self.parent.controllers[self.controllerID].WriteVariable(self.setPosVar, self.pos + factor * self.dpos)
            self.parent.controllers[self.controllerID].GetResponse(self.setCommand, silent = True)
        return None
        
    
    def eventLoopUpdate(self, index=0, pos=None, targetpos=None, airstatus = None, vacstatus = None):
        """Method for updating the motor widgets. "index" is the index of the active tab."""
        if pos == None:
            self.pos = self.parent.controllers[self.controllerID].ReadVariable(self.isPosVar)
        else:
            self.pos = pos
        if targetpos == None:
            self.targetpos = self.parent.controllers[self.controllerID].ReadVariable(self.setPosVar)
        else:
            self.targetpos = targetpos
        if abs(self.pos) < 1e-4: self.pos = abs(self.pos)
        self.pos_window.num_targetpos.setText('%.4f' % self.targetpos)
        
        tmp = self.parent.controllerStatus[self.controllerID]
        if index == 0: window = self.pos_window
        elif index == 1: window = self.mvr_window
        window.num_curpos.setText('%.4f' % self.pos)

        if tmp not in [0,1]: tmp = 2
        window.label_status.setPalette(self.statusPalette[int(tmp)])
        window.label_status.setText(self.statusText[int(tmp)])
        window.label_airstatus.setPalette(self.airPalette[int(airstatus)])
        window.label_airstatus.setText(self.airText[int(airstatus)])
        window.label_vacstatus.setPalette(self.airPalette[int(vacstatus)])
        window.label_vacstatus.setText(self.airText[int(vacstatus)])
        return None


class cSliderPositionForm(QtGui.QWidget):
    def __init__(self, _parent, _tab, _xoffset=0, _yoffset=0, alias='unknown', controllerID=None, setCommand=None, \
                 setPosVar=None, isPosVar=None, bgcolor='#ECECEC'):
        super(cSliderPositionForm, self).__init__()
        
        self.stdsizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.stdsizePolicy.setHorizontalStretch(0)
        self.stdsizePolicy.setVerticalStretch(0)
        self.stdsizePolicy.setHeightForWidth(_parent.parent.sizePolicy().hasHeightForWidth())
        
        self.parent = _parent
        self.parent_widget = _tab
        self.alias = alias
        self.controllerID = controllerID
        self.setCommand = setCommand
        self.setPosVar = setPosVar
        self.isPosVar = isPosVar
        self.bg_color = bgcolor
        
        self.label_name = QtGui.QLabel(self.parent_widget)
        self.label_name.setObjectName("label_name")
        self.label_name.setText(self.alias)
    
        self.label_status = QtGui.QLabel(self.parent_widget)
        self.label_status.setObjectName("label_status")
        self.label_status.setText("disconnected")

        self.label_airname = QtGui.QLabel(self.parent_widget)
        self.label_airname.setObjectName("label_airname")
        self.label_airname.setText('pressurized air:')
        
        self.label_airstatus = QtGui.QLabel(self.parent_widget)
        self.label_airstatus.setObjectName("label_airstatus")
        self.label_airstatus.setText('???')

        self.label_vacname = QtGui.QLabel(self.parent_widget)
        self.label_vacname.setObjectName("label_vacname")
        self.label_vacname.setText('low-pressure:')
        
        self.label_vacstatus = QtGui.QLabel(self.parent_widget)
        self.label_vacstatus.setObjectName("label_vacstatus")
        self.label_vacstatus.setText('???')

        self.label_curpos = QtGui.QLabel(self.parent_widget)
        self.label_curpos.setObjectName("label_curpos")
        self.label_curpos.setText("Current position:")
        
        self.num_curpos = QtGui.QLabel(self.parent_widget)
        self.num_curpos.setObjectName("num_curpos")
        self.num_curpos.setText("???")

        self.label_targetpos = QtGui.QLabel(self.parent_widget)
        self.label_targetpos.setObjectName("label_targetpos")
        self.label_targetpos.setText("Target position:")
        
        self.num_targetpos = QtGui.QLabel(self.parent_widget)
        self.num_targetpos.setObjectName("num_targetpos")
        self.num_targetpos.setText("???")

        self.label_controllerID = QtGui.QLabel(self.parent_widget)
        self.label_controllerID.setObjectName("label_controllerID")
        self.label_controllerID.setText("(Controller %i)" %self.parent.controllerID)
        
        self.labels = [self.label_name, self.label_status, self.label_curpos, self.label_targetpos, self.num_curpos, self.num_targetpos, \
                      self.label_airname, self.label_airstatus, self.label_vacname, self.label_vacstatus, self.label_controllerID]
        for label in self.labels:
            label.setStyleSheet("""QLabel{background-color:%s;}""" % self.bg_color)
            label.setFont(self.parent.parent.stdfont)
        self.label_name.setFont(self.parent.parent.stdfontbold)
        self.label_controllerID.setFont(self.parent.parent.stdfontsmall)

        self.io_newtarget = QtGui.QLineEdit(self.parent_widget)
        self.io_newtarget.setSizePolicy(self.stdsizePolicy)
        self.io_newtarget.setFont(self.parent.parent.stdfont)
        self.io_newtarget.setObjectName("io_newtarget")
        self.io_newtarget.setValidator(_parent.parent.floatValidator)
        self.io_newtarget.setStyleSheet(self.parent.parent.textbox_style)
        
        self.but_setnewtarget = QtGui.QPushButton(self.parent_widget)
        self.but_setnewtarget.setObjectName("but_setnewtarget")
        self.but_setnewtarget.setText("Set target")
        self.but_setnewtarget.hide()

        self.but_moveSolo = QtGui.QPushButton(self.parent_widget)
        self.but_moveSolo.setObjectName("but_moveSolo")
        self.but_moveSolo.setText("solo move")

        self.but_moveAll = QtGui.QPushButton(self.parent_widget)
        self.but_moveAll.setObjectName("but_moveAll")
        self.but_moveAll.setText("move all")

        self.but_activateAir = QtGui.QPushButton(self.parent_widget)
        self.but_activateAir.setObjectName("but_activateAir")
        self.but_activateAir.setText('activate air supply')

        self.but_deactivateAir = QtGui.QPushButton(self.parent_widget)
        self.but_deactivateAir.setObjectName("but_deactivateAir")
        self.but_deactivateAir.setText('deactivate air supply')

        for obj in [self.but_setnewtarget,self.but_moveSolo, self.but_moveAll, self.but_activateAir, self.but_deactivateAir]: 
            obj.setFont(self.parent.parent.stdfont)
            obj.setStyleSheet(self.parent.parent.button_style)

       #_yoffset += 20
        self.label_name.setGeometry(QtCore.QRect(2 + _xoffset, 2 + _yoffset, 151, 21))
        self.label_status.setGeometry(QtCore.QRect(122 + _xoffset, 1 + _yoffset, 101, 21))
        self.label_controllerID.setGeometry(QtCore.QRect(320 + _xoffset, 0 + _yoffset, 70, 21))
        
        self.label_airname.setGeometry(QtCore.QRect(2 + _xoffset, 21 + _yoffset, 101, 21))
        self.label_airstatus.setGeometry(QtCore.QRect(122 + _xoffset, 21 + _yoffset, 101, 21))
        self.but_activateAir.setGeometry(QtCore.QRect(193 + _xoffset, 21 + _yoffset, 197, 21))
        
        self.label_vacname.setGeometry(QtCore.QRect(2 + _xoffset, 42 + _yoffset, 101, 21))
        self.label_vacstatus.setGeometry(QtCore.QRect(122 + _xoffset, 42 + _yoffset, 101, 21))
        self.but_deactivateAir.setGeometry(QtCore.QRect(193 + _xoffset, 42 + _yoffset, 197, 21))
        
        self.label_curpos.setGeometry(QtCore.QRect(2 + _xoffset, 63 + _yoffset, 111, 21))
        self.num_curpos.setGeometry(QtCore.QRect(122 + _xoffset, 63 + _yoffset, 71, 21))
        
        self.label_targetpos.setGeometry(QtCore.QRect(2 + _xoffset, 84 + _yoffset, 105, 21))
        self.num_targetpos.setGeometry(QtCore.QRect(122 + _xoffset, 84 + _yoffset, 71, 21))
        
        self.io_newtarget.setGeometry(QtCore.QRect(193 + _xoffset, 80 + _yoffset, 81, 21))
        self.but_moveSolo.setGeometry(QtCore.QRect(280 + _xoffset, 80 + _yoffset, 110, 21))
        
        self.but_moveAll.setGeometry(QtCore.QRect(280 + _xoffset, 101 + _yoffset, 110, 21))
        self.but_setnewtarget.setGeometry(QtCore.QRect(193 + _xoffset, 101 + _yoffset, 81, 21))
        return None


class cSliderRelMoveForm(QtGui.QWidget):
    def __init__(self, _parent, _tab, _xoffset=0, _yoffset=0, alias='unknown', controllerID=None, setCommand=None, \
                 setPosVar=None, isPosVar=None, bgcolor='#ECECEC'):
        super(cSliderRelMoveForm, self).__init__()
        
        self.stdsizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.stdsizePolicy.setHorizontalStretch(0)
        self.stdsizePolicy.setVerticalStretch(0)
        self.stdsizePolicy.setHeightForWidth(_parent.parent.sizePolicy().hasHeightForWidth())
        
        self.parent = _parent
        self.parent_widget = _tab
        self.alias = alias
        self.controllerID = controllerID
        self.setCommand = setCommand
        self.setPosVar = setPosVar
        self.isPosVar = isPosVar
        self.bg_color = bgcolor
        
        self.label_name = QtGui.QLabel(self.parent_widget)
        self.label_name.setObjectName("label_name")
        self.label_name.setText(self.alias)
    
        self.label_status = QtGui.QLabel(self.parent_widget)
        self.label_status.setObjectName("label_status")
        self.label_status.setText("disconnected")

        self.label_airname = QtGui.QLabel(self.parent_widget)
        self.label_airname.setObjectName("label_airname")
        self.label_airname.setText('pressurized air:')
        
        self.label_airstatus = QtGui.QLabel(self.parent_widget)
        self.label_airstatus.setObjectName("label_airstatus")
        self.label_airstatus.setText('???')

        self.label_vacname = QtGui.QLabel(self.parent_widget)
        self.label_vacname.setObjectName("label_vacname")
        self.label_vacname.setText('low-pressure:')
        
        self.label_vacstatus = QtGui.QLabel(self.parent_widget)
        self.label_vacstatus.setObjectName("label_vacstatus")
        self.label_vacstatus.setText('???')

        self.label_curpos = QtGui.QLabel(self.parent_widget)
        self.label_curpos.setObjectName("label_curpos")
        self.label_curpos.setText("Current position:")
        
        self.num_curpos = QtGui.QLabel(self.parent_widget)
        self.num_curpos.setObjectName("num_curpos")
        self.num_curpos.setText("???")

        self.label_moverelby = QtGui.QLabel(self.parent_widget)
        self.label_moverelby.setObjectName("label_moverelby")
        self.label_moverelby.setText("Move relative by:")

        self.label_controllerID = QtGui.QLabel(self.parent_widget)
        self.label_controllerID.setObjectName("label_controllerID")
        self.label_controllerID.setText("(Controller %i)" %self.parent.controllerID)
        
        for obj in [self.label_name, self.label_status, self.label_curpos, self.num_curpos, \
                      self.label_airname, self.label_airstatus, self.label_vacname, self.label_vacstatus, self.label_moverelby, self.label_controllerID ]:
            obj.setStyleSheet("""QLabel{background-color:%s;}""" % self.bg_color)
            obj.setFont(self.parent.parent.stdfont)
        self.label_name.setFont(self.parent.parent.stdfontbold)
        self.label_controllerID.setFont(self.parent.parent.stdfontsmall)

        self.box_delta = QtGui.QDoubleSpinBox(self.parent_widget)
        self.box_delta.setSizePolicy(self.stdsizePolicy)
        self.box_delta.setFont(self.parent.parent.stdfont)
        self.box_delta.setSuffix("")
        self.box_delta.setDecimals(4)
        self.box_delta.setMaximum(1.0)
        self.box_delta.setSingleStep(0.001)
        self.box_delta.setObjectName("box_delta")
        self.box_delta.setToolTip('The maximum allowed step width is "1.0". Only numerical input is allowed.')
        self.box_delta.setStyleSheet(self.parent.parent.spin_style)
        
        self.but_moverel_pos = QtGui.QPushButton(self.parent_widget)
        self.but_moverel_pos.setObjectName("but_moverel_pos")
        self.but_moverel_pos.setText("positive")
        
        self.but_moverel_neg = QtGui.QPushButton(self.parent_widget)
        self.but_moverel_neg.setObjectName("but_moverel_neg")
        self.but_moverel_neg.setText("negative")

        self.but_activateAir = QtGui.QPushButton(self.parent_widget)
        self.but_activateAir.setObjectName("but_activateAir")
        self.but_activateAir.setText('activate air supply')

        self.but_deactivateAir = QtGui.QPushButton(self.parent_widget)
        self.but_deactivateAir.setObjectName("but_deactivateAir")
        self.but_deactivateAir.setText('deactivate air supply')

        for obj in [self.but_moverel_pos, self.but_moverel_neg, self.but_activateAir, self.but_deactivateAir]:
            obj.setFont(self.parent.parent.stdfont)
            obj.setStyleSheet(self.parent.parent.button_style)
            
        self.label_name.setGeometry(QtCore.QRect(2 + _xoffset, 2 + _yoffset, 151, 21))
        self.label_status.setGeometry(QtCore.QRect(122 + _xoffset, 1 + _yoffset, 101, 21))
        self.label_controllerID.setGeometry(QtCore.QRect(320 + _xoffset, 0 + _yoffset, 70, 21))
        
        self.label_airname.setGeometry(QtCore.QRect(2 + _xoffset, 21 + _yoffset, 101, 21))
        self.label_airstatus.setGeometry(QtCore.QRect(122 + _xoffset, 21 + _yoffset, 101, 21))
        self.but_activateAir.setGeometry(QtCore.QRect(193 + _xoffset, 21 + _yoffset, 197, 21))
        
        self.label_vacname.setGeometry(QtCore.QRect(2 + _xoffset, 42 + _yoffset, 101, 21))
        self.label_vacstatus.setGeometry(QtCore.QRect(122 + _xoffset, 42 + _yoffset, 101, 21))
        self.but_deactivateAir.setGeometry(QtCore.QRect(193 + _xoffset, 42 + _yoffset, 197, 21))
        
        self.label_curpos.setGeometry(QtCore.QRect(2 + _xoffset, 60 + _yoffset, 111, 21))
        self.num_curpos.setGeometry(QtCore.QRect(122 + _xoffset, 60 + _yoffset, 71, 21))
        
        self.label_moverelby.setGeometry(QtCore.QRect(2 + _xoffset, 81 + _yoffset, 107, 21))
        self.box_delta.setGeometry(QtCore.QRect(122 + _xoffset, 81 + _yoffset, 68, 21))
        self.but_moverel_pos.setGeometry(QtCore.QRect(295 + _xoffset, 81 + _yoffset, 95, 21))
        self.but_moverel_neg.setGeometry(QtCore.QRect(194 + _xoffset, 81 + _yoffset, 95, 21))
        return None
