from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import relationship

from db import db
from models.CategoryModel import CategoryModel


class TransactionModel(db.Model):
    __tablename__ = 'transaction'

    id = db.Column('transaction_id', db.Integer, primary_key=True)
    categoryId = db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'))
    transactionDate = db.Column(DATETIME, nullable=False, default=func.now())
    description = db.Column('description', db.String(32))
    amount = db.Column('amount', db.Numeric, nullable=False)

    def __init__(self, param_dict):
        self.categoryId = param_dict['categoryId']
        self.transactionDate = param_dict['transactionDate']
        self.description = param_dict['description']
        self.amount = param_dict['amount']

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_params(cls, queryParams):
        query = cls.query
        if queryParams['startDate']:
            query = query.filter(func.date(TransactionModel.transactionDate) >= func.date(queryParams['startDate']))
        if queryParams['endDate']:
            query = query.filter(func.date(TransactionModel.transactionDate) <= func.date(queryParams['endDate']))
        if queryParams['categoryName']:
            cat = CategoryModel.find_by_name(queryParams['categoryName'])
            if cat:
                query = query.filter(TransactionModel.categoryId == cat.id)
            else:
                return []
        return query

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def update(self):
        db.session.query(TransactionModel).filter(TransactionModel.id == self.id) \
            .update(
            {
                'categoryId': self.categoryId,
                'transactionDate': self.transactionDate,
                'description': self.description,
                'amount': self.amount
            }
        )
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        resp = {
            'id': self.id,
            'categoryId': self.categoryId,
            'transactionDate': self.transactionDate.replace(
                microsecond=0).isoformat() if self.transactionDate else datetime.now().replace(
                microsecond=0).isoformat(),
            'description': self.description,
            'amount': "{0:.2f}".format(float(self.amount))
        }

        if self.categoryId:
            cat = CategoryModel.find_by_id(self.categoryId)
            if cat:
                resp['categoryName'] = cat.name

        return resp
