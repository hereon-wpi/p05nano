from PyQt4 import QtCore, QtGui
import time
import numpy


class cPMACmotor(QtCore.QObject):
    def __init__(self, _parent, _xoffset =0, _yoffset = 0, alias = 'unknown', controllerID = None, setCommand = None, \
                 setPosVar = None, isPosVar = None, lowerlimit = -10000, upperlimit = 10000, bgcolor='#ECECEC', motorindex = -1):
        super(cPMACmotor, self).__init__()
        self.parent = _parent
        self.alias = alias
        self.controllerID = controllerID
        self.setCommand = setCommand
        self.setPosVar = setPosVar
        self.isPosVar = isPosVar
        self.lowerlimit = lowerlimit
        self.upperlimit = upperlimit
        self.bgcolor = bgcolor
        self.motorindex = motorindex

        self.pos_window = cMotorPositionForm(self, self.parent.tab_positions, _xoffset = _xoffset, _yoffset = _yoffset, alias = alias, bgcolor = self.bgcolor)
        self.mvr_window = cMotorRelMoveForm(self, self.parent.tab_relativemovement, _xoffset = _xoffset, _yoffset = _yoffset, alias = alias, bgcolor = self.bgcolor)
        
        QtCore.QObject.connect(self.pos_window.but_move, QtCore.SIGNAL('clicked()'), self.clickButtonMove)
#        QtCore.QObject.connect(self.pos_window.but_setnewtarget, QtCore.SIGNAL('clicked()'), self.clickButtonSetNewTarget)
        QtCore.QObject.connect(self.mvr_window.but_moverel_pos, QtCore.SIGNAL('clicked()'), self.clickButtonMoveRelPos)
        QtCore.QObject.connect(self.mvr_window.but_moverel_neg, QtCore.SIGNAL('clicked()'), self.clickButtonMoveRelNeg)
        self.ActivateMotor(False)
        return None
    #end __init__

    
    def ActivateMotor(self, activationState):
        """Method to activate (activationState = True) or deactivate 
        (activationState = False) the motor movement by enabling or
        disabling the motor buttons."""
        self.pos_window.but_move.setEnabled(activationState)
        self.mvr_window.but_moverel_pos.setEnabled(activationState)
        self.mvr_window.but_moverel_neg.setEnabled(activationState)
        self.mvr_window.box_delta.setEnabled(activationState)
        self.pos_window.but_setnewtarget.setEnabled(activationState)
        return None
    #end ActivateMotor


    def clickButtonMove(self):
        """Method to set the target variable from the input box and start the movement of the coordinate system."""
        _txt= self.pos_window.io_newtarget.text().replace(',', '.')
        self.mvr_window.box_delta.setValue(0)
        if self.parent.controllerFaultB[self.controllerID] == True:
            QtGui.QMessageBox.warning(self.parent, 'Warning', 'Cannot move the motor "%s" while PMAC in unacknowledged error state.' %self.alias, QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            return None
        if _txt not in ['', '.', ','] and self.parent.global_pmacsconnected:
            _val = float(_txt)
            if self.lowerlimit <= _val <= self.upperlimit:
                self.pos_window.num_targetpos.setText('%.4f' %_val)
                self.pos_window.num_curpos.setText('%.4f' %_val)
                if self.parent.controllers[self.controllerID].IsReady():
                    self.parent.controllers[self.controllerID].WriteVariable(self.setPosVar, _val)
                    self.parent.controllers[self.controllerID].GetResponse(self.setCommand)
            else:
                QtGui.QMessageBox.warning(self.parent, 'Warning', "The number %.4f is out of bounds of the accessible position range. (%f, %f)" %(_val, self.lowerlimit, self.upperlimit), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
                self.pos_window.io_newtarget.setText('')
                return None
        return None
    #end clickButtonMove
        
    def clickButtonSetNewTarget(self):
        """Method to set a new target variable without starting a movement."""
        _txt= self.pos_window.io_newtarget.text().replace(',', '.')
        self.mvr_window.box_delta.setValue(0)
        if _txt not in ['', '.', ','] and self.parent.global_pmacsconnected:
            _val = float(_txt)
            if self.lowerlimit <= _val <= self.upperlimit:
                self.parent.controllers[self.controllerID].WriteVariable(self.setPosVar, _val)
                self.pos_window.num_targetpos.setText('%.4f' %_val)
            else:
                QtGui.QMessageBox.warning(self.parent, 'Warning', "The number %.4f is out of bounds of the accessible position range." %_val, QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
                self.pos_window.io_newtarget.setText('')
                return None
        return None
    #end clickButtonSetNewTarget
    
    def clickButtonMoveRelPos(self):
        self.moveRel(1.0)
        return None
    
    def clickButtonMoveRelNeg(self):
        self.moveRel(-1.0)
        return None
    
    def moveRel(self, factor):
        """Relative movement by value defined in Delta box from current (!!) position.
        Factor determines is movement is positive or negative, i.e. factor = 1 or factor = -1.
        The current position is rounded to 4 significant digits.
        """
        if self.parent.controllerFaultB[self.controllerID] == True:
            QtGui.QMessageBox.warning(self.parent, 'Warning', 'Cannot move the motor "%s" while PMAC in unacknowledged error state.' %self.alias, QtGui.QMessageBox.Ok | QtGui.QMessageBox.Ok)
            return None
        self.dpos = float(self.mvr_window.box_delta.text().replace(',', '.'))
        if self.parent.controllers[self.controllerID].IsReady():
            self.pos = self.parent.controllers[self.controllerID].ReadVariable(self.isPosVar)
            _target = numpy.round(self.pos, decimals = 4) + factor * self.dpos
            self.parent.controllers[self.controllerID].WriteVariable(self.setPosVar, _target)
            self.parent.controllers[self.controllerID].GetResponse(self.setCommand)
        return None
    #end moveRel
    
    def eventLoopUpdate(self, index = 0, pos = None, targetpos = None):
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
        self.pos_window.num_curpos.setText('%.4f' %self.pos)
        self.pos_window.num_targetpos.setText('%.4f' %self.targetpos)
        self.mvr_window.num_curpos.setText('%.4f' %self.pos)
        tmp = self.parent.controllerStatus[self.controllerID]
        if index == 0: window = self.pos_window
        elif index == 1: window = self.mvr_window
        if tmp == 0:
            window.label_status.setPalette(self.parent.palette_green)
            window.label_status.setText('moving')
        elif tmp == 1:
            window.label_status.setPalette(self.parent.palette_blk)
            window.label_status.setText('idle')
        elif tmp not in [0,1]:
            window.label_status.setPalette(self.parent.palette_red)
            window.label_status.setText('error')
        return None
    #end eventLoopUpdate
#endcPMACmotor


def commonInitialization(target):
    """
    Routine to initialize common variables for both position forms.
    """
    target.stdfont = QtGui.QFont()
    target.stdfont.setFamily("Arial")
    target.stdfont.setPointSize(11)
    
    target.stdfontbold = QtGui.QFont()
    target.stdfontbold.setFamily("Arial")
    target.stdfontbold.setPointSize(11)
    target.stdfontbold.setBold(True)
    target.stdfontbold.setWeight(75)
    
    target.stdsizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    target.stdsizePolicy.setHorizontalStretch(0)
    target.stdsizePolicy.setVerticalStretch(0)
    target.stdsizePolicy.setHeightForWidth(target.parent.parent.sizePolicy().hasHeightForWidth())
    
    target.label_name = QtGui.QLabel(target.parent_widget)
    target.label_name.setObjectName("label_name")
    target.label_name.setText(target.alias)
    
    target.label_status = QtGui.QLabel(target.parent_widget)
    target.label_status.setObjectName("label_status")
    target.label_status.setText("disconnected")
    
    target.label_curpos = QtGui.QLabel(target.parent_widget)
    target.label_curpos.setObjectName("label_curpos")
    target.label_curpos.setText("Current position:")
    
    target.num_curpos = QtGui.QLabel(target.parent_widget)
    target.num_curpos.setObjectName("num_curpos")
    target.num_curpos.setText("???")

    for label in [target.label_name, target.label_status, target.label_curpos, target.num_curpos]:
        label.setStyleSheet("""QLabel{background-color:%s;}""" % target.bg_color)
        label.setFont(target.stdfont)

    target.label_name.setFont(target.stdfontbold)
    return target
#end commonInitialization

class cMotorPositionForm(QtGui.QWidget):
    def __init__(self, _parent, _tab, _xoffset =0, _yoffset = 0, alias = 'unknown', bgcolor='#ECECEC'):
        super(cMotorPositionForm, self).__init__()
        
        self.parent = _parent
        self.parent_widget = _tab
        self.alias = alias
        self.bg_color = bgcolor
        
        self.stdsizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.stdsizePolicy.setHorizontalStretch(0)
        self.stdsizePolicy.setVerticalStretch(0)
        self.stdsizePolicy.setHeightForWidth(self.parent.parent.sizePolicy().hasHeightForWidth())
        
        self.label_name = QtGui.QLabel(self.parent_widget)
        self.label_name.setObjectName("label_name")
        self.label_name.setText(self.alias)
        
        self.label_status = QtGui.QLabel(self.parent_widget)
        self.label_status.setObjectName("label_status")
        self.label_status.setText("disconnected")
        
        self.label_curpos = QtGui.QLabel(self.parent_widget)
        self.label_curpos.setObjectName("label_curpos")
        self.label_curpos.setText("Current position:")
        
        self.num_curpos = QtGui.QLabel(self.parent_widget)
        self.num_curpos.setObjectName("num_curpos")
        self.num_curpos.setText("???")
        
        self.label_controllerID = QtGui.QLabel(self.parent_widget)
        self.label_controllerID.setObjectName("label_controllerID")
        self.label_controllerID.setText("(Controller %i)" %self.parent.controllerID)
        
        
        for label in [self.label_name, self.label_status, self.label_curpos, self.num_curpos, self.label_controllerID]:
            label.setStyleSheet("""QLabel{background-color:%s;}""" % self.bg_color)
            label.setFont(self.parent.parent.stdfont)
    
        self.label_name.setFont(self.parent.parent.stdfontbold)
        self.label_controllerID.setFont(self.parent.parent.stdfontsmall)

        self.label_targetpos = QtGui.QLabel(self.parent_widget)
        self.label_targetpos.setObjectName("label_targetpos")
        self.label_targetpos.setText("Target position:")
        
        self.num_targetpos = QtGui.QLabel(self.parent_widget)
        self.num_targetpos.setObjectName("num_targetpos")
        self.num_targetpos.setText("???")
                
        for object in [self.label_targetpos, self.num_targetpos]:
            object.setStyleSheet("""QLabel{background-color:%s;}""" % self.bg_color)
            object.setFont(self.parent.parent.stdfont)    
        
        self.io_newtarget = QtGui.QLineEdit(self.parent_widget)
        self.io_newtarget.setSizePolicy(self.stdsizePolicy)
        self.io_newtarget.setFont(self.parent.parent.stdfont)
        self.io_newtarget.setObjectName("io_newtarget")
        self.io_newtarget.setValidator(_parent.parent.floatValidator)
        self.io_newtarget.setStyleSheet(self.parent.parent.textbox_style)
        
        self.but_setnewtarget = QtGui.QPushButton(self.parent_widget)
        self.but_setnewtarget.setObjectName("but_setnewtarget")
        self.but_setnewtarget.setText("Set new target")
        self.but_setnewtarget.hide()

        self.but_move = QtGui.QPushButton(self.parent_widget)
        self.but_move.setObjectName("but_move")
        self.but_move.setText("Direct move to")

        for object in [self.but_setnewtarget,self.but_move]: 
            object.setFont(self.parent.parent.stdfont)
            object.setStyleSheet(self.parent.parent.button_style)

        self.label_name.setGeometry(QtCore.QRect(2 + _xoffset, 2 + _yoffset, 151, 21))
        self.label_status.setGeometry(QtCore.QRect(122 + _xoffset, 1 + _yoffset, 101, 21))
        self.label_controllerID.setGeometry(QtCore.QRect(320 + _xoffset, 0 + _yoffset, 70, 21))
        
        self.label_curpos.setGeometry(QtCore.QRect(2 + _xoffset, 20 + _yoffset, 111, 21))
        self.num_curpos.setGeometry(QtCore.QRect(122 + _xoffset, 20 + _yoffset, 71, 21))
        #self.but_move.setGeometry(QtCore.QRect(280 + _xoffset, 20 + _yoffset, 110, 21))
        self.but_move.setGeometry(QtCore.QRect(280 + _xoffset, 41 + _yoffset, 110, 21))
        
        self.label_targetpos.setGeometry(QtCore.QRect(2+ _xoffset, 41 + _yoffset, 105, 21))
        self.num_targetpos.setGeometry(QtCore.QRect(122 + _xoffset, 41 + _yoffset, 71, 21))
        self.io_newtarget.setGeometry(QtCore.QRect(193 + _xoffset, 41 + _yoffset, 81, 21))
        #self.but_setnewtarget.setGeometry(QtCore.QRect(280 + _xoffset, 41 + _yoffset, 110, 21))
        return None


class cMotorRelMoveForm(QtGui.QWidget):
    def __init__(self, _parent, _tab, _xoffset =0, _yoffset = 0, alias = 'unknown', controllerID = None, setCommand = None, \
                 setPosVar = None, isPosVar = None, bgcolor='#ECECEC'):
        super(cMotorRelMoveForm, self).__init__()
        
        self.parent = _parent
        self.parent_widget = _tab
        self.alias = alias
        self.controllerID = controllerID
        self.setCommand = setCommand
        self.setPosVar = setPosVar
        self.isPosVar = isPosVar
        self.bg_color = bgcolor
                
        self.stdsizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.stdsizePolicy.setHorizontalStretch(0)
        self.stdsizePolicy.setVerticalStretch(0)
        self.stdsizePolicy.setHeightForWidth(self.parent.parent.sizePolicy().hasHeightForWidth())
        
        self.label_name = QtGui.QLabel(self.parent_widget)
        self.label_name.setObjectName("label_name")
        self.label_name.setText(self.alias)
        
        self.label_status = QtGui.QLabel(self.parent_widget)
        self.label_status.setObjectName("label_status")
        self.label_status.setText("disconnected")
        
        self.label_curpos = QtGui.QLabel(self.parent_widget)
        self.label_curpos.setObjectName("label_curpos")
        self.label_curpos.setText("Current position:")
        
        self.num_curpos = QtGui.QLabel(self.parent_widget)
        self.num_curpos.setObjectName("num_curpos")
        self.num_curpos.setText("???")
    
        self.label_controllerID = QtGui.QLabel(self.parent_widget)
        self.label_controllerID.setObjectName("label_controllerID")
        self.label_controllerID.setText("(Controller %i)" %self.parent.controllerID)
        
        
        for label in [self.label_name, self.label_status, self.label_curpos, self.num_curpos, self.label_controllerID]:
            label.setStyleSheet("""QLabel{background-color:%s;}""" % self.bg_color)
            label.setFont(self.parent.parent.stdfont)
    
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
        
        self.label_moverelby = QtGui.QLabel(self.parent_widget)
        self.label_moverelby.setFont(self.parent.parent.stdfont)
        self.label_moverelby.setObjectName("label_moverelby")
        self.label_moverelby.setText("Move relative by:")
        self.label_moverelby.setStyleSheet("""QLabel{background-color:%s;}""" % self.bg_color)
        
        self.but_moverel_pos = QtGui.QPushButton(self.parent_widget)
        self.but_moverel_pos.setFont(self.parent.parent.stdfont)
        self.but_moverel_pos.setObjectName("but_moverel_pos")
        self.but_moverel_pos.setText("positive")
        self.but_moverel_pos.setStyleSheet(self.parent.parent.button_style)
        
        self.but_moverel_neg = QtGui.QPushButton(self.parent_widget)
        self.but_moverel_neg.setFont(self.parent.parent.stdfont)
        self.but_moverel_neg.setObjectName("but_moverel_neg")
        self.but_moverel_neg.setText("negative")
        self.but_moverel_neg.setStyleSheet(self.parent.parent.button_style)

        #QtCore.QMetaObject.connectSlotsByName(self.parent_widget)

        self.label_name.setGeometry(QtCore.QRect(2 + _xoffset, 2 + _yoffset, 151, 21))
        self.label_status.setGeometry(QtCore.QRect(122 + _xoffset, 1 + _yoffset, 101, 21))
        self.label_controllerID.setGeometry(QtCore.QRect(320 + _xoffset, 0 + _yoffset, 70, 21))
        
        self.label_curpos.setGeometry(QtCore.QRect(2 + _xoffset, 20 + _yoffset, 111, 21))
        self.num_curpos.setGeometry(QtCore.QRect(122 + _xoffset, 20 + _yoffset, 71, 21))
        
        self.label_moverelby.setGeometry(QtCore.QRect(2 + _xoffset, 41 + _yoffset, 107, 21))
        self.box_delta.setGeometry(QtCore.QRect(122 + _xoffset, 41 + _yoffset, 68, 21))
        self.but_moverel_pos.setGeometry(QtCore.QRect(295 + _xoffset, 41 + _yoffset, 95, 21))
        self.but_moverel_neg.setGeometry(QtCore.QRect(194 + _xoffset, 41 + _yoffset, 95, 21))
        return None
