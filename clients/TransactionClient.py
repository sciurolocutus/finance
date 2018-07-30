import requests

class TransactionClient:
    def __init__(self, baseurl, jwt):
        self.baseurl = baseurl + '/transactions'
        self.jwt = jwt

    def getTransactions(self, params=None):
        return requests.get("{0}".format(self.baseurl), params=params)

    def getTransaction(self, transaction_id):
        return requests.get("{0}/{1}".format(self.baseurl, transaction_id))

    def deleteTransaction(self, transaction_id):
        headers={'Authorization': 'JWT ' + self.jwt}
        return requests.delete("{0}/{1}".format(self.baseurl, transaction_id), headers=headers)

    def putTransaction(self, transaction_id, transaction):
        headers={'Authorization': 'JWT ' + self.jwt}
        return requests.put("{0}/{1}".format(self.baseurl, transaction_id), headers=headers, json=transaction)

    def postTransaction(self, transaction):
        headers={'Authorization': 'JWT ' + self.jwt}
        return requests.post("{0}".format(self.baseurl), headers=headers, json=transaction)
