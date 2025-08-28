from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///budget.db')
Session = sessionmaker(bind=engine)

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    
    transactions = relationship('Transaction', back_populates='category')
    
    @classmethod
    def create(cls, name):
        session = Session()
        category = cls(name=name)
        session.add(category)
        session.commit()
        result = {'id': category.id, 'name': category.name}
        session.close()
        return result
    
    @classmethod
    def get_all(cls):
        session = Session()
        categories = session.query(cls).all()
        result = [{'id': c.id, 'name': c.name} for c in categories]
        session.close()
        return result
    
    @classmethod
    def find_by_id(cls, id):
        session = Session()
        category = session.query(cls).filter(cls.id == id).first()
        result = {'id': category.id, 'name': category.name} if category else None
        session.close()
        return result
    
    @classmethod
    def delete(cls, id):
        session = Session()
        category = session.query(cls).filter(cls.id == id).first()
        if category:
            session.delete(category)
            session.commit()
            session.close()
            return True
        session.close()
        return False

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # 'income' or 'expense'
    description = Column(String)
    date = Column(DateTime, default=datetime.now)
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    category = relationship('Category', back_populates='transactions')
    
    @classmethod
    def create(cls, amount, type, category_id, description=None):
        session = Session()
        transaction = cls(amount=amount, type=type, category_id=category_id, description=description)
        session.add(transaction)
        session.commit()
        result = {
            'id': transaction.id,
            'amount': transaction.amount,
            'type': transaction.type,
            'description': transaction.description,
            'date': transaction.date,
            'category_id': transaction.category_id
        }
        session.close()
        return result
    
    @classmethod
    def get_all(cls):
        session = Session()
        transactions = session.query(cls).all()
        result = []
        for t in transactions:
            result.append({
                'id': t.id,
                'amount': t.amount,
                'type': t.type,
                'description': t.description,
                'date': t.date,
                'category_id': t.category_id
            })
        session.close()
        return result
    
    @classmethod
    def find_by_id(cls, id):
        session = Session()
        transaction = session.query(cls).filter(cls.id == id).first()
        if transaction:
            result = {
                'id': transaction.id,
                'amount': transaction.amount,
                'type': transaction.type,
                'description': transaction.description,
                'date': transaction.date,
                'category_id': transaction.category_id
            }
        else:
            result = None
        session.close()
        return result
    
    @classmethod
    def find_by_category(cls, category_id):
        session = Session()
        transactions = session.query(cls).filter(cls.category_id == category_id).all()
        result = []
        for t in transactions:
            result.append({
                'id': t.id,
                'amount': t.amount,
                'type': t.type,
                'description': t.description,
                'date': t.date,
                'category_id': t.category_id
            })
        session.close()
        return result
    
    @classmethod
    def find_by_date(cls, date):
        session = Session()
        transactions = session.query(cls).filter(cls.date.like(f'{date}%')).all()
        result = []
        for t in transactions:
            result.append({
                'id': t.id,
                'amount': t.amount,
                'type': t.type,
                'description': t.description,
                'date': t.date,
                'category_id': t.category_id
            })
        session.close()
        return result
    
    @classmethod
    def get_balance(cls):
        session = Session()
        income = session.query(cls).filter(cls.type == 'income').all()
        expenses = session.query(cls).filter(cls.type == 'expense').all()
        
        total_income = sum(t.amount for t in income)
        total_expenses = sum(t.amount for t in expenses)
        balance = total_income - total_expenses
        
        session.close()
        return balance
    
    @classmethod
    def delete(cls, id):
        session = Session()
        transaction = session.query(cls).filter(cls.id == id).first()
        if transaction:
            session.delete(transaction)
            session.commit()
            session.close()
            return True
        session.close()
        return False

Base.metadata.create_all(engine)