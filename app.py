from fastapi import FastAPI
from routers import category_db

app = FastAPI()

app.include_router(category_db.router)

@app.get('/')
async def root():
    return 'APIRest con FastApi'