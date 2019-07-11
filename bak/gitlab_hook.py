#!/usr/bin/python
from flask import Flask
from flask import request
import os
import sys
from wechat_sender import Sender

app = Flask(__name__)

@app.route("/github", methods=["GET", "POST"])
def msg_from_gitlab():
    c = request.get_json()
    msg = 'Repository '
    msg = c.get('repository',{}).get('name')
    msg += ' just happened to submit as follows: '
    commit = c.get('commits')[0]
    msg += commit.get('message')
    msg += ' author '
    msg += commit.get('author',{}).get('name')
    print msg
    sender = Sender(token='test')
    sender.send(msg)
    return "..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
