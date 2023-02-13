#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd

from materials.obj.finders import Finder
from materials.scr.gen_fun import get_table_tensile_strength
from materials.scr.gen_fun import get_table_hardness


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
        self._hardness = hardness_finder

    def by_brand(self, any_brand: str) -> pd.DataFrame:
        hardness = self._hardness.by_brand(any_brand)[0]
        return get_table_hardness(any_brand, hardness['hardness'])


class TensileStrengthHandler:
    def __init__(self,
                 mechanical_properties_finder: Finder,
                 ):
        self._mechanical_properties = mechanical_properties_finder

    def by_brand(self, any_brand: str) -> pd.DataFrame:
        mechanical_properties = self._mechanical_properties.by_brand(any_brand)[0]
        return get_table_tensile_strength(mechanical_properties['tensile_strength'])

