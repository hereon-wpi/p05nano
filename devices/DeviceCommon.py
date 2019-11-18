import PyTango
import time
import p05.common.TangoFailsaveComm as tfs


class DeviceCommon(object):
    def __init__(self, devdict=None):
        self.__devdict = devdict

    def _tRead(self, tObject, attribute):
        """
        DESCRIPTION:
            Read tango attribute of a specified tango object.
        PARAMETER:
            tObject:
                Tango Object
            attribute:
                attribute of the Tango object which is to be read
        """
        return tfs.tSaveCommReadAttribute(tObject, attribute, silent=True)

    def _tWrite(self, tObject, attribute, value, wait=True):
        """
        DESCRIPTION:
            Write tango attribute of a specified tango object.
        PARAMETER:
            tObject:
                Tango Object
            attribute:
                attribute of the Tango object which is to be set
            value:
                new value for the Tango object's attribute
        KEYWORDS:
            wait:
                waits for Tango device ON state before continuing
                default: True
        """
        tfs.tSaveCommWriteAttribute(tObject, attribute, value, silent=True,
                                    wait=wait)
        return None

    def _tExec(self, tObject, command, param=None, wait=True):
        """
        DESCRIPTION:
            Execute tango command of a specified tango object.
        PARAMETER:
            tObject:
                Tango Object
            cmd:
                command which is passed to the Tango object.
        KEYWORDS:
            param=<*>
                command parameter, if existing
        """
        return tfs.tSaveCommCommand(tObject, command, Argument=param,
                                    silent=True, wait=wait)
        # tcmd = getattr(tObject,cmd)
        # if param==None:
        #    tcmd()
        # else:
        #    tcmd(param)
        # return None

    def _tMotionWait(self, tObject, poll_time=0.1):
        """
        DESCRIPTION:
            Poll Tango device state until it is not in moving state.
        PARAMETER:
            tObject:
                Tango Object
        KEYWORDS:
            poll_time=<FLOAT>
                poll time interval. Default: 0.1
        """
        while tObject.State() == PyTango.DevState.MOVING:
            time.sleep(poll_time)
        return None

    def _MoveMotor(self, tObject, attribute, position=None, wait=True,
                   relative=False, backlash=None, verbose=True):
        """
        DESCRIPTION:
            Pass motion command to Tango server.
        PARAMETER:
            tObject:
                Tango Object
            attribute:
                The Tango Object's attribute
        KEYWORDS:
            position=<FLOAT>/<STRING>/None:
                set <value> to move to a position,
                set 'home' to home this motor
                set None to read the current position of the motor
            wait=<BOOLEAN>:
                wait for the motor motion to be complete before command prompt is released.
                Default: True
            relative=<BOOLEAN>:
                move relative to current position. Default: False
            backlash=<FLOAT>/None:
                move with backlash. Default: None
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        CurrentPosition = self._tRead(tObject, attribute)
        if position is None:
            current_position = self._tRead(tObject, attribute)
            if verbose is True:
                print('%s %s: %f' % (tObject, attribute, current_position))
            return current_position
        else:
            if relative is True:
                position = CurrentPosition + position
            if verbose is True:
                print('Move %s from %s to %s.' % (tObject, CurrentPosition,
                                                  position))
            try:
                if not backlash:
                    self._tWrite(tObject, attribute, position, wait)
                    #if wait:
                    #    self._tMotionWait(tObject)
                else:
                    self._tWrite(tObject, attribute, position + backlash, wait)
                    #if wait is True:
                    #    self._tMotionWait(tObject)
                    self._tWrite(tObject, attribute, position, wait)
                    #if wait is True:
                    #    self._tMotionWait(tObject)
            except (KeyboardInterrupt, SystemExit):
                self.stop()
            return None

    def _HomeAxis(self, tObject, command, wait=True):
        self._tExec(tObject, command)
        if wait:
            self._tMotionWait(tObject)
        return None

    def pos(self, device='all', verbose=True):
        """
        DESCRIPTION:
            Returns the position of either all axis or a given axis.
        KEYWORDS:
            device=<STRING>:
                returns the position of axis <STRING>. Use Show() to list device names.
                if <STRING>=='all', the position of all devices of this class are shown.
                Default: 'all'
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetValue = {}
        if device == 'all':
            for iDev in sorted(self.__devdict):
                iDevValue = []
                for attribute in self.__devdict[iDev][1]:
                    if type(attribute) is dict:
                        pass
                    else:
                        iDevValue.append(
                            self._tRead(self.__devdict[iDev][0], attribute))
                        if verbose is True:
                            print("%s %s: %s" % (iDev, attribute, self._tRead(self.__devdict[iDev][0], attribute)))
                RetValue[iDev] = iDevValue
        else:
            iDev = self.__devdict[device]
            for attribute in iDev[1]:
                if type(attribute) is dict:
                    pass
                else:
                    RetValue[device] = self._tRead(iDev[0], attribute)
                    if verbose is True:
                        print("%s %s: %s" % (device, attribute, self._tRead(iDev[0], attribute)))
        return RetValue

    def state(self, device='all', verbose=True):
        """
        DESCRIPTION:
            Returns the State of either all axis or a given axis.
        KEYWORDS:
            device=<STRING>:
                returns the state of axis <STRING>. Use Show() to list device names.
                if <STRING>=='all', the position of all devices of this class are shown.
                Default: 'all'
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetValue = []
        if device == 'all':
            for iDev in sorted(self.__devdict):
                RetValue.append(self._tRead(self.__devdict[iDev][0], 'State'))
                if verbose is True:
                    print("%s: %s" % (iDev, self._tRead(self.__devdict[iDev][0], 'State')))
        else:
            iDev = self.__devdict[device]
            RetValue.append(self._tRead(self.__devdict[iDev][0], 'State'))
            if verbose is True:
                print('%s: %s ' % (device, self._tRead(iDev[0], 'State')))
        return RetValue

    def status(self, device='all', verbose=True):
        """
        DESCRIPTION:
            Returns the Status of either all axis or a given axis.
        KEYWORDS:
            device=<STRING>:
                returns the state of axis <STRING>. Use Show() to list device names.
                if <STRING>=='all', the position of all devices of this class are shown.
                Default: 'all'
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetValue = []
        if device == 'all':
            for iDev in sorted(self.__devdict):
                RetValue.append(self._tRead(self.__devdict[iDev][0], 'Status'))
                if verbose is True:
                    print("%s: %s" % (iDev, self._tRead(self.__devdict[iDev][0], 'Status')))
        else:
            iDev = self.__devdict[device]
            RetValue.append(self._tRead(self.__devdict[iDev][0], 'Status'))
            if verbose is True:
                print('%s: %s ' % (device, self._tRead(iDev[0], 'Status')))
        return RetValue

    def stop(self):
        """
        DESCRIPTION:
            Stops motion of all axis of this class.
        """
        for iDev in sorted(self.__devdict):
            if self.__devdict[iDev][1][-1]['ismotor'] is False:
                pass
            else:
                self._tExec(self.__devdict[iDev][0], 'StopMove')
        return None

    def show(self, verbose=True):
        """
        DESCRIPTION:
            Print a list of all devices and their attributes controlled by this class.
        KEYWORDS:
            verbose=<BOOLEAN>:
                Print messages on screen.
                Default: True
        """
        RetValue = []
        for device in sorted(self.__devdict):
            RetValue.append([device, self.__devdict[device][1]])
            if verbose is True:
                print('Device: %s, %s' % (device, self.__devdict[device][1]))
        return RetValue
