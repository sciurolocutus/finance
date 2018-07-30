from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from datetime import datetime

from exceptions.ValidationException import ValidationException
from models.CategoryModel import CategoryModel
from models.TransactionModel import TransactionModel

TRANSACTION_NOT_FOUND = {'message': 'Transaction not found'}
TRANSACTION_NOT_UPDATED = {'message': 'An error occurred updating the transaction'}
TRANSACTION_NOT_CREATED = {'message': 'An error occurred creating the transaction'}


def validate_category_reference(t):
    if t.categoryId:
        cat = CategoryModel.find_by_id(t.categoryId)
        if not cat:
            raise ValidationException('category ID specified does not exist.')


class Transaction(Resource):
    TABLE_NAME = 'transaction'
    parser = reqparse.RequestParser()
    parser.add_argument('categoryId',
                        type=int,
                        required=False,
                        help='The category to which this transaction belongs')
    parser.add_argument('transactionDate',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'),
                        required=True,
                        help='When this transaction occurred')
    parser.add_argument('description',
                        type=str,
                        required=False,
                        help='A description of this transaction',
                        )
    parser.add_argument('amount',
                        type=lambda x: "{0:.2f}".format(float(x)),
                        required=True,
                        help='Amount of this transaction')

    queryParser = reqparse.RequestParser()
    queryParser.add_argument('startDate',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        location='args',
                        required=False,
                        help='The earliest date allowed')
    queryParser.add_argument('endDate',
                        type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                        location='args',
                        required=False,
                        help='The latest date allowed')
    queryParser.add_argument('categoryName',
                        type=str,
                        location='args',
                        required=False,
                        help='The category name to filter by')

    def get(self, transaction_id):
        cat = TransactionModel.find_by_id(transaction_id)
        if not cat:
            return TRANSACTION_NOT_FOUND, 404
        else:
            return cat.json()

    @jwt_required()
    def put(self, transaction_id):
        data = Transaction.parser.parse_args()

        t = TransactionModel.find_by_id(transaction_id)
        if not t:
            return TRANSACTION_NOT_FOUND, 404

        validate_category_reference(t)

        transaction = TransactionModel(data)
        transaction.id = transaction_id

        try:
            transaction.update()
        except Exception as e:
            print(e)
            return TRANSACTION_NOT_UPDATED, 500

        return transaction.json()

    @jwt_required()
    def delete(self, transaction_id):
        t = TransactionModel.find_by_id(transaction_id)
        if not t:
            return TRANSACTION_NOT_FOUND, 404
        t.delete_from_db()

        return {'message': 'success'}, 200


class TransactionList(Resource):
    def get(self):
        params = Transaction.queryParser.parse_args()
        resp = {'transactions': list(map(lambda t: t.json(), TransactionModel.find_by_params(params)))}
        if not resp['transactions']:
            return TRANSACTION_NOT_FOUND, 404
        return resp

    @jwt_required()
    def post(self):
        data = Transaction.parser.parse_args()

        t = TransactionModel(data)

        validate_category_reference(t)

        try:
            t.save_to_db()
        except Exception as err:
            print(err)
            return TRANSACTION_NOT_CREATED, 500

        return t.json(), 201
