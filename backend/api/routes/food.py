from fastapi import APIRouter, HTTPException, Query, Depends
from backend.api.services.food import repo
from backend.api.models.food import (
    Food, FoodCreate, FoodUpdate, FoodFilter, FoodList, ApiResponse,
    create_success_response, create_error_response
)
from typing import Optional
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/food", response_model=ApiResponse)
async def get_food_list(
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Размер страницы"),
    name: Optional[str] = Query(None, description="Фильтр по названию"),
    min_price: Optional[float] = Query(None, ge=0, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, ge=0, description="Максимальная цена"),
    search: Optional[str] = Query(None, description="Поиск по названию и описанию")
):
    """Получить список продуктов с фильтрацией и пагинацией"""
    try:
        logger.info(f"Getting food list with params: page={page}, size={size}, name={name}, min_price={min_price}, max_price={max_price}, search={search}")
        
        # Создаем объект фильтра только если есть хотя бы один параметр фильтрации
        filter_params = None
        if any([name, min_price is not None, max_price is not None, search]):
            filter_params = FoodFilter(
                name=name,
                min_price=min_price,
                max_price=max_price,
                search=search
            )
            logger.info(f"Created filter params: {filter_params}")
        
        result = repo.get_all_food(filter_params, page, size)
        logger.info(f"Successfully retrieved {len(result.items)} items")
        return create_success_response(result)
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")

@router.get("/food/{food_id}", response_model=ApiResponse)
async def get_food(food_id: int):
    """Получить продукт по ID"""
    food = repo.get_food(food_id)
    if food is None:
        raise HTTPException(status_code=404, detail=f"Продукт с ID {food_id} не найден")
    return create_success_response(food)

@router.post("/food", response_model=ApiResponse, status_code=201)
async def create_food(food: FoodCreate):
    """Создать новый продукт"""
    try:
        new_food = repo.create_food(food)
        return create_success_response(new_food)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/food/{food_id}", response_model=ApiResponse)
async def update_food(food_id: int, food: FoodUpdate):
    """Частично обновить существующий продукт"""
    try:
        updated_food = repo.update_food(food_id, food)
        if updated_food is None:
            raise HTTPException(status_code=404, detail=f"Продукт с ID {food_id} не найден")
        return create_success_response(updated_food)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/food/{food_id}", response_model=ApiResponse)
async def delete_food(food_id: int):
    """Удалить продукт"""
    if not repo.delete_food(food_id):
        raise HTTPException(status_code=404, detail=f"Продукт с ID {food_id} не найден")
    return create_success_response(True)

@router.get("/health", response_model=ApiResponse)
async def health_check():
    """Проверка работоспособности API"""
    return create_success_response({"status": "ok"}) 

