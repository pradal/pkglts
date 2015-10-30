""" Set of function to work with resources that are located inside
this package data
"""

from os import listdir
from os.path import dirname, isdir
from os.path import join as pj


pkg_root_dir = dirname(dirname(__file__))
pkg_data_dir = pj(pkg_root_dir, "pkglts_data")


def get_data_dir():
    return pkg_data_dir


def get(file_name):
    """ Retrieve the content of a given filename
    located in the data part of this package.

    args:
     - filename (str): name of the file to read

    return:
     - (str): content of the file red in 'r' mode
    """
    with open(pj(pkg_data_dir, file_name), 'r') as f:
        cnt = f.read()

    return cnt


def ls(dir_name):
    """ List all files and directories in dir_name
    located in the data part of this package.

    args:
     - dir_name (str): name of the directory to walk

    return:
     - (list of (str, bool)): list the content of dir_name
                       without any specific order, items are
                       (entity_name, is_directory)
    """
    pth = pj(pkg_data_dir, dir_name)
    return [(n, isdir(pj(pth, n))) for n in listdir(pth)]
