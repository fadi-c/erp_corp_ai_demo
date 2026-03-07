from ninja import Schema
from typing import List
from pydantic import BaseModel, EmailStr

class QuestionRequest(Schema):
    from_user: EmailStr
    question: str


class QuestionResponse(Schema):
    answer: str
    sources: List[int]