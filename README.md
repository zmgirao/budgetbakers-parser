# budgetbakers-parser
Parser for Wallet transactions from Budget Bakers. Not related in any way.

Since the app from Budget Bakers does not have transaction export via Web app or iOS, I needed to make my own parser.

Instructions:
1) Save as HTML a list of transactions from Wallet app named bakers.html and:
2) Run the Python script to get:

3) You may need to tune line 86 of main.py if you want to exclude certain accounts
from counting as expenses (paying credit cards, putting amounts into savings)

The output will be: 
1) dump.json file with a list of the transactions in JSON object format;
2) ouput.txt file with a customized output for transactions that I used for some chart generation.

Hope it suits you.
