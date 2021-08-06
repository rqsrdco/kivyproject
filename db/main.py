from sqlalchemy import and_, or_, asc, desc, text, between
from sqlalchemy.sql import select, alias, func
from sqlalchemy.sql.expression import update

import objects
import queries
import orm
from database import MyDatabase


def main():
    dbms = MyDatabase()
    engine = dbms.db_engine
    session = dbms.db_session

    # CORE
    #menus = queries.fetch_menu_listings(engine)
    #kq = queries.update_order_listing(engine, 2, 3)
    # CREATE AccountType
    #cs, ad = objects.create_AccountType_objects()

    #cst = orm.create_account_type(session, cs)
    #adt = orm.create_account_type(session, ad)
    # CREATE User
    #cs1, cs2, admin = objects.create_User_objects()

    #cs_1 = orm.create_account(session, cs1)
    #cs_2 = orm.create_account(session, cs2)
    #ad = orm.create_account(session, admin)


if __name__ == "__main__":
    main()
