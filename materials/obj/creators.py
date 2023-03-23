#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import ClassVar, Optional, Union, Callable
from abc import ABC, abstractmethod
from pydantic import ValidationError

from service import ReceivedEmptyDataFrame
from service import logged
from service import output_debug_message_for_init_method as debug_message_for_init

from materials.obj.finders import Finder
from materials.obj.handlers import ChemicalCompositionHandler
from materials.obj.handlers import HardnessHandler
from materials.obj.handlers import TensileStrengthHandler
from materials.obj.entities import Material
from materials.obj.entities import WorkpieceMaterial
from materials.obj.constants import DEFAULT_SETTINGS_FOR_WORKPIECE_MATERIAL as DEFAULT_SETTINGS
from materials.obj.constants import DEFAULT_NAMES_FOR_MATERIALS as DEFAULT_NAMES
from materials.obj.constants import CLASSES_MATERIALS
from materials.obj.entities import ErrorWithData


def output_debug_message():
    """Логирует создание объекта (экземпляра модели данных). При ошибке создания - логирует ошибку."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if not isinstance(result, (ErrorWithData, type(None))) and self._verbose:
                name = " ".join([result.subclass, result.brand])
                self.debug(f"Создан экземпляр класса {result.__class__.__name__}: {name}.")
            return result
        return wrapper
    return decorator


def output_error_message():
    """Логирует ошибку создания объекта (экземпляра модели данных)."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if not isinstance(result, ErrorWithData):
                return result
            if isinstance(result.err, ValueError):
                self.error(f"Переданные данные не соответствуют ожидаемой схеме модели {result.name}."
                           f"Данные, загружаемые в модель: {result.params}.")
            elif isinstance(result.err, TypeError):
                self.error(f"Данные, загружаемые в модель должны быть словарем. "
                           f"Полученный тип данных: {type(result.params)}.")
            elif isinstance(result.err, ValidationError):
                self.error(f"Входные данные содержат неверные значения для полей модели {result.name}."
                           f"Данные, загружаемые в модель: {result.params}.")
            elif isinstance(result.err, AttributeError):
                self.error(f"Входные данные содержат неверные значения для полей модели {result.name}."
                           f"Данные, загружаемые в модель: {result.params}.")
            else:
                self.error(f"Ошибка создания экземпляра класса {result.name} с параметрами {result.params}."
                           f"Данные, загружаемые в модель: {result.params}.")
        return wrapper
    return decorator


@logged
class Creator(ABC):
    """ Базовый класс, для наследования всеми креаторами"""
    @abstractmethod
    @debug_message_for_init()
    def __init__(self,
                 chemical_composition_handler: Callable[..., ChemicalCompositionHandler],
                 hardness_handler: Callable[..., HardnessHandler],
                 materials_finder: Callable[..., Finder],
                 tensile_strength_handler: Callable[..., TensileStrengthHandler],
                 ):
        self._chemical_composition = chemical_composition_handler()
        self._hardness = hardness_handler()
        self._materials = materials_finder()
        self._tensile_strength = tensile_strength_handler()

        self._verbose = True
        self.data = {}

    @abstractmethod
    def _get_data(self, any_brand: str):
        raise NotImplementedError

    @abstractmethod
    def create(self, any_brand: str):
        raise NotImplementedError


class MaterialCreator(Creator):
    """ Создает класс материала с характеристиками"""
    def __init__(self,
                 chemical_composition_handler: Callable[..., ChemicalCompositionHandler],
                 hardness_handler: Callable[..., HardnessHandler],
                 materials_finder: Callable[..., Finder],
                 tensile_strength_handler: Callable[..., TensileStrengthHandler],
                 ):
        Creator.__init__(
            self,
            chemical_composition_handler=chemical_composition_handler,
            hardness_handler=hardness_handler,
            materials_finder=materials_finder,
            tensile_strength_handler=tensile_strength_handler
        )

    def _get_data(self, any_brand: str):
        raw_date = self._materials.by_brand(brand=any_brand)[0]
        self.data['brand'] = raw_date['brand']
        self.data['class_'] = raw_date['class_of_material']
        if self.data['class_'] == "Чугун":
            self.data['class_'] = CLASSES_MATERIALS[raw_date['index_of_material_class']]
        self.data['subclass'] = raw_date['subclass_of_material']
        self.data['chemical_composition'] = self._chemical_composition.by_brand(any_brand)
        try:
            self._hardness.by_brand(any_brand)
        except ReceivedEmptyDataFrame:
            # Таблицы твердости в БД существуют не для всех материалов.
            # Если таблица твердости не найдена, берем твердость для материала по умолчанию.
            default_brand = DEFAULT_NAMES[raw_date['index_of_material_class']]
            self._hardness.by_brand(default_brand)
            # TODO: Придумать декоратор для info
            self.info(f"Твердость материала {any_brand} не найдена. Принята для материала {default_brand}")
        self.data['hardness_tabl_mpa'] = self._hardness.table
        self.data['hardness_mpa'] = self._hardness.value
        try:
            self._tensile_strength.by_brand(any_brand)
        except ReceivedEmptyDataFrame:
            # Таблицы пределов прочности в БД существуют не для всех материалов.
            # Если таблица пределов прочности не найдена, берем предел прочности для материала по умолчанию.
            default_brand = DEFAULT_NAMES[raw_date['index_of_material_class']]
            self._tensile_strength.by_brand(default_brand)
            # TODO: Придумать декоратор для info
            self.info(f"Предел прочности материала {any_brand} не найден. Принят для материала {default_brand}")
        self.data['tensile_strength_tabl_mpa'] = self._tensile_strength.table
        self.data['tensile_strength_mpa'] = self._tensile_strength.value

    @output_debug_message()
    @output_error_message()
    def create(self, any_brand: str):
        self._verbose = True
        self._get_data(any_brand)
        try:
            return Material.parse_obj(self.data)
        except Exception as error:
            return ErrorWithData(err=error, name=Material.__name__, params=self.data)


class WorkpieceMaterialCreator(MaterialCreator):
    """ Создает класс заготовки с характеристиками"""
    DEFAULT_SETTINGS: ClassVar[dict] = DEFAULT_SETTINGS

    def __init__(self,
                 chemical_composition_handler: Callable[..., ChemicalCompositionHandler],
                 hardness_handler: Callable[..., HardnessHandler],
                 materials_finder: Callable[..., Finder],
                 tensile_strength_handler: Callable[..., TensileStrengthHandler],
                 ):
        Creator.__init__(
            self,
            chemical_composition_handler=chemical_composition_handler,
            hardness_handler=hardness_handler,
            materials_finder=materials_finder,
            tensile_strength_handler=tensile_strength_handler
        )

    def _get_data(self, any_brand: str):
        MaterialCreator._get_data(self, any_brand)

    @output_debug_message()
    @output_error_message()
    def create(self,
               any_brand: str,
               heat_treatment: Optional[Union[int, str]] = DEFAULT_SETTINGS["type_of_heat_treatment"],
               workpiece: Optional[Union[int, str]] = DEFAULT_SETTINGS["workpiece"],
               hrc: Optional[int] = DEFAULT_SETTINGS["hrc"]):
        self._verbose = True
        self._get_data(any_brand)
        self.data['heat_treatment'] = heat_treatment
        self.data['workpiece'] = workpiece
        self.data['hrc'] = hrc
        try:
            return WorkpieceMaterial.parse_obj(self.data)
        except Exception as error:
            return ErrorWithData(err=error, name=Material.__name__, params=self.data)
