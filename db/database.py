from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from logger import LOGGER
import config
import model
import objects


class MyDatabase:
    # CORE
    db_engine = None
    # ORM
    db_session = None

    def __init__(self):
        self.db_engine = create_engine(
            config.ENGINE_URL, encoding='utf-8', echo=config.DEBUG)
        session = sessionmaker(bind=self.db_engine)
        self.db_session = session()
        # create DATABASE TABLES
        model.Base.metadata.create_all(self.db_engine)

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

    def get_products(self):
        try:
            return self.db_session.query(
                model.Product).all()
        except Exception as e:
            raise Exception(e)

    def get_orders_by_cashier(self, cashier: model.User):
        try:
            return self.db_session.query(model.Order).filter(
                model.Order.cashier_id == cashier.id).all()
        except Exception as e:
            raise Exception(e)

    def get_orders(self, skip: int = 0, limit: int = 100):
        try:
            return self.db_session.query(model.Order).offset(skip).limit(limit).all()
        except Exception as e:
            raise Exception(e)

    def add_order_detail_to_db(self, order: model.Order):
        try:
            self.db_session.add(order)
            self.db_session.commit()
        except Exception as e:
            raise Exception(e)

    def update_order_detail(self, id: int, order: model.Order):
        try:
            self.db_session.query(model.Order).filter(
                model.Order.order_id == id).update(vars(order))
            self.db_session.commit()
            return self.db_session.query(model.Order).filter(model.Order.id == id).first()
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
        user = (
            self.db_session.query(model.User).filter(
                model.User.email == email).first()
        )
        return user

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
