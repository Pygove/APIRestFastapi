from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Products(BaseModel):
    id : Optional[int] = None
    title : str
    price : int = Field(gt=0)
    description : Optional[str] = None
    category : Optional[int] = None
    creation_date : Optional[str] = str(datetime.now())
    last_modification_date : Optional[str] = str(datetime.now())
    images : Optional[List] = None


