import httpx
import pytest

from api_gateway.main import app as gateway_app
from orders_service.main import app as orders_app
from users_service.main import app as users_app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_services_include_seed_data() -> None:
    async with (
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=users_app),
            base_url="http://users-service",
        ) as users_client,
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=orders_app),
            base_url="http://orders-service",
        ) as orders_client,
    ):
        users_response = await users_client.get("/users")
        orders_response = await orders_client.get("/orders", params={"user_id": 1})

    seeded_users = {user["id"]: user for user in users_response.json()}
    assert seeded_users[1]["email"] == "alice@example.com"
    orders_page = orders_response.json()
    assert {order["id"] for order in orders_page["data"]} == {1, 3}
    assert orders_page["next_cursor"] is None


@pytest.mark.anyio
async def test_orders_cursor_pagination() -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=orders_app),
        base_url="http://orders-service",
    ) as orders_client:
        first_response = await orders_client.get(
            "/orders", params={"user_id": 1, "limit": 1}
        )
        first_page = first_response.json()

        second_response = await orders_client.get(
            "/orders",
            params={
                "user_id": 1,
                "limit": 1,
                "after": first_page["next_cursor"],
            },
        )
        second_page = second_response.json()

    assert [order["id"] for order in first_page["data"]] == [1]
    assert first_page["next_cursor"] == 1
    assert [order["id"] for order in second_page["data"]] == [3]
    assert second_page["next_cursor"] is None


@pytest.mark.anyio
async def test_create_user_and_order_through_gateway() -> None:
    async with (
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=users_app),
            base_url="http://users-service",
        ) as users_client,
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=orders_app),
            base_url="http://orders-service",
        ) as orders_client,
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=gateway_app),
            base_url="http://gateway",
        ) as gateway_client,
    ):
        orders_app.state.users_client = users_client
        gateway_app.state.users_client = users_client
        gateway_app.state.orders_client = orders_client

        user_response = await gateway_client.post(
            "/api/users",
            json={"name": "Ada", "email": "ada@example.com"},
        )
        assert user_response.status_code == 201
        user = user_response.json()

        order_response = await gateway_client.post(
            "/api/orders",
            json={
                "user_id": user["id"],
                "product": "Keyboard",
                "quantity": 2,
                "unit_price": "49.99",
            },
        )
        assert order_response.status_code == 201
        assert order_response.json()["user_id"] == user["id"]

        orders_response = await gateway_client.get(
            "/api/orders", params={"user_id": user["id"]}
        )
        assert orders_response.status_code == 200
        orders_page = orders_response.json()
        assert len(orders_page["data"]) == 1
        assert orders_page["next_cursor"] is None


@pytest.mark.anyio
async def test_order_rejects_unknown_user() -> None:
    async with (
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=users_app),
            base_url="http://users-service",
        ) as users_client,
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=orders_app),
            base_url="http://orders-service",
        ) as orders_client,
    ):
        orders_app.state.users_client = users_client
        response = await orders_client.post(
            "/orders",
            json={
                "user_id": 99999,
                "product": "Mouse",
                "quantity": 1,
                "unit_price": "20.00",
            },
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "User does not exist"}