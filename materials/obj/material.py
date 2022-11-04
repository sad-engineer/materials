#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        material
# Purpose:     Parameters of the processed material
#
# Author:      ANKorenuk
#
# Created:     09.04.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Параметры обрабатываемого материала
# -------------------------------------------------------------------------------
from typing import Optional, Union

from materials.find import characteristics
from materials.find import chem_struct
from materials.find import hardness
from materials.find import tensile_strength
from materials.fun import mean_col
from materials.obj.exceptions import ReceivedEmptyDataFrame
from materials.obj.constants import PATH_DB_FOR_MAT as PATH_DB
from materials.obj.constants import DEFAULT_NAMES_FOR_MATERIALS as DEFAULT_NAMES
from materials.obj.constants import DEFAULT_SETTINGS_FOR_MATERIALS as DEFAULT_SETTINGS
from materials.obj.constants import NAMES_OF_HEAT_TREATMENT as NAMES_HT
from materials.obj.constants import INDEXES_OF_HEAT_TREATMENT as INDEXES_HT
from materials.obj.constants import NAMES_OF_WORKPIECE as NAMES_WP
from materials.obj.constants import INDEXES_OF_WORKPIECE as INDEXES_WP


class Material():
    """ Класс параметров обрабатываемого материала
    
    Parameters
    ----------
    brand : str, optional
        Наименование материала (будет использовано для поиска по базе данных). 
        По умолчанию: None.
    heat_treatment: int, optional
        Тип термообработки:
            None - Без термообработки;
            0 - Нормализация;
            1 - Отжиг;
            2 - Улучшение;
        По умолчанию: None.
    HRC : float, optional
        Значение твердости после термообработки по системе HRC
    workpiece : int, optional
        Тип поверхности заготовки:
            0 - Без корки;
            1 - С коркой: прокат;
            2 - С коркой: поковка;
            3 - Отливка с нормальной коркой;
            4 - Отливка с загрязненной коркой;
            5 - С коркой: Медные и алюминиевые сплавы;
    """
    def __init__(self,
                 brand:Optional[str] = None,
                 heat_treatment:Optional[Union[str, int]] = None,
                 HRC:Optional[Union[float, int]] = None,
                 workpiece:int = 0):
        
        self.brand = brand                                      # наименование материала
        self.type_of_mat:Optional[int] = None                   # индекс типа материала,
        self.class_:Optional[str] = None                        # класс материала,
        self.subclass:Optional[str] = None                      # подкласс материала,
        self.chemical_composition = None                        #Таблица хим.состава материала
        self.tabl_hardness_MPa = None                           #Таблица твердости для материала в различных состояниях поставки
        self.hardness_MPa_for_proc:Optional[Union[float, int]] = None   #Твердость материала, используемая для рассчетов
        self.tabl_tensile_strength_MPa = None                  #Таблица пределов прочности материала в различных состояниях поставки
        self.tensile_strength_MPa_for_proc:Optional[Union[float, int]] = None    #Предел прочности, используемый для рассчетов
        self.update_heat_treatment(heat_treatment)              # Вид термообработки
        self.HRC = HRC                                          # Твердость обрабатываемого материала после термообработки
        self.update_workpiece(workpiece)                        #pz Состояние заготовки (с коркой/ без корки, и т.д.)
        self.get_default_settings

    
    @property
    def show(self) -> None:
        report = f"""
        ### Параметры обрабатываемого материала ###"""
        if self.brand:
            report += f"""
            Наименование материала: {self.brand}."""
        if self.type_of_mat:
            report += f"""
            Тип материала: {self.type_of_mat}."""
        if self.class_:
            report += f"""
            Класс материала: {self.class_}."""
        if self.subclass:
            report += f"""
            Подкласс материала: {self.subclass}."""
        if self.hardness_MPa_for_proc:
            report += f"""
            Твердость обрабатываемого материала = {self.hardness_MPa_for_proc} МПа."""
        if self.tensile_strength_MPa_for_proc:
            report += f"""
            Предел текучести для обрабатываемого материала = {self.tensile_strength_MPa_for_proc} МПа."""
        if self.type_of_heat_treatment:
            report += f"""
            Вид термообработки обрабатываемого материала = {self.type_of_heat_treatment}."""
        if self.HRC:
            report += f"""
            Твердость обрабатываемого материала после термообработки = {self.HRC} HRC."""
        if self.workpiece:
            report += f"""
            Состояние заготовки: {self.workpiece}."""
        print(report)
    

    def get_material_parameters(self, brand:Optional[str] = None) -> None:
        """ Задает: 
            класс материала, 
            подкласс, 
            индекс типа материала, 
            хим.состав, 
            твердость,
            предел прочности.
            
            Если в 'brand' передать новый материал, переопределит параметры 
            для нового материала"""
        
        is_negative_number = True if isinstance(brand, (float, int)) and brand < 0 else False
        new_brand_exists = not (brand in ["", " ", "  ", None, 0] or
                                isinstance(brand, type(None)) or
                                is_negative_number ) 
        
        if new_brand_exists and self.brand != brand:
            self.brand = brand
            self.get_material_characteristics() # По наменованию материала определяем его параметры: индекс типа материала, класс, подкласс материала
            self.get_chemical_composition()     # Заполняем таблицу хим.состава
            self.get_hardness()                 # Заполняем таблицу твердости и находим тверхость для рассчетов
            self.get_tensile_strength()         # Заполняем таблицу пределов прочности и значение для рассчетов

        
    def get_material_characteristics(self) -> None:
        """ Задает класс материала, подкласс, индекс типа материала
        """
        if not isinstance(self.brand, type(None)):
            index, class_, subclass = characteristics(brand = self.brand)
            self.type_of_mat = index
            self.class_ = class_
            self.subclass = subclass
           
            
    def get_chemical_composition(self) -> None:
        """ Создает таблицу химического состава материала. Вибирает хим.состав 
        из БД. Если в БД нет хим состава материала - берет значение по умолчанию
        """
        try:
            self.chemical_composition = chem_struct(brand = self.brand)
        except ReceivedEmptyDataFrame:
            default_brand = DEFAULT_NAMES[self.type_of_mat]
            self.chemical_composition = chem_struct(default_brand)
            print(f"Хим.состав материала {self.brand} не найден. Взят хим.состав материала по умолчанию: {default_brand}")
    
    
    def get_hardness(self) -> None:
        """ Получает таблицу твердости из БД. Если в БД нет таблицы твердости 
        для материала - выполняет то же для материала по умолчанию
        """
        try:
            self.tabl_hardness_MPa = hardness(brand = self.brand)
        except ReceivedEmptyDataFrame:
            default_brand = DEFAULT_NAMES[self.type_of_mat]
            self.hardness_tabl_MPa = hardness(brand = default_brand)
            print(f"Твердость материала {self.brand} не найдена. Взята твердость материала по умолчанию: {default_brand}")
        self.hardness_MPa_for_proc = mean_col(data = self.tabl_hardness_MPa["hardness"])
 
        
    def get_tensile_strength(self) -> None:
        """ Получает таблицу предела кратковременной прочности из БД. Если в 
        БД нет таблицы твердости для материала - выполняет то же для материала по умолчанию
        """
        try:
            self.tabl_tensile_strength_MPa = tensile_strength(brand = self.brand)
        except ReceivedEmptyDataFrame:
            default_brand = DEFAULT_NAMES[self.type_of_mat]
            self.tabl_tensile_strength_MPa = tensile_strength(brand = default_brand)
            print(f"Предел прочности материала {self.brand} не найден. Взят для материала по умолчанию: {default_brand}")
        self.tensile_strength_MPa_for_proc = mean_col(data = self.tabl_tensile_strength_MPa["tensile_strength"])
 
    
    @property
    def get_default_settings(self) -> None:
        """ Настраивает атрибуты класса в соответствии с глобальными дефолтными настрйками
        """
        for setting_name, setting_val in DEFAULT_SETTINGS.items():
            self.get_material_parameters(brand=setting_val) if setting_name == "brand" else setattr(self, setting_name,
                                                                                                    setting_val)


    def update_heat_treatment(self, heat_treatment:Optional[Union[str, int]] = None):
        """ Проверяет значение термообработки. При корректном значении устанавливает тип термообработки
        """
        if isinstance(heat_treatment, type(None)):
            print("Параметр вида термообработки не был передан")
        else:
            if isinstance(heat_treatment, int):
                if heat_treatment in NAMES_HT:
                    self.type_of_heat_treatment = heat_treatment
                else:
                    message = {"Индекс вида термообработки не определен."}
                    raise InvalidValue(message)
            elif isinstance(heat_treatment, str):
                if heat_treatment in INDEXES_HT:
                    self.type_of_heat_treatment = INDEXES_HT[heat_treatment]
                else:
                    message = {"Вид термообработки не определен."}
                    raise InvalidValue(message)
            else:
                message = {"Вид термообработки не определен."}
                raise InvalidValue(message)


    def update_workpiece(self, workpiece:Optional[Union[str, int]] = None):
        """ Проверяет значение типа поверхности заготовки. При корректном значении устанавливает тип  поверхности
        заготовки.
        """
        if  isinstance(workpiece, type(None)):
            print("Параметр типа поверхности заготовки не был передан")
        else:
            if isinstance(workpiece, int):
                if workpiece in NAMES_WP:
                    self.workpiece = workpiece
                else:
                    message = {"Индекс типа поверхности заготовки не определен."}
                    raise InvalidValue(message)
            elif isinstance(workpiece, str):
                if workpiece in INDEXES_WP:
                    self.workpiece = INDEXES_WP[workpiece]
                else:
                    message = {"Тип поверхности заготовки термообработки не определен."}
                    raise InvalidValue(message)
            else:
                message = {"Тип поверхности заготовки термообработки не определен."}
                raise InvalidValue(message)
