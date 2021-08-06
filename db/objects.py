from typing import Tuple
import model


def create_Category_objects() -> Tuple[model.Category, model.Category, model.Category]:
    '''
    Category objects
    '''
    cf = model.Category(category_name='Coffee')
    fd = model.Category(category_name='Food')
    dk = model.Category(category_name='Drink')
    return cf, fd, dk


def create_AccountType_objects() -> Tuple[model.AccountType, model.AccountType]:
    '''
    AccountType objects
    '''
    cashier = model.AccountType(role="Cashier")
    admin = model.AccountType(role="Administrator")
    return cashier, admin


def create_User_objects() -> Tuple[model.User, model.User, model.User]:
    '''
    User objects
    '''
    cs_test = model.User(
        first_name='Cashier',
        last_name='Test',
        email='c',
        password='c',
        phone_number='0908678333',
        gender='Female',
        role='Cashier'
    )
    user_cs = model.User(
        first_name='Fisrt Name',
        last_name='Cashier',
        email='first@cashier.com',
        password='c',
        phone_number='0908678339',
        gender='Female',
        role='Cashier'
    )
    user_ad = model.User(
        first_name='Fisrt Name',
        last_name='Admin',
        email='a',
        password='a',
        phone_number='0908678786',
        gender='Male',
        role='Administrator'
    )
    return cs_test, user_cs, user_ad
