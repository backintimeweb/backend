from fastapi import FastAPI, Path, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional, Union
import sentry_sdk

from app.models import Post
from app.helpers import to_shutdown, to_start, add_new_post_to_db, find_all_posts_from_db, find_post_by_year,delete_post_by_year, update_post_by_year
from app.schemas import PostIn, PostOut

app = FastAPI()

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

origins = [
    os.getenv("ALLOW_HOST")
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup():
    await to_start()

@app.on_event("shutdown")
async def shutdown():
    await to_shutdown()

@app.post('/api/posts', response_model=PostIn)
async def add_new_post(post: PostIn, token: str = Depends(oauth2_scheme)) -> Post:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        new_post = await add_new_post_to_db(post.dict())
        return new_post
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=str(exc))

@app.get('/api/posts', response_model=List[PostOut])
async def get_all_posts() -> List[Post]:
    all_posts_info = await find_all_posts_from_db()
    return all_posts_info

@app.put('/api/posts/{year}', response_model=PostIn)
async def update_post(year: int, post: PostIn, token: str = Depends(oauth2_scheme)) -> Optional[Union[Post,None]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        updated_post = await update_post_by_year(year, post.dict())
        return updated_post
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=str(exc))

@app.delete('/api/posts/{year}', response_model=PostOut)
async def delete_post(year: int = Path(..., title="Year of the Post"), token: str = Depends(oauth2_scheme)) -> Post:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return await delete_post_by_year(year)
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=str(exc))

@app.get('/api/posts/{year}', response_model=PostOut)
async def get_post(year: int = Path(..., title="Year of the Post")) -> Optional[Union[Post, None]]:
    res = await find_post_by_year(year)
    return res
