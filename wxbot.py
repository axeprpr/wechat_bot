#!/usr/bin/python
# -*- coding:UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from wxpy import *
from redmine import redmine_handle
from tuling import dva
from wechat_sender import listen

bot = Bot(console_qr=2)

redmine = ['录单','查单','录工时','查工时']

help = { 'vpn' : 'https://docs.qq.com/doc/DTkxFSExVU1dUbnpB',
         'version': '当前最新版本: http://192.222.1.150:8082/fileserver/jenkins/%E5%8F%91%E5%B8%83%E7%89%88%E6%9C%AC.html',
}

@bot.register()
def text_reply(msg):
    print msg
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
    print message_dict
    if message_dict[0] in help.keys():
        return help.get(message_dict[0])       
    elif message_dict[0] in redmine:      
        return redmine_handle(message_dict)
    else:
        return dva(' '.join(message_dict))

@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    new_friend = msg.card.accept()
    new_friend.send('Atx自动接受了你的好友请求')

#@bot.register()
#def other_msg(msg):
#    print msg

#embed()
listen(bot)
