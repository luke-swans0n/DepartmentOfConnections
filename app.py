from twilio import twiml
from flask import (
    flash,
    render_template,
    redirect,
    request,
    session,
    url_for,
    g
)
from twilio.twiml.voice_response import VoiceResponse, Client, Parameter
import flask
from twilio.rest import Client
import json
from flask import Flask
import os
from flask import Flask
from flaskext.mysql import MySQL
import pandas as pd
import numpy as np
app = Flask(__name__)
app.secret_key = os.urandom(24)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'deptofconnection'
app.config['MYSQL_DATABASE_PASSWORD'] = 'C10H15n!!'
app.config['MYSQL_DATABASE_DB'] = 'cookcounty'
app.config['MYSQL_DATABASE_HOST'] = 'deptofconnections.mysql.pythonanywhere-services.com'
mysql.init_app(app)

@app.route('/', methods=['POST', "GET"])
def home():
    return render_template("./home.html")

@app.route('/intake', methods=['POST'])
def intake():
    response = VoiceResponse()
    response.play("", digits='wwwwwwwwwwwwwwwwwwwwwwwwww0w0')
    response.play("", digits='wwwwwwwwwwwwwwwwwwwwwwwwwwwwww0')
    with response.gather(
            numDigits=10, action=url_for('get_name'), method="POST"
    ) as g:
        g.say("Please enter a 10-digit phone number to send a message to.",
              voice="alice", language="en-GB", loop=4)
    return str(response)
@app.route('/send_sms', methods=['POST'])
def send_sms():
    phone_number = session['phone_number']
    name = request.form['SpeechResult']
    session['username'] = name
    response = VoiceResponse()
    with response.gather(input='speech', action='sent_sms', profanity_filter=False) as g:
        g.say(
            f"Please say the message you'd like to send. This will be recorded, transcribed, then sent via text messsage to {phone_number}. Please speak clearly and at an even pace.",
            voice='alice', language='en-GB')
    return str(response)


@app.route('/get_name', methods=['POST'])
def get_name():
    phone_number = request.form['Digits']
    session['phone_number'] = phone_number
    response = VoiceResponse()
    with response.gather(input='speech', action='send_sms', profanity_filter=False) as g:
        g.say(
            "Please state your name.",
            voice='alice', language='en-GB')
    return str(response)


@app.route('/sent_sms', methods=['POST'])
def sent_sms():
    account='AC99f284918b8ee54f80f5b6f67fbd1bed'
    auth_token = '1a2f3512ce6f0f69d8cc75a0a3fd5a77'
    phone_number = session['phone_number']
    username = session['username']
    message = request.form['SpeechResult']


    client = Client(account, auth_token)

    client.messages.create(
        messaging_service_sid='MGde22decc327802a222043e6fd3b6a1ca',
        body=message,
        to=f'+1{phone_number}')
    client.messages.create(
        messaging_service_sid='MGde22decc327802a222043e6fd3b6a1ca',
        body=1,
        to=f'+1{phone_number}')
    response = VoiceResponse()
    response.say("Message Sent.")
    return str(response)




def _db_phone_check(phone_number):
    curr = mysql.connection.cursor()
    results = curr.execute(f"SELECT number FROM recipients WHERE phone_number={phone_number}")

def _send_preamble(client, username, phone_number):
    preamble = f'Hello this is The Department of Connections, a messaging service for people stuck in the Cook County Department of Corrections. We have received the following message for you from {username}: '
    client.messages.create(
        messaging_service_sid='MGde22decc327802a222043e6fd3b6a1ca',
        body=preamble,
        to=f'+1{phone_number}')
def _send_free_postmessage():
    postmessage = """To keep this service running, we ask that you donate $1 via CashApp to $polynomial (Luke Swanson). We are not officially affiliated with Cook County, the Department of Corrections, or any other governmental entity."""

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
