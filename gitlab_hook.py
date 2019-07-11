#!/usr/bin/python
# -*- coding:UTF-8 -*-
from flask import Flask
from flask import request
import os
import sys
from wxpy import *
from wechat_sender import Sender
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route("/gitlab/", methods=["GET", "POST"])
def msg_from_gitlab():
    c = request.get_json()
    print c
    msg = '[Repository:'
    msg += c.get('repository',{}).get('name')+']'
    msg += ' just happened to submit as follows:'
    commit = c.get('commits')[0]
    msg += '\nmessage:'+commit.get('message')
    msg += 'url:'+commit.get('url')
    msg += '\nauthor:'
    msg += commit.get('author',{}).get('name')
    print msg
    sender = Sender()
    sender.send_to(msg,'Axe')
    return "..."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
