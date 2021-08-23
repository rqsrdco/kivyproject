from sqlalchemy import and_, or_, asc, desc, text, between
from sqlalchemy.sql import select, alias, func
from sqlalchemy.sql.expression import update

import objects
import queries
from database import MyDatabase


def main():
    dbms = MyDatabase()
    engine = dbms.db_engine
    session = dbms.db_session

    # CORE
    #menus = queries.fetch_menu_listings(engine)
    #kq = queries.update_order_listing(engine, 2, 3)
    # CREATE AccountType
    # dbms.init_store()
    records = dbms.get_roles()  # get_menu_by_category(3)
    for row in records:
        print(row)
    print(records)
    # for row in records:
    #photoPath = config.PRODUCT_PHOTO_PATH + row.name + ".png"
    #model.Product.writeTofile(row.image, photoPath)
    # print(row)

    #cst = orm.create_account_type(session, cs)
    #adt = orm.create_account_type(session, ad)
    # CREATE User
    #cs_test, user_cs, user_ad = objects.create_User_objects()
    #cs_1 = orm.create_account(session, cs_test)
    #cs_2 = orm.create_account(session, user_cs)
    #ad = orm.create_account(session, user_ad)


if __name__ == "__main__":
    main()
