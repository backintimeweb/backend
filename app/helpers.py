from typing import Dict, List, Optional, Union
from sqlalchemy.future import select
from sqlalchemy import update

from .database import engine, session, Base
from .models import Post

async def to_start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def to_shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await session.close()
    await engine.dispose()


async def add_new_post_to_db(post: Dict) -> Post:
    new_post = Post(**post)

    session.add(new_post)

    return new_post

async def find_all_posts_from_db()-> List[Post]:
    result = await session.scalars(select(Post))
    return [res for res in result]

async def delete_post_by_year(year: int) -> Optional[Union[Post, None]]:
    res = await session.scalars(select(Post).where(Post.year == int(year)))
    first_res: Optional[Post] = res.first()

    if first_res:
        await session.delete(first_res)
        return first_res

    return None

async def update_post_by_year(post: Dict) -> Optional[Union[Post, None]]:
    stmt = (
        update(Post).
        where(Post.year == int(post['year'])).
        values(post).
        returning(Post)
    )
    result = await session.execute(stmt)
    await session.commit()

    return result.first()

async def find_post_by_year(year: int) -> Optional[Union[Post, None]]:
    res = await session.scalars(select(Post).where(Post.year == int(year)))
    first_res: Optional[Post] = res.first()

    if first_res:
        return first_res
    return None