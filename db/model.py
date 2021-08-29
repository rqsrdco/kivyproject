import typing
import sqlalchemy as sa
from sqlalchemy import (
    Table, Column, Integer, String, ForeignKey, Date, DateTime, Float, Text
)
from sqlalchemy.sql import func
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# bill_menu = Table(
#    "bill_menu",
#    Base.metadata,
#    Column('bill_id', ForeignKey("bill.id"), primary_key=True),
#    Column('menu_id', ForeignKey("menu.id"), primary_key=True)
# )


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    image = Column(LargeBinary, nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", back_populates="product")

    menu = relationship("Menu", back_populates="product", uselist=False)

    def __repr__(self):
        return "Product(id= %s,name= %s, category_id= %s)" % (self.id, self.name, self.category_id)

    def convertToBinaryData(filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def writeTofile(data, filename):
        import os.path
        file_exists = os.path.isfile(filename)
        if file_exists:
            pass
        else:
            # Convert binary data to proper format and write it on Hard Disk
            with open(filename, 'wb') as file:
                file.write(data)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    product = relationship("Product", back_populates="category")

    def __repr__(self):
        return "Category(id=%s, name=%s)" % (self.id, self.name)


class AccountType(Base):
    __tablename__ = 'account_type'

    id = Column(Integer, primary_key=True)
    role = Column(String, default="Cashier", unique=True)

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"AccountType(id={self.id!r}, role={self.role!r})"


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    password = Column(String)
    phone_number = Column(String, nullable=True, unique=True)
    gender = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())
    updated_at = Column(DateTime(
        timezone=True), onupdate=func.now())
    role_id = Column(Integer,
                     ForeignKey('account_type.id'))
    role = relationship("AccountType", back_populates="users")

    bills = relationship("Bill", back_populates="cashiers")
    orders = relationship("Order", back_populates="cashiers")

    def __repr__(self):
        return "<User(id='%s', email='%s', role='%s')>" % (self.id, self.email, self.role_id)


class Bill(Base):
    __tablename__ = 'bill'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    product = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    cashier_id = Column(Integer, ForeignKey('user.id'))
    cashiers = relationship("User", back_populates="bills")

    # menus = relationship(
    #    "Menu", secondary=bill_menu, back_populates="bills"
    # )

    def __repr__(self):
        return "id=%s, quantity=%s, code=%s" % (self.id, self.quantity, self.code)


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    product = Column(String)
    cashier_id = Column(Integer, ForeignKey('user.id'))
    cashiers = relationship("User", back_populates="orders")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "id=%s, quantity=%s, code=%s" % (self.id, self.quantity, self.code)


class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), unique=True)
    products = relationship("Product", backref=backref("store", uselist=False))
    input_price = Column(Float)
    quantity = Column(Integer)

    def __repr__(self):
        return "Store(product_id= %s, input_price= %s, quantity= %s)" % (self.product_id, self.input_price, self.quantity)


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), unique=True)
    product = relationship("Product", back_populates="menu")
    sell_price = Column(Float)

    # bills = relationship(
    #    "Bill", secondary=bill_menu, back_populates="menus"
    # )

    def __repr__(self):
        return "Menu(id=%s, product_id=%s, sell_price=%s)" % (self.id, self.product_id, self.sell_price)


def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
    '''
        Helper for __repr__
        '''
    field_strings = []
    at_least_one_attached_attribute = False
    for key, field in fields.items():
        try:
            field_strings.append(f'{key}={field!r}')
        except sa.orm.exc.DetachedInstanceError:
            field_strings.append(f'{key}=DetachedInstanceError')
        else:
            at_least_one_attached_attribute = True
    if at_least_one_attached_attribute:
        return f"<{self.__class__.__name__}({','.join(field_strings)})>"
    return f"<{self.__class__.__name__} {id(self)}>"
