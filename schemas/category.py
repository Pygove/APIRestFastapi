def category_schema(category) -> dict:
    return { 
            "id" : category["_id"],
            "name_category":category["name_category"],
            "creation_date":category["creation_date"],
            "last_modification_date":category["last_modification_date"]
            }

def categories_schema(categories) -> list:
    return [category_schema(category) for category in categories]