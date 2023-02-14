#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable
from materials.obj.creators import Creator


class Lister:
    def __init__(self, creator: Callable[..., Creator]):
        self._creator = creator

    # def by_marking_and_stand(self, marking: str, standard: str) -> list:
    #     return [tool for tool in self._tool_creator().by_marking_and_stand(marking, standard)]
    #
    # def by_marking(self, marking: str) -> list:
    #     return [tool for tool in self._tool_creator().by_marking(marking)]
    #
    # def by_stand(self, standard: str) -> list:
    #     return [tool for tool in self._tool_creator().by_stand(standard)]

    @property
    def all(self) -> list:
        return [material for material in self._creator().create_all]
