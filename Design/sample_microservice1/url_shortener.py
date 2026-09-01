from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()
dict_urls = {}
id = 0

class UrlShortenRequest(BaseModel):
    long_url: str

@app.post("/shorten")
async def shorten_url(request: UrlShortenRequest):
    global id
    short_code = str(id)
    id += 1

    shortened_url = f"http://short.url/{short_code}"
    dict_urls[short_code] = request.long_url
    return {"shortened_url": shortened_url}

@app.get("/longurl/{short_code}")
async def get_long_url(short_code: str):
    long_url = dict_urls.get(short_code)
    if long_url is None:
        raise HTTPException(
            status_code = 404,
            detail = "Short code not found"
        )

    return RedirectResponse(
        url = long_url,
        status_code = 307
    )

@app.post("/longurl/{short_code}")
async def post_long_url(short_code: str):
    long_url = dict_urls.get(short_code)
    if long_url is None:
        raise HTTPException(
            status_code = 404,
            detail = "Short code not found"
        )

    return RedirectResponse(
        url = long_url,
        status_code = 307
    )

# global is required when you are trying to modify a global variable inside a function. 
# In this case, we are modifying the global variable id, so we need to declare it as global inside the shorten_url function.