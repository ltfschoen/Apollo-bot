from flask import Flask, request
import json
import requests
import sys
from wit import Wit
import traceback
import logging
import os
import chat_client as cc
from random import shuffle
import pandas as pd
from random import randint

app = Flask(__name__)

# User dictionary
users = {}

# Access tokens for Wit & Facebook
fb_AT = 'EAACMg4RPphEBADm7rzRZAm6aZAB7zWIWOr8wabXRLa23EYdFQOB8YrWf01tTtbHlToznm1wClzpflGtNOzV2jjwKwooy7XX9QY2AGNWLFURp3T9LVA9dbNDoXBxr5nnoIgYk88ZBZCsAVHmMuQ7Na2inJay7xHxehA4bKemQkwZDZD'
#access_token = "L3WEHB6WLKM567B4BW4XJMQRS43BCZLR"

#client = Wit(access_token=access_token, actions=actions)
#client.logger.setLevel(logging.WARNING)

# Initialisation for Facebook
@app.route('/', methods=['GET'])
def handle_verification():
    print("Handling Verification: ->")
    if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
        print("Verification successful!")
        return request.args.get('hub.challenge', '')
    else:
        print("Verification failed!")
        return 'Error, wrong validation token'

# Reply to user with text message
def reply(user_id, msg):
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": fb_AT},
    data=json.dumps({
      "recipient": {"id": user_id},
      "message": {"text": msg}
    }),
    headers={'Content-type': 'application/json'})
    print(resp.content)

# Reply to user with audio file
def reply_audio(user_id, msg):
    audio = to_voice(msg)
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": fb_AT},
    data=json.dumps({
      "recipient": {"id": user_id},
      "message": {"attachment": {"type": "audio", "payload": {"url": audio}}}
    }),
    headers={'Content-type': 'application/json'})
    print(resp.content)

# Reply to user with an image
def reply_image(user_id, image_name, type):
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": fb_AT},
    data=json.dumps({
      "recipient": {"id": user_id},
      "message": {"attachment": {"type": "image", "payload": {}}}
      #"message": {"attachment": {"type": "image", "payload": {}}},
      #"filedata": (image_name, open(os.getcwd()+'/'image_name), 'image/jpeg')
    }),
    headers={'Content-type': 'application/json'})
    print(resp.content)

# Messages from Facebook
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    print('message: ' + str(data))
    if data['object'] != 'page':
        return "No"
    try:
        for entry in data['entry']:
            # get all the messages
            messages = entry['messaging']
            context = {}
            if messages[0]:
                # Get the first message
                message = messages[0]
                fb_id = message['sender']['id']
                text = message['message']['text']
                # Forward the message to the Wit.ai Bot Engine
                # We handle the response in the function send()
                #context = client.run_actions(session_id=fb_id, message=text, verbose=True)
                client = cc.create_client(send)
                context = client.run_actions(session_id=fb_id, message=text, verbose=True)
                if fb_id not in users:
                    users[fb_id] = True
                    reply_image(fb_id,"1621742.gif", 'image/gif')
    except Exception as e:
        traceback.print_exc()
        e = sys.exc_info()[0]
        print(e)
        print("error at line: " + sys.exc_traceback.tb_lineno)
        return "No"
    return "ok"


if __name__ == '__main__':
  app.run()
