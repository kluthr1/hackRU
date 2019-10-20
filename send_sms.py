from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse

app = Flask(__name__)

status = -1
first_name = ""
last_name = ""
zip_code = ""

responses = {
    "hi":"Hi!",
    "hello":"Hello!",
    "hey":"Hey!",
    "howdy":"Howdy!",
    "sup":"Sup!",
    "wassup":"Whazzup!",
    "yo":"Yo!",
    "good morning":"Good Morning!",
    "good afternoon":"Good Afternoon!",
    "good evening":"Good Evening!",
    "how do you do":"NO, how do YOU do?",
    "nice to meet you":"Nice to meet you!",
    "pleased to meet you":"Pleased to meet you!",
    "how have you been":"Trash, HBU?",
    "how are you doing":"Aight",
    "how's it going":"Slowly",
    "nice to see you":"I wish I could see you...",
    "it's great to see you":"I'd be great if I could see you!",
    "good to see you":"Do you have a mirror? I want to see what's so good.",
    "long time no see":"Have I seen you before?",
    "it's been a while":"Yes, it has.",
    "whazzup":"Wassup!",
    "are you sure":"YES"
}

@app.route('/')
def pinfo():
    return "hellow worlds"

@app.route('/sms', methods=['POST'])
def sms():
    global status
    global first_name
    global last_name
    global zip_code
    number = request.form['From']
    message_body = request.form['Body']
    message = str(message_body)
    message = message.lower()
    resp = MessagingResponse()
    if message == "find my bank account" and status == -1:
        resp.message("What is your first name?")
        status += 1
    elif status == 0:
        first_name = message
        resp.message("What is your last name?")
        status += 1
    elif status == 1:
        last_name = message
        resp.message("What your zip code?")
        status += 1
    elif status == 2:
        zip_code = message
        status = -1
    elif message not in responses:
        resp.message("I don't understand. Please try 'Find my bank account' or 'Good to see you'")
    else:
        resp.message(responses[message])

    return str(resp)

if __name__ == '__main__':
    app.run()