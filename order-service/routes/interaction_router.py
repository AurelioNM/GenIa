import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.interaction import InteractionOutput, InteractionRequest
from services.interaction_service import InteractionService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_interaction_service(request: Request):
    return request.state.interaction_service


ServiceDep = Annotated[InteractionService, Depends(get_interaction_service)]


@router.post(
    "/v1/chat/interaction",
    status_code=status.HTTP_200_OK,
    response_model=InteractionOutput,
)
def get_interaction(interaction_request: InteractionRequest, service: ServiceDep):
    try:
        logger.info(f"Started request getInteractionV1: body={interaction_request }")
        response: InteractionOutput = service.get_chat_interaction(interaction_request)

        logger.info(
            f"Finished request getInteractionV1: response={response.model_dump()}"
        )
        return response
    except ValueError as ex:
        logger.error(f"Failed request getInteractionV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )
