#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd

from service import RecordRequester


class Finder:
    """ Ищет записи в БД по конкретным параметрам """
    def __init__(self, record_requester: RecordRequester):
        self._requester = record_requester

    def by_brand(self, brand: str) -> pd.DataFrame:
        """ Возвращает найденные записи по значению диаметра в виде таблицы pd.DataFrame.

        Аргументы
        ---------
        dia: str
            Значение диаметра инструмента
        dia_out: str
            Значение диаметра инструмента (указывается для насадных инструментов)
        """
        df = self._requester.get_records({"brand": brand})
        return df if df else None

    @property
    def all(self) -> pd.DataFrame:
        """ Возвращает все записи в виде таблицы pd.DataFrame """
        df = self._requester.get_all_records
        return df if df else None
