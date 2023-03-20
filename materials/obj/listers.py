#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Callable

from service import logged
from service import output_debug_message_for_init_method as debug_message_for_init

from materials.obj.creators import Creator
from materials.obj.constants import CLASSES_MATERIALS
from materials.obj.finders import Finder
from materials.obj.fields_types import InMaterialClass


def output_debug_message(message: str):
    """ Выводит в лог сообщение message"""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            self.debug(message) if message.find("{") == -1 else self.debug(
                message.format('; '.join([f'{k}= {v}' for k, v in kwargs.items()])))
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


@logged
class Lister:
    @debug_message_for_init()
    def __init__(self, creator: Callable[..., Creator], materials_finder: Callable[..., Finder]):
        self._creator = creator()
        self._finder = materials_finder()

    @output_debug_message("Создание списка доступных материалов по классу {}")
    def by_class(self, any_class: InMaterialClass) -> list:
        self._finder._verbose = False
        if isinstance(any_class, int):
            any_class = CLASSES_MATERIALS[any_class]
        return [self._creator.create(record['brand']) for record in self._finder.all
                if record['class_of_material'] == any_class]

    @output_debug_message("Создание списка доступных материалов по подклассу {}")
    def by_subclass(self, any_subclass: str) -> list:
        self._finder._verbose = False
        return [self._creator.create(record['brand']) for record in self._finder.all
                if record['subclass_of_material'] == any_subclass]

    @property
    @output_debug_message("Создание списка всех доступных материалов")
    def all(self) -> list:
        self._finder._verbose = False
        return [self._creator.create(record['brand']) for record in self._finder.all]
