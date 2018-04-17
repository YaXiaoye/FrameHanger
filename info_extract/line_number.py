# used for data processing
# -*- coding: utf-8 -*-
# this is python 2.7


"""
BeautifulSoup does not provide with exact line number, I find the tag to match the body/html/head
Disussions:
https://groups.google.com/forum/#!topic/beautifulsoup/sy2skfowsso
"""

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

import collections
import pprint

class RelativeLocationParse(HTMLParser):
    def __init__(self, tagName="iframe"):

        self.reset()

        self.iframecount = 0

        self.iframeLocationLine = collections.defaultdict(int)
        self.iframeLocationAttr = collections.defaultdict(list)

        self.elementBeginLocation = collections.defaultdict(list)
        self.elementEndLocation = collections.defaultdict(list)

        self.tagName = tagName
        self.line_number = 0

        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        #print (tag,attrs, self.getpos())
        line, off = self.getpos()
        if tag == self.tagName:

            tmp = self.iframecount
            self.iframeLocationLine[tmp] = line
            self.iframeLocationAttr[tmp] = attrs
            self.iframecount += 1

        elif tag in ["body", "html", "header"]:
            self.elementBeginLocation[tag].append(line)

        else:
            pass

    def has_iframes(self):
        if len(self.iframeLocationLine) > 0:
            return True
        else:
            return False

    def handle_endtag(self, tag):
        line, off = self.getpos()

        if line > self.line_number:
            self.line_number = line

        if tag in ["body", "html", "header"]:
            self.elementEndLocation[tag].append(line)

    def get_iframe_count(self):
        return (self.iframecount)

    def print_html_info(self):
        print ("=== Line Number Info === ")
        print ("begin body/html/header line number")
        print (dict(self.elementBeginLocation))

        print ("\nend body/html/header line number")
        print (dict(self.elementEndLocation))

    def print_each_iframe(self, i):
        print (">>line number")
        pprint.pprint(self.iframeLocationLine[i])
        print (">>attribute")
        pprint.pprint(dict(self.iframeLocationAttr[i]))


