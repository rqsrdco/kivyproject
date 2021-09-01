import os
import sys
import random
from pathlib import Path
from typing import List, Dict, Tuple

from sqlalchemy import (
    Table, Column, Integer, String, ForeignKey, Date, DateTime, Float, Text,
    create_engine, and_
)
from sqlalchemy.sql import func
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from sqlalchemy_utils import database_exists, create_database

from logger import LOGGER

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    image = Column(LargeBinary, nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))

    # [ Product --> Category ] | One --> Many
    category = relationship("Category", back_populates="product")
    # [ Menu <--> Product ] | One <--> One
    menu = relationship("Menu", back_populates="product", uselist=False)
    # [ Store <--> Product ] | One <--> One
    store = relationship("Store", back_populates="product", uselist=False)

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

    # [ Product --> Category ] | One --> Many
    product = relationship("Product", back_populates="category")

    def __repr__(self):
        return "Category(id=%s, name=%s)" % (self.id, self.name)


class AccountType(Base):
    __tablename__ = 'account_type'

    id = Column(Integer, primary_key=True)
    role = Column(String, default="Cashier", unique=True)

    # [ User --> AccountType ] | One --> Many
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

    role_id = Column(Integer, ForeignKey('account_type.id'))
    # [ User --> AccountType ] | One --> Many
    role = relationship("AccountType", back_populates="users")
    # [ Bill --> User ] | One --> Many
    bill = relationship("Bill", back_populates="cashier")
    # [ Order --> User ] | One --> Many
    order = relationship("Order", back_populates="cashier")

    def __repr__(self):
        return "<User(id='%s', email='%s', role='%s')>" % (self.id, self.email, self.role_id)


class Bill(Base):
    __tablename__ = 'bill'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    quantity = Column(Integer)
    menu_id = Column(Integer, ForeignKey('menu.id'))
    cashier_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # [ Bill --> Menu ] | One --> Many
    menu = relationship("Menu", back_populates="bill")
    # [ Bill --> User ] | One --> Many
    cashier = relationship("User", back_populates="bill")

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
    menu_id = Column(Integer, ForeignKey('menu.id'))
    cashier_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # [ Order --> Menu ] | One --> Many
    menu = relationship("Menu", back_populates="order")
    # [ Order --> User ] | One --> Many
    cashier = relationship("User", back_populates="order")

    def __repr__(self):
        return "id=%s, quantity=%s, code=%s" % (self.id, self.quantity, self.code)


class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True, autoincrement=True)
    input_price = Column(Float)
    quantity = Column(Integer)
    product_id = Column(Integer, ForeignKey('product.id'), unique=True)

    # [ Store <--> Product ] | One <--> One
    product = relationship("Product", back_populates="store")

    def __repr__(self):
        return "Store(product_id= %s, input_price= %s, quantity= %s)" % (self.product_id, self.input_price, self.quantity)


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sell_price = Column(Float)
    product_id = Column(Integer, ForeignKey('product.id'), unique=True)

    # [ Menu <--> Product ] | One <--> One
    product = relationship("Product", back_populates="menu")
    # [ Bill --> Menu ] | One --> Many
    bill = relationship("Bill", back_populates='menu')
    # [ Order --> Menu ] | One --> Many
    order = relationship("Order", back_populates="menu")

    def __repr__(self):
        return "Menu(id=%s, product_id=%s, sell_price=%s, products=%s)" % (self.id, self.product_id, self.sell_price, self.product)


class InitObjects:
    def create_Product_objects(self) -> List[Product]:
        return [Product(
                name="Coffee %s" % p if p % 2 == 0 else "Food %s" % p if p % 3 == 0 else "Drink %s" % p,
                image=Product.convertToBinaryData(
                    'assets/images/coffee.png') if p % 2 == 0 else Product.convertToBinaryData(
                    'assets/images/food.png') if p % 3 == 0 else Product.convertToBinaryData(
                    'assets/images/drink.png'),
                category_id=1 if p % 2 == 0 else 2 % p if p % 3 == 0 else 3
                ) for p in range(39)]

    def create_Category_objects(self) -> Tuple[Category]:
        '''
        Category objects
        '''
        cf = Category(name='Coffee')
        fd = Category(name='Food')
        dk = Category(name='Drink')
        return cf, fd, dk

    def create_AccountType_objects(self) -> Tuple[AccountType]:
        '''
        AccountType objects
        '''
        cashier = AccountType(role="Cashier")
        admin = AccountType(role="Administrator")
        return cashier, admin

    def create_User_objects(self) -> Tuple[User]:
        '''
        User objects
        '''
        cs_test = User(
            first_name='Cashier',
            last_name='Test',
            email='c',
            password='c',
            phone_number='0908608333',
            gender='Female',
            role_id=1
        )
        user_cs = User(
            first_name='Fisrt Name',
            last_name='Cashier',
            email='firsct@cashier.com',
            password='c',
            phone_number='0908118339',
            gender='Female',
            role_id=1
        )
        user_ad = User(
            first_name='Fisrt Name',
            last_name='Admin',
            email='a',
            password='a',
            phone_number='0908008786',
            gender='Male',
            role_id=1
        )
        return cs_test, user_cs, user_ad


class AlchemySQLite:
    DB_ENGINE = {
        'SQLITE': 'sqlite:///{DB}'
    }
    db_engine = None
    db_session = None

    def __init__(self, db_type='sqlite', db_name="DATA"):
        db_type = db_type.upper()

        if db_type in self.DB_ENGINE.keys():
            base_dir = os.path.abspath(os.path.dirname(__file__))
            db_url = f"{Path(base_dir).as_posix()}/{db_name}.db"
            engine_url = self.DB_ENGINE[db_type].format(DB=db_url)
            self.db_engine = create_engine(
                engine_url, encoding='utf-8', echo=False)
        else:
            print(f'{db_type} is not found in DB_ENGINE')
        print(f"------> db_engine [{self.db_engine}]")
        self.create_session()

    def create_session(self):
        if not database_exists(self.db_engine.url):
            create_database(self.db_engine.url)
        Base.metadata.create_all(self.db_engine)
        Session = sessionmaker(bind=self.db_engine)
        self.db_session = Session()

    def init_product_categories(self):
        self.db_session.add_all(InitObjects().create_Category_objects())
        self.db_session.commit()

    def init_products(self):
        self.db_session.add_all(InitObjects().create_Product_objects())
        self.db_session.commit()

    def init_account_roles(self):
        self.db_session.add_all(InitObjects().create_AccountType_objects())
        self.db_session.commit()

    def init_accounts(self):
        self.db_session.add_all(InitObjects().create_User_objects())
        self.db_session.commit()

    def init_menu(self):
        products = self.db_session.get_products()
        menu = [Menu(
            sell_price=round(random.uniform(19000.99, 39999.99), 2),
            product_id=p.id
        ) for p in products]
        self.db_session.add_all(menu)
        self.db_session.commit()

    def init_store(self):
        products = self.db_session.get_menus()
        store = [Store(
            product_id=p.id,
            input_price=round(p.sell_price * 0.78, 2),
            quantity=random.randint(222, 333)
        ) for p in products]
        self.db_session.add_all(store)
        self.db_session.commit()

    def get_menus(self):
        try:
            return self.db_session.query(Menu).all()
        except Exception as e:
            print(e)
            return None

    def add_new_role(self, new_role: str):
        try:
            fetchRole = self.db_session.query(AccountType).filter(
                AccountType.role == new_role).first()
            if fetchRole is None:
                role = AccountType(role=new_role)
                result = self.db_session.add(role)
                self.db_session.commit()
                return True
            else:
                return False
        except Exception:
            return False

    def get_roles(self) -> List[AccountType]:
        try:
            return self.db_session.query(AccountType).all()
        except Exception:
            return None

    def get_role_id_by_name(self, name: str) -> int:
        try:
            result = self.db_session.query(AccountType).filter(
                AccountType.role == name
            ).first()
            if result:
                print("---------result.id----\n", result.id)
                return result.id
            else:
                return None
        except Exception:
            return None

    def get_staff(self, admin: User) -> List[User]:
        try:
            result = self.db_session.query(User).filter(
                User.role_id != admin.role_id).order_by(User.created_at).all()
            if result:
                return result
            else:
                return None
        except Exception:
            return None

    def create_staff_detail(self, data: dict):
        try:
            staff = User(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_number=data['phone_number'],
                gender=data['gender'],
                role_id=self.db_session.get_role_id_by_name(data['role_id'])
            )
            self.db_session.add(staff)
            self.db_session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def update_staff_detail(self, id: int, data: dict):
        try:
            data["role_id"] = self.db_session.get_role_id_by_name(
                data["role_id"])
            self.db_session.query(User).filter(
                User.id == id).update(data)
            self.db_session.commit()
            return True
        except Exception:
            return False

    def delete_staff_detail(self, id: int):
        try:
            self.db_session.query(User).filter(
                User.id == id).delete(synchronize_session=False)
            self.db_session.commit()
            return True
        except Exception:
            return False

    def get_category(self) -> List[Category]:
        try:
            return self.db_session.query(Category).all()
        except Exception as e:
            raise Exception(e)

    def check_category_exist_byName(self, name: str):
        try:
            return self.db_session.query(Category).filter(
                Category.name == name).first()
        except Exception:
            return False

    def get_menu_by_category(self, category: int = 1) -> List[Dict]:
        try:
            records = self.db_session.query(Menu, Product, Category).join(Product, Menu.product_id == Product.id).join(
                Category, Category.id == Product.category_id).filter(Product.category_id == category).all()
            if records:
                kq = []
                for row in records:
                    kq.append(dict(row))
                return kq

        except Exception as e:
            raise Exception(e)

    def get_ALlproduct_with_category(self, *args):
        try:
            if args:
                return self.db_session.query(Product, Category).join(
                    Category).filter(and_(
                        Product.category_id == Category.id,
                        Product.category_id == args[0].id
                    )).all()
            else:
                return self.db_session.query(Product, Category).join(
                    Category).filter(Product.category_id == Category.id).all()
        except Exception:
            return None

    def delete_product(self, p: Product):
        try:
            self.db_session.query(Product).filter(
                Product.id == p.id).delete()
            self.db_session.commit()
            return True
        except Exception:
            return False

    def check_product_exist_byName(self, name: str):
        try:
            return self.db_session.query(Product).filter(
                Product.name == name).first()
        except Exception:
            return None

    def get_categoryID_byName(self, name: str):
        try:
            result = self.db_session.query(Category.id).filter(
                Category.name == name).first()
            if result:
                return result[0]
            else:
                return None
        except Exception:
            return None

    def get_products(self):
        try:
            return self.db_session.query(
                Product).all()
        except Exception:
            return None

    def delete_category(self, c: Category):
        try:
            self.db_session.query(Category).filter(
                Category.id == c.id).delete()
            self.db_session.commit()
        except Exception:
            return False

    def delete_product_byCategory_Id(self, c_id: int):
        try:
            self.db_session.query(Product).filter(
                Product.category_id == c_id).delete()
            self.db_session.commit()
            return True
        except Exception:
            return False

    def update_product_with_newCategory(self, old_id: int, new_id: int):
        try:
            self.db_session.query(Product).filter(
                Product.category_id == old_id).update({"category_id": new_id})
            self.db_session.commit()
            return True
        except Exception:
            return False

    def update_product_categoryID(self, p: Product, id: int):
        try:
            self.db_session.query(Product).filter(
                Product.id == p.id).update({"category_id": id})
            self.db_session.commit()
            return True
        except Exception:
            return False

    def add_newCategory(self, name: str):
        try:
            c = Category(name=name)
            self.db_session.add(c)
            self.db_session.commit()
            return c
        except Exception:
            return None

    def add_new_category(self, name: str):
        try:
            c = Category(name=name)
            self.db_session.add(c)
            self.db_session.commit()
            return c.id
        except Exception:
            return None

    def add_new_product(self, p: Product):
        try:
            self.db_session.add(p)
            self.db_session.commit()
            return True
        except Exception:
            return False

    def check_product_exist_in_menu(self, product: Product):
        try:
            result = self.db_session.query(Menu).filter(
                Menu.product_id == product.id
            ).first()
            if result is not None:
                return True
            else:
                return False
        except Exception:
            return False

    def check_product_exist_in_store(self, product: Store):
        try:
            result = self.db_session.query(Store).filter(
                Store.product_id == product.id
            ).first()
            if result is not None:
                return True
            else:
                return False
        except Exception:
            return False

    def add_item_to_menu(self, m: Menu):
        try:
            self.db_session.add(m)
            self.db_session.commit()
            return True
        except Exception:
            return False

    def add_item_to_store(self, m: Store):
        try:
            self.db_session.add(m)
            self.db_session.commit()
            return True
        except Exception:
            return False

    def get_product_by_category(self, category: Category):
        try:
            return self.db_session.query(Product).filter(
                Product.category_id == category.id
            ).all()
        except Exception:
            return None

    def get_productId_by_productName(self, productName: str) -> int:
        try:
            result = self.db_session.query(Product.id).filter(
                Product.name == productName
            ).first()
            return result[0]
        except Exception as e:
            raise Exception(e)

    def get_menu_width_category(self, category: Category):
        try:
            records = self.db_session.query(Menu, Product, Category).filter(and_(
                Menu.product_id == Product.id,
                Product.category_id == Category.id,
                Category.id == category.id
            )).order_by(Product.name).all()
            return records
        except Exception:
            return None

    def get_store_width_category(self, category: Category):
        try:
            records = self.db_session.query(Store, Product, Category).filter(and_(
                Store.product_id == Product.id,
                Product.category_id == Category.id,
                Category.id == category.id
            )).order_by(Product.name).all()
            return records
        except Exception:
            return None

    def update_menu_item(self, menu: Menu):
        try:
            self.db_session.query(Menu).filter(
                Menu.id == menu.id
            ).update({
                "sell_price": menu.sell_price
            })
            self.db_session.commit()
            return True
        except Exception:
            return False

    def update_store_item(self, store: Store):
        try:
            self.db_session.query(Store).filter(
                Store.id == store.id
            ).update({
                "input_price": store.input_price,
                "quantity": store.quantity
            })
            self.db_session.commit()
            return True
        except Exception:
            return False

    def delete_store_content(self, store: Store):
        try:
            self.db_session.query(Store).filter(
                Store.id == store.id).delete()
            self.db_session.commit()
            return True
        except Exception:
            return False

    def delete_menu_content(self, menu: Menu):
        try:
            self.db_session.query(Menu).filter(
                Menu.id == menu.id).delete()
            self.db_session.commit()
            return True
        except Exception:
            return False

    def get_quantity_in_store(self, id: int) -> int:
        try:
            result = self.db_session.query(Store.quantity).filter(
                Store.product_id == id).first()
            return result[0]
        except Exception as e:
            print(e)

    def add_bills_to_db(self, bills: List[Bill]):
        try:
            self.db_session.add_all(bills)
            self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def add_bill_detail_to_db(self, bill: Bill):
        try:
            self.db_session.add(bill)
            self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def update_store_quantity_whenPay(self, bills: List[Bill]):
        try:
            for bill in bills:
                product_id = self.db_session.get_productId_by_productName(
                    bill.product)
                store_quantity = self.db_session.get_quantity_in_store(
                    product_id)
                self.db_session.query(Store).filter(
                    Store.product_id == product_id).update({"quantity": store_quantity - bill.quantity})
                self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def get_orders_by_cashier(self, cashier: User) -> List[Dict]:
        try:
            records = self.db_session.query(Order).filter(
                Order.cashier_id == cashier.id).all()
            if records:
                print(records)
                kq = []
                for row in records:
                    kq.append(dict(row))
                return kq
        except Exception as e:
            print(e)
            return None

    def get_orders_orderBy_code(self) -> List[Dict]:
        try:
            codes = self.db_session.query(Order.code).distinct().all()
            if codes:
                result = []
                for code in codes:
                    order = {}
                    order["list_items"] = []
                    cart = self.db_session.query(Order).filter(
                        Order.code == code[0]).all()
                    total_money = 0
                    for od in cart:
                        total_money += od.price*od.quantity
                        item = {
                            "name": od.product,
                            "quantity": od.quantity,
                            "price": od.price,
                            "image": "assets/images/product/" + od.product + ".png"
                        }
                        order["list_items"].append(item)
                    order["descriptions"] = str(round(
                        (total_money + total_money*0.05), 2))
                    order["price"] = len(cart)
                    order["name"] = code[0]
                    order["image"] = "assets/images/order.png"
                    order["_isOrder"] = True
                    result.append(order)
                return result
            else:
                return None
        except Exception:
            return None

    def get_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        try:
            return self.db_session.query(Order).order_by(
                Order.code).offset(skip).limit(limit).all()
        except Exception as e:
            raise Exception(e)
            return None

    def add_orders_to_db(self, orders: List[Order]):
        try:
            self.db_session.add_all(orders)
            self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def add_order_detail_to_db(self, order: Order):
        try:
            self.db_session.add(order)
            self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def update_order_detail_by_id(self, id: int, order: Order):
        try:
            self.db_session.query(Order).filter(
                Order.order_id == id).update(vars(order))
            self.db_session.commit()
            return self.db_session.query(Order).filter(Order.id == id).first()
        except Exception as e:
            raise Exception(e)

    def delete_order_detail_by_code(self, code: str):
        '''
        Delete an Order by code
        '''
        try:
            self.db_session.query(Order).filter(
                Order.code == code).delete(synchronize_session=False)
            self.db_session.commit()
            # del_query = Order.__table__.delete().where(Order.code == code)
            # self.db_session.execute(del_query)
            # self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def delete_order_detail_by_id(self, id: int):
        '''
        Delete an Order by id
        '''
        try:
            existing_order = self.db_session.get(Order, id)
            if existing_order is None:
                LOGGER.warning("Order not exists in database !")
                return
            else:
                self.db_session.delete(existing_order)
                self.db_session.commit()
                LOGGER.success(f"Deleted Order : {existing_order}")
        except Exception as e:
            raise Exception(e)

    def get_user_by_email(self, email: str) -> User:
        try:
            return self.db_session.query(User).filter(
                User.email == email).first()
        except Exception as e:
            return None

    def create_account(self, user: User) -> User:
        '''
        Create an User
        '''
        try:
            existing_user = self.db_session.query(User).filter(
                User.email == user.email).first()
            if existing_user is None:
                self.db_session.add(user)  # Add the user
                self.db_session.commit()  # Commit the change
                LOGGER.success(f"Created user: {user}")
            else:
                LOGGER.warning(
                    f"Users already exists in database: {existing_user}")
            return self.db_session.query(User).filter(User.email == user.email).first()
        except IntegrityError as e:
            LOGGER.error(e.orig)
            raise e.orig
        except SQLAlchemyError as e:
            LOGGER.error(f"Unexpected error when creating user: {e}")
            raise e

    def create_account_role(self, act: AccountType) -> AccountType:
        '''
        Create an AccountType
        '''
        try:
            existing_user_act = self.db_session.query(AccountType).filter(
                AccountType.role == act.role).first()
            if existing_user_act is None:
                self.db_session.add(act)  # Add the user
                self.db_session.commit()  # Commit the change
                LOGGER.success(f"Created AccountType: {act.role}")
            else:
                LOGGER.warning(
                    f"AccountType already exists in database: {existing_user_act}")
            return self.db_session.query(AccountType).filter(AccountType.role == act.role).first()
        except IntegrityError as e:
            LOGGER.error(e.orig)
            raise e.orig
        except SQLAlchemyError as e:
            LOGGER.error(f"Unexpected error when creating user: {e}")
            raise e
