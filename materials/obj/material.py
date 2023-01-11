#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Optional, Union
from dataclasses import dataclass
import pandas as pd

from materials.find import characteristics
from materials.find import chem_struct
from materials.find import hardness
from materials.find import tensile_strength
from materials.scr.gen_fun import get_average
from materials.scr.gen_fun import is_brand_in_database
from materials.obj.exceptions import ReceivedEmptyDataFrame
from materials.obj.constants import DEFAULT_BRAND
from materials.obj.decorators import inheritdocstring


@dataclass
class MaterialData:
    """Класс 'Материал'. Хранит состояние материала

    Parameters:
        brand : (str, optional) : Наименование материала (будет использовано для поиска по базе данных).
        type_of_mat : (int, optional) : Индекс типа материала.
        class_ : (str, optional) : Класс материала.
        subclass : (str, optional) : Подкласс материала.
        chemical_composition : (dict, optional) : Таблица химического состава материала.
        hardness_tabl_mpa : (pd.DataFrame, optional) : Таблица твердости (в МПа) материала в различных состояниях поставки.
        hardness_mpa_for_proc : (Union[float, int], optional) : Твердость материала (в МПа), используемая для расчетов
        tabl_tensile_strength_mpa : (pd.DataFrame, optional) : Таблица пределов прочности материала (в МПа) в различных состояниях поставки
        tensile_strength_mpa_for_proc : (Union[float, int], optional) : Предел прочности (в МПа), используемый для  расчетов
    """
    brand: Optional[str] = None
    type_of_mat: Optional[int] = None
    class_: Optional[str] = None
    subclass: Optional[str] = None
    chemical_composition: Optional[dict] = None
    hardness_tabl_mpa: Optional[pd.DataFrame] = None
    hardness_mpa_for_proc: Optional[Union[float, int]] = None
    tabl_tensile_strength_mpa: Optional[pd.DataFrame] = None
    tensile_strength_mpa_for_proc: Optional[Union[float, int]] = None


@inheritdocstring
class Material(MaterialData):
    def __init__(self, brand: Optional[str] = None):
        MaterialData.__init__(self)

        new_brand_exists = not (brand in ["", " ", "  ", None, 0] or isinstance(brand, type(None)))
        if new_brand_exists and is_brand_in_database(brand):
            self.get_material_parameters(brand)

    def get_material_parameters(self, brand: Optional[str] = None) -> None:
        """ Если в 'brand' передать новый материал, переопределит параметры для нового материала.
        Задает: класс материала, подкласс, индекс типа материала, хим.состав,  твердость, предел прочности.
        """
        self.brand = brand
        self._get_material_characteristics()
        self._get_chemical_composition()
        self._get_hardness()
        self._get_tensile_strength()

    def _get_material_characteristics(self) -> None:
        """ Задает класс материала, подкласс, индекс типа материала
        """
        if not isinstance(self.brand, type(None)):
            index, class_, subclass = characteristics(brand=self.brand)
            self.type_of_mat = index
            self.class_ = class_
            self.subclass = subclass

    def _get_chemical_composition(self) -> None:
        """ Создает таблицу химического состава материала. Выбирает таблицу химического состава из БД. Если в БД нет
        хим состава материала - берет значение по умолчанию
        """
        self.chemical_composition = chem_struct(brand=self.brand)

    def _get_hardness(self) -> None:
        """ Получает таблицу твердости из БД. Если в БД нет таблицы твердости для материала - выполняет тоже для
        материала по умолчанию
        """
        try:
            self.hardness_tabl_mpa = hardness(brand=self.brand)
            self.hardness_mpa_for_proc = get_average(data=self.hardness_tabl_mpa["hardness"])
        except (ReceivedEmptyDataFrame, KeyError):
            self.hardness_tabl_mpa = hardness(brand=DEFAULT_BRAND)
            print(
                f"Твердость материала {self.brand} не найдена. Взята твердость материала по умолчанию: {DEFAULT_BRAND}")

    def _get_tensile_strength(self) -> None:
        """ Получает таблицу предела кратковременной прочности из БД. Если в БД нет таблицы твердости для материала -
        выполняет тоже для материала по умолчанию
        """
        try:
            self.tabl_tensile_strength_mpa = tensile_strength(brand=self.brand)
        except ReceivedEmptyDataFrame:
            self.tabl_tensile_strength_mpa = tensile_strength(brand=DEFAULT_BRAND)
            print(f"Предел прочности материала {self.brand} не найден. Взят для материала по умолчанию: "
                  f"{DEFAULT_BRAND}")
        self.tensile_strength_mpa_for_proc = get_average(data=self.tabl_tensile_strength_mpa["tensile_strength"])

    def get_default_settings(self) -> None:
        """ Настраивает атрибуты класса в соответствии с глобальными дефолтными настройками
        """
        self.get_material_parameters(brand=DEFAULT_BRAND)

    @classmethod
    def default(cls):
        """ Настраивает атрибуты класса в соответствии с глобальными дефолтными настройками
        """
        return cls(brand=DEFAULT_BRAND)


# if __name__ == "__main__":
#     material = MaterialData()
#     print(material.__doc__)
#     print(material)
#
#     material = Material()
#     print(material.__doc__)
#     print(material)
#
#     material = Material.default()
#     print(material.__doc__)
#     print(material)

