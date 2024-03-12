from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    pass

@app.post('/api/year')
async def add_new_year():
    pass

@app.get('/api/year/{year}')
async def get_year():
    pass

