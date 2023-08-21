from fastapi import APIRouter, HTTPException, status
from models.category import Categories
from schemas.category import category_schema, categories_schema
from config.db import db_client
from bson import ObjectId

router = APIRouter(prefix='/api/categories', tags=['categories'], responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})

@router.get('/s', response_model=list[Categories])
async def categories():
    return categories_schema(db_client.categories.find())

@router.get('/{id}')
async def category(id: str):
    return search_category("_id", ObjectId(id))

@router.post('/', response_model=Categories, status_code=status.HTTP_201_CREATED)
async def category(category: Categories):
    if type(search_category('name_category',category.name_category)) == Categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria ya cargada')
    else:
        category_dict = dict(category)
        del category_dict["id"]
        id = db_client.categories.insert_one(category_dict).inserted_id
        new_category = category_schema(db_client.categories.find_one({"_id":id}))
        return Categories(**new_category)
    
@router.put('/', response_model=Categories)
async def category(category: Categories):
    category_dict = dict(category)
    del category_dict["id"]
    try:
        db_client.categories.find_one_and_replace({"_id":ObjectId(category.id)}, category_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria no modificada')
    return search_category("_id", ObjectId(category.id))

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def category(id: str):
    if not db_client.categories.find_one_and_delete({"_id":ObjectId(id)}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Categoria no eliminada')
    else:
        raise HTTPException(status_code=status.HTTP_200_OK,detail='Categoria eliminada correctamente')

def search_category(field: str, key):
    try:
        category = db_client.categories.find_one({field:key})
        return Categories(**(category_schema(category)))
    except:
        return {"Error":"Usuario no encontrado"}