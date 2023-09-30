from fastapi import FastAPI
from routers import category_db, products_db, users_db, jwt_aouth_users
import uvicorn

app = FastAPI()

app.include_router(category_db.router)
app.include_router(products_db.router)
app.include_router(users_db.router)
app.include_router(jwt_aouth_users.router)

@app.get('/')
async def root():
    return 'APIRest con FastApi'

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)