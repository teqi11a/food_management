from fastapi import APIRouter
from backend.api.routes import food

api_router = APIRouter()

api_router.include_router(food.router)