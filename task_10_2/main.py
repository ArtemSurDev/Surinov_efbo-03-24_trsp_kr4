from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .models import User
from .error_models import ValidationErrorResponse, ValidationErrorDetail

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"VALIDATION ERROR: {exc.errors()}")
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append(ValidationErrorDetail(
            field=field,
            message=error["msg"]
        ))
    error_response = ValidationErrorResponse(
        status_code=422,
        message="Request validation failed",
        errors=errors
    )
    return JSONResponse(
        status_code=422,
        content=error_response.dict()
    )

@app.post("/users")
def create_user(user: User):
    return {
        "message": "User created successfully",
        "user": user
    }
