#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Этот модуль определяет модель `Material`, представляющую таблицу с информацией о материалах в базе данных. Модель
используется для хранения данных о различных материалах, их классификации и подклассах, а также для установления связей
с другими характеристиками материалов.

Поля модели:
- `id` (Integer): Первичный ключ, автоматически увеличивается.
- `brand` (String): Название или бренд материала, уникальное значение.
- `class_of_material` (String): Класс материала, определяющий его основные свойства.
- `subclass_of_material` (String): Подкласс материала, уточняющий свойства материала.

Связи:
- `chemical_composition`: Связь один-к-одному с моделью `ChemicalComposition`, представляющей химический состав
материала.
- `hardness`: Связь один-к-одному с моделью `Hardness`, представляющей значение твердости материала.
- `technological_properties`: Связь один-к-одному с моделью `TechnologicalProperties`, представляющей технологические
свойства материала.
- `mechanical_properties`: Связь один-к-одному с моделью `MechanicalProperties`, представляющей механические свойства
материала.
- `characteristics`: Связь один-к-одному с моделью `CharacteristicsOfMaterial`, представляющей дополнительные
характеристики материала.
- `material_indices`: Связь один-к-одному с моделью `MaterialIndices`, представляющей индексы материалов.

Использование:
Модель `Material` используется для хранения информации о материалах. Пример создания экземпляра и добавления его в
базу данных:

    from materials.models import Material
    from sqlalchemy.orm import Session

    new_material = Material(
        brand="SteelX",
        class_of_material="Steel",
        subclass_of_material="Carbon Steel"
    )
    db_session = Session(bind=engine)
    db_session.add(new_material)
    db_session.commit()

Это позволяет добавлять в базу данных информацию о различных материалах и связывать их с характеристиками, такими как
химический состав, твердость и другие свойства.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String, nullable=False, unique=True)
    class_of_material = Column(String, nullable=False)
    subclass_of_material = Column(String)

    chemical_composition = relationship("ChemicalComposition", back_populates="material")
    hardness = relationship("Hardness", back_populates="material")
    technological_properties = relationship("TechnologicalProperties", back_populates="material")
    mechanical_properties = relationship("MechanicalProperties", back_populates="material")
    characteristics = relationship("CharacteristicsOfMaterial", back_populates="material")
    material_indices = relationship("MaterialIndices", back_populates="material")

    def __repr__(self):
        return f"<Material(id={self.id}, brand={self.brand}, class_of_material={self.class_of_material})>"
