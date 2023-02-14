#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
import sqlite3
import pandas as pd
from typing import Optional, Union

# from materials.obj.constants import PATH_DB_FOR_MAT as PATH_DB
# from materials.obj.constants import NAMES_OF_WORKPIECE as NAMES_WP
# from materials.obj.constants import INDEXES_OF_WORKPIECE as INDEXES_WP
# from materials.obj.constants import NAMES_OF_HEAT_TREATMENT as NAMES_HT
# from materials.obj.constants import INDEXES_OF_HEAT_TREATMENT as INDEXES_HT
from service import ReceivedEmptyDataFrame
# from service import ReceivedEmptyDataFrame
from service import InvalidValue


def get_average(data: pd.Series, order: int = 6) -> float:
    """ Считает среднее значение Series

    :param data: Серия значений для подсчета среднего значения.
    :param order: Точность округления
    :return: Возвращает pd.Series, который содержит средние значения по строкам.
    """
    pd.options.mode.chained_assignment = None
    for i, el in enumerate(data.to_numpy()):
        if isinstance(el, list):
            data.loc[i] = round(sum(el)/len(el), 6)
        elif isinstance(el, (float, int)):
            data.loc[i] = float(el)
        elif isinstance(el, str):
            el = get_range(el)
            data.loc[i] = round(sum(el)/len(el), 6)
        else:
            data.loc[i] = None
    return round(data.mean(), order)


def is_correct_record(record: pd.DataFrame):
    """Проверяет полученную запись из БД. Запись должна содержать одну строку

    :param record: проверяемый на соответствие DataFrame.
    :return: True если record содержит одну строку.
    """
    if len(record) == 1:
        if not isinstance(record.loc[0], type(None)):
            return True
        else:
            raise ReceivedEmptyDataFrame("Получена пустая таблица. Проверьте данные БД и запроса.")
    elif len(record) == 0:
        raise ReceivedEmptyDataFrame("Получена пустая таблица. Проверьте данные БД и запроса.")
    elif len(record) > 1:
        message = f"Таблица содержит больше одной строки. Проверь запрос, или данные БД. Должна быть одна строка"
        raise InvalidValue(message)


def is_correct_hardness(hardness: pd.DataFrame):
    """ Проверяет полученную запись твердости из БД на наличие значений во втором столбце.

    :param hardness: проверяемый на соответствие DataFrame.
    :return: True если ячейка во втором столбце содержит данные.
    """
    if isinstance(hardness["hardness"][0], type(None)):
        message = f"Таблица твердости не содержит твердость материала {hardness['brand_of_material'][0]}. " \
                  f"Проверь запрос, или данные БД. Должны быть данные по твердости."
        raise ReceivedEmptyDataFrame(message)
    return True


def is_correct_tensile_strength(brand: str, text_tensile_strength: pd.DataFrame):
    """ Проверяет полученную запись предела прочности из БД на наличие значений.

    :param brand: марка материала.
    :param text_tensile_strength: проверяемая на соответствие запись предела прочности.
    :return: True если запись содержит данные.
    """
    if isinstance(text_tensile_strength[0], type(None)):
        message = f"Таблица твердости не содержит твердость материала {brand}. Проверь запрос, или данные БД. Должны " \
                  f"быть данные по твердости."
        raise ReceivedEmptyDataFrame(message)
    return True


def get_table_hardness(brand: str, text_hardness: str) -> pd.DataFrame:
    """ Восстанавливает таблицу твердости из текста БД.

    :param brand: марка материала.
    :param text_hardness: текст описывающий твердость.
    :return: таблицу твердости.
    """
    rows = text_hardness.split(";")
    data_table = {}
    for row in rows:
        data_row = {}
        items = row.split("/")
        for item in items:
            if item.find("HB 10 -1") != -1:
                data_row["hardness"] = get_hardness(item)
            elif item.find(brand) != -1:
                data_row["condition"] = get_condition(brand, item)
            else:
                raise InvalidValue("В строке передан неверный текст.")
        if "hardness" in data_row:
            data_table[rows.index(row)] = data_row
    data_table = pd.DataFrame(data_table).T
    if data_table.empty:
        raise ReceivedEmptyDataFrame("Таблица твердости не содержит значений твердости")
    return data_table


def get_table_tensile_strength(text_tensile_strength: str) -> pd.DataFrame:
    """ Восстанавливает таблицу предела прочности из текста БД.

    :param text_tensile_strength: текст описывающий предел прочности.
    :return: таблицу предела прочности.
    """
    rows = text_tensile_strength.split(";")
    data_table = {}
    for row in rows:
        data_row = {}
        items = row.strip().split("/")
        for item in items:
            if item.find("еханические свойства") == -1:
                if item != "":
                    if item.find("ГОСТ") != -1:
                        data_row["condition"] = item
                    else:
                        data_row["tensile_strength"] = item
        if data_row != {} and "tensile_strength" in data_row:
            data_table[rows.index(row)] = data_row
    result = pd.DataFrame(data_table).T
    if len(result) != 0:
        return result
    else:
        message = f"Таблица предела прочности не содержит предел прочности. Проверь запрос, или данные БД. Должны " \
                  f"быть данные по твердости"
        raise ReceivedEmptyDataFrame(message)


def get_hardness(text: str) -> str:
    """ Возвращает диапазон численных значений из строки вида: "HB 10 -1 = 140 - 300 МПа"

    :param text: строка вида: "HB 10 -1 = 140 - 300 МПа".
    :return: строку вида: "140 - 300".
    """
    text = text.replace("HB 10 -1 =", "")
    text = text.replace("МПа", "")
    text = text.replace(" ,", "")
    return text.strip()


def get_condition(brand: str, text: str) -> str:
    """ Возвращает описание состояния материала

    :param brand: марка материала.
    :param text: строка, описывающая состояние материала.
    """
    text = text.replace("Твердость", "")
    text = text.replace(brand, "")
    if text.strip() == ",":
        return "Твердость"
    return text.strip()


def get_range(rvalue) -> tuple:
    """ Выделяет минимальное и максимальное значения диапазона 'rvalue'.

    :param rvalue: переменная, описывающая диапазон значений (строка, кортеж, список)
    :return: минимальное и максимальное значение диапазона значение (значения типа "float").
    """
    if isinstance(rvalue, (tuple, list)):
        return get_range_for_list(rvalue)
    elif isinstance(rvalue, str):
        return get_range_for_str(rvalue)
    raise InvalidValue(f"Необходимо передать диапазон числовых значений! Было передано: {rvalue}")


def get_range_for_list(rvalue: [tuple, list]) -> tuple:
    """ Выделяет минимальное и максимальное значения диапазона 'rvalue' и возвращает их.

    :param rvalue: диапазон значений, типа [2.3, 2.9]
    :return: возвращает минимальное и максимальное значение диапазона значение (значения типа "float").
    """
    if len(rvalue) != 2:
        raise InvalidValue(f"Диапазон значений {rvalue} должен содержать 2 числа!")
    new_rvalue = []
    for el in rvalue:
        if isinstance(el, str):
            try:
                new_rvalue.append(float(el))
            except ValueError:
                raise InvalidValue(f"Диапазон значений {rvalue} должен содержать числа")
        elif not isinstance(el, (float, int)):
            raise InvalidValue(f"Диапазон значений {rvalue} должен содержать числа")
        else:
            new_rvalue.append(el)
    return min(new_rvalue), max(new_rvalue)


def get_range_for_str(rvalue: str) -> tuple:
    """Выделяет числовые значения из строки, описывающей диапазон значений.

    :param rvalue: диапазон значений, типа '2.3-2.9' или '2, 5.6'
    :return: возвращает минимальное и максимальное значение диапазона значение (значения типа "float"). Если в строке
        передали число, вернет два экземпляра этого числа
    """
    try:
        return float(rvalue), float(rvalue)
    except ValueError:
        dash = rvalue.find('-')
        comma = rvalue.find(',')
        #TODO: Сделать три точки
        if dash != -1 and comma != -1:
            raise InvalidValue(f"Диапазон значений {rvalue} записан не верно! "
                               f"Запишите диапазон в формате '2.3-2.9' или '2, 5.6'")
        elif dash != -1:
            rvalue = rvalue.split('-')
        elif comma != -1:
            rvalue = rvalue.split(',')
        else:
            raise InvalidValue(f"Диапазон значений {rvalue} записан не верно! Диапазон чисел не определен.")
        if len(rvalue) != 2:
            raise InvalidValue(f"Диапазон значений {rvalue} должен содержать 2 числа!")
        return get_range_for_list(rvalue)


# def is_brand_in_database(brand: str) -> bool:
#     """ Уточняет, есть ли материал "brand" в БД
#
#     :param brand: проверяемый материал
#     :return: True, если материал имеется в базе данных
#     """
#     db, cursor = connect()
#     materials = pd.read_sql(f"SELECT brand FROM materials ", db)
#     db.close()
#     return brand in set(materials["brand_of_material"])


# def check_workpiece(workpiece: Union[str, int]) -> Union[str, int]:
#     """ Проверяет значение типа заготовки
#
#     :param workpiece: тип заготовки.
#     :return: значение типа заготовки, если оно удовлетворяет условиям проверки.
#     """
#     if isinstance(workpiece, int):
#         if workpiece in NAMES_WP:
#             return workpiece
#         else:
#             raise InvalidValue(f"Не верный индекс типа поверхности заготовки: {workpiece=}.")
#     elif isinstance(workpiece, str):
#         if workpiece in INDEXES_WP:
#             return INDEXES_WP[workpiece]
#         else:
#             raise InvalidValue(f"Не верный тип поверхности заготовки термообработки: {workpiece=}.")
#     else:
#         raise InvalidValue(f"Не верный тип поверхности заготовки термообработки: {workpiece=}.")
#
#
# def check_heat_treatment(heat_treatment: Union[str, int]) -> Union[str, int]:
#     """ Проверяет значение вида термообработки
#
#     :param heat_treatment: вид термообработки.
#     :return: значение вида термообработки, если оно удовлетворяет условиям проверки.
#     """
#     if isinstance(heat_treatment, int):
#         if heat_treatment in NAMES_HT:
#             return heat_treatment
#         else:
#             raise InvalidValue(f"Не верный индекс вида термообработки {heat_treatment=}.")
#     elif isinstance(heat_treatment, str):
#         if heat_treatment in INDEXES_HT:
#             return INDEXES_HT[heat_treatment]
#         else:
#             raise InvalidValue(f"Не верный вид термообработки {heat_treatment=}.")
#     else:
#         raise InvalidValue("Вид термообработки не определен.")
