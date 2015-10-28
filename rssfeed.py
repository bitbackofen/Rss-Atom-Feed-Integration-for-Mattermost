#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Markus'


class RssFeed:
    def __init__(self, name, url, lasttitle, newtitle, articleurl):
        self.name = name
        self.url = url
        self.lasttitle = lasttitle
        self.newtitle = newtitle
        self.articleurl = articleurl
