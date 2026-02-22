import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.suggestion import ProductReviewOutput, SuggestionInput, SuggestionOutput
from services.suggestion_service import SuggestionService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_suggestion_service(request: Request):
    return request.state.suggestion_service


ServiceDep = Annotated[SuggestionService, Depends(get_suggestion_service)]


@router.post(
    "/v1/studies/llm-interaction",
    status_code=status.HTTP_200_OK,
    response_model=SuggestionOutput,
)
def get_suggestion(suggestion: SuggestionInput, service: ServiceDep):
    try:
        logger.info(f"Started request getSuggestionV1: body={suggestion.model_dump()}")

        suggestion_output: SuggestionOutput = service.get_suggestion1(suggestion)

        logger.info(f"Finished request getSuggestionV1: response={suggestion_output}")
        return suggestion_output
    except ValueError as ex:
        logger.error(f"Failed request getSuggestionV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )


@router.post(
    "/v2/studies/llm-interaction",
    status_code=status.HTTP_200_OK,
    response_model=SuggestionOutput,
)
def get_suggestion(service: ServiceDep):
    try:
        logger.info(f"Started request getSuggestionV2")
        suggestion_output: SuggestionOutput = service.get_suggestion2()

        logger.info(f"Finished request getSuggestionV2: response={suggestion_output}")
        return suggestion_output
    except ValueError as ex:
        logger.error(f"Failed request getSuggestionV2. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )


@router.post(
    "/v3/studies/llm-interaction",
    status_code=status.HTTP_200_OK,
    response_model=ProductReviewOutput,
)
def get_suggestion(service: ServiceDep):
    try:
        logger.info(f"Started request getSuggestionV3")
        output: ProductReviewOutput = service.get_suggestion3()

        logger.info(f"Finished request getSuggestionV3: response={output.model_dump()}")
        return output
    except ValueError as ex:
        logger.error(f"Failed request getSuggestionV3. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )


@router.post(
    "/v4/studies/llm-interaction",
    status_code=status.HTTP_200_OK,
    response_model=SuggestionOutput,
)
def get_suggestion(suggestion: SuggestionInput, service: ServiceDep):
    try:
        logger.info(f"Started request getSuggestionV4: body={suggestion.model_dump()}")
        output: SuggestionOutput = service.get_suggestion4(suggestion)

        logger.info(f"Finished request getSuggestionV4: response={output.model_dump()}")
        return output
    except ValueError as ex:
        logger.error(f"Failed request getSuggestionV4. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )
