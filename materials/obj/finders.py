#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Any, Callable

from service import RecordRequester
from service import logged
from service import output_debug_message_for_init_method as debug_message_for_init


def output_debug_message_with_kwargs_and_length(message: str):
    """ Выводит в лог сообщение message"""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.debug(message) if message.find("{") == -1 else self.debug(
                message.format(self.__class__.__name__, '; '.join([f'{k}= {v}' for k, v in kwargs.items()]), len(result)))
            return result
        return wrapper
    return decorator


def output_debug_message_with_with_length(message: str):
    """ Выводит в лог сообщение message"""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.debug(message) if message.find("{") == -1 else self.debug(
                message.format(self.__class__.__name__, len(result)))
            return result
        return wrapper
    return decorator


@logged
class Finder:
    """ Ищет записи в БД по конкретным параметрам."""
    @debug_message_for_init()
    def __init__(self, record_requester: Callable[..., RecordRequester]):
        self._requester = record_requester()

    @output_debug_message_with_kwargs_and_length("{0} по ключу {1} нашел записей: {2}")
    def by_brand(self, brand: str) -> Any:
        """ Возвращает найденные записи по наименованию материала. Формат возвращаемых данных определяет self._requester

        Parameters:
            brand : str : Наименование материала
        """
        records = self._requester.get_records({"brand": brand})
        return records if records else None

    @property
    @output_debug_message_with_with_length("{0} ищет все записи таблицы. Найдено записей: {1}")
    def all(self) -> Any:
        """ Возвращает все записи. Формат возвращаемых данных определяет self._requester."""
        for index, record in self._requester.get_all_records.items():
            yield record

    @property
    def available_values(self) -> Any:
        """ Возвращает наборы доступных в таблице БД значений по категориям."""
        return self._requester.available_values


# =====================================================================================================================
# Этот класс создан для читаемости debug сообщений
class MaterialCharacteristicsFinder(Finder):
    """ Ищет записи в БД по конкретным параметрам в таблице характеристик материалов"""
    def __init__(self, record_requester: Callable[..., RecordRequester]):
        super().__init__(record_requester=record_requester)


# Этот класс создан для читаемости debug сообщений
class MaterialChemicalCompositionFinder(Finder):
    """ Ищет записи в БД по конкретным параметрам в таблице химсостава"""
    def __init__(self, record_requester: Callable[..., RecordRequester]):
        super().__init__(record_requester=record_requester)


# Этот класс создан для читаемости debug сообщений
class MaterialHardnessFinder(Finder):
    """ Ищет записи в БД по конкретным параметрам в таблице твердости"""
    def __init__(self, record_requester: Callable[..., RecordRequester]):
        super().__init__(record_requester=record_requester)


# Этот класс создан для читаемости debug сообщений
class MaterialsFinder(Finder):
    """ Ищет записи в БД по конкретным параметрам в таблице общих характеристик материалов"""
    def __init__(self, record_requester: Callable[..., RecordRequester]):
        super().__init__(record_requester=record_requester)


# Этот класс создан для читаемости debug сообщений
class MaterialMechanicalPropertiesFinder(Finder):
    """ Ищет записи в БД по конкретным параметрам в таблице механических свойств"""
    def __init__(self, record_requester: Callable[..., RecordRequester]):
        super().__init__(record_requester=record_requester)


# Этот класс создан для читаемости debug сообщений
class MaterialTechnologicalPropertiesFinder(Finder):
    """ Ищет записи в БД по конкретным параметрам в таблице технических свойств"""

    def __init__(self, record_requester: Callable[..., RecordRequester]):
        super().__init__(record_requester=record_requester)
