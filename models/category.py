from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Categories(BaseModel):
    id : Optional[int] = None
    name_category : str
    creation_date : Optional[str] = str(datetime.now())
    last_modification_date : Optional[str] = str(datetime.now())
    image : Optional[str] = None


