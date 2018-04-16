# used for data processing
# -*- coding: utf-8 -*-
# this is python 2.7

"""
This file is used for log analysis to extract Iframes
"""


def get_iframe_and_source_information(logList):
    con = "[mutationObserve][iframe][summary]"
    texts = ""
    c = 0
    for eachlog in logList:
        c = c + 1
        eachlog = str(eachlog).replace("\"", "")

        if con in eachlog:
            arrow = "->"
            key_value = eachlog.split("[summary]")[-1]
            key = str(key_value.split(arrow)[0])
            value = str(key_value.split(arrow)[1])
            value = value.replace("\\\"", "")
            value = value.replace("\"", "")

            print ("[Detection]Detect an iframe injection: " + str(key) + "->" + str(value))
            if key == 'src':
                texts = texts + '\n[ffff]'+ str(c) + ":" + str(key) + "->" + str(value)
            else:
                texts = texts + '\n'+ str(c) + ":" + str(key) + "->" + str(value)

    if texts == "":
        return None

    return texts

