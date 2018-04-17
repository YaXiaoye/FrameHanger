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

    parser = argparse.ArgumentParser(description="iframe Injection detection", prefix_chars='-')

    parser.add_argument('-s', '--static', action='store_true', default=False, help='Static analyser for Tag-based injection')

    parser.add_argument('-d', '--dynamic', action='store_true', default=False,help='Dynamic analyser for JS-based injection')

    parser.add_argument('-o', '--outputdir', type=str, default='./', help='Analyze the HTML File')

    parser.add_argument('-f', '--html-file', type=extant_file, required=True, help='Analyze the HTML File')

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    pass