#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Этот модуль определяет модель `MaterialIndices`, представляющую таблицу с информацией об индексах материалов в базе
данных. Модель используется для хранения данных об индексах классов материалов, связанных с таблицей `materials`.

Поля модели:
- `id` (Integer): Первичный ключ, автоматически увеличивается.
- `material_id` (Integer): Внешний ключ, ссылающийся на таблицу `materials`, указывающий на соответствующий материал.
- `index_of_material_class` (Integer): Индекс класса материала.

Связи:
- `material`: Связь один-к-одному с моделью `Material`, которая указывает на соответствующий материал.

Использование:
Модель `MaterialIndices` используется для хранения индексов материалов. Пример создания экземпляра и добавления его в
базу данных:

    from materials.models import MaterialIndices
    from sqlalchemy.orm import Session

    new_material_index = MaterialIndices(
        material_id=1,
        index_of_material_class=4
    )
    db_session = Session(bind=engine)
    db_session.add(new_material_index)
    db_session.commit()

Это позволяет добавлять в базу данных информацию об индексах материалов и связывать их с соответствующими записями в
таблице `materials`.
"""

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class MaterialIndices(Base):
    __tablename__ = 'material_indices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    index_of_material_class = Column(Integer, nullable=False)

    material = relationship("Material", back_populates="material_indices")

    def __repr__(self):
        return f"<MaterialIndices(id={self.id}, material_id={self.material_id}, " \
               f"index_of_material_class={self.index_of_material_class})>"
