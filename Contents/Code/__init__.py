# PMS plugin framework
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

####################################################################################################

VERSION = 0.3

VIDEO_PREFIX = "/video/ch9"

NAME = L('Title')

# make sure to replace artwork with what you want
# these filenames reference the example files in
# the Contents/Resources/ folder in the bundle
ART           = 'art-ch9.jpg'
ICON          = 'icon-default.jpg'

FIX_PLAY_ROOT = "http://fixplay.ninemsn.com.au/"
FIX_PLAY_ROOT2 = "http://catchup.ninemsn.com.au/"
FIX_PLAY_LIST = "http://fixplay.ninemsn.com.au/catalogue.aspx"

####################################################################################################
def Start():

    Plugin.AddPrefixHandler(VIDEO_PREFIX, MainMenu, L('VideoTitle'), ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)
    
####################################################################################################
def MainMenu():
    dir = MediaContainer(viewGroup="List")
    content = XML.ElementFromURL(FIX_PLAY_LIST, True)
    for item in content.xpath('//div//div/div[@id="Catalog_right_col"]/span/li'):
        image = item.xpath('./div[2]/img')[0].get('src')
        image = image
        title = item.xpath('./a/div/span[1]')[0].text
        link = item.xpath('./a')[0].get('href')
        link = FIX_PLAY_ROOT2 + link
        Log ("MainMenu -Link: " + link)
        dir.Append(Function(DirectoryItem(SeasonMenu, title=title, thumb=image), pageUrl = link, thumbUrl=image))
    return dir

####################################################################################################
def SeasonMenu(sender, pageUrl, thumbUrl):
    Log("In season menu")
    myNamespaces     = {'ns1':'http://www.w3.org/1999/xhtml'}
    xpathQuery = '//div[@id="cat_hl_224591"]/span/span/a'
    Log ("reading pageUrl: " + pageUrl[:29] + "##" + pageUrl[30:])
    dir = MediaContainer(title2=sender.itemTitle, viewGroup="InfoList")
    content = XML.ElementFromURL(pageUrl[:29]+pageUrl[30:], True)
    seasons = []
    for item in content.xpath('//body/div/form/div/div/div/div/div/div/div/div/span/span/a'):
        Log("matched" + item.text +">>>"+ item.get('href'))
        if item.text not in seasons:
            seasons.append(item.text)
            dir.Append(Function(DirectoryItem(VideoPage, title=item.text,thumb=thumbUrl),pageUrl=item.get('href'), seriesTitle=item.text))
    
    return dir

####################################################################################################
def VideoPage(sender, pageUrl, seriesTitle):
    dir = MediaContainer(title2=sender.itemTitle, viewGroup="InfoList")
    myNamespaces = {'ns1':'http://www.w3.org/1999/xhtml'}
    Log ("reading pageUrl: " + FIX_PLAY_ROOT + pageUrl[1:])
    content = XML.ElementFromURL(FIX_PLAY_ROOT + pageUrl[1:], True)
    xpathQuery = "//*[@id=\"season_table\"]/span/div"
    for item in content.xpath(xpathQuery, namespaces=myNamespaces):
        episode = item.xpath(".//div")[0].text
        title = item.xpath(".//div[@class='td col2']/h3")[0].text
        summary = item.xpath(".//div[@class='td col2']//span[@class='season_desc']")[0].text
        link = item.xpath(".//div[@class='td col3']/a")[0].get('href')
        link = FIX_PLAY_ROOT + link
        Log(link)
        dir.Append(WebVideoItem(link, title=title, summary=summary))
        
    return dir