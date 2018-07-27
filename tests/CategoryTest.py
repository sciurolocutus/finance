import unittest
import json
from pprint import pprint

from clients.AuthClient import AuthClient
from clients.CategoryClient import CategoryClient

class CategoryTest(unittest.TestCase):
    def setUp(self):
        base = 'http://localhost:5000'
        ac = AuthClient(base)
        jwt = ac.getAuth('bob', 'password')
        self.categoryClient = CategoryClient(base, jwt)

    def tearDown(self):
        self.categoryClient = None

    def test_get_all(self):
        resp = self.categoryClient.getCategories()
        resp.raise_for_status()
        categoriesList = resp.json()
        self.assertGreater(len(categoriesList), 0, msg='There is at least one category in the response')

    def test_get_specific(self):
        #grab one
        resp = self.categoryClient.getCategories()
        resp.raise_for_status()
        categoriesList = resp.json()['categories']

        myCat = categoriesList[0]
        resp = self.categoryClient.getCategory(myCat['id'])
        resp.raise_for_status()
        self.assertEqual(myCat, resp.json(), msg='The chosen category has the same content whether from the "all" request or re-requested by id')

    def test_put(self):
        #grab one
        resp = self.categoryClient.getCategories()
        resp.raise_for_status()
        categoriesList = resp.json()['categories']

        myCat = categoriesList[0]
        newCat = {'id': myCat['id'], 'monthlyBudget': str(float(myCat['monthlyBudget']) * 2), 'name': 'Foghorn Leg Horns'}
        resp = self.categoryClient.putCategory(myCat['id'], newCat)
        resp.raise_for_status()

        resp = self.categoryClient.getCategory(myCat['id'])
        resp.raise_for_status()
        self.assertEqual(newCat, resp.json())
        print('we can see that the new category is in place: ', resp.text)

        #now put it back the way it was...
        resp = self.categoryClient.putCategory(myCat['id'], myCat)
        resp.raise_for_status()

        resp = self.categoryClient.getCategory(myCat['id'])
        resp.raise_for_status()
        self.assertEqual(myCat, resp.json())

if __name__ == 'main':
    unittest.main()
