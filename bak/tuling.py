#!/usr/bin/python
# -*- coding:UTF-8 -*-
import urllib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
 
KEY = '92a26cf09750421aa759230493b65b19'

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def dva(msg):
    
    key = KEY
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
    request = api + msg.encode('utf-8')
    response = getHtml(request)
    dic_json = json.loads(response)
    return dic_json['text']
