import os
import dotenv # https://github.com/mattseymour/python-env
from flask import Flask, request
import json
import requests
import sys
import traceback
import logging
import chat_client as cc
import tokens

# Create instance of Flask class using single module
app = Flask(__name__)

# Load .env credentials
APP_ROOT = os.path.join(os.path.dirname(__file__), '')
dotenv_path = os.path.join(APP_ROOT, '.env')
dotenv.load(dotenv_path)

# Facebook Messenger GET Webhook
@app.route('/', methods=['GET'])
def handle_verification():
    """
    Handles matching Verify Token from Facebook Messenger.
    Responds to Facebook Messenger with hub.challenge value to confirm match.
    """
    print("Called handle_verification in apollobot.py with request: %r" % (json.dumps(request.json, indent=4, sort_keys=True)))
    sys.stdout.flush() # Capture in logs
    print("FB_VERIFY_TOKEN is: %r" % (tokens.FB_VERIFY_TOKEN))
    request_hub_verify_token = request.args.get('hub.verify_token', '')
    request_hub_challenge = request.args.get('hub.challenge', '')
    if request_hub_verify_token == tokens.FB_VERIFY_TOKEN:
        print("Verification of Facebook Messenger Verify Token successful. Responding with hub.challenge to confirm.")
        return request_hub_challenge
    else:
        print("Verification failed. Wrong validation token")
        return 'Error, wrong validation token'

# Facebook Messenger POST Webhook
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    """
    Handles messages from Facebook Messenger
    """
    print("Called handle_incoming_messages in apollobot.py")
    response_data = request.json
    print('Received message: %r' % (json.dumps(response_data, indent=4, sort_keys=True)))
    if response_data['object'] != 'page':
        print("Received message's object key does not have value 'page'. Instead it is %r: " % (response_data['object']))

        # TODO - why return No??
        return "No"
    try:
        for entry in response_data['entry']:
            # Get all the received messages
            messages = entry['messaging']
            context = {}
            if messages[0]:

                # Get the first received message
                message = messages[0]
                fb_id = message['sender']['id']
                # Check if 'message' key exists
                if 'message' in message:
                    text = message['message']['text']

                    # Call function to reply to the user with specific image
                    if text == 'show me my image':
                        reply_image(fb_id,'global24','image/jpg')
                        break

                    # Generate Wit Client. Passing 'send' function as argument (handles response).
                    client = cc.create_client(send)
                    # Forward received message to the Wit.ai Bot Engine
                    context = client.run_actions(session_id=fb_id, message=text, verbose=True)
    except Exception as e:
        traceback.print_exc()
        e = sys.exc_info()[0]
        print(e)
        print("Error handling incoming message at line: " + str(sys.exc_traceback.tb_lineno))
        return "No"
    return "ok"

# Reply to user with text message
def reply(user_id, msg):
    print("Called reply in apollobot.py with user_id: %r, msg: %r" % (user_id, msg))
    print("user_id: " + str(user_id))
    print("msg: " + str(msg))
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages",
                         params={"access_token": tokens.FB_PAGE_TOKEN},
                         data=json.dumps({
                             "recipient": {"id": user_id},
                             "message": {"text": msg}
                         }),
                         headers={'Content-type': 'application/json'})
    print(resp.content)

# Reply to user with audio file
def reply_audio(user_id, msg):
    print("Called reply_audio in apollobot.py with user_id: %r, msg: %r" % (user_id, msg))

    def to_voice(text):
        from subprocess import call
        call(["espeak", "-v", text + ".wav", text])
        return text + ".wav"

    audio = to_voice(msg)
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages",
                         params={"access_token": tokens.FB_PAGE_TOKEN},
                         data=json.dumps({
                             "recipient": {"id": user_id},
                             "message": {"attachment": {"type": "audio", "payload": {"url": audio}}}
                         }),
                         headers={'Content-type': 'application/json'})
    print(resp.content)

# Reply to user with an image
def reply_image(user_id, image_name, type):
    print("Called reply_image in apollobot.py with user_id: %r, image_name: %r, type: %r" % (user_id, image_name, type))
    #with open(image_name, 'rb') as f:
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages",
                         params={"access_token": tokens.FB_PAGE_TOKEN},
                         data=json.dumps({
                             "recipient": {"id": user_id},
                             "message": {"attachment": {"type": "image", "payload": {"url": "https://raw.githubusercontent.com/ltfschoen/Apollo-bot/master/image/global24.png"}}}
                             # "filedata": {'filedata': open(image_name, 'rb')}
                         }),
                         headers={'Content-type': 'application/json'})

def send(request, response):
    """
    Sender function
    """
    # We use the fb_id as equal to session_id
    print("Called send action in apollobot.py with response: %r" % (response))
    print(response['text'])
    reply(request['session_id'], response['text'])

if __name__ == '__main__':

    print("Called main in apollobot.py and running Flask server")

    # Run Flask server
    app.run(host='127.0.0.1', port=5000, debug=True)
