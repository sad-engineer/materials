#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable, Union
from materials.obj.creators import Creator
from materials.obj.constants import CLASSES_MATERIALS


class Lister:
    def __init__(self, creator: Callable[..., Creator]):
        self._creator = creator

    def by_class(self, any_class: Union[str, int]) -> list:
        if isinstance(any_class, int):
            return [material for material in self._creator().create_all if material.class_ == any_class]
        return [material for material in self._creator().create_all if material.class_ == CLASSES_MATERIALS[any_class]]

    def by_subclass(self, any_subclass: str) -> list:
        return [material for material in self._creator().create_all if material.subclass == any_subclass]

    @property
    def all(self) -> list:
        return [material for material in self._creator().create_all]
