from pydantic import BaseModel
from typing import List

class ValidationErrorDetail(BaseModel):
    field: str
    message: str

class ValidationErrorResponse(BaseModel):
    status_code: int
    message: str
    errors: List[ValidationErrorDetail]
