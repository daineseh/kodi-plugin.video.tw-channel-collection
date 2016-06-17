# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
from collections import OrderedDict

import re
import requests
import urlparse


YOUTUBE_URL = 'https://www.youtube.com'
BUILD_YOUTUBE_URL = lambda x: urlparse.urljoin(YOUTUBE_URL, x).encode('utf8')

CHANNELS = OrderedDict([
            ("PeoPo 公民新聞", "https://www.youtube.com/user/peoponews/videos"),
            ("PTS 台灣公共電視", "https://www.youtube.com/user/pts/videos"),
            ("The News Lens 關鍵評論網", "https://www.youtube.com/user/thenewslens/videos"),
            ("公視新聞網", "https://www.youtube.com/user/PNNPTS/videos"),
            ("台灣宏觀電視", "https://www.youtube.com/user/macroview/videos")
           ])


class Channel:
    def __init__(self, url):
        self._req = requests.get(url)
        self.soup = BeautifulSoup(self._req.text, "html.parser")

    def get_logo(self):
        img_tag = self.soup.find('img', {'class': 'channel-header-profile-image'})
        if not img_tag:
            return ''
        return img_tag.get('src')

    def length(self, tag):
        tag = tag.find("span", {"class":"video-time"})
        if not tag:
            return ''
        return tag.string

    def link(self, tag):
        tag = tag.find('a', {"aria-hidden":"true"})
        if not tag:
            return ''
        return BUILD_YOUTUBE_URL(tag.get('href'))

    def timestamp(self, tag):
        time = ''
        for tag in tag.find_all('li'):
            time = tag.string
        return time

    def title(self, tag):
        tag = tag.find('a', {"dir":"ltr"})
        if not tag:
            return ''
        return tag.string

    def thumb(self, tag):
        tag = tag.find("img", {"alt": ''})
        if not tag:
            return ''
        return tag.get('src').split('?')[0]

    def info(self):
        info = []
        for tag in self.soup.find_all("div", {"class": "yt-lockup-dismissable"}):
            title = self.title(tag)
            thumb = self.thumb(tag)
            link = self.link(tag)
            length = self.length(tag)
            timestamp = self.timestamp(tag)
            info.append((title, length, timestamp, link, thumb))
        return info


if __name__ == '__main__':
    obj = Channel()
