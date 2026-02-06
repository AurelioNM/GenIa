from datetime import date
import logging
from typing import Dict, List
from psycopg2 import DatabaseError
from psycopg2._psycopg import connection


class CityStorage:
    def __init__(self, db_connection: connection):
        self.logger = logging.getLogger(__name__)
        self.db = db_connection

    def get_all_cities_names(self) -> List[str]:
        try:
            with self.db.cursor() as cursor:
                sql_query = """
                    SELECT c.name
                    FROM cities c;
                """

                cursor.execute(sql_query)
                rows = cursor.fetchall()

                self.logger.debug(f"Get all cities names result: {rows}")

                city_names: List[str] = []

                for row in rows:
                    city_name = row[0]
                    city_names.append(city_name)

                self.logger.debug(f"Mapped cities names in list: {city_names}")

                return city_names
        except DatabaseError as ex:
            self.logger.error(f"Failed get all cities names in DB. DatabaseError: {ex}")
            raise
