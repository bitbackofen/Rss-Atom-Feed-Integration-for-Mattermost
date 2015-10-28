#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Markus'


class RssFeed:
    def __init__(self, name, url, user, channel):
        self.name = name
        self.url = url
        self.user = user
        self.channel = channel
        self.lasttitle = ''
        self.newtitle = ''
        self.articleurl = ''
