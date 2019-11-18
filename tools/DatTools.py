#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
from Tkinter import Tk
from tkFileDialog import askopenfilename
import numpy as N


def read_dat(path=None):
    """
    Load binary data created with IDL routine write_dat to python array.
    """

    if not path:
        path = select_path()
    data_info = check_file(path)
    if data_info is False:
        print(path + ': not a tomo data file.')
        return False

    with open(path) as f:

        # skip header

        f.seek(-(data_info['dim_x'] * data_info['dim_y']
               * data_info['dim_z'] * data_info['byte_length']), 2)

        # load data

        if data_info['byte_length'] == 1:
            data = N.fromfile(f, N.dtype('uint8'))
        if data_info['byte_length'] == 2:
            data = N.fromfile(f, N.dtype('uint16'))
        if data_info['byte_length'] == 4:
            data = N.fromfile(f, N.dtype('f4'))

        # load histogram

        if data_info['dim_y'] == 1 and data_info['dim_z'] == 1:
            data.shape = data_info['dim_x']
            data = data.astype(float)

        # load image

        if data_info['dim_z'] == 1:
            data.shape = (data_info['dim_x'], data_info['dim_y'])
            data = data.astype(float)

        # load volume

        if data_info['dim_z'] != 1:
            data.shape = (data_info['dim_z'], data_info['dim_y'],
                          data_info['dim_x'])
            data = data.astype('uint8')

    return data


def select_path(predir=''):
    """
    Open file dialog and choose filepath.
    """

    # Create an open file dialog
    Tk().withdraw()
    path = askopenfilename()
    return path


def check_file(path):
    """
    Checks if a file is a tomo histogram, binary image or volume . If true, the
    header info is returned as dictionary ('dim_x', 'dim_y', 'dim_z', 'header_
    length', 'byte_length'), else boolean False is returned.
    """

    with open(path) as f:

        # get file size for check_header routine

        fsize = os.path.getsize(path)

        # read first 100 characters of the file (header).

        f_100 = f.read(100)

        # analyze first 100 characters

        header_split = f_100.split('\r\n')

        # check if header contains four underscores (histogram)

        header = header_split[0]
        header_list = header.split('_')

        if len([m.start() for m in re.finditer('_', header)]) == 4:
            dim_x = int(header_list[3])
            dim_y = 1
            dim_z = 1
            header_length = header.__len__() + 2
        elif len([m.start() for m in re.finditer('_', header)]) == 5:

        # check if header contains five underscores (image)

            dim_x = int(header_list[3])
            dim_y = int(header_list[4])
            dim_z = 1
            header_length = header.__len__() + 2
        elif len([m.start() for m in re.finditer('_', header)]) == 6:

        # check if header contains six underscores (volume)

            dim_x = int(header_list[3])
            dim_y = int(header_list[4])
            dim_z = int(header_list[5])
            header_length = header.__len__() + 2
        else:
            return False

        # check if header length is ok and image size given in header matches
        # file size

        if len(header_list) not in (5, 6, 7) and 2 * dim_x * dim_y \
                * dim_z != fsize - header_length:
            return False

        # check byte length

        byte_length = (fsize - header_length) / (dim_x * dim_y * dim_z)

        data_info = dict([('dim_x', dim_x), ('dim_y', dim_y), ('dim_z',
                         dim_z), ('header_length', header_length),
                         ('byte_length', byte_length)])
        return data_info
