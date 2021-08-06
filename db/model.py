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


bill_menu = Table(
    "bill_menu",
    Base.metadata,
    Column('bill_id', Integer, ForeignKey("bill.bill_id")),
    Column('menu_id', Integer, ForeignKey("menu.menu_id"))
)


order_menu = Table(
    "order_menu",
    Base.metadata,
    Column('order_id', Integer, ForeignKey("order.order_id")),
    Column('menu_id', Integer, ForeignKey("menu.menu_id"))
)


class AccountType(Base):
    __tablename__ = 'account_type'

    id = Column(Integer, primary_key=True)
    role = Column(String, default="Cashier", unique=True)

    users = relationship("User", backref=backref("account_type"))

    def __repr__(self):
        return f"AccountType(id={self.id!r}, role={self.role!r})"


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
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
    role = Column(String,
                  ForeignKey('account_type.role'))

    bills = relationship("Bill", backref=backref("user"))
    orders = relationship("Order", backref=backref("user"))

    def __repr__(self):
        return "<User(id='%s', email='%s', type_name='%s')>" % (self.user_id, self.email, self.role)


class Bill(Base):
    __tablename__ = 'bill'

    bill_id = Column(Integer, primary_key=True, autoincrement=True)
    bills_code = Column(String)
    item_quantity = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    item_price = Column(Float, ForeignKey('menu.sell_price'))
    item_bill = Column(String, ForeignKey('menu.item_name'))
    user_sold = Column(Integer, ForeignKey('user.user_id'))
    menus = relationship(
        "Menu", secondary=bill_menu, back_populates="bills"
    )

    def __repr__(self):
        return _repr(bill_id=self.bill_id, item_quantity=self.item_quantity, bills_code=self.bills_code)


class Order(Base):
    __tablename__ = 'order'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    orders_code = Column(String)
    item_order = Column(String, ForeignKey('menu.item_name'))
    item_quantity = Column(Integer)
    item_price = Column(Float, ForeignKey('menu.sell_price'))
    user_sell = Column(Integer, ForeignKey('user.user_id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    menus = relationship(
        "Menu", secondary=order_menu, back_populates="orders"
    )

    def __repr__(self):
        return _repr(order_id=self.order_id, item_quantity=self.item_quantity, orders_code=self.orders_code)


class Menu(Base):
    __tablename__ = 'menu'

    menu_id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String, unique=True)
    item_image = Column(LargeBinary, nullable=True)
    sell_price = Column(Float)
    categories_name = Column(String, ForeignKey('category.category_name'))
    orders = relationship(
        "Order", secondary=order_menu, back_populates="menus"
    )
    bills = relationship(
        "Bill", secondary=bill_menu, back_populates="menus"
    )

    def __repr__(self):
        return _repr(menu_id=self.menu_id, item_name=self.item_name, sell_price=self.sell_price)


class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, unique=True)
    menus = relationship("Menu", backref=backref("category"))

    def __repr__(self):
        return _repr(category_id=self.category_id, category_name=self.category_name)


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


if __name__ == "__main__":
    from database import MyDatabase
    Base.metadata.create_all(MyDatabase().db_engine)
