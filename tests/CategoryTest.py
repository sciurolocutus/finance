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
        self.categoriesToDelete = []

    def tearDown(self):
        for cat in self.categoriesToDelete:
            self.categoryClient.deleteCategory(cat['id'])
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
        self.assertEqual(newCat, resp.json(), msg='The modified category has the content we put into it.')

        #now put it back the way it was...
        resp = self.categoryClient.putCategory(myCat['id'], myCat)
        resp.raise_for_status()

        resp = self.categoryClient.getCategory(myCat['id'])
        resp.raise_for_status()
        self.assertEqual(myCat, resp.json(), msg='The modified category was set back the way it was to begin with.')

    def test_post(self):
        newCat = {'monthlyBudget': '123.32', 'name': 'Fake category 1'}
        resp = self.categoryClient.postCategory(newCat)
        resp.raise_for_status()

        reflectedCat = resp.json()

        resp = self.categoryClient.getCategory(reflectedCat['id'])
        self.assertLess(resp.status_code, 400, msg='The category just created is there when we ask for it.')
        requestedCat = resp.json()

        self.categoriesToDelete.append(reflectedCat)
        self.assertEqual(newCat['monthlyBudget'], reflectedCat['monthlyBudget'], msg='The reflected category has the same monthly budget as what we posted.')
        self.assertEqual(newCat['name'], reflectedCat['name'], msg='The reflected category has the same name as what we posted.')
        self.assertEqual(newCat['monthlyBudget'], requestedCat['monthlyBudget'], msg='The re-requested category has the same monthly budget as what we posted.')
        self.assertEqual(newCat['name'], requestedCat['name'], msg='The re-requested category has the same name as what we posted.')

    def test_delete(self):
        newCat = {'monthlyBudget': '123.32', 'name': 'Fake category 2'}
        resp = self.categoryClient.postCategory(newCat)
        resp.raise_for_status()

        reflectedCat = resp.json()
        catId = reflectedCat['id']

        resp = self.categoryClient.getCategory(catId)
        self.assertEqual(resp.status_code, 200, msg='The category just created is there when we ask for it.')

        catToDelete = resp.json()
        resp = self.categoryClient.deleteCategory(catId)
        self.assertEqual(resp.status_code, 200, msg='The delete claims to have succeeded.')

        resp = self.categoryClient.getCategory(catId)
        self.assertEqual(resp.status_code, 404, msg='The category just deleted should no longer exist.')

if __name__ == 'main':
    unittest.main()
