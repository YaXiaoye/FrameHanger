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
import detection_dynamic
import detection_static


def extant_file(x):
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x


def parse_options():

    parser = argparse.ArgumentParser(description="iframe Injection detection", prefix_chars='-')

    parser.add_argument('-s', '--static', action='store_true', default=False,
                        help='Static analyser for Tag-based iframe injection')

    parser.add_argument('-d', '--dynamic', action='store_true', default=False,
                        help='Dynamic analyser for JS-based iframe injection')

    parser.add_argument('-o', '--outputdir', type=str, default='./',
                        help='Output directory, default is the current directory')

    parser.add_argument('-f', '--htmlfile', type=extant_file, required=True, help='the HTML File needs to be analyzed')

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parse_options()

    input_file = args.htmlfile

    if args.dynamic:
        pass
    elif args.static:
        pass
    else:
        pass


