#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Этот модуль определяет модель `CharacteristicsOfMaterial`, представляющую таблицу с дополнительными характеристиками
материалов в базе данных. Модель используется для хранения информации о классификации, применении, иностранных аналогах,
дополнительной информации и замене для каждого материала.

Поля модели:
- `id` (Integer): Первичный ключ, автоматически увеличивается.
- `material_id` (Integer): Внешний ключ, ссылающийся на таблицу `materials`, указывающий на соответствующий материал.
- `classification` (String): Классификация материала.
- `application` (String): Применение материала.
- `foreign_analogs` (String): Иностранные аналоги материала.
- `additional_info` (String): Дополнительная информация о материале.
- `replacement` (String): Возможная замена материала.

Связи:
- `material`: Связь один-к-одному с моделью `Material`, которая указывает на соответствующий материал.

Использование:
Модель `CharacteristicsOfMaterial` используется для хранения дополнительных характеристик материалов. Пример создания
экземпляра и добавления его в базу данных:

    from materials.models import CharacteristicsOfMaterial
    from sqlalchemy.orm import Session

    new_characteristics = CharacteristicsOfMaterial(
        material_id=1,
        classification="A",
        application="Construction",
        foreign_analogs="Analog X",
        additional_info="Some additional info",
        replacement="Material Y"
    )
    db_session = Session(bind=engine)
    db_session.add(new_characteristics)
    db_session.commit()

Это позволяет добавлять в базу данных информацию о характеристиках материалов и связывать их с соответствующими записями
в таблице `materials`.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class CharacteristicsOfMaterial(Base):
    __tablename__ = 'characteristics_of_material'

    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    classification = Column(String, nullable=True)
    application = Column(String, nullable=True)
    foreign_analogs = Column(String, nullable=True)
    additional_info = Column(String, nullable=True)
    replacement = Column(String, nullable=True)

    material = relationship("Material", back_populates="characteristics")

    def __repr__(self):
        return f"<CharacteristicsOfMaterial(id={self.id}, material_id={self.material_id}, " \
               f"classification={self.classification}, application={self.application}, " \
               f"foreign_analogs={self.foreign_analogs}, additional_info={self.additional_info}, " \
               f"replacement={self.replacement})>"
