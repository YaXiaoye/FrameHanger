# used for data processing
# -*- coding: utf-8 -*-
# this is python 2.7

import sys
import os
from bs4 import BeautifulSoup
from info_extract.line_number import RelativeLocationParse
from info_extract.src_property import source_lexical_information
from info_extract.background import background_analysis


def preprocess_check_for_url(url, tag_name="iframe"):
    with open(url, 'r') as myfile:
        data = myfile.read()

    try:
        data = data.decode('unicode_escape').encode('utf-8')

    except Exception as inst:

        data = None
        f = open('log-error.log','a')
        f.write("Data Encode Exception: " + str(type(inst)) + " " + str(url)+'\n')
        f.close()

    if data is None:
        print ("cannot process data into the utf-8 format")
        return None, None, None

    try:
        line_number_parser = RelativeLocationParse(tagName=tag_name)
        line_number_parser.feed(data)

    except Exception as inst:
        f = open('log-error.log', 'a')
        f.write("HTML.Parse Exception: " + str(type(inst)) + " " + str(url) + '\n')
        f.close()

        return None, None, None

    try:
        soup = BeautifulSoup(data, "html.parser")
        iframes = soup.findAll(tag_name)

    except Exception as inst:
        f = open('log-error.log', 'a')
        f.write("SoupParse Exception: " + str(type(inst)) + " " + str(url) + '\n')
        f.close()
        return None, None, None

    if line_number_parser.iframecount != len(iframes):
        print ("NOT EQUAL in TWO PARSING: HTML.parser and beautifulSoup")
        f = open('log-error.log', 'a')
        f.write("INDEX ERROR  " + str(url) + '\n')
        f.close()
        return None, None, None

    return iframes, soup, line_number_parser


def static_iframe_info(html_file):
    iframes, soup, line_number_parser = preprocess_check_for_url(html_file)

    if iframes is None:
        return None

    print ("We have {} static Iframes".format(len(iframes)))
    line_number_parser.print_html_info()
    background_analysis(soup)

    for idx, ifr in enumerate(iframes):
        print ("=========================== {}-th IFrame ============================".format(idx))
        try:
            iframe = iframes[idx]
            line_number_parser.print_each_iframe(idx)

            if iframe.get('src'):
                src= iframe.get('src').encode('ascii', 'ignore').decode('ascii')
                source_lexical_information(src)
        except:
            print ("Exception for {}-th Iframe".format(idx))
    return


if __name__ == "__main__":

    try:
        input_file_abs_path = sys.argv[1]
    except:
        sys.exit()

    if not os.path.isfile(input_file_abs_path):
        print ("Not a file! safely exit")
        sys.exit()
    try:
        outDir = sys.argv[2]
    except:
        outDir = "/tmp/"

    static_iframe_info(input_file_abs_path)
