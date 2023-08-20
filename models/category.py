from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    id : Optional[str]
    name_category : str
    creation_date : str
    last_modification_date : str
