from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class OrderPage(BaseModel):
    data: list[dict]
    next_cursor: int | None

orders = [
        {"id": 1, "user_id": 1, "product": "Mechanical Keyboard", "quantity": 1, "unit_price": 89.99, "status": "created"},
        {"id": 2, "user_id": 2, "product": "USB-C Dock", "quantity": 1, "unit_price": 129.50, "status": "shipped"},
        {"id": 3, "user_id": 1, "product": "Laptop Stand", "quantity": 2, "unit_price": 34.95, "status": "delivered"}
]

# cursor-based pagination.
# sending back the cursor or pointer to next row for the results so, this fastens
# the data retrieval and reduces the response size
@app.get('/orders/all', response_model=OrderPage)
async def list_orders(
    limit: int = Query(default=2, ge=1, le = 100),
    after: int | None = Query(default=None, ge=0),
):
    start = 0 if after is None else after
    end = start + limit
    data = orders[start:end]
    next_cursor = end if end < len(orders) else None
    return OrderPage(data=data, next_cursor=next_cursor)
