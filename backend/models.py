from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, create_engine, text , JSON, Date
from sqlalchemy.orm import declarative_base
from datetime import datetime


Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key = True, index = True)
    product_name= Column(String)
    product_description = Column(String)
    product_price = Column(Float)
    

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True)
    name = Column(String)
    is_admin = Column(Boolean, default = False)
    phone_number = Column(Integer)
    email = Column(String, unique = True)

class Categories(Base):
    __tablename__= "categories"
    category_id = Column(Integer, primary_key = True, index = True )
    category_name = Column (String)

class Orders(Base):
    __tablename__ = "orders"
    order_id = Column( Integer, primary_key= True , index = True)
    product_id= Column(Integer)
    order_name = Column(String)
    order_date = Column(Date)
    description = Column(String)
