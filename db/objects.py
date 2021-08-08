from typing import Tuple
import model


def create_Product_objects():
    return [model.Product(
            name="Coffee %s" % p if p % 2 == 0 else "Food %s" % p if p % 3 == 0 else "Drink %s" % p,
            image=model.Product.convertToBinaryData(
                'assets/images/coffee.png') if p % 2 == 0 else model.Product.convertToBinaryData(
                'assets/images/food.png') if p % 3 == 0 else model.Product.convertToBinaryData(
                'assets/images/drink.png'),
            category_id=1 if p % 2 == 0 else 2 % p if p % 3 == 0 else 3
            ) for p in range(39)]


def create_Category_objects() -> Tuple[model.Category, model.Category, model.Category]:
    '''
    Category objects
    '''
    cf = model.Category(name='Coffee')
    fd = model.Category(name='Food')
    dk = model.Category(name='Drink')
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
        role_id=1
    )
    user_cs = model.User(
        first_name='Fisrt Name',
        last_name='Cashier',
        email='first@cashier.com',
        password='c',
        phone_number='0908678339',
        gender='Female',
        role_id=1
    )
    user_ad = model.User(
        first_name='Fisrt Name',
        last_name='Admin',
        email='a',
        password='a',
        phone_number='0908678786',
        gender='Male',
        role_id=2
    )
    return cs_test, user_cs, user_ad
