from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import random
from typing import List, Dict
from logger import LOGGER
import config
import model
import objects


class MyDatabase:
    DB_ENGINE = {
        'sqlite': 'sqlite:///{DB}',
        #MYSQL: 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
    }
    # CORE
    db_engine = None
    # ORM
    db_session = None

    def __init__(self):
        self.db_engine = create_engine(
            config.ENGINE_URL, encoding='utf-8', echo=config.DEBUG)
        # create DATABASE TABLES
        model.Base.metadata.create_all(self.db_engine)
        session = sessionmaker(bind=self.db_engine)
        self.db_session = session()

        # self.init_product_categories()
        # self.init_products()
        # self.init_account_roles()
        # self.init_accounts()
        # self.init_menu()
        # self.init_store()

    def init_product_categories(self):
        self.db_session.add_all(objects.create_Category_objects())
        self.db_session.commit()

    def init_products(self):
        self.db_session.add_all(objects.create_Product_objects())
        self.db_session.commit()

    def init_account_roles(self):
        self.db_session.add_all(objects.create_AccountType_objects())
        self.db_session.commit()

    def init_accounts(self):
        self.db_session.add_all(objects.create_User_objects())
        self.db_session.commit()

    def init_menu(self):
        products = self.get_products()
        menu = [model.Menu(
            sell_price=round(random.uniform(19000.99, 39999.99), 2),
            product_id=p.id
        ) for p in products]
        self.db_session.add_all(menu)
        self.db_session.commit()

    def init_store(self):
        products = self.get_products()
        store = [model.Store(
            product_id=p.id,
            input_price=round(random.uniform(18000.99, 29999.99), 2),
            quantity=random.randint(79, 333)
        ) for p in products]
        self.db_session.add_all(store)
        self.db_session.commit()

    def get_category(self) -> List[model.Category]:
        try:
            return self.db_session.query(model.Category).all()
        except Exception as e:
            raise Exception(e)

    def get_menu_by_category(self, category: int = 1) -> List[Dict]:
        try:
            records = self.db_session.query(model.Menu, model.Product, model.Category).join(model.Product, model.Menu.product_id == model.Product.id).join(
                model.Category, model.Category.id == model.Product.category_id).filter(model.Product.category_id == category).all()
            if records:
                kq = []
                for row in records:
                    kq.append(dict(row))
                return kq

        except Exception as e:
            raise Exception(e)

    def get_products(self):
        try:
            return self.db_session.query(
                model.Product).all()
        except Exception:
            return None

    def get_productId_by_productName(self, productName: str) -> int:
        try:
            result = self.db_session.query(model.Product.id).filter(
                model.Product.name == productName
            ).first()
            return result[0]
        except Exception as e:
            raise Exception(e)

    def get_quantity_in_store(self, id: int) -> int:
        try:
            result = self.db_session.query(model.Store.quantity).filter(
                model.Store.product_id == id).first()
            return result[0]
        except Exception as e:
            print(e)

    def add_bills_to_db(self, bills: List[model.Bill]):
        try:
            self.db_session.add_all(bills)
            self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def add_bill_detail_to_db(self, bill: model.Bill):
        try:
            self.db_session.add(bill)
            self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def update_store_quantity_whenPay(self, bills: List[model.Bill]):
        try:
            for bill in bills:
                product_id = self.get_productId_by_productName(bill.product)
                store_quantity = self.get_quantity_in_store(product_id)
                self.db_session.query(model.Store).filter(
                    model.Store.product_id == product_id).update({"quantity": store_quantity - bill.quantity})
                self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def get_orders_by_cashier(self, cashier: model.User) -> List[Dict]:
        try:
            records = self.db_session.query(model.Order).filter(
                model.Order.cashier_id == cashier.id).all()
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
            codes = self.db_session.query(model.Order.code).distinct().all()
            if codes:
                result = []
                for code in codes:
                    order = {}
                    order["list_items"] = []
                    cart = self.db_session.query(model.Order).filter(
                        model.Order.code == code[0]).all()
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

    def get_orders(self, skip: int = 0, limit: int = 100) -> List[model.Order]:
        try:
            return self.db_session.query(model.Order).order_by(
                model.Order.code).offset(skip).limit(limit).all()
        except Exception as e:
            raise Exception(e)
            return None

    def add_orders_to_db(self, orders: List[model.Order]):
        try:
            self.db_session.add_all(orders)
            self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def add_order_detail_to_db(self, order: model.Order):
        try:
            self.db_session.add(order)
            self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def update_order_detail_by_id(self, id: int, order: model.Order):
        try:
            self.db_session.query(model.Order).filter(
                model.Order.order_id == id).update(vars(order))
            self.db_session.commit()
            return self.db_session.query(model.Order).filter(model.Order.id == id).first()
        except Exception as e:
            raise Exception(e)

    def delete_order_detail_by_code(self, code: str):
        '''
        Delete an Order by code
        '''
        try:
            self.db_session.query(model.Order).filter(
                model.Order.code == code).delete(synchronize_session=False)
            self.db_session.commit()
            #del_query = model.Order.__table__.delete().where(model.Order.code == code)
            # self.db_session.execute(del_query)
            # self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def delete_order_detail_by_id(self, id: int):
        '''
        Delete an Order by id
        '''
        try:
            existing_order = self.db_session.get(model.Order, id)
            if existing_order is None:
                LOGGER.warning("Order not exists in database !")
                return
            else:
                self.db_session.delete(existing_order)
                self.db_session.commit()
                LOGGER.success(f"Deleted Order : {existing_order}")
        except Exception as e:
            raise Exception(e)

    def get_user_by_email(self, email: str) -> model.User:
        try:
            return self.db_session.query(model.User).filter(
                model.User.email == email).first()
        except Exception as e:
            return None

    def create_account(self, user: model.User) -> model.User:
        '''
        Create an User
        '''
        try:
            existing_user = self.db_session.query(model.User).filter(
                model.User.email == user.email).first()
            if existing_user is None:
                self.db_session.add(user)  # Add the user
                self.db_session.commit()  # Commit the change
                LOGGER.success(f"Created user: {user}")
            else:
                LOGGER.warning(
                    f"Users already exists in database: {existing_user}")
            return self.db_session.query(model.User).filter(model.User.email == user.email).first()
        except IntegrityError as e:
            LOGGER.error(e.orig)
            raise e.orig
        except SQLAlchemyError as e:
            LOGGER.error(f"Unexpected error when creating user: {e}")
            raise e

    def create_account_role(self, act: model.AccountType) -> model.AccountType:
        '''
        Create an AccountType
        '''
        try:
            existing_user_act = self.db_session.query(model.AccountType).filter(
                model.AccountType.role == act.role).first()
            if existing_user_act is None:
                self.db_session.add(act)  # Add the user
                self.db_session.commit()  # Commit the change
                LOGGER.success(f"Created AccountType: {act.role}")
            else:
                LOGGER.warning(
                    f"AccountType already exists in database: {existing_user_act}")
            return self.db_session.query(model.AccountType).filter(model.AccountType.role == act.role).first()
        except IntegrityError as e:
            LOGGER.error(e.orig)
            raise e.orig
        except SQLAlchemyError as e:
            LOGGER.error(f"Unexpected error when creating user: {e}")
            raise e
