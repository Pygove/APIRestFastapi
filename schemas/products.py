def product_schema(product) -> dict:
    return { 
            "id" : product["_id"],
            "title":product["title"],
            "description": product["description"],
            "price": product["price"],
            "creation_date":product["creation_date"],
            "last_modification_date":product["last_modification_date"],
            "category":product["category"],
            "images" : product["images"]
            }

def products_schema(products) -> list:
    return [product_schema(product) for product in products]