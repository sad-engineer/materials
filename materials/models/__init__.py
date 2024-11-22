#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Этот модуль предоставляет доступ ко всем моделям базы данных, используемым в проекте. Все модели наследуют `Base`, что
позволяет SQLAlchemy управлять таблицами базы данных.

Модели:
- Base: Базовый класс для всех моделей.
- Material: Представляет материалы, содержащие информацию о бренде, классе и подклассе материала.
- MaterialIndices: Содержит индексы материалов, связывающиеся с `Material` по внешнему ключу.
- Hardness: Содержит информацию о твердости материала.
- ChemicalComposition: Содержит химический состав материала, включая различные элементы.
- TechnologicalProperties: Содержит технологические свойства материала, такие как свариваемость, чувствительность к
    растрескиванию и т.д.
- MechanicalProperties: Содержит механические свойства материала, включая предел прочности и относительное удлинение.
- CharacteristicsOfMaterial: Содержит дополнительные характеристики материала, такие как применение, классификация и
    иностранные аналоги.

Использование:
Этот модуль можно использовать для импорта всех моделей в других частях проекта. Пример:

    from materials.models import Material, Hardness

Это упростит работу с различными таблицами базы данных и обеспечит удобство использования всех моделей.
"""
from .base import Base
from .material import Material
from .material_indices import MaterialIndices
from .hardness import Hardness
from .chemical_composition import ChemicalComposition
from .technological_properties import TechnologicalProperties
from .mechanical_properties import MechanicalProperties
from .characteristics import CharacteristicsOfMaterial
