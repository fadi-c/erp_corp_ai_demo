from ninja import Schema
from typing import List
from datetime import date
from pydantic import BaseModel, EmailStr


class QuestionRequest(Schema):
    #from_user: EmailStr
    question: str


class QuestionResponse(Schema):
    answer: str
    sources: List[int]




class InvoiceSchema(Schema):
    id: int
    amount: float
    margin: float
    date: date
    description: str
