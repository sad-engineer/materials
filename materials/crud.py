#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Документация:
Этот модуль содержит функции для выполнения CRUD операций (создание, чтение, обновление, удаление) с базой данных
материалов. Функции предназначены для получения информации о материалах, таких как твердость, химический состав,
технологические и механические свойства.

Основные функции:
- `get_material_by_brand(brand, db)`: Проверяет существование материала по бренду и возвращает объект `Material`.
- `get_material_class_index_by_id(index_id, db)`: Получает индекс класса материала по идентификатору.
- `get_hardness_by_brand(brand, db)`: Возвращает информацию о твердости материала по бренду.
- `get_chemical_composition_by_brand(brand, db)`: Возвращает химический состав материала по бренду.
- `get_technological_properties_by_brand(brand, db)`: Возвращает технологические свойства материала по бренду.
- `get_mechanical_properties_by_brand(brand, db)`: Возвращает механические свойства материала по бренду.
- `get_characteristics_by_brand(brand, db)`: Возвращает дополнительные характеристики материала по бренду.
- `query_data_example(brand, db)`: Пример вызова функций для запроса данных по бренду.

Использование этих функций помогает упростить работу с базой данных и предоставляет удобные методы для доступа к
различным свойствам материалов.
"""

from sqlalchemy.orm import Session
from typing import Optional
from materials.models import Material, MaterialIndices, Hardness, ChemicalComposition, TechnologicalProperties, \
    MechanicalProperties, CharacteristicsOfMaterial
from materials.database import SessionLocal


# Функция для проверки существования материала по бренду
def get_material_by_brand(brand: str, db: Session = SessionLocal()) -> Optional[Material]:
    material = db.query(Material).filter(Material.brand == brand).first()
    if not material:
        print(f"Материал с брендом '{brand}' не найден.")
        return None
    return material


# Функция для получения индекса класса материала по идентификатору
def get_material_class_index_by_id(index_id: int, db: Session = SessionLocal()) -> Optional[MaterialIndices]:
    material_class_index = db.query(MaterialIndices).filter(MaterialIndices.id == index_id).first()
    if not material_class_index:
        print(f"Индекс класса материала с id '{index_id}' не найден.")
        return None
    return material_class_index


# Функция для запроса данных из таблицы Hardness
def get_hardness_by_brand(brand: str, db: Session = SessionLocal()):
    material = get_material_by_brand(brand, db)
    if not material:
        return None
    hardness = db.query(Hardness).filter(Hardness.material_id == material.id).first()
    return hardness


# Функция для запроса данных из таблицы ChemicalComposition
def get_chemical_composition_by_brand(brand: str, db: Session = SessionLocal()):
    material = get_material_by_brand(brand, db)
    if not material:
        return None
    chemical_composition = db.query(ChemicalComposition).filter(ChemicalComposition.material_id == material.id).first()
    return chemical_composition


# Функция для запроса данных из таблицы TechnologicalProperties
def get_technological_properties_by_brand(brand: str, db: Session = SessionLocal()):
    material = get_material_by_brand(brand, db)
    if not material:
        return None
    technological_properties = db.query(TechnologicalProperties).filter(
        TechnologicalProperties.material_id == material.id).first()
    return technological_properties


# Функция для запроса данных из таблицы MechanicalProperties
def get_mechanical_properties_by_brand(brand: str, db: Session = SessionLocal()):
    material = get_material_by_brand(brand, db)
    if not material:
        return None
    mechanical_properties = db.query(MechanicalProperties).filter(
        MechanicalProperties.material_id == material.id).first()
    return mechanical_properties


# Функция для запроса данных из таблицы CharacteristicsOfMaterial
def get_characteristics_by_brand(brand: str, db: Session = SessionLocal()):
    material = get_material_by_brand(brand, db)
    if not material:
        return None
    characteristics = db.query(CharacteristicsOfMaterial).filter(
        CharacteristicsOfMaterial.material_id == material.id).first()
    return characteristics


# Пример вызова функции для запроса данных
def query_data_example(brand: str, db: Session = SessionLocal()):
    try:
        material = get_material_by_brand(brand, db)
        if material:
            print(f"Material: {material.brand}, Class: {material.class_of_material}")

        hardness = get_hardness_by_brand(brand, db)
        if hardness:
            print(f"Hardness: {hardness.hardness_value}")

        chemical_composition = get_chemical_composition_by_brand(brand, db)
        if chemical_composition:
            print(f"Chemical Composition - C: {chemical_composition.C}, Si: {chemical_composition.Si}")

        technological_properties = get_technological_properties_by_brand(brand, db)
        if technological_properties:
            print(f"Weldability: {technological_properties.weldability}")

        mechanical_properties = get_mechanical_properties_by_brand(brand, db)
        if mechanical_properties:
            print(f"Tensile Strength: {mechanical_properties.tensile_strength}")

        characteristics = get_characteristics_by_brand(brand, db)
        if characteristics:
            print(f"Application: {characteristics.application}")

    except Exception as e:
        print(f"Ошибка при выполнении запроса данных: {e}")
    finally:
        db.close()
