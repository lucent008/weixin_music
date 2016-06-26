#!/usr/bin/env python
# -*- coding:utf-8 -*-


import time,hashlib,urllib,json
from lxml import etree

import web

render = web.template.render('templates')

urls =(
    '/weixinapi','WeiXin',
)

class WeiXin(object):
    def GET(self):
        data = web.input()
        signature = data.signature
        timestamp =data.timestamp
        nonce =  data.nonce
        echostr = data.echostr
        token = 'test'
        list = [token,timestamp,nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update,list)
        hashcode =sha1.hexdigest()
        if hashcode == signature:
            return echostr
     
    def POST(self):
        web.header('Content-Type', 'text/xml')
        data_xml = web.data()
        xml = etree.fromstring(data_xml)
        content = xml.find('Content').text
        touser = xml.find('ToUserName').text
        fromuser = xml.find('FromUserName').text
        if type(content).__name__ == 'unicode':
            content = content.encode('utf-8')
        music_Title,music_Desc,music_Url =self.get_music(content)
        return render.music(fromuser,touser,int(time.time()),music_Title,music_Desc,music_Url)
        
    
    def get_music(self,musicname):
        url = 'http://s.music.163.com/search/get/?type=1&s=%s&limit=10'%(urllib.quote(musicname))
        music_lists =urllib.urlopen(url).read()
        music = json.loads(music_lists)[u'result'][u'songs'][0]
        music_Title =music[u'name']
        music_Desc = music[u'album'][u'name']
        music_Url = music[u'audio']
        return music_Title,music_Desc,music_Url

if __name__ == '__main__':
    app = web.application(urls,globals())
    app.run()
    