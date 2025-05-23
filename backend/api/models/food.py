from typing import List, Optional, Generic, TypeVar, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

T = TypeVar('T')

class ApiResponse(BaseModel):
    """Унифицированный формат ответа API"""
    success: bool = Field(..., description="Флаг успешности операции")
    data: Optional[Any] = Field(None, description="Данные ответа")
    error: Optional[str] = Field(None, description="Сообщение об ошибке")

def create_success_response(data: Any) -> ApiResponse:
    """Создает успешный ответ"""
    return ApiResponse(success=True, data=data)

def create_error_response(message: str) -> ApiResponse:
    """Создает ответ с ошибкой"""
    return ApiResponse(success=False, error=message)

class FoodBase(BaseModel):
    """Базовая модель продукта"""
    name: str = Field(..., min_length=1, max_length=100, description="Название продукта")
    price: float = Field(..., gt=0, description="Цена продукта")
    description: str = Field(..., min_length=1, max_length=500, description="Описание продукта")

    @field_validator('name')
    @classmethod
    def name_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('Название не может быть пустым')
        return v.strip()

    @field_validator('description')
    @classmethod
    def description_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('Описание не может быть пустым')
        return v.strip()

class FoodCreate(FoodBase):
    """Модель для создания продукта"""
    pass

class FoodUpdate(BaseModel):
    """Модель для обновления продукта"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Название продукта")
    price: Optional[float] = Field(None, gt=0, description="Цена продукта")
    description: Optional[str] = Field(None, min_length=1, max_length=500, description="Описание продукта")

    @field_validator('name')
    @classmethod
    def name_must_be_valid(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Название не может быть пустым')
        return v.strip() if v is not None else v

    @field_validator('description')
    @classmethod
    def description_must_be_valid(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Описание не может быть пустым')
        return v.strip() if v is not None else v

class Food(FoodBase):
    """Модель продукта"""
    id: int = Field(..., description="Уникальный идентификатор продукта")
    created_at: datetime = Field(..., description="Дата и время создания")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления")

    class Config:
        from_attributes = True

class FoodFilter(BaseModel):
    """Модель для фильтрации продуктов"""
    name: Optional[str] = Field(None, description="Фильтр по названию")
    min_price: Optional[float] = Field(None, ge=0, description="Минимальная цена")
    max_price: Optional[float] = Field(None, ge=0, description="Максимальная цена")
    search: Optional[str] = Field(None, description="Поиск по названию и описанию")

    @field_validator('max_price')
    @classmethod
    def max_price_must_be_greater_than_min(cls, v, info):
        if v is not None and 'min_price' in info.data and info.data['min_price'] is not None:
            if v < info.data['min_price']:
                raise ValueError('Максимальная цена должна быть больше или равна минимальной')
        return v

class FoodList(BaseModel):
    """Модель для пагинированного списка продуктов"""
    items: List[Food] = Field(..., description="Список продуктов")
    total: int = Field(..., description="Общее количество продуктов")
    page: int = Field(..., description="Текущая страница")
    size: int = Field(..., description="Размер страницы")
    pages: int = Field(..., description="Общее количество страниц")