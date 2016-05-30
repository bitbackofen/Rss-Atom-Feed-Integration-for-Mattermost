#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'elpatron@mailbox.org'
# Partially derived from https://github.com/mattermost/mattermost-integration-gitlab

import json
import time
import sys
import logging
import settings
import ssl
try:
    import feedparser
    import requests
except ImportError as exc:
    print('Error: failed to import module ({}). \nInstall missing modules using '
                      '"sudo pip install -r requirements.txt"'.format(exc))
    sys.exit(0)

mattermost_webhook_url = settings.mattermost_webhook_url
delay_between_pulls = settings.delay_between_pulls
verify_cert = settings.verify_cert
silent_mode = settings.silent_mode
feeds = settings.feeds

if (not verify_cert) and hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def post_text(text, username, channel, iconurl):
    """
    Mattermost POST method, posts text to the Mattermost incoming webhook URL
    """
    data = {}
    data['text'] = text
    if len(username) > 0:
        data['username'] = username
    if len(channel) > 0:
        data['channel'] = channel
    if len(iconurl) > 0:
        data['icon_url'] = iconurl

    headers = {'Content-Type': 'application/json'}
    r = requests.post(mattermost_webhook_url, headers=headers, data=json.dumps(data), verify=verify_cert)

    if r.status_code is not requests.codes.ok:
        logging.debug('Encountered error posting to Mattermost URL %s, status=%d, response_body=%s' %
                      (mattermost_webhook_url, r.status_code, r.json()))


if __name__ == "__main__":
    FORMAT = '%(asctime)-15s - %(message)s'
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)
    if len(mattermost_webhook_url) == 0:
        print('mattermost_webhook_url must be configured. Please see instructions in README.md')
        sys.exit()

    while 1:
        for feed in feeds:
            try:
                d = feedparser.parse(feed.Url)
                feed.NewTitle = d['entries'][0]['title']
                feed.ArticleUrl = d['entries'][0]['link']
                feed.Description = d['entries'][0]['description']
                if feed.LastTitle != feed.NewTitle:
                    if not silent_mode:
                        logging.debug('Feed url: ' + feed.Url)
                        logging.debug('Title: ' + feed.NewTitle)
                        logging.debug('Link: ' + feed.ArticleUrl)
                        logging.debug('Posted text: ' + feed.jointext())
                    post_text(feed.jointext(), feed.User, feed.Channel, feed.Iconurl)
                    feed.LastTitle = feed.NewTitle
                else:
                    if not silent_mode:
                        logging.debug('Nothing new. Waiting for good news...')
            except:
                logging.critical('Error fetching feed ' + feed.Url)
                logging.exception(sys.exc_info()[0])

        time.sleep(delay_between_pulls)
