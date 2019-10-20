# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

first_name = ''
last_name = ''
zip_code = ''
price = 100000
apiKey = '418663bb03b9bac82cf01afffca9bc26'
url = 'http://api.reimaginebanking.com'
customer_id = ''
account_nickname = ''
account_id = ''
account_list = ''
account_nickname_list = ''
balance_endpoint = ''
bill_endpoint = ''
# Need to get the following information from chatbot:
# Name, which type they want, and the price of what they want to buy. Maybe to distinguish same names, include prompter for address
# I need to loop through the list of customers and match the name.

# GET request for getting the list of all customers and stores JSON response
get_customers = requests.get(url + "/customers?key=" + apiKey)
customer_list = get_customers.json()

class info:
    def check_for_customer(self):
        global customer_id
        global customer_list
        # Searches for customer based on name and zipcode
        for x in customer_list:
            if x['last_name'].lower() == last_name.lower():
                if x['first_name'].lower() == first_name.lower():
                    if x['address']['zip'] == zip_code:
                        customer_id = x['_id']
                        return 1
                    
    def get_accounts_list(self):
        global account_list
        global account_nickname_list
        # GET request for getting a specific account
        get_accounts = requests.get(url + "/customers/" + customer_id + "/accounts?key=" + apiKey)
        account_list = get_accounts.json()
        count = 0
        for x in account_list:
            if count == 0:
                account_nickname_list = x['nickname']
            else:
                account_nickname_list += x['nickname']


    def find_account(self):
        global account_id
        # Searches for account based on the nickname given
        for x in account_list:
            if x['nickname'].lower() == account_nickname:
                account_id = x['_id']
        return 1

    def set_up_account_endpoints(self):
        global balance_endpoint
        global bill_endpoint
        balance_endpoint = url + "/accounts/" + account_id + "?key=" + apiKey
        bill_endpoint = url + "/accounts/" + account_id + "/bills?key=" + apiKey\

    def check_balance(self):
        temp = requests.get(balance_endpoint)
        temp2 = temp.json()
        return temp2['balance']

    def check_rewards(self):
        temp = requests.get(balance_endpoint)
        temp2 = temp.json()
        return temp2['rewards']

    def check_bills(self):
        temp = requests.get(bill_endpoint)
        temp2 = temp.json()
        return_string = []
        for x in temp2:
            if x['recurring_date'] == 1:
                return_string.append("You have a recurring payment with " + x['nickname'] + " for $" + x['payment_amount'] + ".")
            elif x['status'] == "pending":
                return_string.append("You have a pending bill with " + x['nickname'] + " for $" + x['payment_amount'] + ".")
        return return_string