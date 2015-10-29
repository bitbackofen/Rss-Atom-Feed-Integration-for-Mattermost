#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'elpatron@mailbox.org'
# Derived from https://github.com/mattermost/mattermost-integration-gitlab

import requests
import json
import feedparser
import time
import sys
import logging
from rssfeed import RssFeed

# Paste the Mattermost webhook URL you created here
# See also: https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md
mattermost_webhook_url = 'https://192.168.0.238/hooks/cns14rjjfpfrxpgoujxpm7sy3w'
# Leave this blank to post to the default channel of your webhook
mattermost_channel = 'testing'
# Set the delay between feed pulls to your needs. 5 minutes should be okay.
delay_between_pulls = 60 * 5

# Your feeds come here:
# RssFeed('Feed name', 'Feed URL', 'Mattermost username', 'Mattermost channel',
# show name, show title, show description, show url)
#
# show name, show title, show description, show url can be True or False; at least one of them should be True
# show description (longer text or full article) seems not to work with every feed.
# Set to False it if a feed doesnt´t work.
feeds = (RssFeed('Heise News', 'http://heise.de.feedsportal.com/c/35207/f/653902/index.rss', 'RSS-Bot', 'testing',
                 True, True, True, True),
         RssFeed('t3n', 'https://feeds2.feedburner.com/aktuell/feeds/rss/', 'RSS-Bot', 'testing',
                 True, True, False, True),
         RssFeed('Toms Hardware', 'http://www.tomshardware.com/articles.xml', 'RSS-Bot', 'testing',
                 True, True, True, True),
         RssFeed('Mattermost Forum', 'http://forum.mattermost.org/latest.rss', 'RSS-Bot', 'testing',
                 True, True, True, True))


def post_text(text, username, channel):
    """
    Mattermost POST method, posts text to the Mattermost incoming webhook URL
    """
    data = {}
    data['text'] = text
    if len(username) > 0:
        data['username'] = username
    if len(channel) > 0:
        data['channel'] = channel

    headers = {'Content-Type': 'application/json'}
    r = requests.post(mattermost_webhook_url, headers=headers, data=json.dumps(data), verify=False)

    if r.status_code is not requests.codes.ok:
        logging.debug('Encountered error posting to Mattermost URL %s, status=%d, response_body=%s' % (mattermost_webhook_url,
                                                                                               r.status_code, r.json()))


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    if len(mattermost_webhook_url) == 0:
        print('mattermost_webhook_url must be configured. Please see instructions in README.md')
        sys.exit()

    while 1:
        for feed in feeds:
            d = feedparser.parse(feed.Url)
            feed.NewTitle = d['entries'][0]['title']
            feed.ArticleUrl = d['entries'][0]['link']
            feed.Description = d['entries'][0]['description']
            if feed.LastTitle != feed.NewTitle:
                logging.debug('Feed url: ' + feed.Url)
                logging.debug('Title: ' + feed.NewTitle + '\n')
                logging.debug('Link: ' + feed.ArticleUrl + '\n')
                logging.debug('Posted text: ' + feed.jointext())
                post_text(feed.jointext(), feed.User, feed.Channel)
                feed.LastTitle = feed.NewTitle
            else:
                logging.debug('Nothing new. Waiting for good news...')

        time.sleep(delay_between_pulls)
