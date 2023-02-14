#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar, Optional, Union

from materials.obj.finders import Finder
from materials.obj.handlers import ChemicalCompositionHandler
from materials.obj.handlers import HardnessHandler
from materials.obj.handlers import TensileStrengthHandler
from materials.obj.entities import Material
from materials.obj.entities import WorkpieceMaterial
from materials.obj.constants import DEFAULT_SETTINGS_FOR_MATERIAL as DEFAULT_SETTINGS


class MaterialCreator:
    """ Создает класс материала с характеристиками"""
    def __init__(self,
                 chemical_composition_handler: ChemicalCompositionHandler,
                 hardness_handler: HardnessHandler,
                 materials_finder: Finder,
                 tensile_strength_handler: TensileStrengthHandler,
                 ):
        self._chemical_composition = chemical_composition_handler
        self._hardness = hardness_handler
        self._materials = materials_finder
        self._tensile_strength = tensile_strength_handler

        self.date = {}

    def _get_data(self, any_brand: str):
        raw_date = self._materials.by_brand(any_brand)[0]
        self.date['brand'] = raw_date['brand']
        self.date['index_class'] = raw_date['index_of_material_class']
        self.date['class_'] = raw_date['class_of_material']
        self.date['subclass'] = raw_date['subclass_of_material']
        self.date['chemical_composition'] = self._chemical_composition.by_brand(any_brand)
        self._hardness.by_brand(any_brand)
        self.date['hardness_tabl_mpa'] =self._hardness.table
        self.date['hardness_mpa'] = self._hardness.value
        self._tensile_strength.by_brand(any_brand)
        self.date['tensile_strength_tabl_mpa'] = self._tensile_strength.table
        self.date['tensile_strength_mpa'] = self._tensile_strength.value

    def create(self, any_brand: str):
        self._get_data(any_brand)
        return Material(**self.date)


class WorkpieceMaterialCreator(MaterialCreator):
    """ Создает класс заготовки с характеристиками"""
    DEFAULT_SETTINGS: ClassVar[dict] = DEFAULT_SETTINGS

    def __init__(self,
                 chemical_composition_handler: ChemicalCompositionHandler,
                 hardness_handler: HardnessHandler,
                 materials_finder: Finder,
                 tensile_strength_handler: TensileStrengthHandler,
                 ):
        MaterialCreator.__init__(self,
                                 chemical_composition_handler,
                                 hardness_handler,
                                 materials_finder,
                                 tensile_strength_handler)

    def _get_data(self, any_brand: str):
        MaterialCreator._get_data(self, any_brand)

    def create(self,
               any_brand: str,
               heat_treatment: Optional[Union[int, str]] = DEFAULT_SETTINGS["type_of_heat_treatment"],
               workpiece: Optional[Union[int, str]] = DEFAULT_SETTINGS["workpiece"],
               hrc: Optional[int] = DEFAULT_SETTINGS["hrc"]):
        self._get_data(any_brand)
        self.date['heat_treatment'] = heat_treatment
        self.date['workpiece'] = workpiece
        self.date['hrc'] = hrc
        return WorkpieceMaterial(**self.date)









