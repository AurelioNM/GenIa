from pydantic import BaseModel
from typing import List, Optional


class LlmGenerateResponse(BaseModel):
    model: str
    created_at: str
    response: str
    done: bool
    done_reason: Optional[str] = None
    total_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None
