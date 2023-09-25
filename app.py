from fastapi import FastAPI
from routers import category_db, products_db
import uvicorn

app = FastAPI()

app.include_router(category_db.router)
app.include_router(products_db.router)

@app.get('/')
async def root():
    return 'APIRest con FastApi'

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)