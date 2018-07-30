import unittest
from random import randint

from clients.AuthClient import AuthClient
from clients.CategoryClient import CategoryClient


def make_new_category():
    return {
        'name': 'Fake category ' + randint(1, 4),
        'monthlyBudget': "{0:.2f|".format(randint(30, 120) + 0.03)
    }


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
        categories_list = resp.json()
        self.assertGreater(len(categories_list), 0, msg='There is at least one category in the response')

    def test_get_specific(self):
        # grab one
        resp = self.categoryClient.getCategories()
        resp.raise_for_status()
        categories_list = resp.json()['categories']

        my_cat = categories_list[0]
        resp = self.categoryClient.getCategory(my_cat['id'])
        resp.raise_for_status()
        self.assertEqual(my_cat, resp.json(),
                         msg='The chosen category has the same content whether from the "all" request or re-requested by id')

    def test_put(self):
        # grab one
        resp = self.categoryClient.getCategories()
        resp.raise_for_status()
        categories_list = resp.json()['categories']

        my_cat = categories_list[0]
        new_cat = {'id': my_cat['id'], 'monthlyBudget': str(float(my_cat['monthlyBudget']) * 2),
                   'name': 'Foghorn Leg Horns'}
        resp = self.categoryClient.putCategory(my_cat['id'], new_cat)
        resp.raise_for_status()

        resp = self.categoryClient.getCategory(my_cat['id'])
        resp.raise_for_status()
        self.assertEqual(new_cat, resp.json(), msg='The modified category has the content we put into it.')

        # now put it back the way it was...
        resp = self.categoryClient.putCategory(my_cat['id'], my_cat)
        resp.raise_for_status()

        resp = self.categoryClient.getCategory(my_cat['id'])
        resp.raise_for_status()
        self.assertEqual(my_cat, resp.json(), msg='The modified category was set back the way it was to begin with.')

    def test_post(self):
        new_category = {'monthlyBudget': '123.32', 'name': 'Fake category 1'}
        resp = self.categoryClient.postCategory(new_category)
        resp.raise_for_status()

        reflected_category = resp.json()

        resp = self.categoryClient.getCategory(reflected_category['id'])
        self.assertLess(resp.status_code, 400, msg='The category just created is there when we ask for it.')
        requested_category = resp.json()

        self.categoriesToDelete.append(reflected_category)

        for prop in ['monthlyBudget', 'name']:
            self.assertEqual(new_category[prop], reflected_category[prop],
                             msg='The reflected category has the same ' + prop + ' as what we posted.')
            self.assertEqual(new_category[prop], requested_category[prop],
                             msg='The requested category has the same ' + prop + ' as what we posted.')

    def test_delete(self):
        new_category = {'monthlyBudget': '123.32', 'name': 'Fake category 2'}
        resp = self.categoryClient.postCategory(new_category)
        resp.raise_for_status()

        reflected_category = resp.json()
        category_id = reflected_category['id']

        resp = self.categoryClient.getCategory(category_id)
        self.assertEqual(resp.status_code, 200, msg='The category just created is there when we ask for it.')

        resp = self.categoryClient.deleteCategory(category_id)
        self.assertEqual(resp.status_code, 200, msg='The delete claims to have succeeded.')

        resp = self.categoryClient.getCategory(category_id)
        self.assertEqual(resp.status_code, 404, msg='The category just deleted should no longer exist.')


if __name__ == 'main':
    unittest.main()
