#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Основной модуль для запуска приложения материалов.
Этот файл содержит основную логику для работы с базой данных, используя модели и функции CRUD.
"""
import os

from materials import get_all_brands, get_brands_by_material_class_index

# Настройка логирования
os.environ["SQLALCHEMY_ECHO"] = "False"


def main():
    # Получение всех брендов
    all_brands = get_all_brands()
    print("Все бренды:", all_brands)

    # Получение брендов по index_of_material_class
    index = 4
    brands_by_index = get_brands_by_material_class_index(index)
    print(f"Бренды с index_of_material_class = {index}:", brands_by_index)


if __name__ == "__main__":
    main()
