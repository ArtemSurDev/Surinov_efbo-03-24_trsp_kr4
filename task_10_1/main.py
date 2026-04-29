from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from task_10_1.exceptions import ProductNotFoundException, InvalidProductDataException
from task_10_1.error_models import ErrorResponse

app = FastAPI()

products = {
    1: {"id": 1, "title": "Product 1", "price": 100},
    2: {"id": 2, "title": "Product 2", "price": 200},
}

@app.exception_handler(ProductNotFoundException)
async def product_not_found_handler(request: Request, exc: ProductNotFoundException):
    print(f"ERROR: {exc.message}")
    error_response = ErrorResponse(
        status_code=exc.status_code,
        message=exc.message,
        detail=f"Product with id {exc.product_id} does not exist in database"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )

@app.exception_handler(InvalidProductDataException)
async def invalid_product_data_handler(request: Request, exc: InvalidProductDataException):
    print(f"ERROR: {exc.message}")
    error_response = ErrorResponse(
        status_code=exc.status_code,
        message=exc.message,
        detail=exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise ProductNotFoundException(product_id=product_id)
    return products[product_id]

@app.put("/products/{product_id}")
def update_product(product_id: int, title: str, price: int):
    if product_id not in products:
        raise ProductNotFoundException(product_id=product_id)
    if price <= 0:
        raise InvalidProductDataException(detail="Price must be greater than zero")
    if len(title) < 2:
        raise InvalidProductDataException(detail="Title must be at least 2 characters")
    products[product_id]["title"] = title
    products[product_id]["price"] = price
    return products[product_id]
