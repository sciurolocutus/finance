from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT

from db import db
from resources.Category import Category, CategoryList
#from resources.Transaction import Transaction, TransactionList
from resources.user import UserRegister
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Very secret password.'
app.url_map.strict_slashes = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(CategoryList, '/categories')
api.add_resource(Category, '/categories/<int:categoryId>')
#api.add_resource(TransactionList, '/transactions')
#api.add_resource(Transaction, '/transactions/<int:transactionId>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
