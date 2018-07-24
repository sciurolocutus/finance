from sqlalchemy.orm import relationship

from db import db


class CategoryModel(db.Model):
    __tablename__ = 'category'

    id = db.Column('category_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(32))
    monthlyBudget = db.Column('monthly_budget', db.String(32))

    def __init__(self, name, monthlyBudget):
        self.name = name
        self.monthlyBudget = monthlyBudget

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, _name):
        return cls.query.filter_by(name=_name).first()

    @classmethod
    def find_all(cls):
        resp = cls.query.all()
        print('find all')
        from pprint import pprint
        pprint(resp)
        print('done finding all')
        return resp
        #return cls.query.all()

    def update(self):
        db.session.query.filter_by(id=self.id)\
                .update({'name': self.name, 'monthly_budget': self.monthlyBudget})
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        #TODO: validiate that no transactions refer to this first.
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'monthlyBudget': "{0:.2f}".format(float(self.monthlyBudget))
        }
