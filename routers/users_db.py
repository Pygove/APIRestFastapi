from fastapi import APIRouter, HTTPException, status
from models.user import User
from schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter()