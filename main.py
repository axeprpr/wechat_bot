#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask, render_template, request
from wxpy import *

import atx_nlp
from tuling import tuling

import logging
LOG_FILENAME="frog.log"
logging.basicConfig(filename=LOG_FILENAME,level=logging.WARNING)

app = Flask(__name__)
bot = Bot(console_qr=True)

def monitor(msg_to, msg_type, msg):
    if msg_to=="" or msg=="":
        return "Invalid request..."
    msg_type_dict = {'info' : '[INFO]',
                    'warning': '[WARNING]',
                    'error': '[ERROR!]'}
    logging.warning("wechat msg to:{} type:{} content:{}".format(msg_to, msg_type, msg))
    f = bot.friends().search(msg_to)[0]
    f.send(msg_type_dict[msg_type] + msg)
    return "OK"

# weixin auto reply
@bot.register()
def text_reply(msg):
    if isinstance(msg.chat, Group) and not msg.is_at:
        return
    message = msg.text.lower()
    message_dict = message.split()
    try:
        for i in message_dict:
            if '@' in i:
                message_dict.remove(i)
    except:
        return "Invalid input..."
    if atx_nlp.nlp_text(message_dict[0]):
        return atx_nlp.nlp_text(message_dict[0])
    elif atx_nlp.nlp_func(message_dict[0]):      
        return atx_nlp.nlp_func(atx_nlp.nlp_func(message_dict[0]), message_dict)
    else:
        return tuling(' '.join(message_dict))

# weixin auto add friend
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    new_friend = msg.card.accept()
    new_friend.send('Hi.This is Frog.')

## api part
@app.route("/gitlab/", methods=["GET", "POST"])
def msg_from_gitlab():
    c = request.get_json()
    return atx_nlp.hook(bot, 'gitlab', 'Axe', c)

## monitor is a reserved and decoupled api. forward message to somebody without handle.
@app.route('/monitor', methods=['GET','POST'])
def msg():
    if request.method == "GET":
        result = monitor(request.args.get("to",""), 
                              request.args.get("type","info"), 
                              request.args.get("msg",""))
    elif request.method == "POST":
        result = monitor(request.form.get("to",""), 
                              request.form.get("type","info"),
                              request.form.get("msg",""))
    else:
        return "Invalid request..."
    return result

if __name__ == '__main__':
    app.run(debug=False, port=666, host="0.0.0.0")