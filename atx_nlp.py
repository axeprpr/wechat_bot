#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

NPL_TEXT = {
    "help" : "balabla",
    "vpn" : "xxx",
    "version": "xxx".
    "manual" : "xxx"
}

NLP_FUNC = [
    {'func_name': "redmine",
     'func_keys': ["查单","录单","查工时","录工时"]}
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
            return [ i.func_name for i in NLP_FUNC if keyword in i.func_keys ]
        except:
            return None
    else:
        return eval(keyward)(msg)