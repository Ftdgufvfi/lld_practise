# FastAPI microservice example

This project contains three independent FastAPI applications:

- **Users service** (`8001`) owns user data.
- **Orders service** (`8002`) owns order data and calls the users service before creating an order.
- **API gateway** (`8000`) exposes the public `/api/users` and `/api/orders` routes.

The services use in-memory storage for clarity, so data resets when a service restarts.

## Run with Docker

```powershell
docker compose up --build
```

Open the gateway documentation at <http://localhost:8000/docs>. The individual service documentation is available on ports `8001` and `8002`.

## Run locally

Create a virtual environment and install the dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start each command in a separate terminal from this directory:

```powershell
uvicorn users_service.main:app --port 8001
uvicorn orders_service.main:app --port 8002
uvicorn api_gateway.main:app --port 8000
```

## Try the API

```powershell
$user = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/users `
  -ContentType application/json `
  -Body '{"name":"Ada","email":"ada@example.com"}'

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/orders `
  -ContentType application/json `
  -Body "{`"user_id`":$($user.id),`"product`":`"Keyboard`",`"quantity`":1,`"unit_price`":49.99}"
```

List orders with cursor pagination:

```powershell
$page = Invoke-RestMethod 'http://localhost:8000/api/orders?limit=2'
$nextPage = Invoke-RestMethod "http://localhost:8000/api/orders?limit=2&after=$($page.next_cursor)"
```

Each response has this shape:

```json
{
  "data": [],
  "next_cursor": null
}
```

Pass `next_cursor` as `after` to continue. A `null` cursor means there are no more results. The optional `user_id` filter must be repeated on every page.

Run tests with:

```powershell
pytest
```