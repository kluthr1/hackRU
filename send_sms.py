from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
import check_if_enough_money

import json    # or `import simplejson as json` if on Python < 2.6
import http.client


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
    "yes":"No."
}

def get_price(string):

    conn = http.client.HTTPSConnection("axesso-axesso-amazon-data-service-v1.p.rapidapi.com")

    headers = {
        'x-rapidapi-host': "axesso-axesso-amazon-data-service-v1.p.rapidapi.com",
        'x-rapidapi-key': "4vB59oWlqGmsh8ojOArDODrvo9fKp1hGN3ojsnJeIOXsP621LQ"
    }

    conn.request("GET", "/amz/amazon-search-by-keyword?keyword="+string+"&domainCode=com&sortBy=date-desc-rank&page=1", headers=headers)

    res = conn.getresponse()
    data = res.read()

    string = data.decode("utf-8")
    json_string = string
    obj = json.loads(json_string)   
    for x in obj['foundProductDetails']:
        if x['responseStatus'] =="PRODUCT_FOUND_RESPONSE":
            if x["price"]>0.0:
                return (x["price"], x["productTitle"])
        return (0.0, "n/a")


def get_price(string):

    conn = http.client.HTTPSConnection("axesso-axesso-amazon-data-service-v1.p.rapidapi.com")

    headers = {
        'x-rapidapi-host': "axesso-axesso-amazon-data-service-v1.p.rapidapi.com",
        'x-rapidapi-key': "4vB59oWlqGmsh8ojOArDODrvo9fKp1hGN3ojsnJeIOXsP621LQ"
    }

    conn.request("GET", "/amz/amazon-search-by-keyword?keyword="+string+"&domainCode=com&sortBy=date-desc-rank&page=1", headers=headers)

    res = conn.getresponse()
    data = res.read()

    string = data.decode("utf-8")
    json_string = string
    obj = json.loads(json_string)   
    for x in obj['foundProductDetails']:
        if x['responseStatus'] =="PRODUCT_FOUND_RESPONSE":
            if x["price"]>0.0:
                return (x["price"], x["productTitle"])
        return (0.0, "n/a")
        

@app.route('/sms', methods=['POST'])
def sms():
    global status
    message_body = request.form['Body']
    message = str(message_body)
    message = message.lower()
    resp = MessagingResponse()
    find_str = "find the price of"
    length = length(message)
    if message[0,16] == find_str:
        tup = get_price(message[17,length-1])
        if tup[1] == "n/a":
            resp.message("Couldn't find the product.")
        else
            resp.message("The price of " + tup[1] + " is $" + tup[0])
    elif message == "find my bank account" or message == "find my account" or message == "find my bank account" and status == -1:
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
        temp = check_if_enough_money.info()
        the_account = temp.find_account()
        if the_account == 1:
            temp.set_up_account_endpoints()
            resp.message("Accessing the account...\nWhat do you want to do with it?")
            status += 1
        else:
            resp.message("I couldn't find the account, run it by me again.")
    elif status == 4:
        temp = check_if_enough_money.info()
        if message == "check my balance" or message == "what's my balance" or message == "balance":
            resp.message("Balance: $" + str(temp.check_balance()))
        elif message == "check my rewards" or message == "rewards":
            resp.message("Rewards balance: $" + str(temp.check_rewards()))
        elif message == "check my bills" or message == "bills":
            bills_string = temp.check_bills()
            print(bills_string)
            constructed_string = ""
            for x in bills_string:
                print(x)
                constructed_string = constructed_string + x
            resp.message("Here are your bills: \n" + constructed_string)
        elif message == "done":
            resp.message("Cool, still wanna chat?")
            status = -1
        else:
            resp.message("Sorry, I do not understand. Try 'done' or 'check my balance'")
    elif message not in responses:
        resp.message("I don't understand. Please try 'Find my bank account' or 'Good to see you' or 'Find the price of x'")
    else:
        resp.message(responses[message])
    return str(resp)

if __name__ == '__main__':
    app.run()