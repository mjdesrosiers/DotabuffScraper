import os
import urllib2
import urllib
from flask import Flask, request
import dotabuff
import pprint

app = Flask(__name__)
#
# https://api.groupme.com/v3/bots/post


def send_message(msg):
    print "Sending " + msg
    url = 'https://api.groupme.com/v3/bots/post'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    header = { 'User-Agent' : user_agent }
    values = {
      'bot_id' : '535cbd947cf38b46a83fa3084f',
      'text' : msg,
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, header)
    response = urllib2.urlopen(req)
    return response


def last_game():
    matches = dotabuff.get_new_matches()
    if matches:
        out = ""
        for match in matches:
            matchstr = pprint.pformat(dotabuff.get_match_results(match))
            out += matchstr
        send_message(out)
    return


def current_online():
    return send_message("No one is online!")

options = {"#last" : last_game,
           "#now" : current_online,
}


@app.route('/message/', methods=['POST'])
def message():
    new_message = request.get_json(force=True)
    sender = new_message["name"]
    body = new_message["text"]
    if body.startswith("#"):
        options[body]()

    return


@app.route("/")
def hello():
    return "Hello world!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)