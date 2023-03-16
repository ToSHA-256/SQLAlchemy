import psycopg2
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = 'postgresql://sql_user:sql_password@localhost:5432/dbstudents'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    possession = Column(Integer)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)


Base.metadata.create_all(engine)

session = Session()


def add_in_table(entity, name, value):
    if session.query(entity).filter_by(name=name).first() is None:
        if entity == Customer:
            session.add(entity(name=name, possession=value))
        if entity == Product:
            session.add(entity(name=name, price=value))
        session.commit()


add_in_table(Customer, 'Alice Bork', 550)
add_in_table(Customer, 'Collin Donovan', 980)
add_in_table(Customer, 'Gilbert Harper', 350)

add_in_table(Product, 'POCO X4 Pro', 500)
add_in_table(Product, 'Xiaomi Redmi Note 12', 900)
add_in_table(Product, 'Realme 10 Pro 5G', 200)
add_in_table(Product, 'OnePlus Nord CE 2 Lite 5G', 200)

customers = session.query(Customer).all()
products = session.query(Product).all()
for customer in customers:
    print(f'У {customer.name} {customer.possession}$')
for product in products:
    print(f'{product.name} стоит {product.price}$')

who_can_by = session.query(Customer.name, Product.name).join(Customer, Customer.possession > Product.price)
print("\nКто какой продукт сможет купить: ")
for row in who_can_by.all():
    print(row)
