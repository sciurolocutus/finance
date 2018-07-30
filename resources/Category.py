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

    def get(self, category_id):
        cat = CategoryModel.find_by_id(category_id)
        if not cat:
            return CATEGORY_NOT_FOUND, 404
        else:
            return cat.json()

    @jwt_required()
    def put(self, category_id):
        data = Category.parser.parse_args()

        cat = CategoryModel.find_by_id(category_id)
        if not cat:
            return CATEGORY_NOT_FOUND, 404

        category = CategoryModel(data['name'], data['monthlyBudget'])
        category.id = category_id

        try:
            category.update()
        except:
            return {'message': 'An error occurred updating the category'}, 500

        return category.json()

    @jwt_required()
    def delete(self, category_id):
        cat = CategoryModel.find_by_id(category_id)
        if not cat:
            return CATEGORY_NOT_FOUND, 404
        cat.delete_from_db()


class CategoryList(Resource):
    def get(self):
        resp = {'categories': list(map(lambda cat: cat.json(), CategoryModel.find_all()))}
        if not resp['categories']:
            return CATEGORY_NOT_FOUND, 404
        return resp

    @jwt_required()
    def post(self):
        data = Category.parser.parse_args()

        category = CategoryModel(data['name'], data['monthlyBudget'])

        try:
            category.save_to_db()
        except:
            return {'message': 'An error occurred creating the category'}, 500

        return category.json(), 201

