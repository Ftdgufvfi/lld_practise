import os

import httpx
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, Response


USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://localhost:8001")
ORDERS_SERVICE_URL = os.getenv("ORDERS_SERVICE_URL", "http://localhost:8002")

app = FastAPI(title="Sample API Gateway", version="1.0.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy", "service": "api-gateway"}


async def forward_request(
    request: Request,
    service_url: str,
    path: str,
    client_state_name: str,
) -> Response:
    injected_client: httpx.AsyncClient | None = getattr(
        request.app.state, client_state_name, None
    )
    request_kwargs = {
        "method": request.method,
        "url": path,
        "params": request.query_params,
        "content": await request.body(),
        "headers": {"content-type": request.headers.get("content-type", "")},
    }

    try:
        if injected_client is not None:
            upstream = await injected_client.request(**request_kwargs)
        else:
            async with httpx.AsyncClient(base_url=service_url) as client:
                upstream = await client.request(**request_kwargs)
    except httpx.RequestError:
        return JSONResponse(
            status_code=502,
            content={"detail": f"{client_state_name.removesuffix('_client')} unavailable"},
        )

    headers = {}
    if content_type := upstream.headers.get("content-type"):
        headers["content-type"] = content_type
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=headers,
    )


@app.get("/api/users")
async def list_users(request: Request) -> Response:
    return await forward_request(request, USERS_SERVICE_URL, "/users", "users_client")


@app.post("/api/users")
async def create_user(request: Request) -> Response:
    return await forward_request(request, USERS_SERVICE_URL, "/users", "users_client")


@app.api_route("/api/users/{user_id}", methods=["GET"])
async def user_detail(user_id: int, request: Request) -> Response:
    return await forward_request(
        request, USERS_SERVICE_URL, f"/users/{user_id}", "users_client"
    )


@app.get("/api/orders")
async def list_orders(
    request: Request,
    user_id: int | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    after: int | None = Query(default=None, ge=0),
) -> Response:
    return await forward_request(request, ORDERS_SERVICE_URL, "/orders", "orders_client")


@app.post("/api/orders")
async def create_order(request: Request) -> Response:
    return await forward_request(request, ORDERS_SERVICE_URL, "/orders", "orders_client")


@app.api_route("/api/orders/{order_id}", methods=["GET"])
async def order_detail(order_id: int, request: Request) -> Response:
    return await forward_request(
        request, ORDERS_SERVICE_URL, f"/orders/{order_id}", "orders_client"
    )