#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Union, Optional, ClassVar
from pydantic import BaseModel, validator

from materials.obj.constants import CLASSES_MATERIALS, HEAT_TREATMENT, WORKPIECE


# class FieldMaterialClass:
#     CLASSES_MATERIALS: ClassVar[dict] = CLASSES_MATERIALS
#
#     @classmethod
#     def validate(cls, value):
#         if not isinstance(value, (int, str)):
#             raise ValueError(f"Ожидается целое число или строка, получено: {type(value)}")
#         elif isinstance(value, str):
#             if value not in cls.CLASSES_MATERIALS.values():
#                 raise ValueError(f"Строковое значение должно быть из списка {list(cls.CLASSES_MATERIALS.values())}, "
#                                  f"получено: {value}")
#             return {v: k for k, v in cls.CLASSES_MATERIALS.items()}[value]
#         elif isinstance(value, int):
#             if value not in cls.CLASSES_MATERIALS:
#                 raise ValueError(f"Значение должно быть из списка {list(cls.CLASSES_MATERIALS.keys())}, "
#                                  f"получено: {value}")
#             return value
#
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate


class ValueFromDict:
    """Для определения полей, значение которых должны быть из словаря доступных значений"""
    AVAILABLE_VALUES: ClassVar[dict] = {}

    @classmethod
    def validate(cls, value):
        if not isinstance(value, (int, str)):
            raise ValueError(f"Ожидается целое число или строка, получено: {type(value)}")
        elif isinstance(value, str):
            if value not in cls.AVAILABLE_VALUES.values():
                raise ValueError(f"Строковое значение должно быть из списка {list(cls.AVAILABLE_VALUES.values())}, "
                                 f"получено: {value}")
            return {v: k for k, v in cls.AVAILABLE_VALUES.items()}[value]
        elif isinstance(value, int):
            if value not in cls.AVAILABLE_VALUES:
                raise ValueError(f"Значение должно быть из списка {list(cls.AVAILABLE_VALUES.keys())}, "
                                 f"получено: {value}")
            return value

    @classmethod
    def __get_validators__(cls):
        yield cls.validate


class InMaterialClass(ValueFromDict):
    AVAILABLE_VALUES = CLASSES_MATERIALS


class InHeatTreatment(ValueFromDict):
    AVAILABLE_VALUES = HEAT_TREATMENT


class InTypeWorkpiece(ValueFromDict):
    AVAILABLE_VALUES = WORKPIECE


class Material(BaseModel):
    class_: Optional[InMaterialClass] = None

    class Config:
        validate_assignment = True
        extra = "allow"



if __name__ == "__main__":

    cutter = Material(class_='Сталь инструментальная')
    cutter.class_ = 13
    print(type(cutter.class_))

