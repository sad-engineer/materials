#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable, Union
from materials.obj.creators import Creator
from materials.obj.constants import CLASSES_MATERIALS
from service import logged


@logged
class Lister:
    def __init__(self, creator: Callable[..., Creator]):
        self._creator = creator
        self.debug(f"""Создан {self.__class__.__name__} со следующими зависимостями: {creator=}""")

    def by_class(self, any_class: Union[str, int]) -> list:
        self.debug(f"""Создаем список доступных материалов по классу {any_class}""")
        if isinstance(any_class, int):
            return [material for material in self._creator().create_all if material.class_ == any_class]
        return [material for material in self._creator().create_all if material.class_ == CLASSES_MATERIALS[any_class]]

    def by_subclass(self, any_subclass: str) -> list:
        self.debug(f"""Создаем список доступных материалов по подклассу {any_subclass}""")
        return [material for material in self._creator().create_all if material.subclass == any_subclass]

    @property
    def all(self) -> list:
        self.debug(f"""Создаем список всех доступных материалов""")
        materials = self._creator()._materials.all
        return [self._creator().create(material['brand']) for material in materials]
