#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Optional, Union

from materials.find import characteristics
from materials.find import chem_struct
from materials.find import hardness
from materials.find import tensile_strength
from materials.scr.gen_fun import get_average
from materials.scr.gen_fun import show
from materials.scr.gen_fun import is_brand_in_database
from materials.scr.gen_fun import check_workpiece, check_heat_treatment
from materials.obj.exceptions import ReceivedEmptyDataFrame
from materials.obj.constants import DEFAULT_NAMES_FOR_MATERIALS as DEFAULT_NAMES
from materials.obj.constants import DEFAULT_SETTINGS_FOR_MATERIALS as DEFAULT_SETTINGS


class Material:
    """ Класс параметров обрабатываемого материала
    
    Parameters
    ----------
    brand : str, optional
        Наименование материала (будет использовано для поиска по базе данных). По умолчанию: None.
    heat_treatment: in range(3) or None, optional
        Тип термообработки:
            None - Без термообработки;
            0 - Нормализация;
            1 - Отжиг;
            2 - Улучшение;
        По умолчанию: None.
    hrc : float, optional
        Значение твердости после термообработки по системе HRC
    workpiece : in range(6), optional
        Тип поверхности заготовки:
            0 - Без корки;
            1 - С коркой: прокат;
            2 - С коркой: поковка;
            3 - Отливка с нормальной коркой;
            4 - Отливка с загрязненной коркой;
            5 - С коркой: Медные и алюминиевые сплавы;
    """
    def __init__(self,
                 brand: Optional[str] = None,
                 heat_treatment: Optional[Union[str, int]] = None,
                 hrc: Optional[Union[float, int]] = None,
                 workpiece: int = 0):
        # наименование материала
        self.brand: Optional[str] = None
        # индекс типа материала,
        self.type_of_mat: Optional[int] = None
        # класс материала,
        self.class_: Optional[str] = None
        # подкласс материала,
        self.subclass: Optional[str] = None
        # Таблица химического состава материала
        self.chemical_composition = None
        # Таблица твердости для материала в различных состояниях поставки
        self.hardness_tabl_mpa = None
        # Твердость материала, используемая для расчетов
        self.hardness_mpa_for_proc: Optional[Union[float, int]] = None
        # Таблица пределов прочности материала в различных состояниях поставки
        self.tabl_tensile_strength_mpa = None
        # Предел прочности, используемый для расчетов
        self.tensile_strength_mpa_for_proc: Optional[Union[float, int]] = None
        if not isinstance(brand, type(None)):
            self.get_material_parameters(brand)
        else:
            default_brand = DEFAULT_NAMES[2]
            self.get_material_parameters(default_brand)

        # Вид термообработки
        self.type_of_heat_treatment: Optional[int] = None
        if not isinstance(heat_treatment, type(None)):
            self.update_heat_treatment(heat_treatment)
        # Твердость обрабатываемого материала после термообработки
        self.hrc = hrc
        # pz Состояние заготовки (с коркой/ без корки, и т.д.)
        self.workpiece: Optional[int] = None
        if not isinstance(workpiece, type(None)):
            self.update_workpiece(workpiece)

    def show(self) -> None:
        show(self)

    def get_material_parameters(self, brand: Optional[str] = None) -> None:
        """ Если в 'brand' передать новый материал, переопределит параметры для нового материала.
        Задает: класс материала, подкласс, индекс типа материала, хим.состав,  твердость, предел прочности.
        """
        new_brand_exists = not (brand in ["", " ", "  ", None, 0] or
                                isinstance(brand, type(None)))
        if new_brand_exists and self.brand != brand and is_brand_in_database(brand):
            self.brand = brand
            # По наименованию материала определяем его параметры: индекс типа материала, класс, подкласс материала
            self.get_material_characteristics()
            # Заполняем таблицу химического состава
            self.get_chemical_composition()
            # Заполняем таблицу твердости и находим твердость для расчетов
            self.get_hardness()
            # Заполняем таблицу пределов прочности и значение для расчетов
            self.get_tensile_strength()

    def get_material_characteristics(self) -> None:
        """ Задает класс материала, подкласс, индекс типа материала
        """
        if not isinstance(self.brand, type(None)):
            index, class_, subclass = characteristics(brand=self.brand)
            self.type_of_mat = index
            self.class_ = class_
            self.subclass = subclass

    def get_chemical_composition(self) -> None:
        """ Создает таблицу химического состава материала. Выбирает таблицу химического состава из БД. Если в БД нет
        хим состава материала - берет значение по умолчанию
        """
        self.chemical_composition = chem_struct(brand=self.brand)

    def get_hardness(self) -> None:
        """ Получает таблицу твердости из БД. Если в БД нет таблицы твердости для материала - выполняет тоже для
        материала по умолчанию
        """
        try:
            self.hardness_tabl_mpa = hardness(brand=self.brand)
        except ReceivedEmptyDataFrame:
            self.get_default_hardness()
        try:
            self.hardness_mpa_for_proc = get_average(data=self.hardness_tabl_mpa["hardness"])
        except KeyError:
            self.get_default_hardness()

    def get_tensile_strength(self) -> None:
        """ Получает таблицу предела кратковременной прочности из БД. Если в БД нет таблицы твердости для материала -
        выполняет тоже для материала по умолчанию
        """
        try:
            self.tabl_tensile_strength_mpa = tensile_strength(brand=self.brand)
        except ReceivedEmptyDataFrame:
            self.get_default_tensile_strength()
        self.tensile_strength_mpa_for_proc = get_average(data=self.tabl_tensile_strength_mpa["tensile_strength"])

    def get_default_settings(self) -> None:
        """ Настраивает атрибуты класса в соответствии с глобальными дефолтными настройками
        """
        for setting_name, setting_val in DEFAULT_SETTINGS.items():
            self.get_material_parameters(brand=setting_val) if setting_name == "brand" else setattr(self, setting_name,
                                                                                                    setting_val)

    def get_default_hardness(self) -> None:
        """ Получает таблицу твердости из БД для материала по умолчанию
        """
        default_brand = DEFAULT_NAMES[self.type_of_mat]
        self.hardness_tabl_mpa = hardness(brand=default_brand)
        print(f"Твердость материала {self.brand} не найдена. Взята твердость материала по умолчанию: {default_brand}")

    def get_default_tensile_strength(self) -> None:
        """ Получает таблицу предела кратковременной прочности из БД для материала по умолчанию
        """
        default_brand = DEFAULT_NAMES[self.type_of_mat]
        self.tabl_tensile_strength_mpa = tensile_strength(brand=default_brand)
        print(f"Предел прочности материала {self.brand} не найден. Взят для материала по умолчанию: {default_brand}")

    def update_heat_treatment(self, heat_treatment: Optional[Union[str, int]] = None):
        """ Проверяет значение термообработки. При корректном значении устанавливает тип термообработки
        """
        self.type_of_heat_treatment = check_heat_treatment(heat_treatment)

    def update_workpiece(self, workpiece: Union[str, int]):
        """ Проверяет значение типа поверхности заготовки. При корректном значении устанавливает тип поверхности
        заготовки.
        """
        self.workpiece = check_workpiece(workpiece)

    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        """ Создает словарь ключевых параметров класса 'Материал'."""
        state = dict()
        state["brand"] = self.brand
        state["type_of_heat_treatment"] = self.type_of_heat_treatment
        state["hrc"] = self.hrc
        state["workpiece"] = self.workpiece
        return state

    def __setstate__(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        """ Загружает ключевые параметры класса из словаря, настраивает в зависимости от brand"""
        self.get_material_parameters(brand=state["brand"])
        self.type_of_heat_treatment = state["type_of_heat_treatment"]
        self.hrc = state["hrc"]
        self.workpiece = state["workpiece"]
