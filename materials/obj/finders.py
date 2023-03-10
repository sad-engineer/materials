#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Any

from service import RecordRequester
from service import logged


@logged
class Finder:
    """ Ищет записи в БД по конкретным параметрам."""

    def __init__(self, record_requester: RecordRequester):
        self._requester = record_requester

        self.debug(f"""Создан {self.__class__.__name__} со следующими зависимостями: {record_requester=}""")

    def by_brand(self, brand: str) -> Any:
        """ Возвращает найденные записи по наименованию материала. Формат возвращаемых данных определяет self._requester

        Parameters:
        brand : str : Наименование материала
        """
        records = self._requester.get_records({"brand": brand})
        self.debug(f"""По ключу {brand=} найдено записей: {len(records)}""")
        return records if records else None

    @property
    def all(self) -> Any:
        """ Возвращает все записи. Формат возвращаемых данных определяет self._requester."""
        for index, record in self._requester.get_all_records.items():
            yield record

    @property
    def available_values(self) -> Any:
        """ Возвращает наборы доступных в таблице БД значений по категориям."""
        return self._requester.available_values
