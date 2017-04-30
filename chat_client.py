from random import shuffle
from wit import Wit
import pandas as pd
import requests
from jokes import JOKES
from random import randint
from Visualisation import Data
from decorators import *

# class Data:
#     """ Load DATA """
#
#     def __init__(self, location, time):
#
#         self.DATASET_REMOTE = "https://firms.modaps.eosdis.nasa.gov/active_fire/c6/text/MODIS_C6_{0}_{1}h.csv".format(
#             location, time)
#         self.dataset = self.get_data(None)
#
#     def get_data(self, num_rows):
#         """ Load from remote endpoint """
#         try:
#             def exists(path):
#                 r = requests.head(path)
#                 return r.status_code == requests.codes.ok
#
#             if exists(self.DATASET_REMOTE):
#                 return pd.read_csv(self.DATASET_REMOTE, nrows=num_rows)
#         except Exception as e:
#             print(e.errno)


access_token = "L3WEHB6WLKM567B4BW4XJMQRS43BCZLR"


# all_jokes = {
#     'cat': [
#         'Chuck Norris counted to infinity - twice.',
#         'Death once had a near-Chuck Norris experience.',
#     ],
#     'tech': [
#         'Did you hear about the two antennas that got married? The ceremony was long and boring, but the reception was great!',
#         'Why do geeks mistake Halloween and Christmas? Because Oct 31 === Dec 25.',
#     ],
#     'default': [
#         'Why was the Math book sad? Because it had so many problems.',
#     ],
# }


# def first_entity_value(entities, entity):
#     if entity not in entities:
#         return None
#     val = entities[entity][0]['value']
#     if not val:
#         return None
#     return val['value'] if isinstance(val, dict) else val
#

def send(request, response):
    print(response['text'])


# def merge(request):
#     context = request['context']
#     entities = request['entities']
#
#     if 'joke' in context:
#         del context['joke']
#     category = first_entity_value(entities, 'category')
#     if category:
#         context['cat'] = category
#     sentiment = first_entity_value(entities, 'sentiment')
#     if sentiment:
#         context['ack'] = 'Glad you liked it.' if sentiment == 'positive' else 'Hmm.'
#     elif 'ack' in context:
#         del context['ack']
#     return context


def select_joke(request):
    context = request['context']
    context['joke'] = JOKES[randint(0, 1000) % len(JOKES)]
    return context


@random_joke
@necessary_entities(['location', 'time'])
def get_data(request):
    entities = request['entities']  # client.message(request['text'])['entities']
    # if 'location' not in entities or 'time' not in entities:
    #     context = request['context']
    #     context['ret'] = 'I don\'t understand, please type help for more option'
    #     return context
    location = entities['location'][0]['value']
    time = entities['time'][0]['value']
    context = request['context']
    # ret_str = str(Data(location, time).dataset)
    d = Data(location, time)
    img_name = filename = "image/{0}{1}.png".format(location, time)
    d.graph(filename=img_name)
    # if 'humour_percent' not in context:
    #     context['humour_percent'] = 0
    # if randint() < context['humour_percent']:
    #     ret_str += ' \n ' + all_jokes['cat']
    context['ret'] = img_name
    return context  # str(data.dataset)


@random_joke
@necessary_entities(['percent'])
def set_humour(request):
    entities = client.message(request['text'])['entities']
    # if 'percent' not in entities:
    #     context = request['context']
    #     context['ret'] = 'I don\'t understand, please type help for more option'
    #     return context
    humour_percent = entities['percent'][0]['value']
    context = request['context']
    context['humour_percent'] = float(humour_percent / 100)
    return context


def to_voice(text):
    from subprocess import call
    call(["espeak", "-v", text + ".wav", text])
    return text + ".wav"


actions = {
    'send': send,
    None: select_joke,
    # 'merge': merge,
    'select-joke': select_joke,
    'getdata': get_data,
    'set_humour': set_humour,
}


def create_client(send_function, access_token="L3WEHB6WLKM567B4BW4XJMQRS43BCZLR"):
    actions['send'] = send_function
    return Wit(access_token=access_token, actions=actions)


client = create_client(send)
client.interactive()

# client = Wit(access_token=access_token, actions=actions)
# #t = client.run_actions("16627312704215","hi")
# client.interactive()
