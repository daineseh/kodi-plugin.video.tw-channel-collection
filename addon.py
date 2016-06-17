#-*- coding: utf-8 -*-
import sys
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import youtube_dl

from clawler import CHANNELS, Channel


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def page_number(url):
    return url.split('-')[-1].split('.')[0]

mode = args.get('mode', None)

if mode is None:
    for channel, _url in CHANNELS.iteritems():
        url = build_url({'mode': 'channel', 'folder_name': _url})
        li = xbmcgui.ListItem('[COLOR white]%s[/COLOR]' % channel)
        obj = Channel(_url)
        li.setArt({'thumb': obj.get_logo(), 'icon': obj.get_logo(), 'fanart': obj.get_logo()})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'channel':
    url = args['folder_name'][0]
    obj = Channel(url)
    for (title, length, timestamp, link, thumb) in obj.info():
        url = build_url({'mode': 'play', 'folder_name': link})
        li = xbmcgui.ListItem('[COLOR white]%s[/COLOR][%s][%s]' % (title, length, timestamp))
        li.setArt({'thumb': thumb, 'icon': thumb, 'fanart': thumb})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'play':
    url = args['folder_name'][0]

    opts = {
        'forceurl': True,
        'quiet': True,
        'simulate': True,
    }

    with youtube_dl.YoutubeDL(opts) as ydl:
        resource_uri = ydl.extract_info(url).get('url')
        if not resource_uri:
            entries = ydl.extract_info(url).get('entries')
            resource_uri = entries[-1].get('url')
    xbmc.Player().play(resource_uri)

