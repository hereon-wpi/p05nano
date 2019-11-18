import h5py
import os
import numpy


class xtmH5():
    """
    The tomoh5 class writes and reads hdf5 files during a tomographic scan.
    Each image taken by a CCD is saved to (or read from) single hdf5 file.
    Additionally to the image there is other data stored along with the image,
    like ring current, rotation angle, exposure time, ROI and so on.
    """

    def __init__(self, image=None, fileName=None, path=None, stsVals=None):
        self.Date = None
        self.image = image

        # file information
        self.fileName = fileName
        self.path = path

        # Statusserver
        self.STSvals = stsVals

        self.myDtype = numpy.dtype([('value', numpy.float), (
            'tVal', numpy.float), ('tColl', numpy.float)])
        self.log_dtype = numpy.dtype([('device', numpy.str), (
            'value', numpy.float), ('tVal', numpy.float), ('tColl', numpy.float)])
        self.log_QBPMdtype = numpy.dtype([('X', numpy.float), ('Z', numpy.float), (
            'avgCurrent', numpy.float64), ('tVal', numpy.float), ('tColl', numpy.float)])

    def writeH5(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        fullpath = self.path + self.fileName
        h5file = h5py.File(fullpath, 'a')
        h5file.create_dataset("ccd image", data=self.image)
        posGrp = h5file.create_group("log")
        for i in self.STSvals.keys():
            vals = self.STSvals[i]
            # if i not in
            # ['QBPM1posandavgcurr','QBPM2posandavgcurr','QBPM3posandavgcurr']:
            h5data = numpy.zeros(1, dtype=self.myDtype)
            # h5data["device"]=i
            h5data["value"] = vals["value"]
            h5data["tVal"] = vals["tVal"]
            h5data["tColl"] = vals["tColl"]
            posGrp.create_dataset(i, data=h5data, dtype=self.myDtype)
            # else:
                # print vals

                # h5data=numpy.zeros(1,dtype=self.log_QBPMdtype)
                # h5data["X"]=vals["value"][0]
                # h5data["Z"]=vals["value"][1]
                # h5data["avgCurrent"]=vals["value"][2]
                # h5data["tVal"]=vals["tVal"]
                # h5data["tColl"]=vals["tColl"]
                # print h5data
                # posGrp.create_dataset(i,data=h5data,dtype=self.log_QBPMdtype)

        h5file.close()

    def readH5(self):
        fullpath = self.path + self.fileName
        h5file = h5py.File(fullpath, 'r')
        logGroup = h5file['/log']
        im = h5file['/ccd image']
        logContent = dict(logGroup)
        log = {}
        for item in logContent:
            itemValue = logContent[item]['value']
            itemtColl = logContent[item]['tColl']
            itemtVal = logContent[item]['tVal']
            log[item] = {'value': itemValue, 'tColl':
                         itemtColl, 'tVal': itemtVal}
        nim = numpy.array(im)
        h5file.close()
        return nim, log
