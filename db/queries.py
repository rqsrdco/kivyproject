from typing import List, Optional

from sqlalchemy import text, Integer
from sqlalchemy.engine.base import Engine

from logger import LOGGER


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
