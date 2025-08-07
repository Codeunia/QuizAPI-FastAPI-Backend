from pydantic import BaseModel, Field
from typing import List
from .question import Question

class Quiz(BaseModel): # Represents a quiz
    title: str
    description: str
    questions: List[Question] = []