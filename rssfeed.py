#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Markus'

import html2text

class RssFeed:
    def __init__(self, name, url, user, channel, showtitle, showdescription, showurl):
        self.Name = name
        self.Url = url
        self.User = user
        self.Channel = channel
        self.ShowTitle = showtitle
        self.ShowDescription = showdescription
        self.ShowUrl = showurl
        self.LastTitle = ''
        self.NewTitle = ''
        self.ArticleUrl = ''
        self.Description = ''

    def jointext(self):
        text = ''
        h = html2text.HTML2Text()
        h.ignore_links = True
        self.Description = h.handle(self.Description)
        if self.ShowTitle == True:
            text += self.NewTitle + '\n'
        if self.ShowDescription == True:
            text += self.Description + '\n'
        if self.ShowUrl == True:
            text += self.ArticleUrl
        return text
