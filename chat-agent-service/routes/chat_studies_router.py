import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.chat_studies import (
    ProductReviewOutput,
    ChatStudiesInput,
    ChatStudiesOutput,
)
from services.chat_studies_service import ChatStudiesService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_chat_studies_service(request: Request):
    return request.state.chat_studies_service


ServiceDep = Annotated[ChatStudiesService, Depends(get_chat_studies_service)]


@router.post(
    "/v1/chat/studies",
    status_code=status.HTTP_200_OK,
    response_model=ChatStudiesOutput,
)
def get_chat_studies(chat_studies: ChatStudiesInput, service: ServiceDep):
    try:
        logger.info(
            f"Started request getChatStudiesV1: body={chat_studies.model_dump()}"
        )

        chat_studies_output: ChatStudiesOutput = service.get_chat_studies1(chat_studies)

        logger.info(
            f"Finished request getChatStudiesV1: response={chat_studies_output}"
        )
        return chat_studies_output
    except ValueError as ex:
        logger.error(f"Failed request getChatStudiesV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )


@router.post(
    "/v2/chat/studies",
    status_code=status.HTTP_200_OK,
    response_model=ChatStudiesOutput,
)
def get_chat_studies(service: ServiceDep):
    try:
        logger.info(f"Started request getChatStudiesV2")
        chat_studies_output: ChatStudiesOutput = service.get_chat_studies2()

        logger.info(
            f"Finished request getChatStudiesV2: response={chat_studies_output}"
        )
        return chat_studies_output
    except ValueError as ex:
        logger.error(f"Failed request getChatStudiesV2. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )


@router.post(
    "/v3/chat/studies",
    status_code=status.HTTP_200_OK,
    response_model=ProductReviewOutput,
)
def get_chat_studies(service: ServiceDep):
    try:
        logger.info(f"Started request getChatStudiesV3")
        output: ProductReviewOutput = service.get_chat_studies3()

        logger.info(
            f"Finished request getChatStudiesV3: response={output.model_dump()}"
        )
        return output
    except ValueError as ex:
        logger.error(f"Failed request getChatStudiesV3. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )


@router.post(
    "/v4/chat/studies",
    status_code=status.HTTP_200_OK,
    response_model=ChatStudiesOutput,
)
def get_chat_studies(chat_studies: ChatStudiesInput, service: ServiceDep):
    try:
        logger.info(
            f"Started request getChatStudiesV4: body={chat_studies.model_dump()}"
        )
        output: ChatStudiesOutput = service.get_chat_studies4(chat_studies)

        logger.info(
            f"Finished request getChatStudiesV4: response={output.model_dump()}"
        )
        return output
    except ValueError as ex:
        logger.error(f"Failed request getChatStudiesV4. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )
