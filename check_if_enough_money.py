# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

# Need to get the following information from chatbot:
# Name, which type they want, and the price of what they want to buy. Maybe to distinguish same names, include prompter for address
# I need to loop through the list of customers and match the name.
status = -1
first_name = ''
last_name = ''
zip_code = ''
price = 100000
apiKey = '418663bb03b9bac82cf01afffca9bc26'
url = 'http://api.reimaginebanking.com'
customer_id = ''
account_nickname = ''
account_id = ''
exists = 0
account_list = ''

# GET request for getting the list of all customers and stores JSON response
get_customers = requests.get(url + "/customers?key=" + apiKey)
customer_list = get_customers.json()

def check_for_customer():
    global customer_id
    # Searches for customer based on name and zipcode
    for x in customer_list:
        if x['last_name'].lower() == last_name.lower():
            if x['first_name'].lower() == first_name.lower():
                if x['address']['zip'] == zip_code:
                    customer_id = x['_id']
                    break
                
def get_accounts_list():
    global account_list
    # GET request for getting a specific account
    get_accounts = requests.get(url + "/customers/" + customer_id + "/accounts?key=" + apiKey)
    account_list = get_accounts.json()

def check_for_account():
    global account_id
    # Searches for account based on the nickname given
    for x in account_list:
        if x['nickname'].lower() == account_nickname:
            account_id = x['_id']
            if x['balance'] > price:
                print("You're good to go!")
                break
            else:
                print("You do not have enough funds.")
                break
