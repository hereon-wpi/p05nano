from p05.devices.PMACdict import PMACdict 

def getPMACmotorList():
    """
    allMotors structure:
        item[0]:    motor alias
        item[1]:    controller number
        item[2]:    set command
        item[3]:    target variable
        item[4]:    current position variable
        optional parameters:
        if limits are desired, both limits must be set
        item[5]:    lower limit
        item[6]:    upper limit
    """
    pd = PMACdict(dummy = True).Dict
    for key in pd.keys():
        pd[key]['ul'] = min(pd[key]['upperLim'], pd[key]['upperSoftLim'])
        pd[key]['ll'] = max(pd[key]['lowerLim'], pd[key]['lowerSoftLim'])  

    allMotors = []
    allMotors.append(['VacuumSF x',        1, 'Q70=4', 'Q77', 'Q87', pd['VacuumSF_x']['ll'], pd['VacuumSF_x']['ul']])
    allMotors.append(['VacuumSF y',        1, 'Q70=4', 'Q78', 'Q88', pd['VacuumSF_y']['ll'], pd['VacuumSF_y']['ul']])
    allMotors.append(['VacuumSF z',        1, 'Q70=4', 'Q79', 'Q89', pd['VacuumSF_z']['ll'], pd['VacuumSF_z']['ul']])
    allMotors.append(['VacuumSF Rx',       1, 'Q70=4', 'Q71', 'Q81', pd['VacuumSF_Rx']['ll'], pd['VacuumSF_Rx']['ul']])
    allMotors.append(['VacuumSF Ry',       1, 'Q70=4', 'Q72', 'Q82', pd['VacuumSF_Ry']['ll'], pd['VacuumSF_Ry']['ul']])
    allMotors.append(['VacuumSF Rz',       1, 'Q70=4', 'Q73', 'Q83', pd['VacuumSF_Rz']['ll'], pd['VacuumSF_Rz']['ul']])
    allMotors.append(['VacuumTrans y',     2, 'Q70=4', 'Q77', 'Q87', pd['VacuumTrans_y']['ll'], pd['VacuumTrans_y']['ul']])
    allMotors.append(['Diode z1',          4, 'Q70=8', 'P71', 'P81', pd['Diode1_z']['ll'], pd['Diode1_z']['ul']])
    allMotors.append(['Diode z2',          4, 'Q70=8', 'P72', 'P82', pd['Diode2_z']['ll'], pd['Diode2_z']['ul']])
    allMotors.append(['Aperture x',        3, 'Q70=8', 'P73', 'P83', pd['Aperture_x']['ll'], pd['Aperture_x']['ul']])
    allMotors.append(['Aperture y',        3, 'Q70=8', 'P71', 'P81', pd['Aperture_y']['ll'], pd['Aperture_y']['ul']])
    allMotors.append(['Aperture z',        3, 'Q70=8', 'P72', 'P82', pd['Aperture_z']['ll'], pd['Aperture_z']['ul']])
    allMotors.append(['OpticsSF-1 x',      7, 'Q70=4', 'Q77', 'Q87', pd['OpticsSF1_x']['ll'], pd['OpticsSF1_x']['ul']])
    allMotors.append(['OpticsSF-1 y',      7, 'Q70=4', 'Q78', 'Q88', pd['OpticsSF1_y']['ll'], pd['OpticsSF1_x']['ul']])
    allMotors.append(['OpticsSF-1 z',      7, 'Q70=4', 'Q79', 'Q89', pd['OpticsSF1_z']['ll'], pd['OpticsSF1_x']['ul']])
    allMotors.append(['OpticsSF-1 Rx',     7, 'Q70=4', 'Q71', 'Q81', pd['OpticsSF1_Rx']['ll'], pd['OpticsSF1_Rx']['ul']])
    allMotors.append(['OpticsSF-1 Ry',     7, 'Q70=4', 'Q72', 'Q82', pd['OpticsSF1_Ry']['ll'], pd['OpticsSF1_Ry']['ul']])
    allMotors.append(['OpticsSF-1 Rz',     7, 'Q70=4', 'Q73', 'Q83', pd['OpticsSF1_Rz']['ll'], pd['OpticsSF1_Rz']['ul']])
    allMotors.append(['Optics stage-1 y', 7, 'Q70=8', 'P71', 'P81', pd['OpticsStage1_y']['ll'], pd['OpticsStage1_y']['ul']])
    allMotors.append(['OpticsSF-2 x',      4, 'Q70=4', 'Q77', 'Q87', pd['OpticsSF2_x']['ll'], pd['OpticsSF2_x']['ul']])
    allMotors.append(['OpticsSF-2 y',      4, 'Q70=4', 'Q78', 'Q88', pd['OpticsSF2_y']['ll'], pd['OpticsSF2_y']['ul']])
    allMotors.append(['OpticsSF-2 z',      4, 'Q70=4', 'Q79', 'Q89', pd['OpticsSF2_z']['ll'], pd['OpticsSF2_z']['ul']])
    allMotors.append(['OpticsSF-2 Rx',     4, 'Q70=4', 'Q71', 'Q81', pd['OpticsSF2_Rx']['ll'], pd['OpticsSF2_Rx']['ul']])
    allMotors.append(['OpticsSF-2 Ry',     4, 'Q70=4', 'Q72', 'Q82', pd['OpticsSF2_Ry']['ll'], pd['OpticsSF2_Ry']['ul']])
    allMotors.append(['OpticsSF-2 Rz',     4, 'Q70=4', 'Q73', 'Q83', pd['OpticsSF2_Rz']['ll'], pd['OpticsSF2_Rz']['ul']])
    allMotors.append(['SampleStage x',     5, 'Q70=8', 'P71', 'P81', pd['SampleStage_x']['ll'], pd['SampleStage_x']['ul']])
    allMotors.append(['SampleStage z',     5, 'Q70=4', 'Q79', 'Q89', pd['SampleStage_z']['ll'], pd['SampleStage_z']['ul']])
    allMotors.append(['SampleStage Rx',    5, 'Q70=4', 'Q77', 'Q87', pd['SampleStage_Rx']['ll'], pd['SampleStage_Rx']['ul']])
    allMotors.append(['SampleStage Ry',    5, 'Q70=4', 'Q78', 'Q88', pd['SampleStage_Ry']['ll'], pd['SampleStage_Ry']['ul']])
    allMotors.append(['Sample rotation',   5, 'Q70=8', 'P72', 'P82', pd['Sample_Rot']['ll'], pd['Sample_Rot']['ul']])
    allMotors.append(['Sample x',          6, 'Q70=4', 'Q77', 'Q87', pd['Sample_x']['ll'], pd['Sample_x']['ul']])
    allMotors.append(['Sample y',          6, 'Q70=4', 'Q78', 'Q88', pd['Sample_y']['ll'], pd['Sample_y']['ul']])
    allMotors.append(['Sample z',          6, 'Q70=4', 'Q79', 'Q89', pd['Sample_z']['ll'], pd['Sample_z']['ul']])
    allMotors.append(['Sample Rx',         6, 'Q70=4', 'Q71', 'Q81', pd['Sample_Rx']['ll'], pd['Sample_Rx']['ul']])
    allMotors.append(['Sample Ry',         6, 'Q70=4', 'Q72', 'Q82', pd['Sample_Ry']['ll'], pd['Sample_Ry']['ul']])
    allMotors.append(['Sample Rz',         6, 'Q70=4', 'Q73', 'Q83', pd['Sample_Rz']['ll'], pd['Sample_Rz']['ul']])
    allMotors.append(['Detector x',        5, 'Q70 = 28', 'P77', 'P87', pd['Detector_x']['ll'], pd['Detector_x']['ul']])
    allMotors.append(['Detector z',        5, 'Q70 = 28', 'P78', 'P88', pd['Detector_z']['ll'], pd['Detector_z']['ul']])
    return allMotors

def getPMACmotorGroups():
    groups = []
    groups.append(['Vacuum SpaceFab', 6, '#CCCCCC'])
    groups.append(['Vacuum translations', 1, '#BBBBBB'])
    groups.append(['Diode pushers', 2, '#EEEEEE'])
    groups.append(['Cone-beam aperture system', 3, '#CCDDEE'])
    groups.append(['Optics SpaceFab (condenser optics)', 7, '#CCCCEE'])
    groups.append(['Optics SpaceFab (objective optics)', 6, '#CCEEEE'])
    groups.append(['Sample stage (substructure)', 5, '#EEEECC'])
    groups.append(['Sample positioning SpaceFab', 6, '#EED6BF']) #EECFBF
    groups.append(['Detector mechanics', 2, '#EECCCC'])
    return groups
