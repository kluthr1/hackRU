from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
import check_if_enough_money

app = Flask(__name__)

status = -1

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
    message_body = request.form['Body']
    message = str(message_body)
    message = message.lower()
    resp = MessagingResponse()
    if message == "find my bank account" and status == -1:
        resp.message("What is your first name?")
        status += 1
    elif status == 0:
        check_if_enough_money.first_name = message
        resp.message("What is your last name?")
        status += 1
    elif status == 1:
        check_if_enough_money.last_name = message
        resp.message("What your zip code?")
        status += 1
    elif status == 2:
        check_if_enough_money.zip_code = message
        temp = check_if_enough_money.info()
        if temp.check_for_customer() == 1:
            temp.get_accounts_list()
            resp.message("Found you! Choose the account you would like to access:\n" + check_if_enough_money.account_nickname_list)
            status += 1
        else:
            resp.message("Could not find you.")
            status = -1
    elif status == 3:
        check_if_enough_money.account_nickname = message
        if check_if_enough_money.find_account() == 1:
            resp.message("Accessing the account...\nWhat do you want to do with it?")
            status += 1
        else:
            resp.message("I couldn't find the account, run it by me again.")
    elif status == 4:
        if message == "check my balance" or message == "what's my balance" or message == "balance":
            x=0
    elif message not in responses:
        resp.message("I don't understand. Please try 'Find my bank account' or 'Good to see you'")
    else:
        resp.message(responses[message])

    return str(resp)

if __name__ == '__main__':
    app.run()