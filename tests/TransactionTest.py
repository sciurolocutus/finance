import unittest
from datetime import datetime, timedelta
from random import randint

from clients.AuthClient import AuthClient
from clients.CategoryClient import CategoryClient
from clients.TransactionClient import TransactionClient


def make_new_transaction(category):
    return {
        'categoryId': category['id'],
        'transactionDate': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        'description': 'I bought a ' + category['name'],
        'amount': "{0:.2f}".format(randint(10, 80) + 0.03)
    }


class TransactionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base = 'http://localhost:5000'
        ac = AuthClient(base)
        jwt = ac.getAuth('bob', 'password')
        cls.transactionClient = TransactionClient(base, jwt)
        cls.categoryClient = CategoryClient(base, jwt)
        cls.transactionsToDelete = []
        cls.categoriesToDelete = []

        cls.categories = cls.categoryClient.getCategories().json()['categories']
        if not cls.categories:
            # We need at least one category to exist for these tests.
            cls.categoryClient.postCategory({
                "name": "Books",
                "monthlyBudget": 20.01
            })
            cls.categories = cls.categoryClient.getCategories()
            # Undo what you have done.
            cls.categoriesToDelete = cls.categories

        cat = cls.categories[0]
        # Set up prior purchases
        for x in range(1, 5):
            t = make_new_transaction(cat)
            t['transactionDate'] = (datetime.now() - timedelta(days=x)).strftime("%Y-%m-%dT%H:%M:%S")
            resp = cls.transactionClient.postTransaction(t)
            resp.raise_for_status()
            cls.transactionsToDelete.append(resp.json())

    @classmethod
    def tearDownClass(cls):
        for t in cls.transactionsToDelete:
            cls.transactionClient.deleteTransaction(t['id'])
        cls.transactionClient = None

        for c in cls.categoriesToDelete:
            cls.categoryClient.deleteCategory(c['id'])
        cls.categoryClient = None

    def test_get_all(self):
        resp = self.transactionClient.getTransactions()
        resp.raise_for_status()
        transactions_list = resp.json()
        self.assertGreater(len(transactions_list), 0, msg='There is at least one transaction in the response')

    def test_get_by_date(self):
        # Previously we set up five transactions ranging from yesterday to 5 days ago, in the first category.
        queryParams = {'categoryName': self.categories[0]['name']}
        resp = self.transactionClient.getTransactions(queryParams)
        resp.raise_for_status()
        first_count = len(resp.json()['transactions'])
        last_count = first_count

        for x in range(1, 5):
            queryParams['endDate'] = (datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d')
            resp = self.transactionClient.getTransactions(queryParams)
            resp.raise_for_status()
            current_count = len(resp.json()['transactions'])
            self.assertLess(current_count, last_count,
                            msg='Going backwards by days, each successive response has fewer transactions in it')
            last_count = current_count

    def test_get_specific(self):
        # grab one
        resp = self.transactionClient.getTransactions()
        resp.raise_for_status()
        transactions_list = resp.json()['transactions']

        my_transaction = transactions_list[0]
        resp = self.transactionClient.getTransaction(my_transaction['id'])
        resp.raise_for_status()
        self.assertEqual(my_transaction, resp.json(),
                         msg='The chosen transaction has the same content whether from the "all" request or re-requested by id')

    def test_put(self):
        # grab one
        resp = self.transactionClient.getTransactions()
        resp.raise_for_status()
        transactions_list = resp.json()['transactions']

        my_transaction = transactions_list[0]
        new_transaction = make_new_transaction(self.categories[0])
        new_transaction['id'] = my_transaction['id']
        resp = self.transactionClient.putTransaction(my_transaction['id'], new_transaction)
        resp.raise_for_status()

        resp = self.transactionClient.getTransaction(my_transaction['id'])
        resp.raise_for_status()
        for prop in ['categoryId', 'transactionDate', 'description', 'amount', 'id']:
            self.assertEqual(new_transaction[prop], resp.json()[prop],
                             msg='The modified category has the same ' + prop + ' we put into it.')

        if new_transaction['categoryId']:
            self.assertIn('categoryName', resp.json(),
                          msg='Given the category ID is populated, the response contains a categoryName')

        # now put it back the way it was...
        resp = self.transactionClient.putTransaction(my_transaction['id'], my_transaction)
        resp.raise_for_status()

        resp = self.transactionClient.getTransaction(my_transaction['id'])
        resp.raise_for_status()
        self.assertEqual(my_transaction, resp.json(),
                         msg='The modified category was set back the way it was to begin with.')

    def test_post(self):
        new_transaction = make_new_transaction(self.categories[0])
        resp = self.transactionClient.postTransaction(new_transaction)
        resp.raise_for_status()

        reflected_transaction = resp.json()

        resp = self.transactionClient.getTransaction(reflected_transaction['id'])
        self.assertLess(resp.status_code, 400, msg='The transaction just created is there when we ask for it.')
        requested_transaction = resp.json()

        self.transactionsToDelete.append(reflected_transaction)
        for prop in ['categoryId', 'transactionDate', 'description', 'amount']:
            self.assertEqual(new_transaction[prop], reflected_transaction[prop],
                             msg='The reflected transaction has the same ' + prop + ' as what we posted.')
            self.assertEqual(new_transaction[prop], requested_transaction[prop],
                             msg='The requested transaction has the same ' + prop + ' as what we posted.')

    def test_delete(self):
        new_transaction = make_new_transaction(self.categories[0])
        resp = self.transactionClient.postTransaction(new_transaction)
        resp.raise_for_status()

        reflected_transaction = resp.json()
        transaction_id = reflected_transaction['id']

        resp = self.transactionClient.getTransaction(transaction_id)
        self.assertEqual(resp.status_code, 200, msg='The transaction just created is there when we ask for it.')

        resp = self.transactionClient.deleteTransaction(transaction_id)
        self.assertEqual(resp.status_code, 200, msg='The delete claims to have succeeded.')

        resp = self.transactionClient.getTransaction(transaction_id)
        self.assertEqual(resp.status_code, 404, msg='The transaction just deleted should no longer exist.')


if __name__ == 'main':
    unittest.main()
