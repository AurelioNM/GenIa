from datetime import date
import logging
from typing import Dict, List
from psycopg import DatabaseError
from psycopg_pool import AsyncConnectionPool


class CityStorage:
    def __init__(self, db_connection: AsyncConnectionPool):
        self.logger = logging.getLogger(__name__)
        self.db = db_connection

    async def get_all_cities_names(self) -> List[str]:
        try:
            self.logger.info(f"Geting all cities names on DB")
            async with self.db.connection() as conn:
                async with conn.cursor() as cursor:
                    sql_query = """
                        SELECT c.name
                        FROM cities c;
                    """

                    await cursor.execute(sql_query)
                    rows = await cursor.fetchall()

                    self.logger.info(f"Get all cities names on DB: result={rows}")

                    city_names: List[str] = []

                    for row in rows:
                        city_name = row[0]
                        city_names.append(city_name)

                    self.logger.info(f"Mapped cities names in list: {city_names}")

                    return city_names
        except DatabaseError as ex:
            self.logger.error(f"Failed get all cities names in DB. DatabaseError: {ex}")
            raise
