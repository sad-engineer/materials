#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
from typing import Callable

from service import ReceivedEmptyDataFrame
from service import logged
from service import output_debug_message_for_init_method as debug_message_for_init

from materials.obj.finders import Finder
from materials.scr.gen_fun import get_table_tensile_strength
from materials.scr.gen_fun import get_table_hardness
from materials.scr.gen_fun import get_average


@logged
class ChemicalCompositionHandler:
    """Фильтрует таблицу химического состава из запроса к БД.

    Parameters:
        chemical_composition_finder: Callable[..., Finder] : поисковик по таблице химического состава БД
    Methods:
        by_brand(any_brand: str) : dict : Возвращает словарь, в котором ключи - наименования химических элементов,
        а значения - процент содержания в материале
    """

    @debug_message_for_init()
    def __init__(self,
                 chemical_composition_finder: Callable[..., Finder],
                 ):
        self._chemical_composition = chemical_composition_finder()

    def by_brand(self, any_brand: str) -> dict:
        chem_comp = self._chemical_composition.by_brand(brand=any_brand)[0]
        return dict(filter(lambda item: item[1] is not None, chem_comp.items()))


@logged
class HardnessHandler:
    """Восстанавливает таблицу твердости из запроса к БД.

    Parameters:
        hardness_finder: Callable[..., Finder] : поисковик по таблице твердости БД
    Properties:
        hardness_table : Optional[pd.DataFrame] : поле для записи таблицы твердости
        table : pd.DataFrame : таблица твердости искомого материала
        value : pd.DataFrame : среднее значение таблицы твердости искомого материала
    Methods:
        by_brand(any_brand: str) : None : Восстанавливает таблицу твердости по наименованию материала (any_brand) и
        записывает в поле self.hardness_table
    """

    @debug_message_for_init()
    def __init__(self,
                 hardness_finder: Callable[..., Finder],
                 ):
        self._hardness_finder = hardness_finder()

        self.hardness_table = None

    def by_brand(self, any_brand: str) -> None:
        hardness = self._hardness_finder.by_brand(brand=any_brand)[0]['hardness']
        if hardness:
            self.hardness_table = get_table_hardness(any_brand, hardness)
        else:
            raise ReceivedEmptyDataFrame("Таблица твердости не найдена.")

    @property
    def table(self) -> pd.DataFrame:
        return self.hardness_table

    @property
    def value(self) -> float:
        return get_average(self.hardness_table['hardness'])


@logged
class TensileStrengthHandler:
    """Восстанавливает таблицу предела прочности из запроса к БД.

    Parameters:
        mechanical_properties_finder: Callable[..., Finder] : поисковик по таблице предела прочности БД
    Properties:
        tensile_strength_table : Optional[pd.DataFrame] : поле для записи таблицы предела прочности
        table : pd.DataFrame : таблица предела прочности искомого материала
        value : pd.DataFrame : среднее значение таблицы предела прочности искомого материала
    Methods:
        by_brand(any_brand: str) : None : Восстанавливает таблицу предела прочности по наименованию материала
        (any_brand) и записывает в поле self.tensile_strength_table
    """

    @debug_message_for_init()
    def __init__(self,
                 mechanical_properties_finder: Callable[..., Finder],
                 ):
        self._mechanical_properties = mechanical_properties_finder()

        self.tensile_strength_table = None

    def by_brand(self, any_brand: str) -> pd.DataFrame:
        tensile_strength = self._mechanical_properties.by_brand(brand=any_brand)[0]['tensile_strength']
        if tensile_strength:
            self.tensile_strength_table = get_table_tensile_strength(tensile_strength)
        else:
            raise ReceivedEmptyDataFrame("Таблица пределов прочности не найдена.")

    @property
    def table(self) -> pd.DataFrame:
        return self.tensile_strength_table

    @property
    def value(self) -> float:
        return get_average(self.tensile_strength_table['tensile_strength'])
