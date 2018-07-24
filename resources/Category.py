from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from sqlalchemy.sql.functions import now

from models.CategoryModel import CategoryModel

CATEGORY_NOT_FOUND = {'message': 'Category not found'}

class Category(Resource):
    TABLE_NAME = 'category'
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='The name of this category')
    parser.add_argument('monthlyBudget',
                        type=str,
                        required=True,
                        help='Monthly budgeted amount')

    def get(self, categoryId):
        cat = CategoryModel.find_by_id(categoryId)
        if not cat:
            return CATEGORY_NOT_FOUND, 404
        else:
            return cat.json()


class CategoryList(Resource):
    def get(self):
        print('category list GET')
        resp = {'categories': list(map(lambda cat: cat.json(), CategoryModel.find_all()))}
        from pprint import pprint
        pprint(resp)
        if not resp['categories']:
            return CATEGORY_NOT_FOUND, 404
        return resp

    @jwt_required()
    def post(self):
        print('POST /categories')
        data = Category.parser.parse_args()
        print('POST /categories after parsing args')

        category = CategoryModel(data['name'], data['monthlyBudget'])

        from pprint import pprint
        pprint(category)

        try:
            category.save_to_db()
        except:
            return {'message': 'An error occurred creating the category'}, 500

        return category.json(), 201

    @jwt_required()
    def put(self, categoryId):
        data = Category.parser.parse_args()

        cat = CategoryModel.find_by_id(categoryId)
        if not cat:
            return CATEGORY_NOT_FOUND, 404

        category = CategoryModel(data['name'], data['monthlyBudget'])
        category.id = categoryId

        try:
            category.save_to_db()
        except:
            return {'message': 'An error occurred updating the category'}, 500

        return category.json()
