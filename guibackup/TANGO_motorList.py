def getTANGOmotorList():
    """
    allMotors structure:
        item[0]:    motor alias
        item[1]:    TANGO address
        item[2]:    position attribute
        item[3]:    number of rows in motor GUI (i.e. number of total attributes to be displayed in parallel)
        item[4]:    flag to allow direct relative movements  
        item[5]:    flag to set to read only 
        item[6]:    flag to show command list.
    """
    allMotors = []
    allMotors.append(['Temperature', '//hzgpp05vme1:10000/p05/adc/eh1.07', 'Value', 4, True, False])
    allMotors.append(['Air humidity', '//hzgpp05vme1:10000/p05/adc/eh1.08', 'Value', 3, False, False])
    allMotors.append(['Temperature', '//hzgpp05vme1:10000/p05/adc/eh1.07', 'Value', 2, True, True])
    allMotors.append(['Air humidity', '//hzgpp05vme1:10000/p05/adc/eh1.08', 'Value', 4, True, True])
    allMotors.append(['Motor 01', '//hzgpp05vme1:10000/p05/motor/eh1.01', 'Position', 3, True, False])
    allMotors.append(['Motor 02', '//hzgpp05vme1:10000/p05/motor/eh1.02', 'Position', 3, True, False])
    return allMotors

def getTANGOmotorGroups():
    groups = []
    groups.append(['Ambient conditions', 2, '#ECECEC'])
    groups.append(['Ambient conditions', 2, '#AA3333'])
    groups.append(['Test motors', 2, '#7777DD'])
    return groups
    
    allMotors = []
    allMotors.append(['Slit Z top', '//hzgpp05vme1:10000/p05/motor/eh1.01', 'Position', 3, True, False, True])
    allMotors.append(['Slit Z bottom', '//hzgpp05vme1:10000/p05/motor/eh1.02', 'Position', 3, True, False, True])
    allMotors.append(['Slit x OMS', '//hzgpp05vme1:10000/p05/motor/eh1.03', 'Position', 3, True, False, True])
    allMotors.append(['Slit 4 OMS', '//hzgpp05vme1:10000/p05/motor/eh1.04', 'Position', 3, True, False, True])
    allMotors.append(['Slit 1 ZMX', '//hzgpp05vme1:10000/p05/ZMX/eh1.01', 'Error', 3, False, False, False])
    allMotors.append(['Slit 2 ZMX', '//hzgpp05vme1:10000/p05/ZMX/eh1.02', 'Error', 3, False, False, False])
    allMotors.append(['Slit 3 ZMX', '//hzgpp05vme1:10000/p05/ZMX/eh1.03', 'Error', 3, False, False, False])
    allMotors.append(['Slit 4 ZMX', '//hzgpp05vme1:10000/p05/ZMX/eh1.04', 'Error', 3, False, False, False])
    
    allMotors.append(['DAC output 1', '//hzgpp05vme1:10000/p05/dac/eh1.01', 'Voltage', 3, True, False, True])
    allMotors.append(['ADC input 1', '//hzgpp05vme1:10000/p05/adc/eh1.01', 'Value', 3, False, False, True])
    
    groups = []
    groups.append(['Slits', 8, '#CCCCEE'])
    groups.append(['IOs', 2, '#EECCCC'])
    
    
    app = QtGui.QApplication(sys.argv)
    gui = p05.gui.TANGOgui(devices = allMotors, groups = groups, name = 'EH1 VME device GUI')
    sys.exit(app.exec_())
