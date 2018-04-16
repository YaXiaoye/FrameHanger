#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The code to implement helper functions

(1) pickle related
(2) CSV read and write
(3) process bar
(4) others...

"""


__author__ = "ketian"

import pickle
import sys, os
import hashlib


def get_string_hash(string):
    """
    get a hash of string
    :param string:
    :return:
    """
    mystring = str(string.decode('utf-8', 'ignore'))
    m = hashlib.md5()
    m.update(mystring)

    return str(m.hexdigest())


def make_unicode(input):
    if type(input) != unicode:
        input =  input.decode('utf-8', 'ignore')
        return input
    else:
        return input


def md5(fname, blocksize=4096):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(blocksize), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def saveintopickle(obj, filename="obj.pickle"):
    with open(filename, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print ("[Pickle]: save object into {}".format(filename))
    return


def loadfrompickle(filename="obj.pickle"):
    with open(filename, 'rb') as handle:
        b = pickle.load(handle)
    return b


def update_progress(job_title, progress):
    """
    :param job_title: your job name, a string
    :param progress: a percent show the process, a float belongs 0~1
    :return: None
    """
    length = 20 # modify this to change the length
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2:.2f}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 2))
    if progress >= 1: msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()


def print_np_array(array):
    if array.size == 0:
        print ("Empty array")
        return

    x,y = array.shape
    for i in range(x):
        print ("")
        for j in range(y):
            print (str(array[i][j]) + ' '),

    return


def print_dictionary(adict):

    print ("LENGTH of the dict is {}".format(len(adict)))
    keylist = adict.keys()
    keylist.sort()

    for i in keylist:
        print ("KEY:  {}".format(i)) ,
        print (" | VALUE:  {}".format(adict[i]))
    pass


def read_files_from_a_dir_current_path(dataset):
    cwd = os.getcwd()
    files = os.listdir(dataset)
    files_absolute_paths = []
    for i in files:
        files_absolute_paths.append(cwd+"/"+dataset+str(i))
    return files_absolute_paths


def read_files_from_a_dir_absolute_path(dataset):
    files = os.listdir(dataset)
    files_absolute_paths = []
    for i in files:
        files_absolute_paths.append(dataset+str(i))
    return files_absolute_paths


def writeListIntoFile(alist,filename):
    f = open(filename,'w')
    for item in alist:
        f.write("%s\n" %item)
    f.close()


