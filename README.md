# materials

`materials` - это пакет Python для работы с базой данных материалов. Пакет предоставляет простой доступ к информации о материалах, включая их характеристики, химический состав, механические и технологические свойства. Основная цель пакета - упростить взаимодействие с базой данных материалов через функции, выполняющие CRUD-операции.

## Установка

Для установки пакета `materials` используйте команду:

```sh
pip install git+https://github.com/sad-engineer/materials.git
```

## Подготовка базы данных

База данных устанавливается вместе с пакетом, и настройка не требуется. Пакет поддерживает базу данных SQLite по умолчанию, но можно указать другой URL базы данных через переменную окружения DATABASE_URL.

## Использование

Ниже приведен пример использования пакета materials для получения информации о материалах.

```sh
from materials import get_all_brands, get_brands_by_material_class_index, get_chemical_composition_by_brandget_chemical_composition_by_brand

# Получение всех наименований материалов
all_brands = get_all_brands()
print("Все бренды:", all_brands)

# Получение наименований по индексу класса материала
index = 4
brands_by_index = get_brands_by_material_class_index(index)
print(f"Бренды с index_of_material_class = {index}:", brands_by_index)

brand = "30ХМА"
# Получение хим состава по наименованию материала
chemical_composition = get_chemical_composition_by_brand(brand=brand)
print(f"Хим.состав материала {brand}:", chemical_composition)
standard = chemical_composition.standard.standard
if standard:
    print(f"по стандарту:", standard)
```

## Пример содержимого main.py

```sh
import os
from materials import get_all_brands, get_brands_by_material_class_index, get_chemical_composition_by_brand

# Отключение echo при запуске main.py
os.environ["SQLALCHEMY_ECHO"] = "False"

def main():
    # Получение всех наименований материалов
    all_brands = get_all_brands()
    print("Все бренды:", all_brands)
    
    # Получение наименований по индексу класса материала
    index = 4
    brands_by_index = get_brands_by_material_class_index(index)
    print(f"Бренды с index_of_material_class = {index}:", brands_by_index)
    
    brand = "30ХМА"
    # Получение хим состава по наименованию материала
    chemical_composition = get_chemical_composition_by_brand(brand=brand)
    print(f"Хим.состав материала {brand}:", chemical_composition)
    standard = chemical_composition.standard.standard
    if standard:
        print(f"по стандарту:", standard)


if __name__ == "__main__":
    main()
```

## Настройка параметра echo для SQLAlchemy

Параметр echo управляет выводом SQL-запросов в консоль. Вы можете управлять этим параметром, используя переменную окружения SQLALCHEMY_ECHO.
* При запуске main.py echo отключен (False).
* При использовании функций из пакета materials echo можно включить, установив переменную окружения:

```sh
import os

# Включение echo при работе с пакетом materials
os.environ["SQLALCHEMY_ECHO"] = "True"
from materials import get_all_brands

all_brands = get_all_brands()
print("Все бренды:", all_brands)
```

## Переменные окружения
* DATABASE_URL: URL для подключения к базе данных. По умолчанию используется SQLite (sqlite:///materials.db).
* SQLALCHEMY_ECHO: Устанавливает уровень вывода для SQLAlchemy (True или False). Используйте для включения/отключения вывода SQL-запросов.

## Лицензия
* Подробности смотрите в файле LICENSE.
