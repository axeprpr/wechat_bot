#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from redmine import redmine_handle


NPL_TEXT = {
    "help" : "balabla",
    "vpn" : "xxx",
    "version": "xxx",
    "manual" : "xxx"
}

NLP_FUNC = [
    {'func_name': "redmine",
     'func_keys': ["查单","录单","查工时","录工时"]
    }
]

def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]

def nlp_text(msg):
    try:
        return NPL_TEXT.get(msg)
    except:
        return None

def nlp_func(keyword, msg=[]):
    if not msg:
        try:
            return [ i.get("func_name") for i in NLP_FUNC if keyword in i.get("func_keys") ][0]
        except:
            return None
    else:
        return eval(keyword)(msg)

def hook(bot, func, to, msg):
    eval(func)(bot, to, msg)

## nlp_funcs registered
def redmine(msg):
    return redmine_handle(msg)

## hook_funcs
def gitlab(bot, to, msg):
    res = '[Repository:'
    res += msg.get('repository',{}).get('name')+']'
    res += ' just happened to submit as follows:'
    commit = msg.get('commits')[0]
    res += '\nmessage:'+commit.get('message')
    res += 'url:'+commit.get('url')
    res += '\nauthor:'
    res += commit.get('author',{}).get('name')
    f = bot.friends().search(to)[0]
    f.send(res)