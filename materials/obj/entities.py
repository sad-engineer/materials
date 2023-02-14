#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Optional, Union, Any
import pandas as pd
from pydantic import BaseModel, validator

from materials.obj.constants import CLASSES_MATERIALS, HEAT_TREATMENT, WORKPIECE


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
    index_class: Any = None
    class_: Optional[str] = None
    subclass: Optional[str] = None
    chemical_composition: dict = {}
    hardness_tabl_mpa: Optional[Any] = None
    hardness_mpa: Optional[float] = None
    tensile_strength_tabl_mpa: Optional[Any] = None
    tensile_strength_mpa: Optional[float] = None

    class Config:
        validate_assignment = True
        extra = "forbid"

    @validator('index_class')
    def validate_index_class(cls, value):
        if value not in list(CLASSES_MATERIALS.keys()):
            raise ValueError(f"Неверный индекс типа материала: {value}. "
                             f"Должно быть из {list(CLASSES_MATERIALS.keys())}")
        return value

    @validator('class_')
    def validate_class_(cls, value):
        if value not in list(CLASSES_MATERIALS.values()):
            raise ValueError(f"Неверный класс материала: {value}. "
                             f"Должно быть из {list(CLASSES_MATERIALS.values())}")
        return value

    @validator('hardness_tabl_mpa')
    def validate_hardness_tabl_mpa(cls, value):
        if not isinstance(value, pd.DataFrame):
            raise ValueError('Переменная должна содержать таблицу pandas DataFrame')
        return value

    @validator('tensile_strength_tabl_mpa')
    def validate_tensile_strength_tabl_mpa(cls, value):
        if not isinstance(value, pd.DataFrame):
            raise ValueError('Переменная должна содержать таблицу pandas DataFrame')
        return value


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
    heat_treatment: Optional[Union[int, str]] = None
    workpiece: Optional[Union[int, str]] = None
    hrc: Optional[float] = None

    @validator('heat_treatment')
    def validate_heat_treatment(cls, value):
        if isinstance(value, int):
            if value not in list(HEAT_TREATMENT.keys()):
                raise ValueError(f"Неверный индекс типа термообработки: {value}. "
                                 f"Должно быть из {list(HEAT_TREATMENT.keys())}")
            return value
        elif isinstance(value, str):
            if value not in list(HEAT_TREATMENT.values()):
                raise ValueError(f"Неверный тип термообработки: {value}. "
                                 f"Должно быть из {list(HEAT_TREATMENT.values())}")
            return value if isinstance(value, int) else {v: k for k, v in HEAT_TREATMENT.items()}[value]

    @validator('workpiece')
    def validate_workpiece(cls, value):
        if isinstance(value, int):
            if value not in list(WORKPIECE.keys()):
                raise ValueError(f"Неверный индекс типа поверхности заготовки: {value}. "
                                 f"Должно быть из {list(WORKPIECE.keys())}")
        else:
            if value not in list(HEAT_TREATMENT.values()):
                raise ValueError(f"Неверный тип поверхности заготовки: {value}. "
                                 f"Должно быть из {list(WORKPIECE.values())}")
        return value if isinstance(value, int) else {v: k for k, v in WORKPIECE.items()}[value]
