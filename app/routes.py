import os
from typing import Any, List, Optional, Union, Dict

import sentry_sdk
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Path,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.helpers import (
    add_new_post_to_db,
    delete_post_by_year,
    find_all_posts_from_db,
    find_post_by_year,
    to_shutdown,
    to_start,
    update_post_by_year,
)
from app.models import Post
from app.schemas import PostIn, PostOut, PostOutByYear

app = FastAPI()
static = os.path.dirname(os.path.abspath(__file__)).replace("/app", "/static")
templates = Jinja2Templates(directory=static)

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

SECRET_KEY: Any = os.getenv("SECRET_KEY")
ALGORITHM: Any = os.getenv("ALGORITHM")

origins = [os.getenv("ALLOW_HOST")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
async def startup():
    await to_start()


@app.on_event("shutdown")
async def shutdown():
    await to_shutdown()

@app.post("/api/posts", response_model=PostIn)
async def add_new_post(
    post: PostIn, token: Union[str, bytes] = Depends(oauth2_scheme)
) -> Post:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return await add_new_post_to_db(post.dict())
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=str(exc))

@app.get("/api/posts", response_model=List[PostOutByYear])
async def get_all_posts() -> List[Dict[str,Any]]:
    return await find_all_posts_from_db()


@app.put("/api/posts/{year}", response_model=PostIn)
async def update_post(
    year: int, post: PostIn, token: str = Depends(oauth2_scheme)
) -> Optional[Union[Post, None]]:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return await update_post_by_year(year, post.dict())
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=str(exc))


@app.delete("/api/posts/{year}", response_model=PostOut)
async def delete_post(
    year: int = Path(..., title="Year of the Post"), token: str = Depends(oauth2_scheme)
) -> Optional[Union[Post, None]]:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return await delete_post_by_year(year)
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=str(exc))


@app.get("/api/posts/{year}", response_model=PostOut)
async def get_post(
    year: int = Path(..., title="Year of the Post")
) -> Optional[Union[Post, None]]:
    return await find_post_by_year(year)

@app.get("/api/posts/html/{year}", response_class=HTMLResponse)
async def get_post_html(
    request: Request,
    year: int = Path(..., title="Year of the Post")
) -> HTMLResponse:
    return templates.TemplateResponse(f"{year}.html", {"request": request})