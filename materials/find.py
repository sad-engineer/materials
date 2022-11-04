#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        find
# Purpose:     Contains the functions of working with the database for the machine_tools
#
# Author:      ANKorenuk
#
# Created:     28.10.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Содержит функции работы с базой данных по станкам
# -------------------------------------------------------------------------------
import re
import pandas as pd
from materials.fun import connect
from materials.fun import mean_col
from materials.obj.constants import PATH_DB_FOR_MAT as PATH_DB


def by_class(class_of_material: str = "Сталь для отливок", path_bd: str = PATH_DB):
    """Открывает базу данных по материаллам (по пути 'path_bd'), запрашивает
    список всех доступных материалов по наименованию группы материала
    ('class_of_material'). Возвращает сортированный список.

    Parameters
    ----------
    class_of_material : str, optional
        Класс материала, по которому нужно выполнить поиск материалов.
        По умолчанию : "Сталь для отливок"
    path_bd : str, optional
        Путь к базе данных по материаллам

    Returns
    -------
    list_of_materials : list
        Сортированный список имен доступных в БД материалов.
    """
    db, cursor = connect(path_bd)
    materials = pd.read_sql(f"SELECT * FROM materials WHERE class_of_material = '{class_of_material}'", db)
    db.close()
    return sorted(list(materials["brand_of_material"]))


def by_index(index: int = 0,
             path_bd: str = PATH_DB):
    """Открывает базу данных по материаллам (по пути 'path_bd'), запрашивает
    список всех доступных материалов по индексу группы материала
    ('index_of_material'). Возвращает сортированный список.

    Parameters
    ----------
    index : , optional
        Игдекс класса материала, по которому нужно выполнить поиск материалов.
        От 0 до 11
        По умолчанию : 0
    path_bd : str, optional
        Путь к базе данных по материаллам

    Returns
    -------
    list_of_materials : list
        Сортированный список имен доступных в БД материалов.
    """
    db, cursor = connect(path_bd)
    materials = pd.read_sql(f"SELECT * FROM materials WHERE index_of_material_class = '{index}'", db)
    db.close()
    return sorted(list(materials["brand_of_material"]))


def characteristics(brand: str = "20",
                    path_bd: str = PATH_DB):
    """Запрашивает из БД индекс, группу и подгруппу материала.

    Parameters
    ----------
    brand : str, optional
        Наименование материала, например "07Х17Н16ТЛ".
        По умолчанию : "20".
    path_bd : str, optional
        Путь к базе данных по материаллам.

    Returns
    -------
    index, class_, subclass
        где:

        index : int
            Индекс класса материала
        class_ : str
            Класс материала
        subclass : str
            Подгруппа материала
    """

    db, cursor = connect(path_bd)
    material = pd.read_sql(f"SELECT * FROM materials WHERE brand_of_material = '{brand}'", db)
    db.close()
    index = material.loc[0]["index_of_material_class"]
    class_ = material.loc[0]["class_of_material"]
    subclass = material.loc[0]["subclass_of_material"]
    return index, class_, subclass


def chem_struct(brand: str = "20",
                path_bd: str = PATH_DB):
    """Запрашивает из БД химический состав материала.

    Parameters
    ----------
    brand : str, optional
        Наименование материала, например "07Х17Н16ТЛ".
        По умолчанию : "20".
    path_bd : str, optional
        Путь к базе данных по материаллам.

    Returns
    -------
    chemical_composition : dict
        Возвращает словарь, содержащий хим состав материала.
        Если таблица хим.состава, полученная в результате запроса, содержит
        более одной строки или не содержит строк вообще, выкидывает ошибку.
    """
    db, cursor = connect(path_bd)
    chemical_composition = pd.read_sql(
        f"SELECT * FROM chemical_composition WHERE brand_of_material = '{brand}'", db).transpose().to_dict()
    db.close()
    if len(chemical_composition) == 1:
        return chemical_composition[0]
    elif len(chemical_composition) == 0:
        from obj.exceptions import ReceivedEmptyDataFrame
        message = f"Получена пустая таблица химического состава материала:{brand}. Проверьте данные БД: {path_bd}"
        raise ReceivedEmptyDataFrame(message)
    elif len(chemical_composition) > 1:
        from obj.exceptions import UnexpectedDataInDataFrame
        message = f"Таблица хим.состава материала содержит больше одной строки. Проверь запрос, или данные БД: {path_bd}. Должна быть одна строка"
        raise UnexpectedDataInDataFrame(message)


def hardness(brand: str = "20",
             path_bd: str = PATH_DB):
    """Запрашивает из БД твердость материала.

    Parameters
    ----------
    brand : str, optional
        Наименование материала, например "07Х17Н16ТЛ".
        По умолчанию : "20".
    path_bd : str, optional
        Путь к базе данных по материаллам.

    Returns
    -------
    pd.DataFrame
        Возвращает таблицу с твердостью материала для различных условий
        состояния материала.
    """
    db, cursor = connect(path_bd)
    hardness = pd.read_sql(f"SELECT * FROM hardness WHERE brand_of_material = '{brand}'", db)
    db.close()

    # Проверяем запрошенные данные. По наименованию материала, от БД должен
    # приходить Датафрейм, содержащий одну строку, во втором столбце которого
    # должны быть значения (не None)
    if len(hardness) != 1:
        if len(hardness) == 0:
            from obj.exceptions import ReceivedEmptyDataFrame
            message = f"Получена пустая таблица твердости материала:{brand}. Проверьте данные БД: {path_bd}"
            raise ReceivedEmptyDataFrame(message)
        elif len(hardness) > 1:
            from obj.exceptions import UnexpectedDataInDataFrame
            message = f"Таблица твердости материала содержит больше одной строки. Проверь запрос, или данные БД: {path_bd}. Должна быть одна строка"
            raise UnexpectedDataInDataFrame(message)
    else:
        if isinstance(hardness["hardness"][0], type(None)):
            from obj.exceptions import ReceivedEmptyDataFrame
            message = f"Таблица твердости не содержит твердость материала {brand}. Проверь запрос, или данные БД: {path_bd}. Должны быть данные по твердости"
            raise ReceivedEmptyDataFrame(message)
        else:
            data = {}
            hardness_pro = pd.DataFrame()
            value = hardness["hardness"][0]
            value = value.split(";")
            for item in value:
                index_row = value.index(item)
                if item != "":
                    item = item.split("/")
                    if len(item) == 1:
                        data["material_condition"] = None
                    elif len(item) > 1:
                        val = item[1].split("=")
                        if re.search("\d{1,4} - \d{1,4}", val[1]):
                            # Ищем запись типа "126 - 178"
                            result = re.search("\d{1,4} - \d{1,4}", val[1]).group(0)
                            result = result.split(" - ")
                            for j in range(len(result)):
                                result[j] = float(result[j])
                        elif re.search("\d{1,4}-\d{1,4}", val[1]):
                            # Ищем запись типа "126-178"
                            result = re.search("\d{1,4}-\d{1,4}", val[1]).group(0)
                            result = result.split("-")
                            for j in range(len(result)):
                                result[j] = float(result[j])
                        elif re.search("\d{1,4}", val[1]):
                            # Ищем запись типа "126"
                            result = re.search("\d{1,4}", val[1]).group(0)
                            result = float(result)
                        data["material_condition"] = item[0]
                        data["hardness"] = result
                        hardness_pro = pd.concat([hardness_pro, pd.DataFrame(data, index=[index_row])], axis=0,
                                                 ignore_index=True)
    return hardness_pro


def tensile_strength(brand: str = "20",
                     path_bd: str = PATH_DB):
    """Запрашивает из БД предел прочности.

    Parameters
    ----------
    brand : str, optional
        Наименование материала, например "07Х17Н16ТЛ".
        По умолчанию : "20".
    path_bd : str, optional
        Путь к базе данных по материаллам.

    Returns
    -------
        Возвращает DataFrame, содержащий пределы текучести материала для
        различных условий состояния материала.
    """
    db, cursor = connect(path_bd)
    mechanical_properties = pd.read_sql(
        f"SELECT * FROM mechanical_properties WHERE brand_of_material = '{brand}'", db)
    tensile_strength_table = mechanical_properties["tensile_strength"]
    db.close()

    if len(tensile_strength_table) != 1:
        if len(tensile_strength_table) == 0:
            from obj.exceptions import ReceivedEmptyDataFrame
            message = f"Получена пустая таблица твердости материала:{brand}. Проверьте данные БД: {path_bd}"
            raise ReceivedEmptyDataFrame(message)
        elif len(tensile_strength_table) > 1:
            from obj.exceptions import UnexpectedDataInDataFrame
            message = f"Таблица твердости материала содержит больше одной строки. Проверь запрос, или данные БД: {path_bd}. Должна быть одна строка"
            raise UnexpectedDataInDataFrame(message)
    else:
        if isinstance(tensile_strength_table[0], type(None)):
            from obj.exceptions import ReceivedEmptyDataFrame
            message = f"Таблица твердости не содержит твердость материала {brand}. Проверь запрос, или данные БД: {path_bd}. Должны быть данные по твердости"
            raise ReceivedEmptyDataFrame(message)
        else:
            data_to_row = {}
            strength_pro = pd.DataFrame()
            tensile_strength_table[0] = tensile_strength_table[0].strip()
            list_row = tensile_strength_table[0].split(";")

            for row in list_row:
                if row in ["", " ", "  "]:
                    list_row.remove(row)

            for row in list_row:
                index_row = list_row.index(row)
                row = row.strip()
                data = row.split("/")
                if data[1] != "None" or not isinstance(data[1], type(None)):
                    if re.search("\d{1,4} - \d{1,4}", data[1]):
                        # Ищем запись типа "126 - 178"
                        result = re.search("\d{1,4} - \d{1,4}", data[1]).group(0)
                        result = result.split(" - ")
                        for j in range(len(result)):
                            result[j] = float(result[j])
                    elif re.search("\d{1,4}-\d{1,4}", data[1]):
                        # Ищем запись типа "126-178"
                        result = re.search("\d{1,4}-\d{1,4}", data[1]).group(0)
                        result = result.split("-")
                        for j in range(len(result)):
                            result[j] = float(result[j])
                    elif re.search("\d{1,4}", data[1]):
                        # Ищем запись типа "126"
                        result = re.search("\d{1,4}", data[1]).group(0)
                        result = float(result)

                    data_to_row["material_condition"] = data[0]
                    data_to_row["tensile_strength"] = result
                new_row = pd.Series(data=data_to_row, name=str(index_row))
                strength_pro = pd.concat([strength_pro, pd.DataFrame(new_row).T], axis=0, ignore_index=True)
    return strength_pro


if __name__ == "__main__":
    print(by_class())
    print(by_index())
    print(characteristics())
    print(chem_struct())
    print(hardness())
    print(tensile_strength())
    print(mean_col(tensile_strength()['tensile_strength']))

