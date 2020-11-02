import os
import sys
import time

def StringFill(_string, _len, fill_front = False, fill_spaces = False):
    """Function to fill the string _string up to length _len
    with dots. If len(_string) > _len, the string is cropped.
    **kwargs: fill_front = True to fill in front of the input string.
    (Preset fill_front = False)
    Examples:
    StringFill('test 123', 12) = 'test 123 ...'
    StringFill('test 123', 12, fill_front = True) = '... test 123'
    """
    tmp = len(_string)
    if tmp < _len:
        if fill_spaces == False:
            if fill_front == True:
                return (_len-tmp-1)*'.'+' '+_string
            else:
                return _string+' '+(_len-tmp-1)*'.'
        else:
            if fill_front == True:
                return (_len-tmp)*' '+_string
            else:
                return _string+(_len-tmp)*' '

    else:
        return _string[:_len]
#end Stringfill


def GetTimeString(_epoch=None):
    """Function to get a string output of the current time."""
    _time = time.localtime(_epoch)
    _tmp = time.time()
    _msec = int((_tmp - int(_tmp))*1000)
    return '%02i/%02i/%04i %02i:%02i:%02i.%03i'\
                  %(_time[1], _time[2], _time[0], _time[3], _time[4], _time[5], _msec)
#end GetTimeString

def GetShortTimeString(_epoch=None):
    """Function to get a string output of the current time."""
    _time = time.localtime(_epoch)
    return '%02i.%02i %02i:%02i:%02i'\
                  %(_time[2], _time[1], _time[3], _time[4], _time[5])
#end GetTimeString


def GetArgTypeStr(_n):
    """Function to return the string representation of the PyTango.ArgType value from
    its integer code."""
    _list = ['Void', 'Boolean', 'Short', 'Long', 'Float', 'Double', 'UShort', 'ULong', 'String', \
             'CharArray', 'ShortArray', 'LongArray', 'FloatArray', 'DoubleArray', 'UShortArray', \
             'ULongArray', 'StringArray', 'LongStringArray', 'DoubleStringArray', 'DevState', \
             'ConstDevState', 'DevVarBooleanArray', 'DevUChar', 'DevLong64', 'DevULong64',\
             'DevVarLong64Array', 'DevVarULong64Array', 'Int', 'DevEncoded']
    return _list[_n]
#end GetArgTyoeStr

def CheckFilename(fname):
    """Function to check whether the specified filename exists and whether
    it is writable."""
    while True:
        _fname = os.path.split(fname)[1]
        _fpath = os.path.split(fname)[0]
        if _fpath == '': _fpath = os.getcwd()
        if not os.access(_fpath, os.F_OK):
            print('Warning. Path does not exist. Exiting procedure.')
            return None
        if not os.access(_fpath, os.W_OK):
            print('Warning. No writing access for chosen path. Exiting procedure.')
            return None
        try:
            if os.path.exists(fname):
                tmp = input(
                    'Warning: The specified file\n\t"%s"\nalready exists. Do you want to overwrite the file? (y/n): ' % fname)
                if tmp in ['y', 'yes', 'Y', 'Yes']:
                    if not os.access(fname, os.W_OK):
                        print('Warning: No permission to write file %s. Exiting procedure' % fname)
                        return None
                    os.remove(fname)
                    if os.path.exists(os.path.join(_fpath, _fname.split('.')[0]+'.info')):
                        os.remove(os.path.join(_fpath, _fname.split('.')[0]+'.info'))
                else:
                    fname = input('Please select new filename:')
            else:
                break
        except KeyboardInterrupt:
            return None
    return fname
#end CheckFilename

def GetPath(_file):
    """Function to get the path of the p05.gui module."""
    #t0 = time.time()
    for masterdir in sys.path:
        for dirname in os.walk(masterdir):
            #print dirname[0], os.path.join(dirname[0], _file)
            try:
                possible = os.path.join(dirname[0], _file)
                if os.path.isfile(possible):
                    #print time.time()- t0
                    return possible
            except:
                #print time.time()- t0
                print('Error while searching the directory "%s"' % dirname)
    return None
    

