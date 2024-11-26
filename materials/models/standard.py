#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Этот модуль определяет модель `Standard`, представляющую таблицу с информацией о стандартах материалов в базе данных.
Модель используется для хранения данных о стандартах, применяемых к каждому материалу.

Поля модели:
- `id` (Integer): Первичный ключ, автоматически увеличивается.
- `material_name` (String): Название материала, для которого применяется стандарт.
- `standard` (String): Стандарт, применяемый к материалу (например, ГОСТ, ТУ).

Использование:
Модель `Standard` используется для хранения стандартов материалов. Пример создания экземпляра и добавления его в базу
данных:

    from materials.models import Standard
    from sqlalchemy.orm import Session

    new_standard = Standard(
        material_name="03Н12Х5М3ТЛ",
        standard="ГОСТ 977 - 88"
    )
    db_session = Session(bind=engine)
    db_session.add(new_standard)
    db_session.commit()

Это позволяет добавлять в базу данных информацию о стандартах материалов и связывать их с соответствующими названиями
материалов.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Standard(Base):
    __tablename__ = 'standards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_name = Column(String, nullable=False)
    standard = Column(String, nullable=False)

    chemical_compositions = relationship("ChemicalComposition", back_populates="standard", lazy='dynamic')

    def __repr__(self):
        return f"<Standard(id={self.id}, material_name={self.material_name}, standard={self.standard})>"
