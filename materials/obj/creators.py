#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd

from materials.obj.finders import Finder
from materials.obj.handlers import ChemicalCompositionHandler
from materials.obj.handlers import HardnessHandler
from materials.obj.handlers import TensileStrengthHandler


class Creator:
    """ Создает класс материалла с характеристиками"""
    def __init__(self,
                 characteristics_finder: Finder,
                 chemical_composition_handler: ChemicalCompositionHandler,
                 hardness_handler: HardnessHandler,
                 materials_finder: Finder,
                 tensile_strength_handler: TensileStrengthHandler,
                 technological_properties_finder: Finder,
                 ):
        self._characteristics_finder = characteristics_finder
        self._chemical_composition = chemical_composition_handler
        self._hardness = hardness_handler
        self._materials = materials_finder
        self._tensile_strength = tensile_strength_handler
        self._technological_properties = technological_properties_finder

    def by_brand(self, any_brand: str):
        chars = self._characteristics_finder.by_brand(any_brand)
        chem_comp = self._chemical_composition.by_brand(any_brand)
        hardness = self._hardness.by_brand(any_brand)
        mats = self._materials.by_brand(any_brand)
        mech_props = self._tensile_strength.by_brand(any_brand)
        tech_props = self._technological_properties.by_brand(any_brand)

        print(chars[0])
        print(chem_comp)
        print(hardness)
        print(mats[0])
        print(mech_props)
        print(tech_props[0])









