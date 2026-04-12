import os
from dotenv import load_dotenv
from aioboto3 import Session


load_dotenv()


async def get_queue_client():
    session = Session()
    return session.client(
        "sqs",
        region_name=os.getenv("REGION"),
        endpoint_url=os.getenv("AWS_ENDPOINT"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
