class ProductNotFoundException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"Product with id {product_id} not found"
        self.status_code = 404

class InvalidProductDataException(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        self.message = f"Invalid product data: {detail}"
        self.status_code = 422