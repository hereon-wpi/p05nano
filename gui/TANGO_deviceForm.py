import PyTango
import numpy
from PyQt5 import QtCore, QtGui


class cTANGOdevice(QtCore.QObject):
    def __init__(self, _parent, _xoffset=0, _yoffset=0, alias='unknown', serveraddress=None, \
                 numrows=3, allowmvr=True, readonly=False, showcmds = False, bgcolor='#ECECEC', \
                 mainatt='Position', ZMXdevice = None):
        """
        Main class for the implementation of TANGO devices in Qt Gui.
        Requird input:
        _parent:    the main widget instance
        _xoffset:   the x position value for the upper left corner
        _yoffset:   the y position value for the upper left corner
        alias:      the alias name for the motor to be displayed
        serveraddress:
                    the TANGO server address
        numrows:    total number of rows for attributes to be shown
        allowmvr:   <True> allows relative movements of the motor 
                    (performed by using push buttons)
        readonly:   <True> blocks all set commands 
        bgcolor:    RGB value for the motor background (typically taken from group box)
        mainatt:    main attribute to be always displayed
        """
        super(cTANGOdevice, self).__init__()
        self.parent = _parent
        self.alias = alias
        self.serveraddress = serveraddress
        self.numrows = max(min(numrows, 5), 1)
        self.allowmvr = allowmvr
        self.readonly = readonly
        self.showcmds = showcmds
        self.attnames = numpy.empty(self.numrows, dtype =object)
        self.attformatter = numpy.empty(self.numrows, dtype =object)
        self.attformatter[:] = '%.5f'
        self.attnames[:] = 'None'
        if mainatt != None: self.attnames[0] = mainatt
        self.attvalues= numpy.empty(self.numrows, dtype =object)
        self.attvalues[:] = None
        self.zmxerrorstatus = ''

        if self.serveraddress == None:
            QtGui.QMessageBox.critical(self, 'Error', 'No TANGO server address selected for the device "%s".' % self.alias, buttons=QtGui.QMessageBox.Ok)
            return None
        self.TangoObject = PyTango.DeviceProxy(self.serveraddress)
        if self.attnames[0] != 'None':
            tmp = self.TangoObject.read_attribute(self.attnames[0])
            if tmp.type in [PyTango.CmdArgType.DevShort, PyTango.CmdArgType.DevLong, PyTango.CmdArgType.DevUShort, \
                            PyTango.CmdArgType.DevULong, PyTango.CmdArgType.DevLong64, PyTango.CmdArgType.DevULong64, \
                            PyTango.CmdArgType.DevInt]: self.attformatter[0] = '%i'
            elif tmp.type in [PyTango.CmdArgType.DevFloat, PyTango.CmdArgType.DevDouble]: self.attformatter[0] = '%.5f'
            elif tmp.type in [PyTango.CmdArgType.DevString, PyTango.CmdArgType.DevVarCharArray, PyTango.CmdArgType.ConstDevString, PyTango.CmdArgType.DevState]: \
                            self.attformatter[0] = '%s'
        tmp = list(self.TangoObject.get_attribute_list())
        tmp.sort()
        tmp.insert(0, 'None')
        self.TangoAttList = numpy.asarray(tmp, dtype = object)
        tmp = self.TangoObject.command_list_query()
        tmp = []
        for item in self.TangoObject.command_list_query(): tmp.append(item.cmd_name)
        tmp.insert(0, 'None')
        self.TangoCmdList = numpy.asarray(tmp, dtype = object)

        self.ZMXdevice = ZMXdevice
        if ZMXdevice != None:
            self.ZMXtangoObject = PyTango.DeviceProxy(self.ZMXdevice)

        self.window = cTANGOdeviceForm(self, self.parent, _xoffset=_xoffset, _yoffset=_yoffset, bgcolor=bgcolor)
        self.height = self.numrows * 25 + 20 
        if self.allowmvr: self.height += 25
        
        if self.attnames[0] == 'None':
            for att in self.TangoAttList: self.window.att_select_buttons[0].addItem(att)
            QtCore.QObject.connect(self.window.att_select_buttons[0], QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo0)
        
        for att in self.TangoAttList: self.window.att_select_buttons[1].addItem(att)
        QtCore.QObject.connect(self.window.att_select_buttons[1], QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo1)
        if self.numrows >= 3:
            for att in self.TangoAttList: self.window.att_select_buttons[2].addItem(att)
            QtCore.QObject.connect(self.window.att_select_buttons[2], QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo2)
        if self.numrows >= 4:
            for att in self.TangoAttList: self.window.att_select_buttons[3].addItem(att)
            QtCore.QObject.connect(self.window.att_select_buttons[3], QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo3)
        if self.numrows >= 5:
            for att in self.TangoAttList: self.window.att_select_buttons[4].addItem(att)
            QtCore.QObject.connect(self.window.att_select_buttons[4], QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCombo4)
        
        if not self.readonly:
            # QtCore.QObject.connect(self.window.att_set_buttons[0], QtCore.SIGNAL('clicked()'), self.clickButtonMove)
            self.window.att_set_buttons[0].clicked.connect(self.clickButtonMove)
            # QtCore.QObject.connect(self.window.att_set_buttons[1], QtCore.SIGNAL('clicked()'), self.clickButton2)
            self.window.att_set_buttons[1].clicked.connect(self.clickButton2)
            if self.numrows >= 3:
                # QtCore.QObject.connect(self.window.att_set_buttons[2], QtCore.SIGNAL('clicked()'), self.clickButton3)
                self.window.att_set_buttons[2].clicked.connect(self.clickButton3)
            if self.numrows >= 4:
                # QtCore.QObject.connect(self.window.att_set_buttons[3], QtCore.SIGNAL('clicked()'), self.clickButton4)
                self.window.att_set_buttons[3].clicked.connect(self.clickButton4)
            if self.numrows == 5:
                # QtCore.QObject.connect(self.window.att_set_buttons[4], QtCore.SIGNAL('clicked()'), self.clickButton5)
                self.window.att_set_buttons[4].clicked.connect(self.clickButton5)
            if self.allowmvr:
                # QtCore.QObject.connect(self.window.but_moverel_pos, QtCore.SIGNAL('clicked()'), self.clickButtonMoveRelPos)
                self.window.but_moverel_pos.clicked.connect(self.clickButtonMoveRelPos)
                # QtCore.QObject.connect(self.window.but_moverel_neg, QtCore.SIGNAL('clicked()'), self.clickButtonMoveRelNeg)
                self.window.but_moverel_neg.clicked.connect(self.clickButtonMoveRelNeg)
            if self.showcmds:
                # QtCore.QObject.connect(self.window.but_send_cmd, QtCore.SIGNAL('clicked()'), self.clickButtonSendCmd)
                self.window.but_send_cmd.clicked.connect(self.clickButtonSendCmd)
                QtCore.QObject.connect(self.window.cmd_selector, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeCmd)
                # QtCore.QObject.connect(self.window.but_clear_cmd, QtCore.SIGNAL('clicked()'), self.clearCmdResponse)
                self.window.but_clear_cmd.clicked.connect(self.clearCmdResponse)
                for item in self.TangoCmdList: self.window.cmd_selector.addItem(item)
        return None

    ############
    ### Olga: controller for a button, not a view thing - move to another file
    ############

    def SetAttribute(self, _index):
        _txt = self.window.io_newvals[_index].text()
        if self.TangoObject.state() == PyTango.DevState.ON:
            try:
                if   self.attformatter[_index] == '%.5f':  _val = float(_txt)
                elif self.attformatter[_index] == '%i':    _val = int(float(_txt))
                elif self.attformatter[_index] == '%s':    _val = str(_txt)
                self.TangoObject.write_attribute(self.attnames[_index], _val)
            except Exception as e:
                self.window.io_newvals[_index].setText('')
                if _txt == '': _txt = '<None>'
                QtGui.QMessageBox.critical(self.parent, 'Error', "The value '%s' could not be written to attribute '%s'. Error code:\n%s" %( _txt, self.attnames[_index], e), buttons = QtGui.QMessageBox.Ok)
        return None

    ############
    ### Olga: controller for a button, not a view thing - move to another file
    ############
    def clickButtonSendCmd(self):
        self.cmd = self.TangoObject.command_query(self.cmd_name)
        if self.cmd.in_type in [PyTango.CmdArgType.DevShort, PyTango.CmdArgType.DevLong, PyTango.CmdArgType.DevUShort, \
                            PyTango.CmdArgType.DevULong, PyTango.CmdArgType.DevLong64, PyTango.CmdArgType.DevULong64, \
                            PyTango.CmdArgType.DevInt]:
            self.cmdformatter = '%i'
            self.cmd_input = int(float(self.window.io_cmd.text()))
        elif self.cmd.in_type in [PyTango.CmdArgType.DevFloat, PyTango.CmdArgType.DevDouble]: 
            self.cmdformatter = '%.5f'
            self.cmd_input = float(self.window.io_cmd.text())
        elif self.cmd.in_type in [PyTango.CmdArgType.DevString, PyTango.CmdArgType.DevVarCharArray, PyTango.CmdArgType.ConstDevString, PyTango.CmdArgType.DevState]:
            self.cmdformatter = '%s'
            self.cmd_input = str(self.window.io_cmd.text())
        elif self.cmd.in_type in [PyTango.CmdArgType.DevVoid]:
            self.cmdformatter = None
            self.cmd_input = None
        
        if self.cmd_input == None or self.cmd_input == '':
            tmp = self.TangoObject.command_inout(self.cmd_name)
        else:
            tmp = self.TangoObject.command_inout(self.cmd_name, cmd_param =  self.cmd_input)
        
        self.window.cmd_response.setText(str(tmp))
        return None
    
    
    def clickButtonMove(self):
        self.SetAttribute(0)
        return None
    
    def clickButton2(self):
        self.SetAttribute(1)
        return None
    
    def clickButton3(self):
        self.SetAttribute(2)
        return None

    def clickButton4(self):
        self.SetAttribute(3)
        return None

    def clickButton5(self):
        self.SetAttribute(4)
        return None

    def MoveRel(self, _factor):
        self.delta = self.window.box_delta.value()
        if self.TangoObject.state() == PyTango.DevState.ON:
            try:
                tmp = self.TangoObject.read_attribute(self.attnames[0]).value + _factor * self.delta
                self.TangoObject.write_attribute(self.attnames[0], tmp)
            except:
                QtGui.QMessageBox.critical(self.parent, 'Error', "The %s could not be changed by %f." %(self.attnames[0], tmp), buttons = QtGui.QMessageBox.Ok)

    def clickButtonMoveRelPos(self):
        self.MoveRel(1.0)
        return None
    
    def clickButtonMoveRelNeg(self):
        self.MoveRel(-1.0)
        return None
    
    def eventLoopUpdate(self):
        if self.parent.global_TANGOactive:
            self.window.label_status.setText(str(self.state))
            if self.ZMXdevice != None:
                self.window.label_zmxerr.setText(self.zmxerrorstatus)
            for i1 in range(self.numrows):
                if self.attnames[i1] != 'None':
                    try:
                        self.window.num_attributevals[i1].setText(self.attformatter[i1] %self.attvalues[i1])
                    except:
                        print(self.attnames[i1], self.attformatter[i1], self.attvalues[i1])
                        print(self.attformatter[i1] % self.attvalues[i1])
            
        return None

    ############
    ### Olga: used only in TANGO_gui_master -> move to this file
    ############
    def enable(self, _value):
        if not self.readonly:
            for button in self.window.att_set_buttons:
                button.setEnabled(_value)
            for io in self.window.io_newvals:
                io.setEnabled(_value)
            if self.allowmvr:
                self.window.but_moverel_pos.setEnabled(_value)
                self.window.but_moverel_neg.setEnabled(_value)
                self.window.box_delta.setEnabled(_value)
            if self.showcmds:
                self.window.but_clear_cmd.setEnabled(_value)
                self.window.but_send_cmd.setEnabled(_value)
                self.window.io_cmd.setEnabled(_value)
        return None
    
    def ChanceAttSelection(self, _index):
        self.attnames[_index] = str(self.window.att_select_buttons[_index].currentText())
        self.window.num_attributevals[_index].setText('')
        if self.attnames[_index]!= 'None':
            tmp = self.TangoObject.read_attribute(self.attnames[_index])
            if tmp.type in [PyTango.CmdArgType.DevShort, PyTango.CmdArgType.DevLong, PyTango.CmdArgType.DevUShort, \
                            PyTango.CmdArgType.DevULong, PyTango.CmdArgType.DevLong64, PyTango.CmdArgType.DevULong64, \
                            PyTango.CmdArgType.DevInt]: self.attformatter[_index] = '%i'
            elif tmp.type in [PyTango.CmdArgType.DevFloat, PyTango.CmdArgType.DevDouble]: self.attformatter[_index] = '%.5f'
            elif tmp.type in [PyTango.CmdArgType.DevString, PyTango.CmdArgType.DevVarCharArray, PyTango.CmdArgType.ConstDevString, PyTango.CmdArgType.DevState]:
                self.attformatter[_index] = '%s'
            #self.window.num_attributevals[_index].setText(self.attformatter[_index] %tmp.value)
        return None
    
    def changeCmd(self):
        self.cmd_name = str(self.window.cmd_selector.currentText())
        self.window.io_cmd.setText('')
        self.window.cmd_response.setText('')
        return None
    
    def clearCmdResponse(self):
        self.window.cmd_response.setText('')
        return None
    
    def changeCombo0(self):
        self.ChanceAttSelection(0)
        return None

    def changeCombo1(self):
        self.ChanceAttSelection(1)
        return None

    def changeCombo2(self):
        self.ChanceAttSelection(2)
        return None

    def changeCombo3(self):
        self.ChanceAttSelection(3)
        return None

    def changeCombo4(self):
        self.ChanceAttSelection(4)
        return None


############
### Olga: move above to another file
############
        
class cTANGOdeviceForm(QtGui.QWidget):
    def __init__(self, _parent_motor, _parent_widget, _xoffset=0, _yoffset=0, bgcolor='#ECECEC'):
        super(cTANGOdeviceForm, self).__init__()
        
        self.stdsizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.stdsizePolicy.setHorizontalStretch(0)
        self.stdsizePolicy.setVerticalStretch(0)
        self.stdsizePolicy.setHeightForWidth(_parent_motor.parent.sizePolicy().hasHeightForWidth())
        
        self.button_style = """QPushButton{border: solid; border-bottom-color: #777777; border-bottom-width: 2px; border-right-color:#777777;\
                               border-right-width: 2px; border-top-color:#AAAAAA; border-top-width: 1px; border-left-color:#AAAAAA;\
                               border-left-width: 1px; border-radius: 3px; padding: 1px;  background: qlineargradient(x1: 0, y1: \
                               0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}\
                               QPushButton:pressed{background:qlineargradient(x1: 0, y1: \
                               0, x2: 0, y2: 1, stop: 0 #dadada, stop: 0.4 #d4d4d4, stop: 0.5 #c7c7c7, stop: 1.0 #dadada) }"""
        self.io_style = """QLineEdit{border: solid; border-bottom-color: #777777; border-bottom-width: 1px; border-right-color:\
                               #777777; border-right-width: 1px; border-top-color:#AAAAAA; border-top-width: 1px; border-left-color:\
                               #AAAAAA; border-left-width: 1px; background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, \
                               stop: 0.4 #f4f4f4,stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}"""
        self.bg_color = bgcolor
        self.combo_style = """QComboBox{border: solid; border-bottom-color: #777777; border-bottom-width: 2px; border-right-color:#777777;\
                               border-right-width: 2px; border-top-color:#AAAAAA; border-top-width: 1px; border-left-color:#AAAAAA;\
                               border-left-width: 1px; border-radius: 3px; padding: 0px;  background: %s;}""" % bgcolor
        
        self.parent_motor = _parent_motor
        self.parent_widget = _parent_widget
        
        self.label_name = QtGui.QLabel(self.parent_widget)
        self.label_name.setObjectName("label_name")
        self.label_name.setText(self.parent_motor.alias)

        self.label_status = QtGui.QLabel(self.parent_widget)
        self.label_status.setObjectName("label_status")
        self.label_status.setText("unknown")

        self.label_position = QtGui.QLabel(self.parent_widget)
        self.label_position.setObjectName("label_position")
        if self.parent_motor.attnames[0] != 'None':
            self.label_position.setText(self.parent_motor.attnames[0])

        _labels = [self.label_name, self.label_position, self.label_status]
        self.label_name.setGeometry(QtCore.QRect(2 + _xoffset, 1 + _yoffset, 201, 21))
        self.label_status.setGeometry(QtCore.QRect(208 + _xoffset, 1 + _yoffset, 101, 21))
        
        if self.parent_motor.ZMXdevice != None:
            self.label_zmx = QtGui.QLabel(self.parent_widget)
            self.label_zmx.setObjectName("label_name")
            self.label_zmx.setText('ZMX device error:')
            self.label_zmxerr = QtGui.QLabel(self.parent_widget)
            self.label_zmxerr.setObjectName("label_zmxerr")
            self.label_zmxerr.setText('')
            self.label_zmx.setGeometry(QtCore.QRect(2 + _xoffset, 22 + _yoffset, 180, 21))
            self.label_zmxerr.setGeometry(QtCore.QRect(208 + _xoffset, 22 + _yoffset, 180, 21))
            _yoffset += 23
            _labels.append(self.label_zmx)
            _labels.append(self.label_zmxerr)
            
        for obj in _labels:
            obj.setFont(self.parent_widget.stdfont)
            obj.setStyleSheet("""QLabel{background-color:%s;}""" % self.bg_color)
        self.label_name.setFont(self.parent_widget.stdfontbold)
        
        self.num_attributevals = numpy.zeros(self.parent_motor.numrows, dtype=object)
        for i1 in range(self.parent_motor.numrows):
            self.num_attributevals[i1] = QtGui.QLabel(self.parent_widget)
            self.num_attributevals[i1].setFont(self.parent_widget.stdfont)
            self.num_attributevals[i1].setObjectName("num_attributeval%1i" % i1)
            self.num_attributevals[i1].setText("")
            self.num_attributevals[i1].setGeometry(QtCore.QRect(208 + _xoffset, 23 * (i1 + 1) + _yoffset, 80, 21))
            self.num_attributevals[i1].setStyleSheet("""QLabel{background-color:%s;}""" % self.bg_color)
        
        if not self.parent_motor.readonly:
            self.io_newvals = numpy.zeros(self.parent_motor.numrows, dtype=object)
            for i1 in range(self.parent_motor.numrows):
                self.io_newvals[i1] = QtGui.QLineEdit(self.parent_widget)
                self.io_newvals[i1].setSizePolicy(self.stdsizePolicy)
                self.io_newvals[i1].setFont(self.parent_widget.stdfont)
                self.io_newvals[i1].setObjectName("io_newtarget%1i" % i1)
                self.io_newvals[i1].setGeometry(QtCore.QRect(290 + _xoffset, 23 * (i1 + 1) + _yoffset, 85, 21))
                self.io_newvals[i1].setStyleSheet(self.io_style)
                # self.io_newvals[i1].setValidator(_parent_motor.parent.floatValidator)
            
            self.att_set_buttons = numpy.zeros(self.parent_motor.numrows, dtype=object)
            for i1 in range(self.parent_motor.numrows):
                self.att_set_buttons[i1] = QtGui.QPushButton(self.parent_widget)
                self.att_set_buttons[i1].setFont(self.parent_widget.stdfont)
                self.att_set_buttons[i1].setObjectName("but_setnewtarget%1i" % i1)
                self.att_set_buttons[i1].setText("Set attribute")
                self.att_set_buttons[i1].setGeometry(QtCore.QRect(378 + _xoffset, 23 * (i1 + 1) + _yoffset, 85, 21))
                self.att_set_buttons[i1].setStyleSheet(self.button_style)

        self.att_select_buttons = numpy.zeros(self.parent_motor.numrows, dtype=object)
        if self.parent_motor.attnames[0] == 'None':   
            i0 = 0
        else:
            i0 = 1
        for i1 in range(i0, self.parent_motor.numrows):
            self.att_select_buttons[i1] = QtGui.QComboBox(self.parent_widget)
            self.att_select_buttons[i1].setStyleSheet(self.combo_style)
            self.att_select_buttons[i1].setInsertPolicy(QtGui.QComboBox.InsertAtBottom)
            self.att_select_buttons[i1].setMinimumContentsLength(20)
            self.att_select_buttons[i1].setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
            self.att_select_buttons[i1].setMaxVisibleItems(15)
            self.att_select_buttons[i1].setAutoCompletion(True)
            self.att_select_buttons[i1].setFont(self.parent_widget.stdfont)
            self.att_select_buttons[i1].setObjectName("but_selectattribute%1i" % i1)
            self.att_select_buttons[i1].setGeometry(QtCore.QRect(2 + _xoffset, 23 * (i1 + 1)  + _yoffset, 201, 20))

        if self.parent_motor.attnames[0] != 'None':
            self.label_position.setGeometry(QtCore.QRect(2 + _xoffset, 22 + _yoffset, 180, 21))
        else:
            self.label_position.setGeometry(QtCore.QRect(1 + _xoffset, 22 + _yoffset, 1, 21))
        
        if self.parent_motor.allowmvr and not self.parent_motor.readonly:        
            self.box_delta = QtGui.QDoubleSpinBox(self.parent_widget)
            self.box_delta.setSizePolicy(self.stdsizePolicy)
            self.box_delta.setFont(self.parent_widget.stdfont)
            self.box_delta.setSuffix("")
            self.box_delta.setDecimals(5)
            self.box_delta.setMaximum(500.0)
            self.box_delta.setSingleStep(0.001)
            self.box_delta.setObjectName("box_delta")
            self.box_delta.setStyleSheet(self.io_style)

            self.but_moverel_pos = QtGui.QPushButton(self.parent_widget)
            self.but_moverel_pos.setFont(self.parent_widget.stdfont)
            self.but_moverel_pos.setObjectName("but_moverel_pos")
            self.but_moverel_pos.setText("positive")
            
            self.but_moverel_neg = QtGui.QPushButton(self.parent_widget)
            self.but_moverel_neg.setFont(self.parent_widget.stdfont)
            self.but_moverel_neg.setObjectName("but_moverel_neg")
            self.but_moverel_neg.setText("negative")        
    
            self.label_moverelby = QtGui.QLabel(self.parent_widget)
            self.label_moverelby.setObjectName("label_moverelby")
            self.label_moverelby.setText("Move relative by:")
            self.label_moverelby.setFont(self.parent_widget.stdfont)
            self.label_moverelby.setStyleSheet("""QLabel{background-color:%s;}""" % self.bg_color)
        
            self.label_moverelby.setGeometry(QtCore.QRect(2 + _xoffset, 23 * (self.parent_motor.numrows + 1) + 3 + _yoffset, 107, 21))
            self.box_delta.setGeometry(QtCore.QRect(189 + _xoffset, 23 * (self.parent_motor.numrows + 1) + 3 + _yoffset, 98, 21))
            self.but_moverel_pos.setGeometry(QtCore.QRect(378 + _xoffset, 23 * (self.parent_motor.numrows + 1) + 3 + _yoffset, 85, 21))
            self.but_moverel_neg.setGeometry(QtCore.QRect(290 + _xoffset, 23 * (self.parent_motor.numrows + 1) + 3 + _yoffset, 85, 21))
            self.but_moverel_pos.setStyleSheet(self.button_style)
            self.but_moverel_neg.setStyleSheet(self.button_style)
        #end if self.parent_motor.allowmvr and not self.parent_motor.readonly:        
        
        if self.parent_motor.showcmds and not self.parent_motor.readonly:
            self.cmd_selector = QtGui.QComboBox(self.parent_widget)
            self.cmd_selector.setStyleSheet(self.combo_style)
            self.cmd_selector.setInsertPolicy(QtGui.QComboBox.InsertAtBottom)
            self.cmd_selector.setMinimumContentsLength(20)
            self.cmd_selector.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
            self.cmd_selector.setMaxVisibleItems(15)
            self.cmd_selector.setAutoCompletion(True)
            self.cmd_selector.setFont(self.parent_widget.stdfont)
            self.cmd_selector.setObjectName("cmd_selector")
            
            self.io_cmd = QtGui.QLineEdit(self.parent_widget)
            self.io_cmd.setSizePolicy(self.stdsizePolicy)
            self.io_cmd.setFont(self.parent_widget.stdfont)
            self.io_cmd.setObjectName("io_cmd")
            self.io_cmd.setStyleSheet(self.io_style)
            
            self.label_cmd_response = QtGui.QLabel(self.parent_widget)
            self.label_cmd_response.setObjectName("label_cmd_response")
            self.label_cmd_response.setText("Command response:")
    
            self.cmd_response = QtGui.QLabel(self.parent_widget)
            self.cmd_response.setObjectName("label_cmd_response")
            self.cmd_response.setText("------------response-----")
            
            for obj in [self.label_cmd_response, self.cmd_response]:
                obj.setFont(self.parent_widget.stdfont)
                obj.setStyleSheet("""QLabel{background-color:%s;}""" % self.bg_color)
        
            self.but_send_cmd = QtGui.QPushButton(self.parent_widget)
            self.but_send_cmd.setObjectName("butsend_cmd")
            self.but_send_cmd.setText("Send cmd.")
            
            self.but_clear_cmd = QtGui.QPushButton(self.parent_widget)
            self.but_clear_cmd.setObjectName("butsend_cmd")
            self.but_clear_cmd.setText("clear answer")
            
            for obj in [self.but_clear_cmd, self.but_send_cmd]:
                obj.setStyleSheet(self.button_style)
                obj.setFont(self.parent_widget.stdfont)
    
            _offset = 23 * (self.parent_motor.numrows + 1) + 3
            if self.parent_motor.allowmvr: _offset += 26
            self.cmd_selector.setGeometry(QtCore.QRect(2 + _xoffset, _offset + _yoffset, 201, 20))
            self.io_cmd.setGeometry(QtCore.QRect(205 + _xoffset, _offset + _yoffset, 170, 21))
            self.but_send_cmd.setGeometry(QtCore.QRect(378 + _xoffset, _offset + _yoffset, 85, 21))
            
            self.label_cmd_response.setGeometry(QtCore.QRect(2 + _xoffset, _offset + 23 + _yoffset, 121, 21))
            self.cmd_response.setGeometry(QtCore.QRect(125 + _xoffset, _offset + 23 + _yoffset, 250, 21))
            self.but_clear_cmd.setGeometry(QtCore.QRect(378 + _xoffset, _offset + 23 + _yoffset, 85, 21))
        
            
        #end if self.parent_motor.showcmds and not self.parent_motor.readonly:
        return None
