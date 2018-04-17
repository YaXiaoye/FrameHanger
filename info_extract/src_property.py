#!/usr/bin/env python
# -*- coding: utf-8 -*-
# this is python 2.7

import urlparse
import tldextract


class URL_INFO():
    @staticmethod
    def _get_subdomain_and_tld(url):
        ex = tldextract.extract(url)
        subdomain = ex.subdomain
        #the www is not regarded as a subdomain
        if subdomain == "www":
            subdomain = ""

        if subdomain.startswith("www."):
            subdomain = subdomain[4:]

        tld = ex.suffix #isTLD
        return (subdomain, tld)

    @staticmethod
    def _get_path_query_fragments(url):
        # cleean url
        parser = urlparse.urlparse(url)
        path = parser.path
        query = parser.query
        fragment = parser.fragment
        return path, query, fragment

    @staticmethod
    def _get_netloc(url):
        parser = urlparse.urlparse(url)
        return parser.netloc

    @staticmethod
    def _get_host_name_with_path(url):
        parser = urlparse.urlparse(url)
        path = parser.path
        netloc = parser.netloc
        return str(netloc)+str(path)


def source_lexical_information(iframe_src):
    src = str(iframe_src).replace(" ", "").lower()
    domain_name = URL_INFO._get_netloc(src)
    print ("=== URL info ===")
    print ("sum of dots", domain_name.count("."))
    print ("sun of digits",sum(c.isdigit() for c in domain_name))
    print ("sum of letters", sum(c.isalpha() for c in domain_name))

    subdomain, tld = URL_INFO._get_subdomain_and_tld(src)

    print ("subdomain", subdomain)
    print ("TLD", tld)

    (path, query, fragment) = URL_INFO._get_path_query_fragments(src)

    path = str(path).replace("/", "")
    queryDic = urlparse.parse_qs(query)
    print ("path", path)
    print ("fragment", fragment)
    print ("queryDic", queryDic)

    return
