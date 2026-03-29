import logging
from typing import List
from langchain_core.tools import StructuredTool

from storage.question_storage import QuestionStorage
from models.tool_input import QuestionAndAnswerToolInput, QuestionSubjectEnum


class GetQuestionAnswerBaseTool:
    def __init__(self, question_storage: QuestionStorage):
        self.logger = logging.getLogger(__name__)
        self.question_storage = question_storage

    def _execute(
        self,
        subject: QuestionSubjectEnum,
        question: str,
    ) -> List[dict]:
        self.logger.info(
            f"Executing tool get_question_answer_base: subject={subject}, question={question}"
        )

        questions = self.question_storage.search_similar_questions(question)

        return questions

    def get_tool(self):
        return StructuredTool.from_function(
            func=self._execute,
            name="get_question_answer_base",
            description="Returns a list of Q&A that are similar to the input question if the subject is one of the following: Tarantino.",
            args_schema=QuestionAndAnswerToolInput,
        )
