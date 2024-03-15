from typing import Dict, List
from sqlalchemy.future import select

from .database import engine, session, Base
from .models import Post

async def to_start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def to_shutdown():
    await session.close()
    await engine.dispose()


async def add_new_post_to_db(post: Dict) -> Post:
    new_post = Post(**post)

    session.add(new_post)

    return new_post

async def find_all_posts_from_db()-> List[Post]:
    result = await session.scalars(select(Post))
    return [res for res in result]

