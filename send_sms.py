from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
import check_if_enough_money

import json    # or `import simplejson as json` if on Python < 2.6
import http.client
import random


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
    "are you sure":"YES",
    "yes":"No.",
    "what's the weather like":"Idk have you looked outside?"
}

joke = ["What did Mississippi let Delaware? I don’t know, but Alaska!", 
        "My wife is so negative. I remembered the car seat, the stroller, AND the diaper bag. Yet all she can talk about is how I forgot the baby.",
        "Our wedding was so beautiful … Even the cake was in tiers.",
        "I wouldn’t buy anything with velcro. It’s a total rip-off.",
        "The shovel was a ground-breaking invention."]

daily = ["Make some bread", "Get some money"]


def get_price(r_string):
    string= r_string.strip(" ")
    string  = ("%").join(string.split(" "))
    conn = http.client.HTTPSConnection("axesso-axesso-amazon-data-service-v1.p.rapidapi.com")

    headers = {
        'x-rapidapi-host': "axesso-axesso-amazon-data-service-v1.p.rapidapi.com",
        'x-rapidapi-key': "4vB59oWlqGmsh8ojOArDODrvo9fKp1hGN3ojsnJeIOXsP621LQ"
    }

    conn.request("GET", "/amz/amazon-search-by-keyword?keyword="+string+"&domainCode=com&sortBy=date-desc-rank&page=1", headers=headers)

    res = conn.getresponse()
    data = res.read()
    print(string)
    string2 = data.decode("utf-8")
    json_string = string2
    print(string2)
    obj = json.loads(json_string)   
    for x in obj['foundProductDetails']:
        if x['responseStatus'] =="PRODUCT_FOUND_RESPONSE":
            if x["price"]>0.0:
                return (x["price"], x["productTitle"])
        return (0.0, "n/a")
        
need_money_img = ['https://media.giphy.com/media/h8yeWWvhwVdsI/giphy.gif', 'https://media.giphy.com/media/UufYcEW1dYfNo9pMyj/giphy.gif', 'https://media.giphy.com/media/3o6Mb9oeV59vc1XeEw/giphy.gif']
broke = ['https://media.giphy.com/media/1ppudqsvJAWPa63iLU/giphy.gif', 'https://media.giphy.com/media/123XfyrlS6mpEY/giphy.gif','https://media.giphy.com/media/3orifdO6eKr9YBdOBq/giphy.gif']
spend = ['https://media.giphy.com/media/d3mmdNnW5hkoUxTG/giphy.gif', 'https://media.giphy.com/media/sITUXkRIDG14A/giphy.gif', 'https://media.giphy.com/media/l3V0B6ICVWbg8Xi5q/giphy.gif']
rich = ['https://media.giphy.com/media/h0MTqLyvgG0Ss/giphy.gif', 'https://media.giphy.com/media/HChtj3gzcVsXK/giphy.gif', 'https://media.giphy.com/media/SsTcO55LJDBsI/giphy.gif']
hello = ['https://media.giphy.com/media/dzaUX7CAG0Ihi/giphy.gif', 'https://media.giphy.com/media/Cmr1OMJ2FN0B2/giphy.gif', 'https://media.giphy.com/media/6yU7IF9L3950A/giphy.gif']

@app.route('/sms', methods=['POST'])
def sms():
    global status
    message_body = request.form['Body']
    message = str(message_body)
    message = message.lower().strip(" ")
    resp = MessagingResponse()
    find_str = "find the price of"
    length = len(message)
    if message.startswith(find_str):
        tup = get_price(message.split("price of")[1])
        if tup[1] == "n/a":
            resp.message("Couldn't find the product.")
        else:
            resp.message("The price of " + tup[1] + " is $" + str(tup[0]))
    elif message.startswith("can i afford"):
        tup = get_price(message.split("afford")[1])
        if tup[1] == "n/a":
            temp = resp.message("Couldn't find the product.")
        else:
            string = "The price of " + tup[1] + " is $" + str(tup[0]) + "\n"
            temp2 = check_if_enough_money.info()
            bal = temp2.check_balance()
            if(tup[0] >= bal/2):
                string = string + "No, You Broke"
                temp = resp.message(string)
                temp.media(broke[random.randint(0,2)])
            else:
                string = string + "Sure Thing, You Rich"
                temp = resp.message(string)
                temp.media(spend[random.randint(0,2)])
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
            temp2 = resp.message("Balance: $" + str(temp.check_balance()))
            if (temp.check_balance()>20000):
                temp2.media(rich[random.randint(0,2)])
            else:
                temp2.media(need_money_img[random.randint(0,2)])

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
    elif message == "tell me a joke":
        temp3 = joke[random.randint(0,4)]
        resp.message(temp3)
    elif message == "what should i do today":
        temp4 = daily[random.randint(0,1)]
        resp.message(temp4)
    elif message not in responses:
        resp.message("I don't understand. Please try 'Find my bank account' or 'Good to see you' or 'Find the price of x'")
    else:
        temp = resp.message(responses[message])
        rand = random.randint(0,2)
        temp.media(hello[rand])

    return str(resp)

if __name__ == '__main__':
    app.run()