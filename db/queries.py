from typing import List, Optional

from sqlalchemy import text, Integer, String
from sqlalchemy.engine.base import Engine

from logger import LOGGER


def execute_query(engine: Engine, query: String):
    if query == '':
        return
    try:
        engine.execute(query)
    except Exception as e:
        print(e)


def print_all_data(engine: Engine, table: String, query: String):
    _query = query if query != '' else "SELECT * FROM '{}';".format(table)
    try:
        result = engine.execute(_query)
    except Exception as e:
        print(e)
    else:
        for row in result:
            print(row)
        result.close()


def fetch_menu_listings(engine: Engine) -> Optional[List[dict]]:
    result = engine.execute(
        text(
            "SELECT item_name, sell_price, \
            categories_name, item_image \
            FROM menu ORDER BY RAND() LIMIT 10;"
        )
    )
    rows = [dict(row) for row in result.fetchall()]
    LOGGER.info(f"Selected {result.rowcount} rows: {rows}")
    return rows


def update_order_listing(engine: Engine, id: Integer, sl: Integer) -> Optional[List[dict]]:
    result = engine.execute(
        text(
            "UPDATE order SET item_quantity = {}, \
            WHERE order_id = {};".format(id, sl)
        )
    )
    LOGGER.info(
        f"Selected {result.rowcount} row: \
        {result}"
    )
    return result.rowcount
