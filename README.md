# Food Management System

## Содержание
1. [Описание](#описание)
2. [Структура проекта](#структура-проекта)
3. [Установка и запуск](#установка-и-запуск)
4. [Использование](#использование)
5. [Документация](#документация)

## Описание

Food Management System - это веб-приложение для управления списком продуктов. Система предоставляет REST API для работы с продуктами и современный веб-интерфейс для взаимодействия с пользователем.

## Структура проекта

```
practiceAPI/
├── backend/                 # Backend приложение (FastAPI)
│   ├── api/                # API модуль
│   │   ├── app.py         # Основной файл приложения
│   │   ├── config.py      # Конфигурация (CORS, настройки)
│   │   ├── models/        # Pydantic модели
│   │   ├── routes/        # API маршруты
│   │   ├── services/      # Бизнес-логика
│   │   └── router.py      # Конфигурация роутера
│   └── requirements.txt    # Зависимости Python
│
├── frontend/               # Frontend приложение
│   ├── assets/            # Статические ресурсы
│   │   ├── css/          # Стили
│   │   └── js/           # JavaScript модули
│   └── pages/            # HTML страницы
│
├── .gitignore            # Игнорируемые Git файлы
├── requirements.txt      # Основные зависимости проекта
└── .venv/               # Виртуальное окружение Python
```

### Компоненты системы:

1. **Backend (FastAPI)**:
   - REST API для работы с продуктами
   - Валидация данных через Pydantic
   - In-memory хранилище данных
   - CORS для безопасного взаимодействия с фронтендом
   - Модульная структура с разделением на модели, роуты и сервисы

2. **Frontend**:
   - Современный веб-интерфейс
   - Адаптивный дизайн
   - Поддержка темной темы
   - Живой поиск и фильтрация
   - Модальные окна для редактирования
   - Цветовая индикация цен

## Установка и запуск

### Backend

1. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запуск сервера:
   ```bash
   cd backend
   uvicorn api.app:app --host 0.0.0.0 --port 80
   ```

### Frontend

1. Установите расширение Live Server в VS Code
2. Откройте проект в VS Code
3. Запустите Live Server для директории `frontend`

## Использование

### API Endpoints

- `GET /api/food` - получение списка продуктов с пагинацией и фильтрацией
- `POST /api/food` - создание нового продукта
- `PATCH /api/food/{id}` - обновление продукта
- `DELETE /api/food/{id}` - удаление продукта

### Веб-интерфейс

1. Откройте `http://localhost:5500` в браузере
2. Используйте форму для добавления продуктов
3. Применяйте фильтры для поиска:
   - По названию
   - По цене (мин/макс)
   - Поиск по названию и описанию
4. Переключайте тему для комфортного просмотра
5. Используйте пагинацию для навигации по списку


## Особенности

- 🎨 Современный адаптивный дизайн
- 🌓 Поддержка светлой и темной темы
- 🔍 Расширенный поиск и фильтрация
- 📱 Оптимизировано для мобильных устройств
- 🔄 Живое обновление данных
- 📊 Цветовая индикация цен:
  - 🟢 До 100₽
  - 🟡 От 100₽ до 500₽
  - 🔴 Более 500₽
- 📄 Пагинация и управление списками
- 🖼️ Модальные окна для редактирования

## Технологии

### Backend
- Python 3.8+
- FastAPI
- Pydantic
- Uvicorn

### Frontend
- HTML5
- CSS3 (с поддержкой CSS переменных)
- JavaScript (ES6+)
- Font Awesome (иконки)
- Inter (шрифт)
