from typing import List, Optional, Dict, Any
from datetime import datetime
from backend.api.models.food import Food, FoodCreate, FoodUpdate, FoodFilter, FoodList

class FoodRepository:
    def __init__(self):
        self._foods: List[Food] = [
            Food(
                id=1,
                name="Бананы",
                price=80.0,
                description="Свежие желтые бананы из Эквадора",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Food(
                id=2,
                name="Яблоки",
                price=120.0,
                description="Красные яблоки сорта Голден",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Food(
                id=3,
                name="Авокадо",
                price=250.0,
                description="Спелые авокадо из Мексики",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Food(
                id=4,
                name="Манго",
                price=750.0,
                description="Сладкие манго из Таиланда",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Food(
                id=5,
                name="Клубника",
                price=450.0,
                description="Свежая клубника из местных теплиц",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Food(
                id=6,
                name="Гранат",
                price=180.0,
                description="Сочные гранаты из Азербайджана",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Food(
                id=7,
                name="Ананас",
                price=550.0,
                description="Сладкий ананас из Коста-Рики",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        self._next_id: int = 8

    def _filter_foods(self, foods: List[Food], filter_params: FoodFilter) -> List[Food]:
        """Применяет фильтры к списку продуктов"""
        filtered = foods

        if filter_params.name:
            filtered = [f for f in filtered if filter_params.name.lower() in f.name.lower()]

        if filter_params.min_price:
            filtered = [f for f in filtered if f.price >= filter_params.min_price]

        if filter_params.max_price:
            filtered = [f for f in filtered if f.price <= filter_params.max_price]

        if filter_params.search:
            search = filter_params.search.lower()
            filtered = [
                f for f in filtered 
                if search in f.name.lower() or search in f.description.lower()
            ]

        return filtered

    def get_all_food(
        self,
        filter_params: Optional[FoodFilter] = None,
        page: int = 1,
        size: int = 10
    ) -> FoodList:
        """Получает список продуктов с пагинацией и фильтрацией"""
        try:
            # Применяем фильтры
            filtered_foods = self._filter_foods(self._foods, filter_params) if filter_params else self._foods
            
            # Вычисляем пагинацию
            total = len(filtered_foods)
            if total == 0:
                return FoodList(
                    items=[],
                    total=0,
                    page=1,
                    size=size,
                    pages=0
                )
            
            # Вычисляем количество страниц
            pages = (total + size - 1) // size
            
            # Проверяем и корректируем номер страницы
            if page < 1:
                page = 1
            elif page > pages:
                page = pages
            
            # Получаем срез для текущей страницы
            start = (page - 1) * size
            end = min(start + size, total)
            items = filtered_foods[start:end]

            return FoodList(
                items=items,
                total=total,
                page=page,
                size=size,
                pages=pages
            )
        except Exception as e:
            print(f"Error in get_all_food: {str(e)}")  # Для отладки
            raise ValueError(f"Ошибка при получении списка продуктов: {str(e)}")

    def get_food(self, food_id: int) -> Optional[Food]:
        """Получает продукт по ID"""
        for food in self._foods:
            if food.id == food_id:
                return food
        return None

    def create_food(self, food: FoodCreate) -> Food:
        """Создает новый продукт"""
        # Проверяем уникальность названия
        if any(f.name.lower() == food.name.lower() for f in self._foods):
            raise ValueError(f"Продукт с названием '{food.name}' уже существует")

        new_food = Food(
            id=self._next_id,
            name=food.name,
            price=food.price,
            description=food.description,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self._foods.append(new_food)
        self._next_id += 1
        return new_food

    def update_food(self, food_id: int, food: FoodUpdate) -> Optional[Food]:
        """Обновляет существующий продукт"""
        for i, existing_food in enumerate(self._foods):
            if existing_food.id == food_id:
                # Проверяем уникальность названия, если оно меняется
                if food.name and food.name.lower() != existing_food.name.lower():
                    if any(f.name.lower() == food.name.lower() for f in self._foods):
                        raise ValueError(f"Продукт с названием '{food.name}' уже существует")

                # Обновляем только переданные поля
                update_data = food.dict(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(existing_food, key, value)
                
                existing_food.updated_at = datetime.now()
                self._foods[i] = existing_food
                return existing_food
        return None

    def delete_food(self, food_id: int) -> bool:
        """Удаляет продукт по ID"""
        for i, food in enumerate(self._foods):
            if food.id == food_id:
                self._foods.pop(i)
                return True
        return False

# Создаем экземпляр репозитория
repo = FoodRepository()