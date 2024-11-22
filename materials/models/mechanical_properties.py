#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Этот модуль определяет модель `MechanicalProperties`, представляющую таблицу с информацией о механических свойствах
материалов в базе данных. Модель используется для хранения данных, таких как предел прочности, предел текучести,
относительное удлинение и другие параметры для каждого материала.

Поля модели:
- `id` (Integer): Первичный ключ, автоматически увеличивается.
- `material_id` (Integer): Внешний ключ, ссылающийся на таблицу `materials`, указывающий на соответствующий материал.
- `tensile_strength` (Float): Предел прочности материала на растяжение.
- `yield_strength` (Float): Предел текучести материала.
- `elongation_at_break` (Float): Относительное удлинение при разрыве.
- `relative_narrowing` (Float): Относительное сужение поперечного сечения.
- `impact_strength` (Float): Ударная вязкость материала.

Связи:
- `material`: Связь один-к-одному с моделью `Material`, которая указывает на соответствующий материал.

Использование:
Модель `MechanicalProperties` используется для хранения механических свойств материалов. Пример создания экземпляра и
добавления его в базу данных:

    from materials.models import MechanicalProperties
    from sqlalchemy.orm import Session

    new_mechanical_properties = MechanicalProperties(
        material_id=1,
        tensile_strength=400.0,
        yield_strength=250.0,
        elongation_at_break=20.0,
        relative_narrowing=30.0,
        impact_strength=50.0
    )
    db_session = Session(bind=engine)
    db_session.add(new_mechanical_properties)
    db_session.commit()

Это позволяет добавлять в базу данных информацию о механических свойствах материалов и связывать их с соответствующими
записями в таблице `materials`.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class MechanicalProperties(Base):
    __tablename__ = 'mechanical_properties'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    tensile_strength = Column(String, nullable=True)
    yield_strength = Column(String, nullable=True)
    elongation_at_break = Column(String, nullable=True)
    relative_narrowing = Column(String, nullable=True)
    impact_strength = Column(String, nullable=True)

    material = relationship("Material", back_populates="mechanical_properties")

    def __repr__(self):
        return f"<MechanicalProperties(id={self.id}, material_id={self.material_id}, tensile_strength={self.tensile_strength}, yield_strength={self.yield_strength}, elongation_at_break={self.elongation_at_break}, relative_narrowing={self.relative_narrowing}, impact_strength={self.impact_strength})>"
