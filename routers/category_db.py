from fastapi import APIRouter, HTTPException, status
from models.category import Categories
from schemas.category import category_schema, categories_schema
from config.db import db_client
#from bson import ObjectId
from datetime import datetime
from config.creation_counters import increment_couter

router = APIRouter(prefix='/api/categories', tags=['categories'], responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})

@router.get('/s', response_model=list[Categories])
async def categories():
    return categories_schema(db_client.categories.find())

@router.get('/{id}')
async def category(id: int):
    return search_category("_id", id)

@router.post('/', response_model=Categories, status_code=status.HTTP_201_CREATED)
async def category(category: Categories):
    if type(search_category('name_category',category.name_category)) == Categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria ya cargada')
    else:
        category_dict = dict(category)
        del category_dict["id"]
        category_dict["_id"] = increment_couter("categoryID")
        db_client.categories.insert_one(category_dict)
        new_category = category_schema(db_client.categories.find_one({"_id":category_dict["_id"]}))
        return Categories(**new_category)
    
@router.put('/{id}', response_model=Categories)
async def category(category: Categories, id:int):
    category_dict = dict(category)
    try:
        db_client.categories.find_one_and_update({"_id":id}, {"$set": {"last_modification_date": creation_modification_date(), "name_category": category_dict["name_category"]}})
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria no modificada')
    return (search_category("_id", id))

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def category(id: int):
    if not (db_client.categories.find_one_and_delete({"_id":id})):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Categoria no eliminada')
    else:
        raise HTTPException(status_code=status.HTTP_200_OK,detail='Categoria eliminada correctamente')

def search_category(field, key):
    try:
        category = db_client.categories.find_one({field:key})
        return Categories(**(category_schema(category)))
    except:
        return {"Error":"Categoria no encontrada"}

def creation_modification_date():
    return str(datetime.now())