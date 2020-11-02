import PyTango

# TODO used only in StatusServer, list of ports for p05 and p07
class CTangoServerMap():
    def __init__(self):
        self.beamline = 'p05'
        self.tInstances = {}
        self.tServers = {
            # Statusserver
            'statusserver': {
            'p05': {'tProxy': 'hzgpp05ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'ibl/ss-1.9/0'},
            'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            # Base stage (Tripod)
            'basestagePods': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/tripod/pods'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/tripod/pods'}
            },
            'basestagePusher': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/tripod/pusher'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/tripod/pusher'}
            },
            # Rotation stage (Aerotech)
            'aerotechMirror': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05ct/aerotech/o_mirror'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/aerotech/o_mirror'}
            },
            'aerotechRot': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05ct/aerotech/s_rot'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/aerotech/s_rot'}
            },
            'aerotechXrot': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05ct/aerotech/s_stage_rotx'}, 'p07':
                {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000, 'tInstance':
                 'p07ct/aerotech/s_stage_rotx'}
            },
            'aerotechYrot': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05ct/aerotech/s_stage_roty'}, 'p07':
                {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000, 'tInstance':
                 'p07ct/aerotech/s_stage_roty'}
            },
            'aerotechX': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05ct/aerotech/s_vert'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/aerotech/s_vert'}
            },
            'aerotechZ': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05ct/aerotech/s_stage_z'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/aerotech/s_stage_z'}
            },
            'aerotechCtrl': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05ct/aerotech/ctrl'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/aerotech/ctrl'}
            },
            # Sample positioning stage (Attocube)
            'attocubeP': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/attocubes/axis_p'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/attocubes/axis_p'}
            },
            'attocubeT': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/attocubes/axis_t'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/attocubes/axis_t'}
            },
            'attocubeX': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/attocubes/axis_x'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/attocubes/axis_x'}
            },
            'attocubeY': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/attocubes/axis_y'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/attocubes/axis_y'}
            },
            'attocubeZ': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/attocubes/axis_z'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/attocubes/axis_z'}
            },
            # Microsope Optics
            'microscopeScintillator': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/tripod/CCD_M1'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/tripod/CCD_M1'}
            },
            'microscopeFocus': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/tripod/CCD_M2'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/tripod/CCD_M2'}
            },
            'microscopeAperture': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/tripod/CCD_M3'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/tripod/CCD_M3'}
            },
            'microscopeFilter': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/tripod/CCD_M4'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/tripod/CCD_M4'}
            },
            'microscopeObjective': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/tripod/CCD_M5'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/tripod/CCD_M5'}
            },
            'microscopeRotHiCam': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/tripod/CCD_M6'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/tripod/CCD_M6'}
            },
            'microscopeRotLoCam': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/tripod/CCD_M7'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/tripod/CCD_M7'}
            },
            'microscopeCamZ': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/tripod/CCD_M8'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/tripod/CCD_M8'}
            },
            'microscopeCtrl': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/tripod/ctrl'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p07ct/tripod/ctrl'}
            },
            # DCM
            'dcmEnergy': {
            'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/dcmener/s01.01'},
            'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            'dcmBragg': {
            'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/dcmmotor/s01.01'},
            'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            'dcmPara': {
            'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/motor/mono.12'},
            'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            'dcmPerp': {
            'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/motor/mono.11'},
            'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            'dcmX1Roll': {
            'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/motor/mono.05'},
            'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            'dcmX2Roll': {
            'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/motor/mono.02'},
            'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            'dcmX2Pitch': {
            'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/motor/mono.01'},
            'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            'dcmJack1': {
            'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/motor/mono.03'},
            'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            'dcmJack2': {
            'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/motor/mono.16'},
            'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            'dcmJack3': {
            'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/motor/mono.07'},
            'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            # Optics stage (Micos Five Axis)
            'opticsstagePodA': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/micos/A'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p05ct/micos/A'}
            },
            'opticsstagePodB': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/micos/B'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p05ct/micos/B'}
            },
            'opticsstagePodC': {
            'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                    'tInstance': 'p05/micos/C'},
            'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                    'tInstance': 'p05ct/micos/C'}
            },
            'opticsstageSlab': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/micos/D'},
                'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                        'tInstance': 'p05ct/micos/D'}
            },
            'opticsstageCablecar': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/micos/E'},
                'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                        'tInstance': 'p05ct/micos/E'}
            },
            'opticsstageMultipleAxis': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/micos/multipleaxis'},
                'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                        'tInstance': 'p05ct/micos/multipleaxis'}
            },
            # QBPM 1
            'qbpm1sensor': {
                'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/i404/exp.01'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            'qbpm1motor': {
                'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/motor/mono.15'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            # QBPM EH2
            'qbpm4sensor': {
                'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/i404/eh2.01'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            'qbpm4motor': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/motor/eh2.16'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            # Undulator
            'undulator': {
                'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/undulator/1'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None}
            },
            # Camera FLI 1
            'cameraFli1': {
                'p05': {'tProxy': 'hzgpp05ct1.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/eh2/smc0900'},
                'p07': {'tProxy': 'hzgpp07ct1.desy.de', 'tPort': 10000,
                        'tInstance': 'p07ct/ccdfli/tum'}
            },
            # PETRA III
            'petra3': {
                'p05': {'tProxy': 'hzgpp05eh1vme.desy.de', 'tPort': 10000,
                        'tInstance': 'PETRA/GLOBALS/keyword'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            # FluorescenceDetector
            'fluorescenceDetector': {
                'p05': {'tProxy': 'hzgpp05eh1vme.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/mca/eh1.01'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            # Hexapod
            'hexpodU': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/hexapodsmall/u'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            'hexpodV': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/hexapodsmall/v'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            'hexpodW': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/hexapodsmall/u'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            'hexpodX': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/hexapodsmall/x'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            'hexpodY': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/hexapodsmall/y'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            'hexpodZ': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/hexapodsmall/z'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            # SampleChanger
            'sampleChanger': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/tripod/wechsler'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            # MCA
            'mca': {
                'p05': {'tProxy': 'hzgpp05vme2.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/mca/eh2.01'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            # KIT4MP camera
            'cameraKit4mp': {
                'p05': {'tProxy': 'hzgpp05ct1.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/imagedevice/0'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            # PS2
            'ps2Left': {
                'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/slt/exp.01'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            'ps2Right': {
                'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/slt/exp.02'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            'ps2Gap': {
                'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/slt/exp.03'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
            'ps2Offset': {
                'p05': {'tProxy': 'hzgpp05vme0.desy.de', 'tPort': 10000,
                        'tInstance': 'p05/slt/exp.04'},
                'p07': {'tProxy': None, 'tPort': 10000, 'tInstance': None},
            },
        }

    def __call__(self, beamline):
        print('XTM package set for beamline: %s' % self.beamline)

    def initAllProxies(self):
        for item in self.tServers.keys():
            self.tInstances[item] = self.initProxy(item)

    def initProxy(self, tServer):
        """
        DESCRIPTION:
            Initializes and return a tango device proxy.
        ATTRIBUTES:
            tServer=<String>
                Tango server name according to map (see method show)
        """
        try:
            tangoAddress = self.__generateAddressString(tServer)
            if not tServer in self.tInstances:
                DeviceProxy = PyTango.DeviceProxy(tangoAddress)
                self.tInstances[tServer] = DeviceProxy
                return DeviceProxy
        except:
            print('Could not initialize %s' % tServer)

    def getProxy(self, tServer):
        if not tServer in self.tInstances:
            self.initProxy(tServer)
        return self.tInstances[tServer]

    def show(self, verbose=True, withaddress=True, grep=''):
        """
        DESCRIPTION:
            Prints a list of mapped Tango servers. This is not necessarily all
            Tango servers available in a beamline.
        OPTIONS:
            verbose=<Boolean>:
                print to screen if True. Ohterwise return list silently.
                Default: True
            withaddress=<Boolean>:
                show tango addresses in list or not. Default: False
            grep=<String>:
                get only Adresses with <String> somewhere in the name.
        """
        tServerList = []
        for item in self.tServers.keys():
            tangoAddress = self.__generateAddressString(item)
            if grep in item:
                if withaddress is True:
                    tServerList.append([item, tangoAddress])
                else:
                    tServerList.append(item)
        if verbose is True:
            if withaddress is False:
                for i in sorted(tServerList):
                    print(i)
            else:
                for i in sorted(tServerList):
                    print('%s : %s' % (i[0], i[1]))
        return tServerList

    def __generateAddressString(self, tServer):
        tAttributes = self.tServers[tServer][self.beamline]
        tProxy = tAttributes['tProxy']
        tPort = tAttributes['tPort']
        tInstance = tAttributes['tInstance']
        addressString = 'tango://' + tProxy + ':' + str(tPort) + '/' + tInstance
        return addressString

#TangoServerMap.initAllProxies()
