#!/usr/bin/env python
# -*- coding: utf-8 -*-
# this is python 2.7

__author__ = "ririhedou"
__time__ = "fall2017"

"""
emulate the browser and get output from the browser
"""

import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


from dynamic_analysis_engine import parse_js_and_save
from dynamic_analysis_engine import post_log_analysis


from sys import platform

if platform == "linux" or platform == "linux2":
    path_to_chrome_driver = os.getcwd() + "/dynamic_analysis_engine/dependence/linux/chromedriver"
elif platform == "darwin":
    path_to_chrome_driver = os.getcwd() + "/dynamic_analysis_engine/dependence/chromedriver"
else:
    raise Exception('Not supported platform')

#Candidate UA list: cover IE/Safari/Chrome/FireFox

UA_IE8_Windows7 = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"
UA_Safari_Mac = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1"
UA_Chrome_Windows = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36"
UA_Firefox_Window = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0"

UAs = [UA_IE8_Windows7, UA_Chrome_Windows, UA_Firefox_Window, UA_Safari_Mac]


os.environ["webdriver.chrome.driver"] = path_to_chrome_driver
LOGGING = False

class ChromeConsoleLogging(object):
    def __init__(self, ):
        self.driver = None

    def setUp(self, user_agent=None):
        if user_agent is None:
            self.user_agent = UA_IE8_Windows7
        else:
            self.user_agent = user_agent

        desired = DesiredCapabilities.CHROME

        PROXY = "localhost:8083"  # IP:PORT or HOST:PORT
        #IMPORTANT
        #This proxy cannot be connected to protect us from downloading malicious files:

        #print ("we use this user agent "+ self.user_agent)
        chrome_options = Options()

        chrome_options.add_argument("user-agent="+self.user_agent)

        chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-wifi")
        chrome_options.add_argument("--disable-local-storage")
        chrome_options.add_argument("--disable-gpu")

        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument("--disable-background-networking")

        desired['loggingPrefs'] = {'browser': 'ALL'}
        desired['browserConnectionEnabled'] = False

        self.driver = webdriver.Chrome(executable_path=path_to_chrome_driver, desired_capabilities=desired,
                                       chrome_options=chrome_options)
        self.driver.set_page_load_timeout(5)
        self.driver.implicitly_wait(5)

    def mimick_user_interactions(self):
        links = self.driver.find_elements_by_tag_name("a")

        if len(links) >= 2:
            link1 = links[0]
            link2 = links[1]

            actions = ActionChains(self.driver)
            actions.move_to_element(link1)
            actions.move_to_element(link2)
            actions.perform()

        elif len(links) > 0:
            link = links[0]
            actions = ActionChains(self.driver)
            actions.move_to_element(link)
            actions.perform()
        else:
            pass

    def quit_driver(self, ):
        self.driver.quit()

    def analyze_html_iframe_detection(self, path):
        try:
            self.driver.get(path)
        except Exception:
            #self.driver.execute_script("window.stop()")
            print ("PAGE LOAD Time out")
            self.quit_driver()
            self.setUp()
            return None

        self.driver.find_element_by_tag_name('body').send_keys(Keys.SHIFT + Keys.ALT + 't')
        self.mimick_user_interactions()
        data = self.driver.get_log('browser')
        texts = []
        for i in data:
            texts.append(str(i['message'].encode('utf-8')))

        src = post_log_analysis.get_iframe_and_source_information(texts)
        return src


def append_iframe_detection_js_to_html(ahtml):

    # the path in inject JS code for mutation observing
    path = "./dynamic_analysis_engine/iframe_detection_code.js"

    with open(path, 'r') as myfile:
        data = myfile.read()

    f = open(ahtml, 'r+')
    lines = f.readlines()  # read old content
    f.seek(0)  # go back to the beginning of the file
    f.write(data)  # write new content at the beginning
    for line in lines:  # write old content after new
        f.write(line)
    f.close()


################ Run Different UAs under selection ##############
def run_selelction_based_emulator(js, input_path, need_ua=False):

    cur_out = "/tmp/"+input_path.split("/")[-1]
    print ("[MutationObserver] Run MutationObserver to capture Iframe Injection")

    try:
        os.remove(cur_out)
    except OSError:
        pass

    parse_js_and_save.concatenate_js_to_a_basic_html(js, saved_name=cur_out)

    append_iframe_detection_js_to_html(cur_out)

    print ("[Temp] Temporary HTML created at {}".format(cur_out))

    srcs = None
    if need_ua:
        srcs = run_different_user_agent_for_html_file(cur_out)
    else:
        src = run_one_user_agent_for_html_file(cur_out)
        if src:
            srcs = [src]
        else:
            pass

    os.remove(cur_out)
    print ("[Temp] Temporary HTML removed at {}".format(cur_out))

    return srcs


def run_one_user_agent_for_html_file(cur_out):
    chrome = ChromeConsoleLogging()
    chrome.setUp(UA_IE8_Windows7)
    src = chrome.analyze_html_iframe_detection("file://" + cur_out)
    return src


def run_different_user_agent_for_html_file(cur_out):
    """
    :param file: format as  /tmp/test.html
    :return: src
    """
    srcs = set()
    chrome = ChromeConsoleLogging()
    for UA in UAs:
        chrome.setUp(UA)
        print ("we use this UA", UA)
        src = chrome.analyze_html_iframe_detection("file://" + cur_out)
        if src is not None:
            srcs.add(src)
    chrome.quit_driver()

    if len(srcs) == 0:
        return None

    return srcs


def create_file_to_store_src(outDir, filename, idx, src):

    if not outDir.endswith("/"):
        outDir = outDir + "/"

    fname = outDir + "detect_"+filename+"-"+str(idx)

    with open(fname,"wb") as f:
         f.write(src)
         f.flush()
         f.close()
    return


def create_file_to_save_concatenated_html(js, idx, input_path, need_ua):
    #cur_out = "/tmp/direct_run_without_condition.html"
    if need_ua:
        cur_out = "/tmp/"+input_path.split("/")[-1] + '_' +'needua' + '_' + str(idx) + '.html'
    else:
        cur_out = "/tmp/"+input_path.split("/")[-1] + '_' + 'Noneedua' + '_' + str(idx) + '.html'

    print ("create file at %s" %cur_out)
    try:
        os.remove(cur_out)
    except OSError:
        pass

    parse_js_and_save.concatenate_js_to_a_basic_html(js, saved_name=cur_out)
    append_iframe_detection_js_to_html(cur_out)
    return


def run_dynamic_analysis(input_file, outDir):

    afile = input_file

    print ("PATH for the chrome is {}".format(path_to_chrome_driver))
    print ("we are analyzing {}".format(afile))

    start_time = time.time()

    (scripts, _) = parse_js_and_save.preprocess_check_for_url(afile)
    if scripts is None:
        sys.exit()
    c = 0
    for js in scripts:
        print ("++++run "+str(c)+"-th JS ++++++")
        ua_need, analysis_need = parse_js_and_save.ast_check_for_obfuscation_profiling(js)
        if not analysis_need:
            pass
        elif ua_need:
            srcs = run_selelction_based_emulator(js, input_file, need_ua=True)
            if srcs is not None:
                create_file_to_store_src(outDir, afile.replace("/","_"), c, "\n".join(list(srcs)))
        else:

            #do not have to specify different UAs, direct run with one UA
            #create_file_to_save_concatenated_html(js, c, input_file, need_ua=False)
            srcs = run_selelction_based_emulator(js, input_file, need_ua=False)
            if srcs:
                create_file_to_store_src(outDir,afile.replace("/","_"),c,"\n".join(list(srcs)))
        c += 1
    end_time = time.time()
    print("time for", input_file, len(scripts), "tags", end_time-start_time)
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

    run_dynamic_analysis(input_file_abs_path, outDir)

"""
./run_fast_linux.sh /mnt/sdb1/domcrawl/iframe_vs_from_zhou/martin/embedScript/12f08b0210e2bc74dcf03ed19aa1490b3d5c2279ae738752ffbbb61fc6d109f1 /tmp/
./run_paralled_linux.sh  /mnt/sdb1/domcrawl/iframe_vs_from_zhou/martin/embedScript/ /tmp/
"""






