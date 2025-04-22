# materials

`materials` - это пакет Python для работы с базой данных материалов. Пакет предоставляет простой доступ к информации о материалах, включая их характеристики, химический состав, механические и технологические свойства. Основная цель пакета - упростить взаимодействие с базой данных материалов через функции, выполняющие CRUD-операции.

Материал демонстрационный, показывает навыки работы.

## Установка

Для установки пакета `materials` используйте команду:

```sh
pip install git+https://github.com/sad-engineer/materials.git
```

## Клонирование проекта

Для клонирования проекта используйте команду:

```sh
git clone https://github.com/sad-engineer/materials.git
cd materials
```

## Подготовка базы данных

База данных устанавливается вместе с пакетом, и настройка не требуется. Пакет поддерживает базу данных SQLite по умолчанию, но можно указать другой URL базы данных через переменную окружения DATABASE_URL.

## Использование

### Основные операции с материалами

```python
from materials import (
    get_material_by_brand,
    get_all_brands,
    get_brands_by_material_class_index,
    get_material_class_index_by_id
)

# Получение всех брендов
all_brands = get_all_brands()
print("Все доступные бренды:", all_brands)

# Получение информации о конкретном материале
brand = "30ХМА"
material = get_material_by_brand(brand)
if material:
    print(f"Информация о материале {brand}:", material)

# Получение брендов по индексу класса материала
index = 4
brands_by_index = get_brands_by_material_class_index(index)
print(f"Бренды с index_of_material_class = {index}:", brands_by_index)

# Получение информации об индексе класса материала
index_id = 1
material_class = get_material_class_index_by_id(index_id)
if material_class:
    print(f"Информация о классе материала с ID {index_id}:", material_class)
```

### Химический состав и стандарты

```python
from materials import get_chemical_composition_by_brand, get_standard_of_chemical_composition_by_brand

brand = "30ХМА"

# Получение химического состава
chemical_composition = get_chemical_composition_by_brand(brand)
if chemical_composition:
    print(f"Химический состав {brand}: {chemical_composition}")

# Получение стандарта материала
standard = get_standard_of_chemical_composition_by_brand(brand)
if standard:
    print(f"Стандарт для {brand}:", standard)
```

### Механические свойства

```python
from materials import get_mechanical_properties_by_brand

brand = "30ХМА"
mechanical_props = get_mechanical_properties_by_brand(brand)
if mechanical_props:
    print(f"Механические свойства {brand}: {mechanical_props}")
```

### Технологические свойства

```python
from materials import get_technological_properties_by_brand

brand = "30ХМА"
tech_props = get_technological_properties_by_brand(brand)
if tech_props:
    print(f"Технологические свойства {brand}: {tech_props}")
```

### Твердость

```python
from materials import get_hardness_by_brand

brand = "30ХМА"
hardness = get_hardness_by_brand(brand)
if hardness:
    print(f"Твердость материала {brand}: {hardness}")
```

### Характеристики материала

```python
from materials import get_characteristics_by_brand

brand = "30ХМА"
characteristics = get_characteristics_by_brand(brand)
if characteristics:
    print(f"Характеристики материала {brand}: {characteristics}")
```

### Комплексный пример

```python
def print_material_info(brand: str):
    """Пример получения всей доступной информации о материале"""
    print(f"\nПолная информация о материале {brand}:")
    print("-" * 50)
    
    # Основная информация
    material = get_material_by_brand(brand)
    if not material:
        print(f"Материал {brand} не найден")
        return
    
    # Химический состав
    chemical = get_chemical_composition_by_brand(brand)
    if chemical:
        print("\nХимический состав:")
        print(f"C: {chemical.c}%, Si: {chemical.si}%, Mn: {chemical.mn}%")
    
    # Механические свойства
    mechanical = get_mechanical_properties_by_brand(brand)
    if mechanical:
        print("\nМеханические свойства:")
        print(f"Предел прочности: {mechanical.tensile_strength} МПа")
        print(f"Относительное удлинение: {mechanical.elongation}%")
    
    # Технологические свойства
    tech = get_technological_properties_by_brand(brand)
    if tech:
        print("\nТехнологические свойства:")
        print(f"Температура ковки: {tech.forging_start}-{tech.forging_end} °C")
    
    # Твердость
    hardness = get_hardness_by_brand(brand)
    if hardness:
        print("\nТвердость:")
        print(f"HB: {hardness.hb}, HRC: {hardness.hrc}")
    
    # Стандарт
    standard = get_standard_of_chemical_composition_by_brand(brand)
    if standard:
        print(f"\nСтандарт: {standard}")

# Использование
print_material_info("30ХМА")
```

## Настройка параметра echo для SQLAlchemy

Параметр echo управляет выводом SQL-запросов в консоль. Вы можете управлять этим параметром, используя переменную окружения SQLALCHEMY_ECHO.
* При запуске main.py echo отключен (False).
* При использовании функций из пакета materials echo можно включить, установив переменную окружения:

```python
import os

# Включение echo при работе с пакетом materials
os.environ["SQLALCHEMY_ECHO"] = "True"
from materials import get_all_brands

all_brands = get_all_brands()
print("Все бренды:", all_brands)
```

## Структура проекта
```
materials/
├── alembic/        # Миграции базы данных
├── materials/      # Основной пакет
│ ├── models/       # Модели данных
│ ├── database.py   # Настройки базы данных
│ ├── crud.py       # CRUD операции
│ └── main.py       # Основной модуль
├── pyproject.toml  # Конфигурация Poetry
├── setup.py        # Настройки установки
└── README.md       # Документация
```

## Требования

- Python 3.8 или выше
- SQLAlchemy 2.0+
- Alembic
- Poetry (для разработки)

## Установка зависимостей

Для установки зависимостей проекта используйте Poetry:

1. Установите Poetry, если он еще не установлен:
```sh
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Linux/MacOS
curl -sSL https://install.python-poetry.org | python3 -
```

2. Установите зависимости проекта:
```sh
# Перейдите в директорию проекта
cd materials

# Установите зависимости
poetry install

# Активируйте виртуальное окружение
poetry shell
```

3. Альтернативная установка через pip:
```sh
# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```



## Версии

- 0.2.09 - Текущая версия
- Поддержка SQLite
- Основные CRUD операции
- Доступ к характеристикам материалов

## Переменные окружения
* DATABASE_URL: URL для подключения к базе данных. По умолчанию используется SQLite (sqlite:///materials.db).
* SQLALCHEMY_ECHO: Устанавливает уровень вывода для SQLAlchemy (True или False). Используйте для включения/отключения вывода SQL-запросов.

## Вклад в проект

1. Создайте форк проекта
2. Создайте ветку для ваших изменений
3. Внесите изменения
4. Отправьте pull request

Пожалуйста, убедитесь, что ваши изменения:
- Сопровождаются тестами
- Следуют существующему стилю кода
- Обновляют документацию при необходимости
