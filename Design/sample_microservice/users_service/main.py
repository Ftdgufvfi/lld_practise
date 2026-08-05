from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class User(UserCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


app = FastAPI(title="Users Service", version="1.0.0")

users: dict[int, User] = {
    1: User(id=1, name="Alice Johnson", email="alice@example.com"),
    2: User(id=2, name="Bob Smith", email="bob@example.com"),
    3: User(id=3, name="Carol Williams", email="carol@example.com"),
}
next_user_id = 4


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy", "service": "users"}


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate) -> User:
    global next_user_id

    if any(user.email == user_data.email for user in users.values()):
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User(id=next_user_id, **user_data.model_dump())
    users[user.id] = user
    next_user_id += 1
    return user


@app.get("/users", response_model=list[User])
async def list_users() -> list[User]:
    return list(users.values())


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int) -> User:
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user