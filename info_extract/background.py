#!/usr/bin/env python
# -*- coding: utf-8 -*-
# this is python 2.7

"""
Extract background information
"""


def background_analysis(soup):
    body = str("body")
    html = str("html")
    head = str("head")

    print ('=== Background Info ===')
    if len(soup.findAll(body)) >= 2:
        print ('presence_of_double_body')

    if len(soup.findAll(html)) >= 2:
        print ('presence_of_double_html')

    if len(soup.findAll(head)) >= 2:
        print ('presence_of_double_head')

    content_tags = soup.findAll('meta', attrs={"name": "generator"})

    content_string = ""

    for tag in content_tags:
        if tag.has_attr('content'):
            content_string += str(tag.get('content'))

    print ('content type', content_string)

    return



