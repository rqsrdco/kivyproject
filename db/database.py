from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
# Global Variables
DEBUG = True
SQLITE = 'sqlite'
DB = 'db/database.db'
# MYSQL                   = 'mysql'
# POSTGRESQL              = 'postgresql'
# MICROSOFT_SQL_SERVER    = 'mssqlserver'


class MyDatabase:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        # MYSQL: 'mysql://scott:tiger@localhost/{DB}',
        # POSTGRESQL: 'postgresql://scott:tiger@localhost/{DB}',
        # MICROSOFT_SQL_SERVER: 'mssql+pymssql://scott:tiger@hostname:port/{DB}'
    }
    # Main DB Connection Ref Obj
    db_engine = None
    db_session = None

    def __init__(self, dbtype=SQLITE, username='', password='', dbname=DB):
        dbtype = dbtype.lower()
        engine_url = ''
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
        else:
            engine_url = self.DB_ENGINE[SQLITE].format(DB=DB)

        self.db_engine = create_engine(
            engine_url, encoding='utf-8', echo=DEBUG)
        # print(self.db_engine)
        session = sessionmaker(bind=self.db_engine)
        self.db_session = session()

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '':
            return
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        # print(query)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)  # print(row[0], row[1], row[2])
                result.close()
        print("\n")
