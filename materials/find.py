#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
import pandas as pd
from materials.scr.gen_fun import connect
from materials.obj.constants import INDEXES_OF_CLASS_MATERIALS
from materials.scr.gen_fun import is_correct_record
from materials.scr.gen_fun import is_correct_hardness
from materials.scr.gen_fun import is_correct_tensile_strength
from materials.scr.gen_fun import get_table_hardness
from materials.scr.gen_fun import get_table_tensile_strength


def by_class(class_of_material: str = "Сталь для отливок") -> list[str]:
    """Открывает базу данных по материалам (по пути 'path_bd'), запрашивает список всех доступных материалов по
    наименованию группы материала ('class_of_material'). Возвращает сортированный список.

    Parameters:
        class_of_material : Класс материала, по которому нужно выполнить поиск материалов

    Returns:
        Сортированный список имен доступных в БД материалов.
    """
    db, cursor = connect()
    if class_of_material in ['Чугун серый', 'Чугун ковкий']:
        materials = pd.read_sql(f"SELECT * FROM materials WHERE index_of_material_class = "
                                f"'{INDEXES_OF_CLASS_MATERIALS[class_of_material]}'", db)
    else:
        materials = pd.read_sql(f"SELECT * FROM materials WHERE class_of_material = '{class_of_material}'", db)
    db.close()
    return sorted(list(materials["brand_of_material"]))


def by_index(index: int = 0) -> list[str]:
    """Открывает базу данных по материалам (по пути 'path_bd'), запрашивает список всех доступных материалов по индексу
    группы материала ('index_of_material'). Возвращает сортированный список.

    Parameters:
        index : Индекс класса материала, по которому нужно выполнить поиск материалов. От 0 до 11.

    Returns:
        Сортированный список имен доступных в БД материалов.
    """
    db, cursor = connect()
    materials = pd.read_sql(f"SELECT * FROM materials WHERE index_of_material_class = '{index}'", db)
    db.close()
    return sorted(list(materials["brand_of_material"]))


def characteristics(brand: str = "20") -> tuple[int, str, str]:
    """Запрашивает из БД индекс, группу и подгруппу материала.

    Parameters:
        brand : Наименование материала, например "07Х17Н16ТЛ"

    Returns:
        Индекс класса, класс, подгруппа материала
    """
    db, cursor = connect()
    material = pd.read_sql(f"SELECT * FROM materials WHERE brand_of_material = '{brand}'", db)
    db.close()
    index = material.loc[0]["index_of_material_class"]
    class_ = material.loc[0]["class_of_material"]
    subclass = material.loc[0]["subclass_of_material"]
    return index, class_, subclass


def chem_struct(brand: str = "20") -> dict:
    """Запрашивает из БД химический состав материала.

    Parameters:
        brand : Наименование материала, например "07Х17Н16ТЛ"

    Returns:
        Возвращает словарь, содержащий хим состав материала. Если таблица химсостава, полученная в результате запроса,
        содержит более одной строки или не содержит строк вообще, выкидывает ошибку.
    """
    db, cursor = connect()
    chemical_composition = pd.read_sql(f"SELECT * FROM chemical_composition WHERE brand_of_material = '{brand}'", db)
    db.close()
    if is_correct_record(chemical_composition):
        return chemical_composition.transpose().dropna().to_dict()[0]


def hardness(brand: str = "20"):
    """Запрашивает из БД твердость материала.

    Parameters:
        brand : Наименование материала, например "07Х17Н16ТЛ".

    Returns:
        Возвращает таблицу с твердостью материала для различных условий состояния материала.
    """
    db, cursor = connect()
    hardness = pd.read_sql(f"SELECT * FROM hardness WHERE brand_of_material = '{brand}'", db)
    db.close()

    # Проверяем запрошенные данные. По наименованию материала, от БД должен приходить DataFrame, содержащий одну строку,
    # во втором столбце которого должны быть значения (не None)
    if is_correct_record(hardness):
        if is_correct_hardness(hardness):
            return get_table_hardness(brand=brand, text_hardness=hardness["hardness"][0])


def tensile_strength(brand: str = "20"):
    """Запрашивает из БД предел прочности.

    Parameters:
        brand : Наименование материала, например "07Х17Н16ТЛ".

    Returns:
        Возвращает DataFrame, содержащий пределы текучести материала для различных условий состояния материала.
    """
    db, cursor = connect()
    mechanical_properties = pd.read_sql(
        f"SELECT * FROM mechanical_properties WHERE brand_of_material = '{brand}'", db)
    data = mechanical_properties["tensile_strength"]
    db.close()
    if is_correct_record(data):
        if is_correct_tensile_strength(brand, data):
            if not isinstance(data[0], type(None)):
                return get_table_tensile_strength(text_tensile_strength=data[0])
