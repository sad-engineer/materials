#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
from typing import Any

from service import RecordRequester


class Finder:
    """ Ищет записи в БД по конкретным параметрам """
    def __init__(self, record_requester: RecordRequester):
        self._requester = record_requester

    def by_brand(self, brand: str) -> Any:
        """ Возвращает найденные записи по наименованию материала. Формат возвращаемых данных определяет self._requester

        Аргументы
        ---------
        brand : str : Наименование материала

        """
        records = self._requester.get_records({"brand": brand})
        return records if records else None

    # @property
    # def all(self) -> Any:
    #     """ Возвращает все записи. Формат возвращаемых данных определяет self._requester"""
    #     df = self._requester.get_all_records
    #     return df if df else None

    @property
    def all(self) -> Any:
        """ Возвращает все записи. Формат возвращаемых данных определяет self._requester"""
        for index, record in self._requester.get_all_records.items():
            yield record
