from model import AccountType, User, Bill
from logger import LOGGER
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import String
import os


def get_user_by_email(session: Session, email: String) -> User:
    user = (
        session.query(User)
        .filter(User.email == email).first()
    )
    return user


def get_all_bills(session: Session, cashier: User):
    '''
    Fetch all bills belonging to an Cashier user.
    '''
    bills = (
        session.query(Bill)
        .join(User, Bill.user_sold == User.user_id)
        .filter_by(role=cashier.role)
        .all()
    )
    for bill in bills:
        bill_record = {
            "bill_id": bill.bill_id,
            "bills_code": bill.bills_code,
            "item_quantity": bill.item_quantity,
            "created_at": bill.created_at,
            "updated_at": bill.updated_at,
            "item_price": bill.item_price,
            "item_bill": bill.item_bill,
            "user_sold": bill.user_sold
        }
        LOGGER.info(bill_record)


def create_account_type(session: Session, act: AccountType) -> AccountType:
    try:
        existing_user_act = session.query(AccountType).filter(
            AccountType.role == act.role).first()
        if existing_user_act is None:
            session.add(act)  # Add the user
            session.commit()  # Commit the change
            LOGGER.success(f"Created AccountType: {act}")
        else:
            LOGGER.warning(
                f"AccountType already exists in database: {existing_user_act}")
        return session.query(AccountType).filter(AccountType.role == act.role).first()
    except IntegrityError as e:
        LOGGER.error(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        LOGGER.error(f"Unexpected error when creating user: {e}")
        raise e


def create_account(session: Session, user: User) -> User:
    try:
        existing_user = session.query(User).filter(
            User.email == user.email).first()
        if existing_user is None:
            session.add(user)  # Add the user
            session.commit()  # Commit the change
            LOGGER.success(f"Created user: {user}")
        else:
            LOGGER.warning(
                f"Users already exists in database: {existing_user}")
        return session.query(User).filter(User.email == user.email).first()
    except IntegrityError as e:
        LOGGER.error(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        LOGGER.error(f"Unexpected error when creating user: {e}")
        raise e
