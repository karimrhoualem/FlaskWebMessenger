import os

from dotenv import load_dotenv
from twilio.rest import Client
from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    request,
    url_for
)

load_dotenv()
app = Flask(__name__)
app.secret_key = "It's a secret..."

TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def get_sent_messages():
    messages = client.messages.list(from_=TWILIO_PHONE_NUMBER)
    return messages

def send_message(to, body):
    client.messages.create(
        to=to,
        body=body,
        from_=TWILIO_PHONE_NUMBER
    )

@app.route("/", methods=["GET"])
def index():
    messages = get_sent_messages()
    return render_template("index.html", messages=messages)

@app.route("/add-message", methods=["POST"])
def add_message():
    sender = request.values.get('sender', 'Someone')
    receiver = request.values.get('receiver', 'Someone')
    message = request.values.get('message', 'Hello!')
    to = request.values.get('to')
    body = f'{sender} says: {message}.'
    send_message(to, body)
    flash('Your message was successfully sent.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
