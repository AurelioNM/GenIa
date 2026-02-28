import logging
import pandas as pd
import os

from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status
from services.file_service import FileService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_file_service(request: Request):
    return request.state.file_service


ServiceDep = Annotated[FileService, Depends(get_file_service)]


@router.post(
    "/v1/files/create",
    status_code=status.HTTP_201_CREATED,
)
def create_file():
    try:
        logger.info("Started request createFileV1")

        data = [
            {
                "subject": "TARANTINO",
                "question": "Which films were directed by Quentin Tarantino?",
                "answer": "Some films directed by Quentin Tarantino include Pulp Fiction, Kill Bill Vol. 1, Kill Bill Vol. 2, Django Unchained, Inglourious Basterds, and Once Upon a Time in Hollywood.",
            },
            {
                "subject": "TARANTINO",
                "question": "Which Tarantino film won an Oscar?",
                "answer": "Django Unchained and Pulp Fiction won Oscars. Tarantino won for Best Original Screenplay.",
            },
            {
                "subject": "TARANTINO",
                "question": "What is Tarantino's characteristic style?",
                "answer": "Tarantino is known for long and striking dialogues, stylized violence, non-linear storytelling, and impactful soundtracks.",
            },
            {
                "subject": "TARANTINO",
                "question": "In what year was Pulp Fiction released?",
                "answer": "Pulp Fiction was released in 1994.",
            },
            {
                "subject": "TARANTINO",
                "question": "Who stars in Kill Bill?",
                "answer": "Uma Thurman is the protagonist of Kill Bill.",
            },
        ]

        file_path = os.getenv("TARANTINO_Q&A_FILE_PATH")

        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)

        logger.info(f"Finished request createFileV1: path={file_path}")

    except ValueError as ex:
        logger.error(f"Failed request createFileV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )


@router.post(
    "/v1/files/embeddings",
    status_code=status.HTTP_201_CREATED,
)
def embed_file(service: ServiceDep):
    try:
        logger.info(f"Started request embedFileV1")

        file_path = os.getenv("TARANTINO_Q&A_FILE_PATH")
        service.embed_file(file_path)

        logger.info(f"Finished request embedFileV1")
    except ValueError as ex:
        logger.error(f"Failed request embedFileV1. Error: {ex}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {ex}"
        )
