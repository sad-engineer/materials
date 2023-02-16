#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar, Optional, Union
from abc import ABC, abstractmethod

from materials.obj.finders import Finder
from materials.obj.handlers import ChemicalCompositionHandler
from materials.obj.handlers import HardnessHandler
from materials.obj.handlers import TensileStrengthHandler
from materials.obj.entities import Material
from materials.obj.entities import WorkpieceMaterial
from materials.obj.constants import DEFAULT_SETTINGS_FOR_WORKPIECE_MATERIAL as DEFAULT_SETTINGS
from materials.obj.constants import DEFAULT_NAMES_FOR_MATERIALS as DEFAULT_NAMES
from materials.obj.constants import CLASSES_MATERIALS
from service import ReceivedEmptyDataFrame


class Creator(ABC):
    """ Базовый класс, для наследования всеми креаторами"""
    @abstractmethod
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

        self.data = {}
    @abstractmethod
    def _get_data(self, any_brand: str): pass

    @abstractmethod
    def create(self, any_brand: str): pass

    @property
    @abstractmethod
    def create_all(self): pass


class MaterialCreator(Creator):
    """ Создает класс материала с характеристиками"""
    def __init__(self,
                 chemical_composition_handler: ChemicalCompositionHandler,
                 hardness_handler: HardnessHandler,
                 materials_finder: Finder,
                 tensile_strength_handler: TensileStrengthHandler,
                 ):
        Creator.__init__(
            self,
            chemical_composition_handler,
            hardness_handler,
            materials_finder,
            tensile_strength_handler
        )
        self._chemical_composition = chemical_composition_handler
        self._hardness = hardness_handler
        self._materials = materials_finder
        self._tensile_strength = tensile_strength_handler

        self.data = {}

    def _get_data(self, any_brand: str):
        raw_date = self._materials.by_brand(any_brand)[0]
        self.data['brand'] = raw_date['brand']
        self.data['class_'] = raw_date['class_of_material']
        if self.data['class_'] == "Чугун":
            self.data['class_'] = CLASSES_MATERIALS[raw_date['index_of_material_class']]
        self.data['subclass'] = raw_date['subclass_of_material']
        self.data['chemical_composition'] = self._chemical_composition.by_brand(any_brand)
        try:
            self._hardness.by_brand(any_brand)
        except ReceivedEmptyDataFrame:
            # Таблицы твердости в БД существуют не для всех материалов
            # Если таблица твердости не найдена, берем твердость для материала по умолчанию.
            default_brand = DEFAULT_NAMES[raw_date['index_of_material_class']]
            self._hardness.by_brand(default_brand)
            # TODO: Ошибку в лог
            # print(f"Твердость материала {any_brand} не найдена. Принята для материала {default_brand}")
        self.data['hardness_tabl_mpa'] = self._hardness.table
        self.data['hardness_mpa'] = self._hardness.value
        try:
            self._tensile_strength.by_brand(any_brand)
        except ReceivedEmptyDataFrame:
            # Таблицы пределов прочности в БД существуют не для всех материалов
            # Если таблица пределов прочности не найдена, берем предел прочности для материала по умолчанию.
            default_brand = DEFAULT_NAMES[raw_date['index_of_material_class']]
            self._tensile_strength.by_brand(default_brand)
            # TODO: Ошибку в лог
            # print(f"Предел прочности материала {any_brand} не найден. Принят для материала {default_brand}")
        self.data['tensile_strength_tabl_mpa'] = self._tensile_strength.table
        self.data['tensile_strength_mpa'] = self._tensile_strength.value

    def create(self, any_brand: str):
        self._get_data(any_brand)
        return Material.parse_obj(self.data)

    @property
    def create_all(self):
        for row in self._materials.all:
            brand = row["brand"]
            yield self.create(brand)


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
        self.data['heat_treatment'] = heat_treatment
        self.data['workpiece'] = workpiece
        self.data['hrc'] = hrc
        return WorkpieceMaterial.parse_obj(self.data)

    @property
    def create_all(self):
        for row in self._materials.all:
            brand = row["brand"]
            yield self.create(brand)
