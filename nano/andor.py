#!/bin/env python
#
## All defined functions are ordered alphabetically

from __future__ import print_function
import PyTango
import p06
import os
import time
import warnings


# device
# (rw) electronic_shutter_mode == rolling | global
# (ro) readout_time
# max_frame_rate_transfer
# frame_rate (depends on the acd_rate, shutter mode, and the exposure time)
# adc_rate (influences the readout time and thus frame_rate) 100 and 280 possible.
# adc_gain

# lima

## acq exposure time
## acq number frames
## saving frame per file
## file suffix
## file prefix
## saving_directory
## prepare acquisition
## start acquisition


## Saving managed mode == SOFTWARE (original value)
## SAVING FORMAT == RAW (original value)
## set acq_mode to single


# saving_mode = auto_frame
# acq_trigger_mode = internal_trigger | External_gate
# External_trigger, wait for an external trigger signal to start the an acquisition for the acq_nb_frames number of frames.
# External_trigger_multi, as the previous mode except that each frames need a new trigger input (e.g. for 4 frames 4 pulses are waiting for)
# Internal_trigger_multi, as for internal_trigger except that for each frame the acqStart() has to called once


# the status does not seem to change except for the lima attribute "acq_status". (Running|Ready)

class andor_device:

    ##############
    ## __init__ ##
    ##############

    def __init__(self,andorDevice,verbosity=0):

        ## Init
        self.verbosity = verbosity
        self.detectorDevice = andorDevice
        self.detectorType = 'andor'

        ## Get P06 Devices
        try:
            self.p06Devices = p06.beamline.p06_devices()
        except:
            raise Exception

        ## Create Device Proxy
        try:
            self.deviceProxy = PyTango.DeviceProxy(self.p06Devices['Detectors']
                                                                    [self.detectorType]
                                                                    [self.detectorDevice]
                                                                    ['device']
                                                    )
            self.limaDeviceProxy = PyTango.DeviceProxy(self.p06Devices['Detectors']
                                                                        [self.detectorType]
                                                                        [self.detectorDevice]
                                                                        ['device_lima']
                                                        )
            if self.verbosity > 0:
                print('Proxy: %s' % self.deviceProxy)
                print('Lima Proxy: %s' % self.limaDeviceProxy)
        except Exception as err:
            raise Exception(err)


    #######################
    ## abort_acquisition ##
    #######################

    def abort_acquisition(self):
        '''
        Aborts the acquisition.
        '''

        return self.execute_lima_command('abortAcq')


    #########################
    ## check_configuration ##
    #########################

    def check_configuration(self):
        '''
        Applies the standard configuration of the device.
        '''

        ## ADC Frequency
        _ADCFrequency = (self.p06Devices['Detectors']
                        [self.detectorType]
                        [self.detectorDevice]
                        ['adc_frequency']
                        )

        self.set_adc_frequency(_ADCFrequency)
        
        ## File Output Type
        _type = (self.p06Devices['Detectors']
                        [self.detectorType]
                        [self.detectorDevice]
                        ['file_type']
                        )

        self.set_file_type(_type)

        ## shutter mode
        _mode = (self.p06Devices['Detectors']
                        [self.detectorType]
                        [self.detectorDevice]
                        ['shutter_mode']
                        )

        self.set_shutter_mode(_mode)

        ## Configure the Saving Mode
        self.set_saving_mode()



    #####################
    ## execute_command ##
    #####################

    def execute_command(self,deviceServer,command,value = None):
        '''
        Execute a Command.
        '''

        try:
            if value == None:
                return deviceServer.command_inout(command)
            else:
                return deviceServer.command_inout(command,
                                                cmd_param = value
                                                )
        except Exception as err:
            raise Exception(err)


    ############################
    ## execute_device_command ##
    ############################

    def execute_device_command(self,command,value = None):
        '''
        Execute a Command on the device.
        '''

        return self.execute_command(self.deviceProxy,command,value)


    ##########################
    ## execute_lima_command ##
    ##########################

    def execute_lima_command(self,command,value = None):
        '''
        Execute a Command on the Lima device.
        '''

        return self.execute_command(self.limaDeviceProxy,command,value)


    ###################
    ## finalise_scan ##
    ###################

    def finalise_scan(self):
        '''
        Post Scan Actions.
        '''

        self.go_to_on_state()


    ######################
    ## get_readout_time ##
    ######################

    def get_readout_time(self,):
        '''
        Returns the readout time in seconds.
        '''

        self.check_configuration()
        return self.read_device_attribute('readout_time')


    ######################
    ## get_shutter_mode ##
    ######################

    def get_shutter_mode(self,):
        '''
        Returns the shutter mode.
        '''

        return self.read_device_attribute('electronic_shutter_mode').lower()


    #######################
    ## go_to_on_state ##
    #######################

    def go_to_on_state(self):
        '''
        Attempts to bring the detector back to ON state.
        '''

        _state = self.state()

        if _state == PyTango.DevState.MOVING:
            self.stop_acquisition()
        elif _state == PyTango.DevState.FAULT:
            self.abort_acquisition()


    #########################
    ## prepare_acquisition ##
    #########################

    def prepare_acquisition(self):
        '''
        Prepares the lima device for acquisition.
        '''

        return self.execute_lima_command('prepareAcq')


    ##################
    ## prepare_scan ##
    ##################

    def prepare_scan(self,scanParameters):
        '''
        Prepares the scan.
        '''

        self.go_to_on_state()

        self.check_configuration()

        ## Add Extra Keys to Scan Parameter Dictionary
        ### Check if scan_devices Exists
        if not 'detectors' in scanParameters.keys():
            scanParameters['detectors'] = {}

        ### Check if the detctor is already Defined
        if not self.detectorDevice in scanParameters['detectors'].keys():
            scanParameters['detectors'][self.detectorDevice]= {}

        ### Detector Enabled
        scanParameters['detectors'][self.detectorDevice]['enabled'] = True


        ## Data Directory
        (scanParameters['detectors']
                        [self.detectorDevice]
                        ['data_directory']) = (scanParameters['scan']['scan_directory']
                                                + self.p06Devices['Detectors']
                                                                    [self.detectorType]
                                                                    [self.detectorDevice]
                                                                    ['data_directory_suffix']
                                                )

        ## Create Data Directory if it does not exists to avoid Lima Error
        if not os.path.isdir(scanParameters['detectors']
                                            [self.detectorDevice]
                                            ['data_directory']
                                            ):
                os.makedirs(scanParameters['detectors']
                                            [self.detectorDevice]
                                            ['data_directory'],
                                0777
                                )
        ### Make Sure Everyone has Write Access. Xspress3 has a different user...
        os.chmod(scanParameters['detectors']
                                [self.detectorDevice]
                                ['data_directory'],
                    0777
                    )

        ## File Prefix
        (scanParameters['detectors']
                        [self.detectorDevice]
                        ['file_prefix']) = (
                                            scanParameters['scan']
                                                            ['scan_prefix']
                                            + '_'
                                            )

        ## File Type
        (scanParameters['detectors']
                        [self.detectorDevice]
                        ['file_type']) = (self.p06Devices['Detectors']
                                                            [self.detectorType]
                                                            [self.detectorDevice]
                                                            ['file_type']
                                                )

        ## File Index Length
        (scanParameters['detectors']
                        [self.detectorDevice]
                        ['file_index_length']) = (
                                                    '%' +
                                                    str(self.p06Devices['Detectors']
                                                            [self.detectorType]
                                                            [self.detectorDevice]
                                                            ['file_index_length']).zfill(2)
                                                    + 'd'
                                                    )

        ## File Index Start
        (scanParameters['detectors']
                        [self.detectorDevice]
                        ['file_index_start']) = (self.p06Devices['Detectors']
                                                            [self.detectorType]
                                                            [self.detectorDevice]
                                                            ['file_index_start']
                                                )

        ## Images per File
        (scanParameters['detectors']
                        [self.detectorDevice]
                        ['images_per_file']) = (
                                                    scanParameters['axis0']
                                                                    ['nr_interv']
                                                    + 1
                                                    )

        ## Integration Time
        (scanParameters['detectors']
                        [self.detectorDevice]
                        ['integ_time']) = (
                                            scanParameters['scan']
                                                            ['integ_time']
                                            )

        ### Number of Triggers
        (scanParameters['detectors']
                        [self.detectorDevice]
                        ['nb_triggers']) = int(scanParameters['scan']['nr_scan_points']
                                                * 1.1 #FIXME
                                                )


        ## Trigger Mode
        ### Trigger Mode is determined using the acquisition mode.
        if scanParameters['scan']['acquisition_mode'] == 0:
            _mode = 'external_gate'
        elif scanParameters['scan']['acquisition_mode'] == 1:
            _mode = 'external_trigger_multi'

        self.set_trigger_mode(_mode)

        ## Write Parameters to the Device
        self.set_parameters(scanParameters)

        ## Prepare Acquisition
        self.prepare_acquisition()

        ## Start Acquisition
        self.start_acquisition()

        return scanParameters

    ####################
    ## read_attribute ##
    ####################

    def read_attribute(self,deviceServer,attribute):
        '''
        Reads an attribute of the device server.
        '''

        try:
            _returnValue = deviceServer.read_attribute(attribute).value
            return _returnValue
        except Exception as err:
            raise Exception(err)


    ###########################
    ## read_device_attribute ##
    ###########################

    def read_device_attribute(self,attribute):
        '''
        Reads an attribute to the Detector Device.
        '''

        return self.read_attribute(self.deviceProxy,attribute)


    #########################
    ## read_lima_attribute ##
    #########################

    def read_lima_attribute(self,attribute):
        '''
        Reads an attribute of the Lima device.
        '''

        return self.read_attribute(self.limaDeviceProxy,attribute)


    #######################
    ## set_adc_frequency ##
    #######################

    def set_adc_frequency(self,frequency):
        '''
        Sets the file output type.
        '''
        if frequency not in (self.p06Devices['Detectors']
                                            [self.detectorType]
                                            [self.detectorDevice]
                                            ['adc_frequency_possibilities']
                                            ):
            raise ValueError('Unsupported frequency.')

        _ADCFrequency = (
                    'MHZ'
                    + str(frequency)
                    )

        _currentADCFrequency = self.read_device_attribute('adc_rate')

        if _currentADCFrequency.lower() != _ADCFrequency.lower():
            if self.verbosity > 0:
                print('Changing the file type from "%s" to "%s"' % (
                                                        _currentADCFrequency,
                                                        _ADCFrequency
                                                        )
                        )
            self.write_device_attribute('adc_rate',_ADCFrequency)


    ###################
    ## set_file_type ##
    ###################

    def set_file_type(self,_type):
        '''
        Sets the file output type.
        '''

        _currentType = self.read_lima_attribute('saving_format')

        if _currentType.lower() != _type.lower():
            if self.verbosity > 0:
                print('Changing the file type from "%s" to "%s"' % (
                                                        _currentType,
                                                        _type
                                                        )
                        )
            self.write_lima_attribute('saving_format',_type)

    #####################
    ## set_saving_mode ##
    #####################

    def set_saving_mode(self):
        '''
        Configures the saving mode.
        '''

        _savingMode = 'auto_frame'

        _currentMode = self.read_lima_attribute('saving_mode')

        if _currentMode.lower() != _savingMode.lower():
            if self.verbosity > 0:
                print('Changing the triggering mode from "%s" to "%s"' % (
                                                        _currentMode,
                                                        _savingMode
                                                        )
                        )
            self.write_lima_attribute('saving_mode',_savingMode)

    ######################
    ## set_trigger_mode ##
    ######################

    def set_trigger_mode(self,_mode):
        '''
        Sets the file output type.
        '''

        _currentMode = self.read_lima_attribute('acq_trigger_mode')

        if _currentMode.lower() != _mode.lower():
            if self.verbosity > 0:
                print('Changing the triggering mode from "%s" to "%s"' % (
                                                        _currentMode,
                                                        _mode
                                                        )
                        )
            self.write_lima_attribute('acq_trigger_mode',_mode)


    ####################
    ## set_parameters ##
    ####################

    def set_parameters(self,scanParameters):

        ## Lima Attribute Dictionary
        attribute_dict_lima = {
                                'data_directory':'saving_directory',
                                'file_index_length':'saving_index_format',
                                'file_index_start':'saving_next_number',
                                'file_prefix':'saving_prefix',
                                'images_per_file':'saving_frame_per_file',
                                'integ_time':'acq_expo_time',
                                'nb_triggers':'acq_nb_frames'
                                }


        ## Set Parameters
        for key,value in scanParameters['detectors'][self.detectorDevice].iteritems():
            if key in attribute_dict_lima:
                if self.verbosity > 0:
                    print('Setting %s to %s' % (attribute_dict_lima[key],str(value)))
                self.write_lima_attribute(attribute_dict_lima[key],value)

            ## If Not Defined it Does not to be Set
            else:
                if self.verbosity > 0:
                    print('Not defined attribute: %s' % (key))


    ######################
    ## set_shutter_mode ##
    ######################

    def set_shutter_mode(self,shutterMode):
        '''
        Sets the shutter mode.
        '''

        return self.write_device_attribute('electronic_shutter_mode',shutterMode.upper())


    ###########
    ## state ##
    ###########

    def state(self):
        '''
        Returns the State.
        '''

        _states = []
        _states.append(self.execute_lima_command('State'))
        _states.append(self.execute_device_command('State'))

        ## The device does not change state when acquiring, hence the following
        _state = self.read_lima_attribute('acq_status')
        if _state == 'Running':
            _states.append(PyTango.DevState.MOVING)
        elif _state == 'Fault':
            _states.append(PyTango.DevState.FAULT)

        ## State Machine
        if PyTango.DevState.FAULT in _states:
            return PyTango.DevState.FAULT
        elif PyTango.DevState.ALARM in _states:
            return PyTango.DevState.ALARM
        elif PyTango.DevState.MOVING in _states:
            return PyTango.DevState.MOVING
        elif PyTango.DevState.RUNNING in _states:
            return PyTango.DevState.RUNNING
        elif PyTango.DevState.ON in _states:
            return PyTango.DevState.ON

    #######################
    ## start_acquisition ##
    #######################

    def start_acquisition(self):
        '''
        Starts the acquisition.
        '''

        return self.execute_lima_command('startAcq')


    ######################
    ## stop_acquisition ##
    ######################

    def stop_acquisition(self):
        '''
        Stops the acquisition.
        '''

        return self.execute_lima_command('stopAcq')


    #####################
    ## write_attribute ##
    #####################

    def write_attribute(self,deviceServer,attribute,value):
        '''
        Writes an attribute to the device server.
        '''

        try:
            deviceServer.write_attribute(attribute,value)
        except Exception as err:
            raise Exception(err)


    ############################
    ## write_device_attribute ##
    ############################

    def write_device_attribute(self,attribute,value):
        '''
        Writes an attribute to the detector device.
        '''

        self.write_attribute(self.deviceProxy,attribute,value)

        return 1

    ##########################
    ## write_lima_attribute ##
    ##########################

    def write_lima_attribute(self,attribute,value):
        '''
        Writes an attribute to the lima device.
        '''

        self.write_attribute(self.limaDeviceProxy,attribute,value)

        return 1


