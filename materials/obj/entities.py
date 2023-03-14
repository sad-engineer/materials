#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Optional, Any
import pandas as pd
from pydantic import BaseModel, validator
from collections import namedtuple

from materials.obj.constants import CLASSES_MATERIALS, HEAT_TREATMENT, WORKPIECE
from materials.obj.fields_types import InMaterialClass, InTypeWorkpiece, InHeatTreatment


ErrorWithData = namedtuple('ErrorWithData', ['err', 'name', 'params'])   # для сохранения данных с ошибкой


class Material(BaseModel):
    """Класс 'Материал'.

    Parameters:
    brand : (str, optional) : Наименование материала (будет использовано для поиска по базе данных).
    type_of_mat : (int, optional) : Индекс типа материала.
    class_ : (str, optional) : Класс материала.
    subclass : (str, optional) : Подкласс материала.
    chemical_composition : (dict, optional) : Таблица химического состава материала.
    hardness_tabl_mpa : (pd.DataFrame, optional) : Таблица твердости (в МПа) материала в различных состояниях поставки.
    hardness_mpa : (Union[float, int], optional) : Твердость материала (в МПа), используемая для расчетов
    tensile_strength_tabl_mpa : (pd.DataFrame, optional) : Таблица пределов прочности материала (в МПа) в различных
        состояниях поставки
    tensile_strength_mpa : (Union[float, int], optional) : Предел прочности (в МПа), используемый для расчетов
    """
    brand: Optional[str] = None
    class_: Optional[InMaterialClass] = None
    subclass: Optional[str] = None
    chemical_composition: dict = {}
    hardness_tabl_mpa: Optional[Any] = None
    hardness_mpa: Optional[float] = None
    tensile_strength_tabl_mpa: Optional[Any] = None
    tensile_strength_mpa: Optional[float] = None

    class Config:
        validate_assignment = True
        extra = "allow"

    @validator('hardness_tabl_mpa')
    def validate_hardness_tabl_mpa(cls, value):
        if not isinstance(value, type(None)):
            if not isinstance(value, pd.DataFrame):
                raise ValueError('Переменная должна содержать таблицу pandas DataFrame')
        return value

    @validator('hardness_mpa')
    def validate_hardness_mpa(cls, value):
        if not isinstance(value, type(None)):
            if value < 0:
                raise ValueError(f"Ожидается положительное число, получено: {value}")
        return value

    @validator('tensile_strength_tabl_mpa')
    def validate_tensile_strength_tabl_mpa(cls, value):
        if not isinstance(value, type(None)):
            if not isinstance(value, pd.DataFrame):
                raise ValueError('Переменная должна содержать таблицу pandas DataFrame')
        return value

    @validator('tensile_strength_mpa')
    def validate_tensile_strength_mpa(cls, value):
        if not isinstance(value, type(None)):
            if value < 0:
                raise ValueError(f"Ожидается положительное число, получено: {value}")
        return value

    @property
    def available_classes_of_materials(self):
        return CLASSES_MATERIALS


class WorkpieceMaterial(Material):
    """ Класс 'Материал заготовки'. Хранит состояние материала

    Parameters:
    brand : (str, optional) : Наименование материала (будет использовано для поиска по базе данных).
    type_of_mat : (int, optional) : Индекс типа материала.
    class_ : (str, optional) : Класс материала.
    subclass : (str, optional) : Подкласс материала.
    chemical_composition : (dict, optional) : Таблица химического состава материала.
    hardness_tabl_mpa : (pd.DataFrame, optional) : Таблица твердости (в МПа) материала в различных состояниях поставки.
    hardness_mpa : (Union[float, int], optional) : Твердость материала (в МПа), используемая для расчетов
    tensile_strength_tabl_mpa : (pd.DataFrame, optional) : Таблица пределов прочности материала (в МПа) в различных
        состояниях поставки
    tensile_strength_mpa : (Union[float, int], optional) : Предел прочности (в МПа), используемый для расчетов
    heat_treatment: (in range(3) or None, optional) : Тип термообработки:
    hrc : (float, optional) : Значение твердости после термообработки по системе HRC
    workpiece : (in range(6), optional) : Тип поверхности заготовки:
    """
    heat_treatment: Optional[InHeatTreatment] = None
    workpiece: Optional[InTypeWorkpiece] = None
    hrc: Optional[float] = None

    @validator('hrc')
    def validate_hrc(cls, value):
        if not isinstance(value, type(None)):
            if value < 0:
                raise ValueError(f"Ожидается положительное число, получено: {value}")
        return value

    @property
    def available_types_of_heat_treatment(self):
        return HEAT_TREATMENT

    @property
    def available_types_of_workpiece(self):
        return WORKPIECE
