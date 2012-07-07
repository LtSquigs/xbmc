import urllib
import urllib2
import simplejson
import xbmcaddon
import xbmcplugin
import xbmcgui

my_addon = xbmcaddon.Addon('plugin.video.tested')

def CATEGORIES():

    iconPath = my_addon.getAddonInfo('path') + '\\icons\\'

    name = 'Latest'
    url = 'https://gdata.youtube.com/feeds/api/users/testedcom/uploads?alt=json&prettyprint=true&v=2&max-results=20'
    addDir(name, url, 2, iconPath + "latest.png")

    #TODO: ADD IN "ALL", CLICK PAGES TO GO FORWARD
    name = 'Science & Technology'
    url = 'http://gdata.youtube.com/feeds/api/videos?alt=json&author=testedcom&prettyprint=true&v=2&max-results=50&orderby=published&category=Tech'
    addDir(name, url, 2,  iconPath + "science.png")
	
    name = 'Reviews'
    url = 'http://gdata.youtube.com/feeds/api/videos?alt=json&author=testedcom&prettyprint=true&v=2&max-results=50&orderby=published&category=review'
    addDir(name, url, 2,  iconPath + "review.png")
	
    name = 'App Of The Day'
    url = 'http://gdata.youtube.com/feeds/api/videos?alt=json&author=testedcom&prettyprint=true&v=2&max-results=50&orderby=published&category=app,of,the,day'
    addDir(name, url, 2,  iconPath + "app-of-the-day.png")
    
    name = 'DIY'
    url = 'http://gdata.youtube.com/feeds/api/videos?alt=json&author=testedcom&prettyprint=true&v=2&max-results=50&orderby=published&category=diy'
    addDir(name, url, 2,  iconPath + "diy.png")
	
    name = 'Coffee'
    url = 'http://gdata.youtube.com/feeds/api/videos?alt=json&author=testedcom&prettyprint=true&v=2&max-results=50&orderby=published&category=coffee'
    addDir(name, url, 2,  iconPath + "coffee.png")
	
    name = 'Howtos'
    url = 'http://gdata.youtube.com/feeds/api/videos?alt=json&author=testedcom&prettyprint=true&v=2&max-results=50&orderby=published&category=howto'
    addDir(name, url, 2,  iconPath + "howto.png")
	
    name = 'Makerbot'
    url = 'http://gdata.youtube.com/feeds/api/videos?alt=json&author=testedcom&prettyprint=true&v=2&max-results=50&orderby=published&category=makerbot'
    addDir(name, url, 2,  iconPath + "makerbot.png")
	
    name = 'Search'
    addDir(name, 'search', 1,  iconPath + "search.png")


def INDEX(url):
    if url == 'search':
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText().replace(' ', '%20')
            url = 'http://gdata.youtube.com/feeds/api/videos?alt=json&author=testedcom&prettyprint=true&v=2&q=' + query
            VIDEOLINKS(url, 'search')

def VIDEOLINKS(url, name):
    response = urllib2.urlopen(url)
    video_data = simplejson.loads(response.read())
    response.close()

    for vid in video_data['feed']['entry']:
        name = vid['title']['$t']
        
        url = 'plugin://plugin.video.youtube/?action=play_video&quality=720p&videoid=' + vid['media$group']['yt$videoid']['$t'] # to flash file, need to download it I guess?

        # Try to get the HD Thumbnail, if you cant than just grab the default one
        try:
            thumbnail = vid['media$group']['media$thumbnail'][2]['url']
        except:
            thumbnail = vid['media$group']['media$thumbnail'][0]['url']
        
        addLink(name,url,thumbnail)

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]

    return param

def addLink(name, url, iconimage):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("fanart_image", my_addon.getAddonInfo('path') + "/art.png")
    liz.setProperty( "Video", "true" )
    liz.setProperty( "IsPlayable", "true")
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir(name, url, mode, iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("fanart_image", my_addon.getAddonInfo('path') + "/art.png")
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

params=get_params()
url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
    print ""
    CATEGORIES()

elif mode==1:
    print ""+url
    INDEX(url)

elif mode==2:
    print ""+url
    VIDEOLINKS(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
