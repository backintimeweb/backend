from fastapi import FastAPI

from app.helpers import to_shutdown, to_start

app = FastAPI()

@app.on_event("startup")
async def startup():
    await to_shutdown()

@app.on_event("shutdown")
async def shutdown():
    await to_start()

@app.post('/api/year')
async def add_new_year():
    pass

@app.get('/api/year/{year}')
async def get_year():
    pass

