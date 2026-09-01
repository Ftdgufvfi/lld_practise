import httpx
from fastapi import Body, FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from ratelimitor import RateLimitor

class User(BaseModel):
    name: str
    email: str

app = FastAPI()
app.add_middleware(RateLimitor)

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

@app.post("/graphql/hobbies")
async def hobbies_graphql(request_body: dict = Body()):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8007/graphql",
                json=request_body
            )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Hobbies service unavailable")

    return JSONResponse(
        content=response.json(),
        status_code=response.status_code
    )

@app.post("/api/urls")
async def shorten_url(request_body: dict = Body()):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8008/urls", json=request_body)
    content = response.json()
    if response.is_success:
        content["short_url"] = f"http://localhost:8006/s/{content['short_code']}"
    return JSONResponse(content=content, status_code=response.status_code)

@app.get("/s/{short_code}")
async def redirect_short_url(short_code: str):
    async with httpx.AsyncClient(follow_redirects=False) as client:
        response = await client.get(f"http://localhost:8008/{short_code}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(response.headers["location"], status_code=307)
