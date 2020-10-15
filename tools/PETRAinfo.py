import time


# TODO Is it used?
def GetPETRAinfoString(itype, infostr, inumber, time0, tTTTGW, tQBPM):
    """
    Layout: Petra Beam Current // Beam Lifetime // Orbit RMSx // Orbit RMSy // Topup status // QBPM current // QBPM pos x //QBPM pos  y
    if not readable, return value is -1
    """
    s = '%13s\t%5s\t%05i\t%e\t' %(itype[:13], infostr[:5], inumber, time.time()-time0)
    try:
        tmp = tTTTGW.read_attribute('BeamCurrent').value
        s += '%010.6f\t' %tmp
    except:
        s += '-01.000000\t'
    try:
        tmp = tTTTGW.read_attribute('BeamLifetime').value
        s += '%06.3f\t' %tmp
    except:
        s += '-1.000\t'
    try:
        tmp = tTTTGW.read_attribute('OrbitRMSX').value
        s += '%010.6f\t' %tmp
    except:
        s += '-01.000000\t'
    try:
        tmp = tTTTGW.read_attribute('OrbitRMSY').value
        s += '%010.6f\t' %tmp
    except:
        s += '-01.000000\t'
    try:
        tmp = tTTTGW.read_attribute('TopUpStatus').value
        s += '%04.1f\t' %tmp
    except:
        s += '-1.0\t'
    try:
        tmp = tQBPM.read_attribute('PosAndAvgCurr').value
        s += '%e\t' %tmp[2]
    except:
        s += '-01.000000\t'
    try:
        tmp = tQBPM.read_attribute('PosAndAvgCurr').value
        s += '%e\t' %tmp[0]
    except:
        s += '-01.000000\t'
    try:
        tmp = tQBPM.read_attribute('PosAndAvgCurr').value
        s += '%e\t' %tmp[1]
    except:
        s += '-01.000000\t'
    return s+'\n'

def GetPETRAinfoStringShort(itype, infostr, inumber, motorpos, time0, tTTTGW, tQBPM):
    """
    Layout: image identifier // infostr // image number // motorpos // timestamp // Petra Beam Current // Orbit RMSx // Orbit RMSy // QBPM current // QBPM pos x //QBPM pos  y
    if not readable, return value is -1
    """
    s = '%13s\t%5s\t%05i\t%e\t%e\t' %(itype[:13], infostr[:5], inumber, motorpos, time.time()-time0)
    try:
        tmp = tTTTGW.read_attribute('BeamCurrent').value
        s += '%010.6f\t' %tmp
    except:
        s += '-01.000000\t'
    try:
        tmp = tTTTGW.read_attribute('OrbitRMSX').value
        s += '%010.6f\t' %tmp
    except:
        s += '-01.000000\t'
    try:
        tmp = tTTTGW.read_attribute('OrbitRMSY').value
        s += '%010.6f\t' %tmp
    except:
        s += '-01.000000\t'
    try:
        tmp = tQBPM.read_attribute('PosAndAvgCurr').value
        s += '%e\t' %tmp[2]
        s += '%e\t' %tmp[0]
        s += '%e\t' %tmp[1]
    except:
        s += '-01.000000\t'
        s += '-01.000000\t'
        s += '-01.000000\t'
    return s+'\n'
