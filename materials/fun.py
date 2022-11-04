#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        fun
# Purpose:     Contains local functions for working with the database
#
# Author:      ANKorenuk
#
# Created:     28.10.2022
# Copyright:   (c) ANKorenuk 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# Содержит локальные функции работы с БД
# -------------------------------------------------------------------------------
import sqlite3
# from typing import Optional, Union
import pandas as pd


def connect(filename: str):
    """ Создает и подключает базу данных если ее нет. Если БД есть - подключает ее

    Parameters
    ----------
    filename : str
        Имя файла БД.

    Returns
    -------
    db : TYPE
        Указатель на подключенную БД.
    cursor : TYPE
        Указатель на курсор БД.
    """
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    db.commit()
    return db, cursor


def mean_col(data: pd.Series,
             order: int = 3) -> pd.Series:
    """ Считает среднее значение Series

    Parameters
    ----------
    data : pd.Series
        Серия значений для подсчета среднего значения.
    order : int, optional
        Точность округления
        По умолчанию = 3.

    Returns
    -------
    pd.Series
        Возвращает Series, который содержит средние значения по строкам.
    """
    pd.options.mode.chained_assignment = None
    for i, el in enumerate(data.to_numpy()):
        if isinstance(el, list):
            data.loc[i] = sum(el)/len(el)
        elif isinstance(el, (float, int)):
            data.loc[i] = float(el)
        else:
            data.loc[i] = None
    return round(data.mean(), order)
#
#
# def average(range_val:str):
#     """На вход подать строку типа 'до 0.05' / '0.2 - 0.5'
#     На выходе получим среднее значение диапазона (значение типа float)"""
#     if isinstance(range_val, type(None)):
#         return 0
#     elif isinstance(range_val, (float, int)):
#         return range_val
#     else:
#         if range_val == range_val:
#             if range_val.find("-") != -1:
#                 range_val = range_val.split("-")
#             elif range_val.find(" - ") != -1:
#                 range_val = range_val.split("-")
#             elif range_val.find("до") != -1:
#                 range_val = [range_val.replace("до", "").replace(" ", "")]
#             elif range_val.find("min") != -1:
#                 range_val = [range_val.replace("min", "").replace(" ", ""),
#                              range_val.replace("min", "").replace(" ", "")]
#         if isinstance(range_val, (tuple, list)):
#             if len(range_val) == 1:
#                 range_val = float(range_val[0])/2
#             elif len(range_val) == 2:
#                 range_val = (float(range_val[1]) + float(range_val[0]))/2
#             return range_val
#         else:
#             print (f"Ошибка обработки значения {range_val=}")
