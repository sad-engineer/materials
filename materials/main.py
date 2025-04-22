#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Основной модуль для запуска приложения материалов.
Этот файл содержит основную логику для работы с базой данных, используя модели и функции CRUD.
"""
import os

# Настройка логирования
os.environ["SQLALCHEMY_ECHO"] = "False"


from materials import (
    get_all_brands, 
    get_brands_by_material_class_index, 
    get_chemical_composition_by_brand, 
    get_standard_of_chemical_composition_by_brand
)


def main():
    # Получение всех брендов
    all_brands = get_all_brands()
    print("Все бренды:", all_brands)

    # Получение брендов по index_of_material_class
    index = 4
    brands_by_index = get_brands_by_material_class_index(index)
    print(f"Бренды с index_of_material_class = {index}:", brands_by_index)

    brand = "30ХМА"
    chemical_composition = get_chemical_composition_by_brand(brand=brand)
    print(f"Хим.состав материала {brand}:", chemical_composition)
    standard = get_standard_of_chemical_composition_by_brand(brand)
    if standard:
        print(f"по стандарту:", standard)


if __name__ == "__main__":
    main()  
