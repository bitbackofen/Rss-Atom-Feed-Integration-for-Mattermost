#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'elpatron@mailbox.org'
# Partially derived from https://github.com/mattermost/mattermost-integration-gitlab

import json
import time
import sys
import logging
import os
import settings
import ssl
import threading
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from rssfeed import RssFeed

try:
    import feedparser
    import requests
except ImportError as exc:
    print('Error: failed to import module ({}). \nInstall missing modules using '
                      '"sudo pip install -r requirements.txt"'.format(exc))
    sys.exit(0)

mattermost_webhook_url = settings.mattermost_webhook_url
mattermost_integration_token = settings.mattermost_integration_token
delay_between_pulls = settings.delay_between_pulls
verify_cert = settings.verify_cert
silent_mode = settings.silent_mode
feeds = settings.feeds
integration_listening_addr = settings.integration_listening_addr
integration_listening_port = settings.integration_listening_port

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

class RSSManagementRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.data = {
            'response_type': 'ephemeral'
        }
        if len(settings.integration_bot_name) > 0:
            self.data['username'] = settings.integration_bot_name
        if len(settings.integration_bot_img) > 0:
            self.data['icon_url'] = settings.integration_bot_img

        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _check_header(self, token):
        if token == mattermost_integration_token:
            return True
        else:
            self.send_response(403)
            return False

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        global feeds
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        params = urlparse.parse_qs(post_body)

        if self._check_header(params.get('token')[0]):
            self._set_headers()
            commands = params.get('text', ['list'])[0].split(' ')

            if commands[0] == 'add' and len(commands) >= 3 and len(commands) <= 8:
                print(commands)
                feed = RssFeed(
                    commands[1],
                    commands[2],
                    commands[3] if len(commands) >= 4 and commands[3].startswith('http') else '',
                    commands[1],
                    params.get('channel_name', [settings.default_channel])[0],
                    commands[4] == 'True' if len(commands) >= 5 else settings.default_show_name,
                    commands[5] == 'True' if len(commands) >= 6 else settings.default_show_title,
                    commands[6] == 'True' if len(commands) >= 7 else settings.default_show_description,
                    commands[7] == 'True' if len(commands) >= 8 else settings.default_show_url
                )

                feed.LastTitle = 'Init'
                fetching_feed(feed)
                feeds.append(feed)
                if os.path.isfile('feeds.env'):
                    with open('feeds.env', 'a') as feeds_env:
                        feeds_env.write(feed.env_definition())

            elif commands[0] == 'remove' and len(commands) == 2:
                feeds = [feed for feed in feeds if feed.Name != commands[1]]
                if os.path.isfile('feeds.env'):
                    with open('feeds.env', 'r') as feeds_env:
                        lines = feeds_env.readlines()
                    with open('feeds.env', 'w') as feeds_env:
                        for line in [l for l in lines if not l.startswith('RSS_FEED_' + commands[1] + '=')]:
                            feeds_env.write(line)

            if commands[0] in ('list', 'add', 'remove'):
                self.data['text'] = '---\n' + '\n'.join(['* [' + feed.Name + '](' + feed.Url + ') on @' + feed.Channel for feed in feeds]) + '\n---'
            else:
                self.data['text'] = 'Sorry, I don\'t understand your command: `' + params.get('text', '')[0] + '`'
            self.wfile.write(json.dumps(self.data))

def fetching_feed(feed):
    try:
        d = feedparser.parse(feed.Url)
        feed.NewTitle = d['entries'][0]['title']
        feed.ArticleUrl = d['entries'][0]['link']
        feed.Description = d['entries'][0]['description']
        if settings.skip_init_article and len(feed.LastTitle) <= 0:
            if not silent_mode:
                logging.debug('Initializing feed: ' + feed.Name + '. Skipping the last news: ' + feed.NewTitle)
            feed.LastTitle = feed.NewTitle
        elif feed.LastTitle != feed.NewTitle:
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

if __name__ == "__main__":
    FORMAT = '%(asctime)-15s - %(message)s'
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)

    if len(mattermost_integration_token) == 0:
        print('mattermost_integration_token must be configured to enable integration. Please see instructions in README.md')
    else:
        httpd = HTTPServer((integration_listening_addr, integration_listening_port), RSSManagementRequestHandler)

        t = threading.Thread(target=httpd.serve_forever)
        t.daemon = True
        t.start()

    if len(mattermost_webhook_url) == 0:
        print('mattermost_webhook_url must be configured. Please see instructions in README.md')
        sys.exit()

    while 1:
        for feed in feeds:
            fetching_feed(feed)

        time.sleep(delay_between_pulls)
