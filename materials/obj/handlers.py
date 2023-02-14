#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd

from materials.obj.finders import Finder
from materials.scr.gen_fun import get_table_tensile_strength
from materials.scr.gen_fun import get_table_hardness
from materials.scr.gen_fun import get_average
from service import ReceivedEmptyDataFrame


class ChemicalCompositionHandler:
    def __init__(self,
                 chemical_composition_finder: Finder,
                 ):
        self._chemical_composition = chemical_composition_finder

    def by_brand(self, any_brand: str) -> dict:
        chem_comp = self._chemical_composition.by_brand(any_brand)[0]
        return dict(filter(lambda item: item[1] is not None, chem_comp.items()))


class HardnessHandler:
    def __init__(self,
                 hardness_finder: Finder,
                 ):
        self._hardness_finder = hardness_finder
        self.hardness_table = None

    def by_brand(self, any_brand: str) -> None:
        hardness = self._hardness_finder.by_brand(any_brand)[0]['hardness']
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


class TensileStrengthHandler:
    def __init__(self,
                 mechanical_properties_finder: Finder,
                 ):
        self._mechanical_properties = mechanical_properties_finder
        self.tensile_strength_table = None

    def by_brand(self, any_brand: str) -> pd.DataFrame:
        tensile_strength = self._mechanical_properties.by_brand(any_brand)[0]['tensile_strength']
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
