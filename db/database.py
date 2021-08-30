from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import create_engine, and_
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
            config.ENGINE_URL, encoding='utf-8', echo=False)  # config.DEBUG)
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

    def add_new_role(self, new_role: str):
        try:
            fetchRole = self.db_session.query(model.AccountType).filter(
                model.AccountType.role == new_role).first()
            if fetchRole is None:
                role = model.AccountType(role=new_role)
                result = self.db_session.add(role)
                self.db_session.commit()
                return True
            else:
                return False
        except Exception:
            return False

    def get_roles(self) -> List[model.AccountType]:
        try:
            return self.db_session.query(model.AccountType).all()
        except Exception:
            return None

    def get_role_id_by_name(self, name: str) -> int:
        try:
            result = self.db_session.query(model.AccountType).filter(
                model.AccountType.role == name
            ).first()
            if result:
                print("---------result.id----\n", result.id)
                return result.id
            else:
                return None
        except Exception:
            return None

    def get_staff(self, admin: model.User) -> List[model.User]:
        try:
            result = self.db_session.query(model.User).filter(
                model.User.role_id != admin.role_id).order_by(model.User.created_at).all()
            if result:
                return result
            else:
                return None
        except Exception:
            return None

    def create_staff_detail(self, data: dict):
        try:
            staff = model.User(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_number=data['phone_number'],
                gender=data['gender'],
                role_id=self.get_role_id_by_name(data['role_id'])
            )
            self.db_session.add(staff)
            self.db_session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def update_staff_detail(self, id: int, data: dict):
        try:
            data["role_id"] = self.get_role_id_by_name(data["role_id"])
            self.db_session.query(model.User).filter(
                model.User.id == id).update(data)
            self.db_session.commit()
            return True
        except Exception:
            return False

    def delete_staff_detail(self, id: int):
        try:
            self.db_session.query(model.User).filter(
                model.User.id == id).delete(synchronize_session=False)
            self.db_session.commit()
            return True
        except Exception:
            return False

    def get_category(self) -> List[model.Category]:
        try:
            return self.db_session.query(model.Category).all()
        except Exception as e:
            raise Exception(e)

    def check_category_exist_byName(self, name: str):
        try:
            return self.db_session.query(model.Category).filter(
                model.Category.name == name).first()
        except Exception:
            return False

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

    def get_ALlproduct_with_category(self, *args):
        try:
            if args:
                return self.db_session.query(model.Product, model.Category).join(
                    model.Category).filter(and_(
                        model.Product.category_id == model.Category.id,
                        model.Product.category_id == args[0].id
                    )).all()
            else:
                return self.db_session.query(model.Product, model.Category).join(
                    model.Category).filter(model.Product.category_id == model.Category.id).all()
        except Exception:
            return None

    def delete_product(self, p: model.Product):
        try:
            self.db_session.query(model.Product).filter(
                model.Product.id == p.id).delete()
            self.db_session.commit()
            return True
        except Exception:
            return False

    def check_product_exist_byName(self, name: str):
        try:
            return self.db_session.query(model.Product).filter(
                model.Product.name == name).first()
        except Exception:
            return None

    def get_categoryID_byName(self, name: str):
        try:
            result = self.db_session.query(model.Category.id).filter(
                model.Category.name == name).first()
            if result:
                return result[0]
            else:
                return None
        except Exception:
            return None

    def get_products(self):
        try:
            return self.db_session.query(
                model.Product).all()
        except Exception:
            return None

    def delete_category(self, c: model.Category):
        try:
            self.db_session.query(model.Category).filter(
                model.Category.id == c.id).delete()
            self.db_session.commit()
        except Exception:
            return False

    def delete_product_byCategory_Id(self, c_id: int):
        try:
            self.db_session.query(model.Product).filter(
                model.Product.category_id == c_id).delete()
            self.db_session.commit()
            return True
        except Exception:
            return False

    def update_product_with_newCategory(self, old_id: int, new_id: int):
        try:
            self.db_session.query(model.Product).filter(
                model.Product.category_id == old_id).update({"category_id": new_id})
            self.db_session.commit()
            return True
        except Exception:
            return False

    def update_product_categoryID(self, p: model.Product, id: int):
        try:
            self.db_session.query(model.Product).filter(
                model.Product.id == p.id).update({"category_id": id})
            self.db_session.commit()
            return True
        except Exception:
            return False

    def add_newCategory(self, name: str):
        try:
            c = model.Category(name=name)
            self.db_session.add(c)
            self.db_session.commit()
            return c
        except Exception:
            return None

    def add_new_category(self, name: str):
        try:
            c = model.Category(name=name)
            self.db_session.add(c)
            self.db_session.commit()
            return c.id
        except Exception:
            return None

    def add_new_product(self, p: model.Product):
        try:
            self.db_session.add(p)
            self.db_session.commit()
            return True
        except Exception:
            return False

    def check_product_exist_in_menu(self, product: model.Product):
        try:
            result = self.db_session.query(model.Menu).filter(
                model.Menu.product_id == product.id
            ).first()
            if result is not None:
                return True
            else:
                return False
        except Exception:
            return False

    def check_product_exist_in_store(self, product: model.Store):
        try:
            result = self.db_session.query(model.Store).filter(
                model.Store.product_id == product.id
            ).first()
            if result is not None:
                return True
            else:
                return False
        except Exception:
            return False

    def add_item_to_menu(self, m: model.Menu):
        try:
            self.db_session.add(m)
            self.db_session.commit()
            return True
        except Exception:
            return False

    def add_item_to_store(self, m: model.Store):
        try:
            self.db_session.add(m)
            self.db_session.commit()
            return True
        except Exception:
            return False

    def get_product_by_category(self, category: model.Category):
        try:
            return self.db_session.query(model.Product).filter(
                model.Product.category_id == category.id
            ).all()
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

    def get_menu_width_category(self, category: model.Category):
        try:
            records = self.db_session.query(model.Menu, model.Product, model.Category).filter(and_(
                model.Menu.product_id == model.Product.id,
                model.Product.category_id == model.Category.id,
                model.Category.id == category.id
            )).order_by(model.Product.name).all()
            return records
        except Exception:
            return None

    def get_store_width_category(self, category: model.Category):
        try:
            records = self.db_session.query(model.Store, model.Product, model.Category).filter(and_(
                model.Store.product_id == model.Product.id,
                model.Product.category_id == model.Category.id,
                model.Category.id == category.id
            )).order_by(model.Product.name).all()
            return records
        except Exception:
            return None

    def update_menu_item(self, menu: model.Menu):
        try:
            self.db_session.query(model.Menu).filter(
                model.Menu.id == menu.id
            ).update({
                "sell_price": menu.sell_price
            })
            self.db_session.commit()
            return True
        except Exception:
            return False

    def update_store_item(self, store: model.Store):
        try:
            self.db_session.query(model.Store).filter(
                model.Store.id == store.id
            ).update({
                "input_price": store.input_price,
                "quantity": store.quantity
            })
            self.db_session.commit()
            return True
        except Exception:
            return False

    def delete_store_content(self, store: model.Store):
        try:
            self.db_session.query(model.Store).filter(
                model.Store.id == store.id).delete()
            self.db_session.commit()
            return True
        except Exception:
            return False

    def delete_menu_content(self, menu: model.Menu):
        try:
            self.db_session.query(model.Menu).filter(
                model.Menu.id == menu.id).delete()
            self.db_session.commit()
            return True
        except Exception:
            return False

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
