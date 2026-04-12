import os
import logging


class SQSClient:
    def __init__(self, client):
        self.logger = logging.getLogger(__name__)
        self.client = client

    async def get_queue_url(self):
        response = await self.client.get_queue_url(QueueName=os.getenv("QUEUE_NAME"))
        return response["QueueUrl"]

    async def send_message(self, message: str):
        self.logger.info(f"Sending menssage to queue: message={message}")
        queue_url = await self.get_queue_url()

        await self.client.send_message(
            QueueUrl=queue_url,
            MessageBody=message,
        )

    async def receive_messages(self):
        queue_url = await self.get_queue_url()

        response = await self.client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1,
        )

        return response.get("Messages", [])

    async def delete_message(self, receipt_handle: str):
        queue_url = await self.get_queue_url()

        await self.client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle,
        )
