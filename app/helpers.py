from typing import Dict, List, Optional, Union

import nh3
from sqlalchemy import update
from sqlalchemy.future import select

from .database import Base, engine, session
from .models import Post


async def to_start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def to_shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def add_new_post_to_db(post: Dict) -> Post:
    post["desc"] = nh3.clean(post["desc"])
    new_post = Post(**post)

    session.add(new_post)

    return new_post


async def find_all_posts_from_db() -> List[Post]:
    result = await session.scalars(select(Post))
    return [res for res in result]


async def delete_post_by_year(year: int) -> Optional[Union[Post, None]]:
    res = await session.scalars(select(Post).where(Post.year == int(year)))
    first_res: Optional[Post] = res.first()

    if first_res:
        await session.delete(first_res)
        return first_res

    return None


async def update_post_by_year(year, post: Dict) -> Optional[Union[Post, None]]:
    post["desc"] = nh3.clean(post["desc"])
    stmt = update(Post).where(Post.year == int(year)).values(post).returning(Post)
    res = await session.execute(stmt)
    await session.commit()

    return Post(**post) if res else None


async def find_post_by_year(year: int) -> Optional[Union[Post, None]]:
    res = await session.scalars(select(Post).where(Post.year == int(year)))
    first_res: Optional[Post] = res.first()

    if first_res:
        return first_res
    return None
