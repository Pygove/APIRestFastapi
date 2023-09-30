from fastapi import APIRouter, HTTPException, status
from models.user import User
from schemas.user import user_schema, users_schema
from config.db import db_client
from datetime import datetime
from config.creation_counters import increment_couter
from passlib.context import CryptContext

router = APIRouter(prefix='/api/users', tags=['users'],responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})

@router.get('/s', response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

@router.get('/{id}')
async def user(id : int):
    return search_user('_id',id)

@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user : User):
    if type(search_user('username',user.username)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario ya cargado')
    else:
        user_dict = dict(user)
        del user_dict["id"]
        user_dict["_id"] = increment_couter("usersID")
        user_dict["password"] = CryptContext(schemes=["bcrypt"]).hash(user_dict["password"])
        db_client.users.insert_one(user_dict)
        new_user = user_schema(db_client.users.find_one({"_id":user_dict["_id"]}))
        return User(**new_user)

@router.put('/{id}', response_model=User)
async def user(user : User,id:int):
    user_dict = dict(user)
    try:
        db_client.users.find_one_and_update({"_id":id}, {"$set": {"last_modification_date": str(datetime.now()), "username": user_dict["username"],"password": user_dict["password"],"email": user_dict["email"],"avatar": user_dict["avatar"]}})
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario no modificado')
    return (search_user("_id", id))

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def user(id: int):
    if not (db_client.users.find_one_and_delete({"_id":id})):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Usuario no eliminado')
    else:
        raise HTTPException(status_code=status.HTTP_200_OK,detail='Usuario eliminado correctamente')

def search_user(field, key):
    try:
        category = db_client.users.find_one({field:key})
        return User(**(user_schema(category)))
    except:
        return {"Error":"Usuario no encontrado"}