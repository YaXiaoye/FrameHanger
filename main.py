# used for data processing
# -*- coding: utf-8 -*-
# this is python 2.7

__author__ = "ririhedou"

"""
several steps
1) get HTML
2) extract JS Script -> concatenate to a new HTML
3) inject monitoring JS code
4) run the browseer simulation in a container
"""

import os
import argparse


def extant_file(x):
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x


def parse_options():

    parser = argparse.ArgumentParser(description="iframe JavaScript detection" , prefix_chars='-')

    #parser.add_argument('-f', '--feainfo', action='store_true',default=False, help='get HTML feature information and its types')

    parser.add_argument('-v', '--virtual', action='store_true',default=False, help='Virtual Display is On' )

    parser.add_argument('-a', '--analysis', type=extant_file, help='Analyze the HTML File')

    args = parser.parse_args()

    return args


def real_whole_process(args):
    pass


if __name__ == "__main__":

    path_rig_js = "/Users/ketian/Desktop/jsiframe/analysis_engine/dependence/pure-maliciou-js-iframe.txt"

    def open_files(path):
        with open(path, 'r') as f:
            files = []
            for i in f.readlines():
                i = i.strip()
                files.append(i)
        return files

    scanned = open_files("analysis_engine/dependence/scanned.txt")
    args = parse_options()

    fname = args.analysis.split("/")[-1]
    real_whole_process(args)