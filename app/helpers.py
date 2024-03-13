from .database import engine, session, Base

async def to_start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def to_shutdown():
    await session.close()
    await engine.dispose()