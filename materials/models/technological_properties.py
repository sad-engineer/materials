#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Этот модуль определяет модель `TechnologicalProperties`, представляющую таблицу с информацией о технологических
свойствах материалов в базе данных. Модель используется для хранения данных о таких свойствах, как свариваемость,
чувствительность к растрескиванию и склонность к отпускной хрупкости.

Поля модели:
- `id` (Integer): Первичный ключ, автоматически увеличивается.
- `material_id` (Integer): Внешний ключ, ссылающийся на таблицу `materials`, указывающий на соответствующий материал.
- `weldability` (String): Свариваемость материала.
- `flock_sensitivity` (String): Чувствительность к растрескиванию.
- `temper_brittleness` (String): Склонность к отпускной хрупкости.

Связи:
- `material`: Связь один-к-одному с моделью `Material`, которая указывает на соответствующий материал.

Использование:
Модель `TechnologicalProperties` используется для хранения технологических свойств материалов. Пример создания
экземпляра и добавления его в базу данных:

    from materials.models import TechnologicalProperties
    from sqlalchemy.orm import Session

    new_technological_properties = TechnologicalProperties(
        material_id=1,
        weldability="Good",
        flock_sensitivity="Low",
        temper_brittleness="Medium"
    )
    db_session = Session(bind=engine)
    db_session.add(new_technological_properties)
    db_session.commit()

Это позволяет добавлять в базу данных информацию о технологических свойствах материалов и связывать их с
соответствующими записями в таблице `materials`.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class TechnologicalProperties(Base):
    __tablename__ = 'technological_properties'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    weldability = Column(String, nullable=True)
    flock_sensitivity = Column(String, nullable=True)
    temper_brittleness = Column(String, nullable=True)

    material = relationship("Material", back_populates="technological_properties")

    def __repr__(self):
        return f"<TechnologicalProperties(id={self.id}, material_id={self.material_id}, " \
               f"weldability={self.weldability}, flock_sensitivity={self.flock_sensitivity}, " \
               f"temper_brittleness={self.temper_brittleness})>"
