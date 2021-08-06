"""Purge all data from database."""
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database import MyDatabase
from logger import LOGGER


def cleanup_data():
    session = MyDatabase().db_session
    LOGGER.info("Purging all created data...")
    try:
        session.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
        session.commit()
        session.execute(text("TRUNCATE TABLE account_type;"))
        session.commit()
        session.execute(text("TRUNCATE TABLE user;"))
        session.commit()
        session.execute(text("TRUNCATE TABLE bill;"))
        session.commit()
        session.execute(text("TRUNCATE TABLE order;"))
        session.commit()
        session.execute(text("TRUNCATE TABLE menu;"))
        session.commit()
        session.execute(text("TRUNCATE TABLE category;"))
        session.commit()
        session.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
        session.commit()
        LOGGER.success("Successfully reset all data.")
    except IntegrityError as e:
        LOGGER.error(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        LOGGER.error(f"Unexpected error when resetting data: {e}")
        raise e
