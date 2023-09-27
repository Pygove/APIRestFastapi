from fastapi import APIRouter, HTTPException, status
from models.products import Products
from models.category import Categories
from schemas.products import product_schema, products_schema
from config.db import db_client
#from bson import ObjectId
from datetime import datetime
from config.creation_counters import increment_couter
from routers.category_db import search_category

router = APIRouter(prefix='/api/products', tags=['products'], responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})

@router.get('/s', response_model=list[Products])
async def products():
    return products_schema(db_client.products.find())

@router.get('/{id}')
async def product(id: int):
    return search_product("_id", id)

@router.post('/', response_model=Products, status_code=status.HTTP_201_CREATED)
async def product(product: Products):
    if type(search_product('title',product.title)) == Products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Producto ya cargado')
    elif type(search_category('_id',product.category)) != Categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria inexistente')
    else:
        product_dict = dict(product)
        del product_dict["id"]
        product_dict["_id"] = increment_couter("productsID")
        db_client.products.insert_one(product_dict)
        new_product = product_schema(db_client.products.find_one({"_id":product_dict["_id"]}))
        return Products(**new_product)
    
@router.put('/{id}', response_model=Products)
async def product(product: Products, id:int):
    product_dict = dict(product)
    try:
        db_client.products.find_one_and_update({"_id":id}, {"$set": {"last_modification_date": creation_modification_date(), "title": product_dict["title"],"price": product_dict["price"]}})
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Producto no modificado')
    return search_product("_id", id)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def product(id: int):
    if not db_client.products.find_one_and_delete({"_id":id}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Producto no eliminado')
    else:
        raise HTTPException(status_code=status.HTTP_200_OK,detail='Producto eliminado correctamente')

def search_product(field: int, key):
    try:
        product = db_client.products.find_one({field:key})
        return Products(**(product_schema(product)))
    except:
        return {"Error":"Producto no encontrado"}

def creation_modification_date():
    return str(datetime.now())