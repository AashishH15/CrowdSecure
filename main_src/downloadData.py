import json

def getAccountBalance(account_id):
    
    f = open('C:/Users/aashi/OneDrive/Desktop/MHack/data/data.json', 'r')

    data = json.loads(f.read())

    accountBalance = data[account_id]['account-balance']

    f.close()

    return float(accountBalance)

def getTransactionReceipt(account_id):
    
    f = open('C:/Users/aashi/OneDrive/Desktop/MHack/data/data.json', 'r')

    data = json.loads(f.read())

    transactionReceipt = data[account_id]['transaction-receipt']

    f.close()
    
    return transactionReceipt

def getKeys():
     
    f = open('C:/Users/aashi/OneDrive/Desktop/MHack/data/data.json', 'r')

    key_list = []

    data = json.loads(f.read())

    for key in data.keys():
        if key != 'git-coin':
            key_list.append(key)

    f.close()
    
    return tuple(key_list)