# used for data processing
# -*- coding: utf-8 -*-
# this is python 2.7

__author__ = "ketian"
__time__ = "summer2017"

import bs4
from bs4 import BeautifulSoup
import os

LOGGING = False

from indicator_identify import inital_check_for_obfuscation_condtiion_sensitiveFunctions


def preprocess_check_for_url(url):
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
        if LOGGING:
            print ("cannot process data into the utf-8 format")
        return (None,None)

    soup = BeautifulSoup(data, "html.parser")
    scripts = soup.findAll("script")

    return scripts, soup


def ast_check_for_obfuscation_profiling(js):

    assert isinstance(js, bs4.element.Tag)

    if len(js.text) == 0:
        return False,False

    try:
        if_condition, obfuscation, profiling = inital_check_for_obfuscation_condtiion_sensitiveFunctions(js.text)
    except:
        print ("AST breaks! conservative analysis")
        obfuscation, profiling = True, True

    #force it into javascript code
    if js.get('type'):
        js_type =  js.get('type')
        if js_type != 'text/javascript':
            js['type'] = 'text/javascript'

    if obfuscation or profiling:
        return True, True

    return False, True


def concatenate_js_to_a_basic_html(js, saved_name="/tmp/temp.html"):

    basic_html = "basic.html"
    _basic_html = os.getcwd() + '/dynamic_analysis_engine/' + basic_html

    with open(_basic_html, 'r') as myfile:
        data = myfile.read()

    soup = BeautifulSoup(data, "html.parser")
    body = soup.find('body')
    body.append(js)

    html = soup.prettify("utf-8")
    file = open(saved_name, "wb")
    file.write(str(html))
    file.flush()
    file.close()


################################  TEST ##################################
def parse_js_in_soup(url):

    filename = url.split('/')[-1]
    _, soup = preprocess_check_for_url(url)

    if soup is None:
        if LOGGING:
            print ("None data")
        return False

    scripts = soup.findAll('script')

    count_js = 0
    for js in scripts:

        if not ast_check_for_obfuscation_profiling(js):
            continue

        save_file_name = os.getcwd() + "/tmp_html/" + filename + "-" +str(count_js)
        concatenate_js_to_a_basic_html(js, saved_name=save_file_name)
        count_js += 1

    print ('[Step][parse] total: '+ str(count_js)+' JS files, concatenated,saved in to tmp_html/*.html---------')
    return True

