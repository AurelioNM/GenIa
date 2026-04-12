import logging
import random
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from clients.dto.open_weather_forecast_dto import OpenWeatherForecastResponse
from models.weather import CityWeather, PagedCityWeather, PagedCityWeatherV2
from services.weather_service import WeatherService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_weather_service(request: Request):
    return request.state.weather_service


ServiceDep = Annotated[WeatherService, Depends(get_weather_service)]


@router.get("/v1/weathers/cities/{city_name}", response_model=CityWeather)
async def get_weather_by_city_name(city_name: str, service: ServiceDep):
    try:
        logger.info(f"Started request getWeatherByCityName: city_name={city_name}")
        weather: CityWeather = await service.get_weather_by_city_name(city_name)

        logger.info(f"Finished request getWeatherByCityName: response={weather}")
        return weather
    except ValueError as ex:
        logger.error(f"Failed request getWeatherByCityName. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {ex}"
        )


@router.get("/v1/weathers/cities", response_model=PagedCityWeather)
async def get_paged_cities_weather(
    page: int,
    size: int,
    service: ServiceDep,
):
    try:
        logger.info(f"Started request getPagedCitiesWeather: page={page} size={size}")

        result: PagedCityWeather = await service.get_cities_weather(page, size)

        logger.info(
            f"Finished request getPagedCitiesWeather: "
            f"cities_count={len(result.cities_weather)} "
            f"has_next_page={result.has_next_page}"
        )

        return result

    except ValueError as ex:
        logger.error(f"Failed request getPagedCitiesWeather. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error: {ex}",
        )


@router.get("/v2/weathers/cities", response_model=PagedCityWeatherV2)
async def get_paged_cities_weather(
    page: int,
    size: int,
    service: ServiceDep,
):
    try:
        correlation = random.randint(1, 50)

        logger.info(
            f"Started request getPagedCitiesWeatherV2: page={page} size={size}, correlation={correlation}"
        )

        result: PagedCityWeatherV2 = await service.get_cities_weather_v2(
            page, size, correlation
        )

        logger.info(
            f"Finished request getPagedCitiesWeatherV2: correlation={correlation}, "
            f"cities_count={len(result.cities_weather)}, "
            f"has_next_page={result.has_next_page}"
        )

        return result

    except ValueError as ex:
        logger.error(f"Failed request getPagedCitiesWeatherV2. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error: {ex}",
        )


@router.post("/v1/run-job")
async def run_job(service: ServiceDep):
    try:
        logger.info("Started request runJob")

        await service.run_job()

        logger.info("Finished request runJob")

    except ValueError as ex:
        logger.error(f"Failed request runJob. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {ex}",
        )
