import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.chat_interaction import (
    ProductReviewOutput,
    ChatInteractionInput,
    ChatInteractionOutput,
)
from services.chat_interaction_service import ChatInteractionService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_chat_interaction_service(request: Request):
    return request.state.chat_interaction_service


ServiceDep = Annotated[ChatInteractionService, Depends(get_chat_interaction_service)]


@router.post(
    "/v1/studies/chat-interaction",
    status_code=status.HTTP_200_OK,
    response_model=ChatInteractionOutput,
)
def get_chat_interaction(chat_interaction: ChatInteractionInput, service: ServiceDep):
    try:
        logger.info(
            f"Started request getChatInteractionV1: body={chat_interaction.model_dump()}"
        )

        chat_interaction_output: ChatInteractionOutput = service.get_chat_interaction1(
            chat_interaction
        )

        logger.info(
            f"Finished request getChatInteractionV1: response={chat_interaction_output}"
        )
        return chat_interaction_output
    except ValueError as ex:
        logger.error(f"Failed request getChatInteractionV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )


@router.post(
    "/v2/studies/chat-interaction",
    status_code=status.HTTP_200_OK,
    response_model=ChatInteractionOutput,
)
def get_chat_interaction(service: ServiceDep):
    try:
        logger.info(f"Started request getChatInteractionV2")
        chat_interaction_output: ChatInteractionOutput = service.get_chat_interaction2()

        logger.info(
            f"Finished request getChatInteractionV2: response={chat_interaction_output}"
        )
        return chat_interaction_output
    except ValueError as ex:
        logger.error(f"Failed request getChatInteractionV2. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )


@router.post(
    "/v3/studies/chat-interaction",
    status_code=status.HTTP_200_OK,
    response_model=ProductReviewOutput,
)
def get_chat_interaction(service: ServiceDep):
    try:
        logger.info(f"Started request getChatInteractionV3")
        output: ProductReviewOutput = service.get_chat_interaction3()

        logger.info(
            f"Finished request getChatInteractionV3: response={output.model_dump()}"
        )
        return output
    except ValueError as ex:
        logger.error(f"Failed request getChatInteractionV3. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )


@router.post(
    "/v4/studies/chat-interaction",
    status_code=status.HTTP_200_OK,
    response_model=ChatInteractionOutput,
)
def get_chat_interaction(chat_interaction: ChatInteractionInput, service: ServiceDep):
    try:
        logger.info(
            f"Started request getChatInteractionV4: body={chat_interaction.model_dump()}"
        )
        output: ChatInteractionOutput = service.get_chat_interaction4(chat_interaction)

        logger.info(
            f"Finished request getChatInteractionV4: response={output.model_dump()}"
        )
        return output
    except ValueError as ex:
        logger.error(f"Failed request getChatInteractionV4. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )
