from fastapi import FastAPI, Path
from typing import List, Optional, Union

from app.models import Post
from app.helpers import to_shutdown, to_start, add_new_post_to_db, find_all_posts_from_db, find_post_by_year,delete_post_by_year, update_post_by_year
from app.schemas import PostIn, PostOut

app = FastAPI()

@app.on_event("startup")
async def startup():
    await to_start()

@app.on_event("shutdown")
async def shutdown():
    await to_shutdown()

@app.post('/api/posts', response_model=PostIn)
async def add_new_post(post: PostIn) -> Post:
    new_post = await add_new_post_to_db(post.dict())

    return new_post

# @app.put('/api/posts', response_model=PostIn)
# async def update_post(post: PostIn) -> Post:
#     return await update_post_by_year(post.dict())

@app.get('/api/posts', response_model=List[PostOut])
async def get_all_posts() -> List[Post]:
    all_posts_info = await find_all_posts_from_db()
    return all_posts_info

@app.delete('/api/posts/{year}', response_model=PostOut)
async def delete_post(year: int = Path(..., title="Year of the Post")) -> Post:
    return await delete_post_by_year(year)

@app.get('/api/posts/{year}', response_model=PostOut)
async def get_post(year: int = Path(..., title="Year of the Post")) -> Optional[Union[Post, None]]:
    res = await find_post_by_year(year)
    return res