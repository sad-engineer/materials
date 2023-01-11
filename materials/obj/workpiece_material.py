#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from typing import Optional, Union

from materials.scr.gen_fun import check_workpiece, check_heat_treatment
from materials.obj.material import Material
from materials.obj.constants import DEFAULT_NAMES_FOR_MATERIALS as DEFAULT_NAMES
from materials.obj.constants import DEFAULT_SETTINGS_FOR_MATERIAL as DEFAULT_SETTINGS


class WorkpieceMaterial(Material):
    """ Класс параметров обрабатываемого материала

    Parameters:
        brand : (str, optional) : Наименование материала (будет использовано для поиска по базе данных).
        type_of_mat : (int, optional) : Индекс типа материала.
        class_ : (str, optional) : Класс материала.
        subclass : (str, optional) : Подкласс материала.
        chemical_composition : (dict, optional) : Таблица химического состава материала.
        hardness_tabl_mpa : (pd.DataFrame, optional) : Таблица твердости (в МПа) материала в различных состояниях
            поставки.
        hardness_mpa_for_proc : (Union[float, int], optional) : Твердость материала (в МПа), используемая для расчетов.
        tabl_tensile_strength_mpa : (pd.DataFrame, optional) : Таблица пределов прочности материала (в МПа) в различных.
            состояниях поставки.
        tensile_strength_mpa_for_proc : (Union[float, int], optional) : Предел прочности (в МПа), используемый для
            расчетов.
        heat_treatment: (in range(3) or None, optional) : Тип термообработки:
            None - Без термообработки;
            0 - Нормализация;
            1 - Отжиг;
            2 - Улучшение;
        hrc : (float, optional) : Значение твердости после термообработки по системе HRC
        workpiece : (in range(6), optional) : Тип поверхности заготовки:
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
        Material.__init__(self, brand=None)
        self.type_of_heat_treatment: Optional[int] = None
        self.workpiece: Optional[int] = None
        self.hrc = hrc

        if isinstance(brand, type(None)):
            brand = DEFAULT_NAMES[2]
        self.get_material_parameters(brand)

        if not isinstance(heat_treatment, type(None)):
            self.update_heat_treatment(heat_treatment)

        if not isinstance(workpiece, type(None)):
            self.update_workpiece(workpiece)

    def update_heat_treatment(self, heat_treatment: Optional[Union[str, int]] = None):
        """ Проверяет значение термообработки. При корректном значении устанавливает тип термообработки
        """
        self.type_of_heat_treatment = check_heat_treatment(heat_treatment)

    def update_workpiece(self, workpiece: Union[str, int]):
        """ Проверяет значение типа поверхности заготовки. При корректном значении устанавливает тип поверхности
        заготовки.
        """
        self.workpiece = check_workpiece(workpiece)

    def get_default_settings(self) -> None:
        """ Настраивает атрибуты класса в соответствии с глобальными дефолтными настройками
        """
        for setting_name, setting_val in DEFAULT_SETTINGS.items():
            self.get_material_parameters(brand=setting_val) if setting_name == "brand" else setattr(
                self, setting_name, setting_val)

    @classmethod
    def default(cls):
        """ Возвращает экземпляр класса с настройками по умолчанию
        """
        return cls(brand=DEFAULT_SETTINGS["brand"],
                   heat_treatment=DEFAULT_SETTINGS["type_of_heat_treatment"],
                   hrc=DEFAULT_SETTINGS["hrc"],
                   workpiece=DEFAULT_SETTINGS["workpiece"],)


# if __name__ == "__main__":
    # material = WorkpieceMaterial()
    # print(material.__doc__)
    # print(material)
    # #
    # material.get_material_parameters("20")
    # print(material)
    # material.get_material_parameters("30")
    # print(material)
    # material.get_default_settings()
    # print(material)
    # print(material.type_of_heat_treatment)
    # print(material.workpiece)
    # print(material.hrc)
    #
    # material = WorkpieceMaterial(brand="35", heat_treatment=1, hrc=55, workpiece=2)
    # print(material)
    # print(material.type_of_heat_treatment)
    # print(material.workpiece)
    # print(material.hrc)
    #
    # material = WorkpieceMaterial()
    # material.get_default_settings()
    # print(material)
    # print(material.type_of_heat_treatment)
    # print(material.workpiece)
    # print(material.hrc)
    #
    # material = WorkpieceMaterial.default_material()
    # print(material)
    # print(material.type_of_heat_treatment)
    # print(material.workpiece)
    # print(material.hrc)
