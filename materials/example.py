#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Основной модуль для запуска приложения материалов.
Этот файл содержит основную логику для работы с базой данных, используя модели и функции CRUD.
"""
import os
# Настройка логирования
os.environ["SQLALCHEMY_ECHO"] = "False"

from materials import ( 
    get_chemical_composition_by_brand, 
    get_standard_of_chemical_composition_by_brand, 
    get_material_by_brand, 
    get_mechanical_properties_by_brand, 
    get_technological_properties_by_brand, 
    get_hardness_by_brand
)


def print_material_info(brand: str):
    """Пример получения всей доступной информации о материале"""
    print(f"\nПолная информация о материале {brand}:")
    print("-" * 50)

    # Основная информация
    material = get_material_by_brand(brand)
    if not material:
        print(f"Материал {brand} не найден")
        return

    # Химический состав
    chemical = get_chemical_composition_by_brand(brand)
    if chemical:
        print(f"\nХимический состав: {chemical}")
        print(f"Cu = {chemical.Cu}")
        print(f"Ni = {chemical.Ni}")
        print(f"C = {chemical.C}")
        print(f"Si = {chemical.Si}")
        print(f"Mn = {chemical.Mn}")
        print(f"P = {chemical.P}")
        print(f"Mo = {chemical.Mo}")
        print(f"S = {chemical.S}")
        print(f"Cr = {chemical.Cr}")

        # Механические свойства
    mechanical = get_mechanical_properties_by_brand(brand)
    if mechanical:
        print("\nМеханические свойства:")
        print(f"Механические свойства {brand}:")
        print(f"Предел текучести: {mechanical.yield_strength} МПа")
        print(f"Предел прочности: {mechanical.tensile_strength} МПа")
        print(f"Относительное удлинение: {mechanical.elongation_at_break}%")
        print(f"Ударная вязкость: {mechanical.impact_strength} Дж/см²")

    # Технологические свойства
    tech = get_technological_properties_by_brand(brand)
    if tech:
        print("\nТехнологические свойства:")
        print(f"Свариваемость: {tech.weldability}")
        print(f"Чувствительность к флокуляции: {tech.flock_sensitivity}")
        print(f"Температурная хрупкость: {tech.temper_brittleness}")

    # Твердость
    hardness = get_hardness_by_brand(brand)
    if hardness:
        print("\nТвердость:")
        print(f"Твердость: {hardness.hardness_value}")

    # Стандарт
    standard = get_standard_of_chemical_composition_by_brand(brand)
    if standard:
        print(f"\nСтандарт: {standard}")


# Использование
print_material_info("30ХМА")
