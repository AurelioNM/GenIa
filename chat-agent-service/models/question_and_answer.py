from datetime import datetime
from pydantic import BaseModel, Field


class QuestionAndAnswer(BaseModel):
    subject: str
    question: str
    answer: str
