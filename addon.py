#-*- coding: utf-8 -*-
import sys
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import youtube_dl

from clawler import NEWS_CHANNELS, KNOWLEDGE_CHANNELS, COMMENT_CHANNELS, LIFE_CHANNELS, Channel


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def page_number(url):
    return url.split('-')[-1].split('.')[0]

def build_items(channel, url_str, color='lightgray'):
    url = build_url({'mode': 'channel', 'folder_name': url_str})
    li = xbmcgui.ListItem('[COLOR %s]%s[/COLOR]' % (color, channel))
    obj = Channel(url_str)
    li.setArt({'thumb': obj.get_logo(), 'icon': obj.get_logo(), 'fanart': obj.get_logo()})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

def banner_item(title, color='lightgray'):
    li = xbmcgui.ListItem('[COLOR %s]%s[/COLOR]' % (color, title))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=None, listitem=li, isFolder=False)


mode = args.get('mode', None)

if mode is None:
    banner_item('新聞', 'gold')
    for channel, _url in NEWS_CHANNELS.iteritems():
        build_items(channel, _url)

    banner_item('知識', 'gold')
    for channel, _url in KNOWLEDGE_CHANNELS.iteritems():
        build_items(channel, _url)

    banner_item('談論', 'gold')
    for channel, _url in COMMENT_CHANNELS.iteritems():
        build_items(channel, _url)

    banner_item('生活', 'gold')
    for channel, _url in LIFE_CHANNELS.iteritems():
        build_items(channel, _url)
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
        info = ydl.extract_info(url)
        resource_uri = info.get('url')
        if not resource_uri:
            vid = info.get('format_id')
            for item in info.get('formats'):
                if vid == item.get('format_id'):
                    resource_uri = item.get('url')
    if resource_uri:
        xbmc.Player().play(resource_uri)
    else:
        xbmc.log('[Youtube url]: %s,' % url, 0)
        xbmcgui.Dialog().notification("Oops!", "找不到影片串流", xbmcgui.NOTIFICATION_ERROR)

