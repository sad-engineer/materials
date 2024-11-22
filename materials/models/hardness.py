#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Этот модуль определяет модель `Hardness`, представляющую таблицу с информацией о твердости материалов в базе данных.
Модель используется для хранения данных о твердости каждого материала, связанного с таблицей `materials`.

Поля модели:
- `id` (Integer): Первичный ключ, автоматически увеличивается.
- `material_id` (Integer): Внешний ключ, ссылающийся на таблицу `materials`, указывающий на соответствующий материал.
- `hardness_value` (Float): Значение твердости материала.

Связи:
- `material`: Связь один-к-одному с моделью `Material`, которая указывает на соответствующий материал.

Использование:
Модель `Hardness` используется для хранения значений твердости материалов. Пример создания экземпляра и добавления его
в базу данных:

    from materials.models import Hardness
    from sqlalchemy.orm import Session

    new_hardness = Hardness(
        material_id=1,
        hardness_value=150.0
    )
    db_session = Session(bind=engine)
    db_session.add(new_hardness)
    db_session.commit()

Это позволяет добавлять в базу данных информацию о твердости материалов и связывать их с соответствующими записями в
таблице `materials`.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Hardness(Base):
    __tablename__ = 'hardness'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    hardness_value = Column(String, nullable=False)

    material = relationship("Material", back_populates="hardness")

    def __repr__(self):
        return f"<Hardness(id={self.id}, material_id={self.material_id}, hardness_value={self.hardness_value})>"
