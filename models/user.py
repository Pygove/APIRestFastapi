from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    id : Optional[int] = None
    username : str = None
    first_name : str = None
    last_name : str = None
    email : str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.]+$")
    password : str
    gender : Gender = None
    role : List[Role] = []
    avatar : Optional[str] = None
    creation_date : Optional[str] = str(datetime.now())
    last_modification_date : Optional[str] = str(datetime.now())

