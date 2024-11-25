#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Этот модуль инициализации позволяет импортировать все компоненты пакета `materials` из одного места. Он включает в себя
подключение к базе данных, все модели данных и функции для выполнения CRUD операций.

Импортируя `materials`, вы получаете доступ ко всем компонентам, необходимым для работы с материалами, включая базы
данных и модели.

Основные компоненты:
- Модели: Base, Material, MaterialIndices, Hardness, ChemicalComposition, TechnologicalProperties,
MechanicalProperties, CharacteristicsOfMaterial.
- Функции CRUD: get_material_by_brand, get_hardness_by_brand, get_chemical_composition_by_brand,
get_technological_properties_by_brand, get_mechanical_properties_by_brand,
get_characteristics_by_brand, query_data_example.
- Подключение к базе данных: SessionLocal, engine.

Пример использования:
    from materials import SessionLocal, Material, get_material_by_brand

    # Создание сессии
    db = SessionLocal()
    # Получение материала по бренду
    material = get_material_by_brand("SteelX", db)
    print(material)
"""
import os

from .database import SessionLocal, engine
from .models import (
    Base,
    Material,
    MaterialIndices,
    Hardness,
    ChemicalComposition,
    TechnologicalProperties,
    MechanicalProperties,
    CharacteristicsOfMaterial
)
from .crud import (
    get_material_by_brand,
    get_material_class_index_by_id,
    get_hardness_by_brand,
    get_chemical_composition_by_brand,
    get_technological_properties_by_brand,
    get_mechanical_properties_by_brand,
    get_characteristics_by_brand,
    get_all_brands,
    get_brands_by_material_class_index,
)

# Настройка логирования пакета
os.environ["SQLALCHEMY_ECHO"] = "False"

# Экспортируем все функции, чтобы они были доступны через `import materials`
__all__ = [
    "get_material_by_brand",
    "get_material_class_index_by_id",
    "get_hardness_by_brand",
    "get_chemical_composition_by_brand",
    "get_technological_properties_by_brand",
    "get_mechanical_properties_by_brand",
    "get_characteristics_by_brand",
    "get_all_brands",
    "get_brands_by_material_class_index",
]
