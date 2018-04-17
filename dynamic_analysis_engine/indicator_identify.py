#!/usr/bin/env python
# -*- coding: utf-8 -*-

__atuthor__ = "ririhedou"
__time__ = "fall2017"

from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit.ast import DotAccessor, Identifier, If

#functions are usually used for obfuscation
obfuscation_function_names = ['eval', 'replace', 'charCodeAt', 'fromCharCode', 'split', 'substr','unescape']

#user agent, app version, location, time,
profiling_function_names = ['navigator','userAgent','appVersion','appName',
                            'geolocation', 'Date', 'getTime', 'getMonth', 'getYear',
                            'getMinutes', 'getSeconds']


def inital_check_for_obfuscation_condtiion_sensitiveFunctions(js_text):
    """
    :param js_text:
    :return:
    """
    parser = Parser()
    tree = parser.parse(js_text)

    keywords = set()
    if_condition = False

    for node in nodevisitor.visit(tree):

        if isinstance(node, If):
            if_condition = True
            continue

        stack = [node]

        #Depth first to go to every depth of the AST tree
        while stack:

            node = stack.pop()

            #only dot access has a.b.getStringfromChar
            if isinstance(node, DotAccessor):
                try:
                    for i in node.children():
                        stack.append(i)
                except:
                    pass

                continue

            if isinstance(node, Identifier):
                #print (node.value),
                keywords.add(node.value)

    obfuscation = False
    profiling = False

    if if_condition:
        pass

    for ob in obfuscation_function_names:
        if ob in keywords:
            print ("[Obfuscation keywords]", ob)
            obfuscation = True
            break

    for pro in profiling_function_names:
        if pro in keywords:
            print ("[Profiling keywords]", pro)
            profiling = True
            break

    #conserveation
    if len(profiling_function_names) == 0 and len(obfuscation_function_names)==0:
        #we conservatively set it true
        print ("[No Obfuscation and Prifling] Conservative analysis")
        obfuscation = True
        profiling = True

    print ("[Obfuscation Summary] if_condition: {}, obfuscation {}, profiling {}".format(if_condition, obfuscation, profiling))
    return if_condition, obfuscation, profiling

