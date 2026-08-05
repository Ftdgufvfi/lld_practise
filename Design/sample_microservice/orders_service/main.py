import os
from decimal import Decimal

import httpx
from fastapi import FastAPI, HTTPException, Query, Request, status
from pydantic import BaseModel, Field


USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://localhost:8001")


class OrderCreate(BaseModel):
    user_id: int
    product: str
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0, decimal_places=2)


class Order(OrderCreate):
    id: int
    status: str


class OrderPage(BaseModel):
    data: list[Order]
    next_cursor: int | None


app = FastAPI(title="Orders Service", version="1.0.0")

orders: dict[int, Order] = {
    1: Order(
        id=1,
        user_id=1,
        product="Mechanical Keyboard",
        quantity=1,
        unit_price=Decimal("89.99"),
        status="created",
    ),
    2: Order(
        id=2,
        user_id=2,
        product="USB-C Dock",
        quantity=1,
        unit_price=Decimal("129.50"),
        status="shipped",
    ),
    3: Order(
        id=3,
        user_id=1,
        product="Laptop Stand",
        quantity=2,
        unit_price=Decimal("34.95"),
        status="delivered",
    ),
}
next_order_id = 4


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy", "service": "orders"}


async def ensure_user_exists(request: Request, user_id: int) -> None:
    injected_client: httpx.AsyncClient | None = getattr(
        request.app.state, "users_client", None
    )
    try:
        if injected_client is not None:
            response = await injected_client.get(f"/users/{user_id}")
        else:
            async with httpx.AsyncClient(base_url=USERS_SERVICE_URL) as client:
                response = await client.get(f"/users/{user_id}")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail="Users service unavailable") from exc

    if response.status_code == 404:
        raise HTTPException(status_code=400, detail="User does not exist")
    if response.is_error:
        raise HTTPException(status_code=502, detail="Users service returned an error")


@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, request: Request) -> Order:
    global next_order_id

    await ensure_user_exists(request, order_data.user_id)
    order = Order(
        id=next_order_id,
        status="created",
        **order_data.model_dump(),
    )
    orders[order.id] = order
    next_order_id += 1
    return order


@app.get("/orders", response_model=OrderPage)
async def list_orders(
    user_id: int | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    after: int | None = Query(default=None, ge=0),
) -> OrderPage:
    matching_orders = sorted(
        (
            order
            for order in orders.values()
            if (user_id is None or order.user_id == user_id)
            and (after is None or order.id > after)
        ),
        key=lambda order: order.id,
    )
    page_with_extra = matching_orders[: limit + 1]
    page = page_with_extra[:limit]
    next_cursor = page[-1].id if len(page_with_extra) > limit else None
    return OrderPage(data=page, next_cursor=next_cursor)


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int) -> Order:
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order