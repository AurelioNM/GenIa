import asyncio
import json
import logging

from services.weather_service import WeatherService
from models.payload import ProcessCityPayload
from queues.sqs_client import SQSClient


class SQSListener:
    def __init__(self, sqs_client: SQSClient, service: WeatherService):
        self.logger = logging.getLogger(__name__)
        self.sqs_client = sqs_client
        self._running = True
        self.service = service

    async def process_message(self, message: dict):
        body = json.loads(message["Body"])
        payload = ProcessCityPayload(**body)

        self.logger.info(f"Processing city: {payload.name}")
        await self.service.handle_city_process(payload.name)

    async def _poll(self):
        while self._running:
            try:
                messages = await self.sqs_client.receive_messages()

                if not messages:
                    continue

                for msg in messages:
                    try:
                        await self.process_message(msg)

                        await self.sqs_client.delete_message(msg["ReceiptHandle"])

                    except Exception as e:
                        self.logger.error(f"Error processing message: {e}")

            except Exception as e:
                self.logger.error(f"Error polling SQS: {e}")

    async def start(self):
        self.logger.info("Starting SQS listener...")
        await self._poll()

    async def stop(self):
        self.logger.info("Stopping SQS listener...")
        self._running = False
