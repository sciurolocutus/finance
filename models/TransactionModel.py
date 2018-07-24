from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import relationship

from db import db


class TransactionModel(db.Model):
    __tablename__ = 'transaction'

    id = db.Column('transaction_id', db.Integer, primary_key=True)
    categoryId = db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'))
    transactionDate = db.Column(DATETIME, nullable=False, default=func.now())
    description = db.Column('description', db.String(32))
    amount = db.Column('amount', db.Numeric, nullable=False)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_params(cls, queryParams):
        query = cls.query
        if 'startDate' in queryParams:
            query = query.filter_by(transactionDate >= queryParams['startDate']
        if 'endDate' in queryParams:
            query = query.filter_by(transactionDate <= queryParams['endDate']
        if 'categoryName' in queryParams:
            cat = CategoryModel.find_by_name(queryParams['categoryName'])
            if cat:
                query = query.filter_by(categoryId = cat.id)
            else:
                return []
        return cls.query.filter_by(category=_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'categoryId': self.categoryId,
            'categoryName': CategoryModel.find_by_id(self.categoryId) if self.categoryId else None,
            'transactionDate': self.transactionDate.replace(microsecond=0).isoformat() if self.entry_start else datetime.now().replace(microsecond=0).isoformat(),
            'description': self.description,
            'amount': "0:.2f".format(self.amount)
        }

