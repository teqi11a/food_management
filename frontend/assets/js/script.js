// Константы для API
const API_BASE_URL = 'http://localhost:80/api';
const DEFAULT_PAGE_SIZE = 6; // Изменено на 6 для главной страницы
const FULL_LIST_PAGE_SIZE = 10; // Для страницы со всеми продуктами

// Состояние пагинации и фильтров
let currentPage = 1;
let currentFilters = {
    name: null,
    min_price: null,
    max_price: null,
    search: null
};

// Функция для управления темой
function initTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle.querySelector('i');
    
    // Проверяем сохраненную тему
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }
    
    // Обработчик переключения темы
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
}

// Функция для обновления иконки темы
function updateThemeIcon(theme) {
    const themeIcon = document.querySelector('#theme-toggle i');
    themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

// Функция для определения класса цены
function getPriceClass(price) {
    if (price <= 100) return 'price-low';
    if (price <= 500) return 'price-medium';
    return 'price-high';
}

// Функция для получения списка продуктов с фильтрацией и пагинацией
async function get_food(isFullList = false) {
    try {
        const container = document.getElementById('food-container');
        container.innerHTML = '<div class="loading">Загрузка...</div>';
        
        // Формируем URL с параметрами, исключая null значения
        const params = new URLSearchParams({
            page: currentPage,
            size: isFullList ? FULL_LIST_PAGE_SIZE : DEFAULT_PAGE_SIZE
        });

        // Добавляем только не-null параметры фильтрации
        if (currentFilters.name) params.append('name', currentFilters.name);
        if (currentFilters.min_price !== null) params.append('min_price', currentFilters.min_price);
        if (currentFilters.max_price !== null) params.append('max_price', currentFilters.max_price);
        if (currentFilters.search) params.append('search', currentFilters.search);

        const response = await fetch(`${API_BASE_URL}/food?${params}`, {
            method: 'GET',
        });
        
        const apiResponse = await response.json();
        
        if (!response.ok) {
            // Обработка ошибок валидации (422)
            if (response.status === 422) {
                const validationErrors = apiResponse.detail || [];
                const errorMessage = Array.isArray(validationErrors) 
                    ? validationErrors.map(err => `${err.loc[1]}: ${err.msg}`).join('\n')
                    : 'Ошибка валидации данных';
                throw new Error(errorMessage);
            }
            throw new Error(apiResponse.error || `HTTP error! status: ${response.status}`);
        }

        if (!apiResponse.success) {
            throw new Error(apiResponse.error || 'Ошибка при получении данных');
        }

        const data = apiResponse.data;
        container.innerHTML = '';
        
        // Отображаем продукты с анимацией
        data.items.forEach((food, index) => {
            const foodElement = document.createElement('div');
            foodElement.className = 'food-item';
            foodElement.style.animationDelay = `${index * 0.1}s`;
            const priceClass = getPriceClass(food.price);
            foodElement.innerHTML = `
                <h3>${food.name}</h3>
                <p class="price ${priceClass}">${food.price.toFixed(2)} ₽</p>
                <p>${food.description}</p>
                <div class="meta">
                    <small><i class="fas fa-clock"></i> Создан: ${new Date(food.created_at).toLocaleString()}</small>
                    <small><i class="fas fa-edit"></i> Обновлен: ${new Date(food.updated_at).toLocaleString()}</small>
                </div>
                <div class="actions">
                    <div class="btn-group">
                        <button class="btn btn-primary" onclick='openEditModal(${JSON.stringify(food)})'>
                            <i class="fas fa-edit"></i> Изменить
                        </button>
                        <button class="btn btn-danger" onclick="deleteFood(${food.id})">
                            <i class="fas fa-trash"></i> Удалить
                        </button>
                    </div>
                </div>
            `;
            container.appendChild(foodElement);
        });

        // Обновляем пагинацию только если это полный список
        if (isFullList) {
            updatePagination(data);
        } else {
            // Показываем кнопку "Показать все" если есть больше продуктов
            updateShowAllButton(data.total > DEFAULT_PAGE_SIZE);
        }
        
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
        const container = document.getElementById('food-container');
        container.innerHTML = `
            <div class="error">
                <i class="fas fa-exclamation-circle"></i>
                <p>${error.message}</p>
            </div>
        `;
    }
}

// Функция для обновления кнопки "Показать все"
function updateShowAllButton(hasMore) {
    const container = document.getElementById('pagination');
    if (!container) return;

    container.innerHTML = '';
    
    if (hasMore) {
        const showAllButton = document.createElement('a');
        showAllButton.href = 'all-products.html';
        showAllButton.className = 'btn btn-primary';
        showAllButton.innerHTML = `
            <i class="fas fa-list"></i>
            Показать все продукты
        `;
        container.appendChild(showAllButton);
    }
}

// Функция для обновления пагинации
function updatePagination(data) {
    const paginationContainer = document.getElementById('pagination');
    if (!paginationContainer) return;

    paginationContainer.innerHTML = '';
    
    // Кнопка "Предыдущая"
    const prevButton = document.createElement('button');
    prevButton.className = 'pagination-btn';
    prevButton.disabled = data.page === 1;
    prevButton.innerHTML = '<i class="fas fa-chevron-left"></i>';
    prevButton.onclick = () => {
        if (data.page > 1) {
            currentPage = data.page - 1;
            get_food(true);
        }
    };
    paginationContainer.appendChild(prevButton);

    // Номера страниц
    for (let i = 1; i <= data.pages; i++) {
        const pageButton = document.createElement('button');
        pageButton.className = `pagination-btn ${i === data.page ? 'active' : ''}`;
        pageButton.textContent = i;
        pageButton.onclick = () => {
            currentPage = i;
            get_food(true);
        };
        paginationContainer.appendChild(pageButton);
    }

    // Кнопка "Следующая"
    const nextButton = document.createElement('button');
    nextButton.className = 'pagination-btn';
    nextButton.disabled = data.page === data.pages;
    nextButton.innerHTML = '<i class="fas fa-chevron-right"></i>';
    nextButton.onclick = () => {
        if (data.page < data.pages) {
            currentPage = data.page + 1;
            get_food(true);
        }
    };
    paginationContainer.appendChild(nextButton);
}

// Функция для применения фильтров
function applyFilters(event) {
    event.preventDefault();
    
    // Получаем значения из формы
    const nameValue = document.getElementById('filter-name').value.trim();
    const minPriceValue = document.getElementById('filter-min-price').value.trim();
    const maxPriceValue = document.getElementById('filter-max-price').value.trim();
    const searchValue = document.getElementById('filter-search').value.trim();

    // Обновляем фильтры, преобразуя числовые значения
    currentFilters = {
        name: nameValue || null,
        min_price: minPriceValue ? parseFloat(minPriceValue) : null,
        max_price: maxPriceValue ? parseFloat(maxPriceValue) : null,
        search: searchValue || null
    };

    // Проверяем валидность числовых значений
    if (minPriceValue && isNaN(currentFilters.min_price)) {
        alert('Минимальная цена должна быть числом');
        return;
    }
    if (maxPriceValue && isNaN(currentFilters.max_price)) {
        alert('Максимальная цена должна быть числом');
        return;
    }

    // Проверяем, что минимальная цена не больше максимальной
    if (currentFilters.min_price !== null && currentFilters.max_price !== null && 
        currentFilters.min_price > currentFilters.max_price) {
        alert('Минимальная цена не может быть больше максимальной');
        return;
    }

    currentPage = 1; // Сбрасываем на первую страницу
    get_food();
}

// Функция для сброса фильтров
function resetFilters() {
    document.getElementById('filter-form').reset();
    currentFilters = {
        name: null,
        min_price: null,
        max_price: null,
        search: null
    };
    currentPage = 1;
    get_food();
}

// Функция для добавления нового продукта
async function addFood(event) {
    event.preventDefault();
    
    const foodData = {
        name: document.getElementById('name').value,
        price: parseFloat(document.getElementById('price').value),
        description: document.getElementById('description').value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/food`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(foodData)
        });

        const apiResponse = await response.json();
        if (!response.ok || !apiResponse.success) {
            throw new Error(apiResponse.error || `HTTP error! status: ${response.status}`);
        }

        // Очищаем форму
        document.getElementById('addFoodForm').reset();
        
        // Обновляем список продуктов
        await get_food();
    } catch (error) {
        console.error('Ошибка при добавлении продукта:', error);
        alert(`Ошибка при добавлении продукта: ${error.message}`);
    }
}

// Функция для удаления продукта
async function deleteFood(id) {
    if (!confirm('Вы уверены, что хотите удалить этот продукт?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/food/${id}`, {
            method: 'DELETE'
        });

        const apiResponse = await response.json();
        if (!response.ok || !apiResponse.success) {
            throw new Error(apiResponse.error || `HTTP error! status: ${response.status}`);
        }

        // Обновляем список продуктов
        await get_food();
    } catch (error) {
        console.error('Ошибка при удалении продукта:', error);
        alert(`Ошибка при удалении продукта: ${error.message}`);
    }
}

// Функция для открытия модального окна редактирования
function openEditModal(food) {
    const modal = document.getElementById('editModal');
    const form = document.getElementById('editFoodForm');
    
    // Заполняем форму данными продукта
    document.getElementById('edit-id').value = food.id;
    document.getElementById('edit-name').value = food.name;
    document.getElementById('edit-price').value = food.price;
    document.getElementById('edit-description').value = food.description;
    
    modal.style.display = 'block';
}

// Функция для закрытия модального окна
function closeEditModal() {
    const modal = document.getElementById('editModal');
    modal.style.display = 'none';
}

// Функция для обновления продукта
async function updateFood(event) {
    event.preventDefault();
    
    const id = document.getElementById('edit-id').value;
    const foodData = {
        name: document.getElementById('edit-name').value,
        price: parseFloat(document.getElementById('edit-price').value),
        description: document.getElementById('edit-description').value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/food/${id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(foodData)
        });

        const apiResponse = await response.json();
        if (!response.ok || !apiResponse.success) {
            throw new Error(apiResponse.error || `HTTP error! status: ${response.status}`);
        }

        // Закрываем модальное окно
        closeEditModal();
        
        // Обновляем список продуктов
        await get_food();
    } catch (error) {
        console.error('Ошибка при обновлении продукта:', error);
        alert(`Ошибка при обновлении продукта: ${error.message}`);
    }
}

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', function() {
    // Инициализируем тему
    initTheme();
    
    // Добавляем обработчики форм
    const addFoodForm = document.getElementById('addFoodForm');
    if (addFoodForm) {
        addFoodForm.addEventListener('submit', addFood);
    }

    const editFoodForm = document.getElementById('editFoodForm');
    if (editFoodForm) {
        editFoodForm.addEventListener('submit', updateFood);
    }

    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', applyFilters);
    }

    // Закрытие модального окна при клике вне его
    window.onclick = function(event) {
        const modal = document.getElementById('editModal');
        if (event.target == modal) {
            closeEditModal();
        }
    }

    // Загружаем список продуктов
    get_food();
});