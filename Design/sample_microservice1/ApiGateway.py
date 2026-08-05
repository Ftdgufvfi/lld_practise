import httpx
from fastapi import FastAPI, Header
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str

app = FastAPI()

@app.get('/api/users/all')
async def list_users():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8004/users/all')
        return response.json()

@app.get('/api/orders/all')
async def list_orders():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8005/orders/all')
        return response.json()

@app.post("/api/users")
async def create_user(user: User,
    idempotency_key: str = Header(alias="Idempotency-Key", default=None)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8004/users",
            json=user.model_dump(),
            headers={"Idempotency-Key": idempotency_key} if idempotency_key else None
        )
        return response.json()
