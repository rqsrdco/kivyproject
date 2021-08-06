
class SQLRawCommand:

    create_table_user = """
        CREATE TABLE IF NOT EXISTS Users (
            id integer PRIMARY KEY,
            first_name text,
            last_name text,
            gender text,
            email text,
            phone_number text,
            password text,
            account_type text,
            datetime_created datetime
            );
    """
    create_table_report = """
        CREATE TABLE IF NOT EXISTS Reports (
            id integer PRIMARY KEY,
            datetime_created datetime,
            bill_code text,
            money real
            );
    """
    create_table_store = """
        CREATE TABLE IF NOT EXISTS Store (
            id integer PRIMARY KEY,
            code text,
            name text,
            import_amount integer,
            unit text,
            price_import real
            category text,
            description text,
            datetime_imported datetime,
            datetime_expiry datetime
            );
    """
    create_table_menu = """
        CREATE TABLE Menus (
        	code text PRIMARY KEY,
         	category text,
         	name text NOT NULL,
        	price_sell real,
         	quantity integer,
         	is_enable integer,
            FOREIGN KEY (category) REFERENCES Types (name)
        );
    """
    create_table_bill = """
        CREATE TABLE IF NOT EXISTS Bills (
            id integer PRIMARY KEY,
            code text,
            item text,
            quantity integer,
            price real,
            user text,
            datetime_sell datetime
            );
    """
    create_table_order = """
        CREATE TABLE IF NOT EXISTS Orders (
            id integer PRIMARY KEY,
            order_code text,
            order_item text,
            order_quantity integer,
            item_price real,
            cashier text,
            datetime_order datetime
            );
    """
