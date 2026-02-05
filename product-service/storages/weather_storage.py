from datetime import date
import logging
from typing import Dict, List
from psycopg2 import DatabaseError
from psycopg2._psycopg import connection

from models.weather import (
    CityWeather,
    PagedCityWeather,
    PagedCityWeatherV2,
    Weather,
    WeatherType,
    WeatherV2,
)


class WeatherStorage:
    def __init__(self, db_connection: connection):
        self.logger = logging.getLogger(__name__)
        self.db = db_connection

    def get_weather_by_city_name(self, city_name: str) -> Weather:
        try:
            with self.db.cursor() as cursor:
                sql_query = """
                    SELECT
                        c.id            AS city_id,
                        c.name          AS city_name,
                        w.id            AS weather_id,
                        w.day,
                        w.description,
                        w.temp,
                        w.temp_min,
                        w.temp_max,
                        w.feels_like,
                        w.humidity,
                        w.wind_speed
                    FROM cities c
                    JOIN weather_records w
                    ON w.city_name = c.name
                    WHERE c.name = %s
                    AND w.day BETWEEN
                            CURRENT_DATE - INTERVAL '7 day'
                        AND CURRENT_DATE + INTERVAL '7 day'
                    ORDER BY
                        w.day ASC;
                """

                cursor.execute(sql_query, (city_name,))
                result = cursor.fetchall()

                return self.map_weather_rows_to_model(result)
        except DatabaseError as ex:
            self.logger.error(
                f"Failed to search weather by city_name={city_name} in DB. DatabaseError: {ex}"
            )
            raise

    def map_weather_rows_to_model(self, rows) -> CityWeather:
        first_row = rows[0]

        city_id = first_row[0]
        city_name = first_row[1]

        weather_list: List[Weather] = []

        for row in rows:
            weather = Weather(
                day=row[3],
                type=self._resolve_weather_type(row[3]),
                description=row[4],
                temp=row[5],
                temp_min=row[6],
                temp_max=row[7],
                feels_like=row[8],
                humidity=row[9],
                wind_speed=row[10],
            )

            weather_list.append(weather)

        return CityWeather(
            city_id=city_id,
            city_name=city_name,
            weathers=weather_list,
        )

    def get_paged_cities_weather(
        self,
        page: int,
        size: int,
    ) -> PagedCityWeather:

        limit = size
        offset = (page - 1) * size

        try:
            with self.db.cursor() as cursor:

                sql = """
                    SELECT
                        c.id            AS city_id,
                        c.name          AS city_name,
                        w.id            AS weather_id,
                        w.day,
                        w.description,
                        w.temp,
                        w.temp_min,
                        w.temp_max,
                        w.feels_like,
                        w.humidity,
                        w.wind_speed
                    FROM cities c
                    JOIN weather_records w
                      ON w.city_name = c.name
                    WHERE w.day BETWEEN
                          CURRENT_DATE - INTERVAL '7 day'
                      AND CURRENT_DATE + INTERVAL '7 day'
                    ORDER BY
                        w.day ASC
                    LIMIT %s
                    OFFSET %s;
                """

                cursor.execute(sql, (limit + 1, offset))
                rows = cursor.fetchall()

                if not rows:
                    return PagedCityWeather(
                        page=page,
                        size=size,
                        has_next_page=False,
                        cities_weather=[],
                    )

                cities_weather = self._map_rows_to_city_weather(rows[:size])

                has_next_page = len(rows) > size

                return PagedCityWeather(
                    page=page,
                    size=size,
                    has_next_page=has_next_page,
                    cities_weather=cities_weather,
                )

        except DatabaseError as ex:
            self.logger.error(
                "Failed to fetch paged cities weather. page=%s size=%s error=%s",
                page,
                size,
                ex,
            )
            raise

    def get_paged_cities_weather_v2(
        self,
        page: int,
        size: int,
    ) -> PagedCityWeatherV2:

        limit = size
        offset = (page - 1) * size

        try:
            with self.db.cursor() as cursor:

                sql = """
                    SELECT
                        c.id            AS city_id,
                        c.name          AS city_name,
                        w.id            AS weather_id,
                        w.day,
                        w.description,
                        w.temp,
                        w.temp_min,
                        w.temp_max,
                        w.feels_like,
                        w.humidity,
                        w.wind_speed
                    FROM cities c
                    JOIN weather_records w
                      ON w.city_name = c.name
                    WHERE w.day = CURRENT_DATE
                    ORDER BY
                        w.day ASC
                    LIMIT %s
                    OFFSET %s;
                """

                cursor.execute(sql, (limit + 1, offset))
                rows = cursor.fetchall()

                if not rows:
                    return PagedCityWeatherV2(
                        page=page,
                        size=size,
                        has_next_page=False,
                        cities_weather=[],
                    )

                cities_weather = self._map_rows_to_city_weather_v2(rows[:size])

                has_next_page = len(rows) > size

                return PagedCityWeatherV2(
                    page=page,
                    size=size,
                    has_next_page=has_next_page,
                    cities_weather=cities_weather,
                )

        except DatabaseError as ex:
            self.logger.error(
                "Failed to fetch paged cities weather. page=%s size=%s error=%s",
                page,
                size,
                ex,
            )
            raise

    def _map_rows_to_city_weather(
        self,
        rows: List[tuple],
    ) -> List[CityWeather]:

        cities: Dict[str, CityWeather] = {}

        for row in rows:
            city_id = row[0]
            city_name = row[1]

            if city_id not in cities:
                cities[city_id] = CityWeather(
                    city_id=city_id,
                    city_name=city_name,
                    weather=[],
                )

            weather = Weather(
                day=row[3],
                type=self._resolve_weather_type(row[3]),
                description=row[4],
                temp=row[5],
                temp_min=row[6],
                temp_max=row[7],
                feels_like=row[8],
                humidity=row[9],
                wind_speed=row[10],
            )

            cities[city_id].weather.append(weather)

        return list(cities.values())

    def _map_rows_to_city_weather_v2(
        self,
        rows: List[tuple],
    ) -> List[WeatherV2]:

        result: List[WeatherV2] = []

        for row in rows:
            weather = WeatherV2(
                city_id=row[0],
                city_name=row[1],
                day=row[3],
                type=self._resolve_weather_type(row[3]),
                description=row[4],
                temp=row[5],
                temp_min=row[6],
                temp_max=row[7],
                feels_like=row[8],
                humidity=row[9],
                wind_speed=row[10],
            )

            result.append(weather)

        return result

    def _resolve_weather_type(self, weather_day: date) -> WeatherType:
        today = date.today()

        if weather_day < today:
            return WeatherType.PAST
        elif weather_day == today:
            return WeatherType.TODAY
        return WeatherType.FUTURE
