#!/usr/bin/python
# -*- coding:UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from wxpy import *
from redmine import redmine_handle

bot = Bot(console_qr=2)

redmine = ['录单','查单','录工时','查工时']


@bot.register()
def text_reply(msg):
    if isinstance(msg.chat, Group) and not msg.is_at:
        return
    else:      
        if [ rd for rd in redmine if rd in msg.text ]:
            return redmine_handle(msg.text)
embed()

