#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Документация:
Этот модуль определяет модель `ChemicalComposition`, представляющую таблицу с химическим составом материалов в базе
данных.
Модель используется для хранения информации о содержании различных химических элементов в каждом материале.

Поля модели:
- `id` (Integer): Первичный ключ, автоматически увеличивается.
- `material_id` (Integer): Внешний ключ, ссылающийся на таблицу `materials`, указывающий на соответствующий материал.
- `Ag`, `Al`, `Al_and_Mg`, ..., `Zr`, `Impurities`, `Rare_Earth_elements` (String): Содержание различных химических
  элементов и характеристик, связанных с материалом. Каждое поле представляет определенный элемент или характеристику.

Связи:
- `material`: Связь один-к-одному с моделью `Material`, которая указывает на соответствующий материал.

Использование:
Модель `ChemicalComposition` используется для хранения химического состава материалов. Пример создания экземпляра и
добавления его в базу данных:

    from materials.models import ChemicalComposition
    from sqlalchemy.orm import Session

    new_composition = ChemicalComposition(
        material_id=1,
        C="0.3",
        Si="0.2",
        Mn="1.0"
    )
    db_session = Session(bind=engine)
    db_session.add(new_composition)
    db_session.commit()

Это позволяет добавлять в базу данных информацию о химическом составе материалов и связывать их с соответствующими
записями в таблице `materials`.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class ChemicalComposition(Base):
    __tablename__ = 'chemical_composition'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    standard_id = Column(Integer, ForeignKey('standards.id'), nullable=True)

    Ag = Column(String)
    Al = Column(String)
    Al_and_Mg = Column(String)
    Arsenicum = Column(String)
    B = Column(String)
    Ba = Column(String)
    Be = Column(String)
    Bi = Column(String)
    C = Column(String)
    Ca = Column(String)
    Cd = Column(String)
    Ce = Column(String)
    Co = Column(String)
    Cr = Column(String)
    Cu = Column(String)
    Cu_and_Ag = Column(String)
    Cu_and_P = Column(String)
    F = Column(String)
    Fe = Column(String)
    Ga = Column(String)
    Hf = Column(String)
    La = Column(String)
    Li = Column(String)
    Mg = Column(String)
    Mn = Column(String)
    Mo = Column(String)
    N = Column(String)
    Na = Column(String)
    Nb = Column(String)
    Ni = Column(String)
    Ni_and_Co = Column(String)
    O = Column(String)
    Other = Column(String)
    P = Column(String)
    Pb = Column(String)
    S = Column(String)
    Sb = Column(String)
    Sc = Column(String)
    Se = Column(String)
    Si = Column(String)
    Sn = Column(String)
    Sr = Column(String)
    Ta = Column(String)
    Te = Column(String)
    Ti = Column(String)
    V = Column(String)
    W = Column(String)
    Y = Column(String)
    Zn = Column(String)
    Zr = Column(String)
    Impurities = Column(String)
    Rare_Earth_elements = Column(String)

    material = relationship("Material", back_populates="chemical_composition")
    standard = relationship("Standard", back_populates="chemical_compositions")

    def __repr__(self):
        attrs = {key: value for key, value in self.__dict__.items() if
                 value is not None and key != '_sa_instance_state' and key != 'material_id' and key != 'standard_id'}
        return f"<ChemicalComposition({', '.join([f'{key}={value}' for key, value in attrs.items()])})>"
