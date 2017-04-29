from flask import Flask, request
import json
import requests
import sys
from wit import Wit
import traceback
import logging

app = Flask(__name__)

# User dictionary
users = {}

# Access tokens for Wit & Facebook
fb_AT = 'EAACMg4RPphEBADm7rzRZAm6aZAB7zWIWOr8wabXRLa23EYdFQOB8YrWf01tTtbHlToznm1wClzpflGtNOzV2jjwKwooy7XX9QY2AGNWLFURp3T9LVA9dbNDoXBxr5nnoIgYk88ZBZCsAVHmMuQ7Na2inJay7xHxehA4bKemQkwZDZD'
access_token = "L3WEHB6WLKM567B4BW4XJMQRS43BCZLR"

# Wit methods

from random import shuffle
import pandas as pd
from random import randint


class Data:
   """ Load DATA """

   def __init__(self, location, time):

       self.DATASET_REMOTE = "https://firms.modaps.eosdis.nasa.gov/active_fire/c6/text/MODIS_C6_{0}_{1}h.csv".format(
           location, time)
       self.dataset = self.get_data(None)

   def get_data(self, num_rows):
       """ Load from remote endpoint """
       try:
           def exists(path):
               r = requests.head(path)
               return r.status_code == requests.codes.ok

           if exists(self.DATASET_REMOTE):
               return pd.read_csv(self.DATASET_REMOTE, nrows=num_rows)
       except Exception as e:
           print(e.errno)


all_jokes = {
   'cat': [
       'Chuck Norris counted to infinity - twice.',
       'Death once had a near-Chuck Norris experience.',
   ],
   'tech': [
       'Did you hear about the two antennas that got married? The ceremony was long and boring, but the reception was great!',
       'Why do geeks mistake Halloween and Christmas? Because Oct 31 === Dec 25.',
   ],
   'default': [
       'Why was the Math book sad? Because it had so many problems.',
   ],
}


def first_entity_value(entities, entity):
   if entity not in entities:
       return None
   val = entities[entity][0]['value']
   if not val:
       return None
   return val['value'] if isinstance(val, dict) else val


def send(request, response):
   print(response['text'])
   reply(request['session_id'], response['text'])


def merge(request):
   context = request['context']
   entities = request['entities']

   if 'joke' in context:
       del context['joke']
   category = first_entity_value(entities, 'category')
   if category:
       context['cat'] = category
   sentiment = first_entity_value(entities, 'sentiment')
   if sentiment:
       context['ack'] = 'Glad you liked it.' if sentiment == 'positive' else 'Hmm.'
   elif 'ack' in context:
       del context['ack']
   return context


def select_joke(request):
   context = request['context']

   # jokes = all_jokes[context['cat'] or 'default']
   # shuffle(jokes)
   context['joke'] = all_jokes['cat']
   return context


def get_data(request):
   entities = client.message(request['text'])['entities']
   if 'location' not in entities or 'time' not in entities:
       context = request['context']
       context['ret'] = 'I don\'t understand, please type help for more option'
       return context
   location = entities['location'][0]['value']
   time = entities['time'][0]['value']
   context = request['context']
   ret_str = str(Data(location, time).dataset)
   if 'humour_percent' not in context:
       context['humour_percent'] = 0
   if randint() < context['humour_percent']:
       ret_str += ' \n ' + all_jokes['cat']
   context['ret'] = ret_str
   return context  # str(data.dataset)

def set_humour(request):
   entities = client.message(request['text'])['entities']
   if 'percent' not in entities:
       context = request['context']
       context['ret'] = 'I don\'t understand, please type help for more option'
       return context
   humour_percent = entities['percent'][0]['value']
   context = request['context']
   context['humour_percent'] = float(humour_percent)
   return context


def to_voice(text):
   from subprocess import call
   call(["espeak", "-v", text + ".wav", text])
   return text + ".wav"

actions = {
   'send': send,
   'merge': merge,
   'select-joke': select_joke,
   'getdata': get_data,
   'set_humour': set_humour,
}


client = Wit(access_token=access_token, actions=actions)
client.logger.setLevel(logging.WARNING)

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
                context = client.run_actions(session_id=fb_id, message=text, verbose=True)
    except Exception as e:
        traceback.print_exc()
        e = sys.exc_info()[0]
        print(e)
        print("error at line: " + sys.exc_traceback.tb_lineno)
        return "No"
    return "ok"


if __name__ == '__main__':
  app.run()
