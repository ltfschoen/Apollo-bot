from random import shuffle
from wit import Wit
from jokes import JOKES
from random import randint
from Visualisation import Data
from decorators import *
import json
import tokens

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
    print("Called send action in chat_client.py with response: %r" % (response))
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
    print("Called select_joke action with: %r" % (request))
    context = request['context']
    context['joke'] = JOKES[randint(0, 1000) % len(JOKES)]
    print("Within select_joke returning context with joke: %r" % (context['joke']))
    return context


@random_joke
@necessary_entities(['location', 'time'])
def get_data(request):
    print("Called get_data action with: %r" % (request))
    entities = request['entities']  # client.message(request['text'])['entities']
    # if 'location' not in entities or 'time' not in entities:
    #     context = request['context']
    #     context['ret'] = 'I don\'t understand, please type help for more option'
    #     return context
    location = entities['location'][0]['value']
    time = entities['time'][0]['value']
    context = request['context']
    # ret_str = str(Data(location, time).dataset)
    #d = Data(location.replace(' ', '_'), time)
    img_name = filename = "image/{0}{1}.png".format(location, time)
    #d.graph(filename=img_name)
    # if 'humour_percent' not in context:
    #     context['humour_percent'] = 0
    # if randint() < context['humour_percent']:
    #     ret_str += ' \n ' + all_jokes['cat']
    context['ret'] = img_name
    print("Within get_data returning context with img_name: %r" % (context['ret']))
    return context  # str(data.dataset)


@random_joke
@necessary_entities(['percent'])
def set_humour(request):
    print("Called set_humour action with: %r" % (request))
    entities = client.message(request['text'])['entities']
    print("Within set_humour with client.message(): %r" % (client.message()))
    # if 'percent' not in entities:
    #     context = request['context']
    #     context['ret'] = 'I don\'t understand, please type help for more option'
    #     return context
    humour_percent = entities['percent'][0]['value']
    context = request['context']
    context['humour_percent'] = float(humour_percent) / 100.0
    rint("Within set_humour returning context with humour_percent: %r" % (context['humour_percent']))
    return context

def clean(request):
    return {}

actions = {
    'send': send,
    # 'merge': merge,
    'select_joke': select_joke,
    'getdata': get_data,
    'set_humour': set_humour,
    'clean': clean
    #None: select_joke,
}

# Setup Wit Client
client = Wit(access_token=tokens.WIT_APP_TOKEN, actions=actions)
client.interactive()

def create_client(send_function, access_token=tokens.WIT_APP_TOKEN):
    """
    Generates Wit Client. Called from apollobot.py
    """
    print("Generated Wit Client with 'send' function provided: %r" % (send_function))
    actions['send'] = send_function
    return Wit(access_token=access_token, actions=actions)

client = create_client(send)
print("Generated Interactive Wit Client with 'send' function provided: %r" % (send))

# client = Wit(access_token=tokens.WIT_APP_TOKEN, actions=actions)
# #t = client.run_actions("16627312704215","hi")
# client.interactive()
