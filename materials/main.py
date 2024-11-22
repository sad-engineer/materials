#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Основной модуль для запуска приложения материалов.
Этот файл содержит основную логику для работы с базой данных, используя модели и функции CRUD.
"""

from sqlalchemy.orm import Session
from materials.database import SessionLocal, engine
from materials.models.base import Base
from materials.models import Material
from materials.crud import (
    get_material_by_brand,
    get_hardness_by_brand,
    get_chemical_composition_by_brand,
    get_technological_properties_by_brand,
    get_mechanical_properties_by_brand,
    get_characteristics_by_brand,
    query_data_example
)


def main():
    # Создание сессии
    db: Session = SessionLocal()
    try:
        # Пример вызова функции для получения данных по бренду
        brand = "20"
        query_data_example(brand, db)

    except Exception as e:
        db.rollback()
        print(f"Произошла ошибка: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
