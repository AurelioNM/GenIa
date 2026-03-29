import logging
from typing import List
import pandas as pd

from storage.question_storage import QuestionStorage
from models.question_and_answer import QuestionAndAnswer


class FileService:
    def __init__(
        self,
        question_storage: QuestionStorage,
    ):
        self.logger = logging.getLogger(__name__)
        self.question_storage = question_storage

    def embed_file(self, file_path: str):
        self.logger.info(f"Embedding file: path={file_path}")

        df = pd.read_csv(file_path)

        entities: List[QuestionAndAnswer] = []

        for _, row in df.iterrows():
            entities.append(
                QuestionAndAnswer(
                    subject=row["subject"],
                    question=row["question"],
                    answer=row["answer"],
                )
            )

        self.question_storage.create_question_and_answer(entities)
