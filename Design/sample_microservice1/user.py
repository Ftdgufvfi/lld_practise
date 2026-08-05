from fastapi import FastAPI, Header
from pydantic import BaseModel
import asyncio

idempotency_lock = asyncio.Lock()

hash = {}


class UserCreate(BaseModel):
    name: str
    email: str

app = FastAPI()

users = [
    {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
    {"id": 3, "name": "Alice Johnson", "email": "alice.johnson@example.com"}
]


@app.get("/health")
async def health() -> str:
    return "healthy"

@app.get('/users/all')
async def list_users():
    return users


@app.post('/users', status_code=201)
async def create_user(user: UserCreate,
    idempotency_key: str = Header(alias="Idempotency-Key", default=None)):

    async with idempotency_lock:
        if(idempotency_key and idempotency_key in hash):
            if hash[idempotency_key] is not None:
                return hash[idempotency_key]
            else:
                from fastapi import HTTPException
                raise HTTPException(status_code=409, detail="Conflict: Duplicate request with the same Idempotency-Key")
        elif idempotency_key:
            hash[idempotency_key] = None


    created_user = {"id": len(users) + 1, **user.model_dump()}
    users.append(created_user)
    if idempotency_key:
        hash[idempotency_key] = created_user
    return created_user


























