#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from materials.obj.containers import Container
import time


def main(brand: str):

    start_time = time.time()
    workpiece_creator = Container().workpiece_material_creator()
    materiall = workpiece_creator.create(brand)
    materiall.hrc = 50.5
    materiall.heat_treatment = 2
    end_time = time.time()
    time_1 = end_time - start_time
    print("Время запроса одного материала", time_1)

    material_lister = Container().material_lister()
    start_time_1 = time.time()
    materials = material_lister.all
    end_time_1 = time.time()
    time_1 = end_time_1 - start_time_1
    print("Время запроса всех материалов", time_1)
    print(f"Количество мвтериалов - {len(materials)} ")

    start_time_2 = time.time()
    selection = material_lister.by_class(1)
    end_time_2 = time.time()
    time_2 = end_time_2 - start_time_2
    print("Время запроса материалов по классу", time_2)

    start_time_3 = time.time()
    selection = material_lister.by_subclass("Силумин")
    end_time_3 = time.time()
    time_3 = end_time_3 - start_time_3
    print("Время запроса материалов по подклассу", time_3)

    start_time_4 = time.time()
    selection = material_lister.by_subclass("Хромокремнемарганцовистая сталь")
    print([item.brand for item in selection])
    end_time_4 = time.time()
    time_4 = end_time_4 - start_time_4
    print("Время запроса материалов по подклассу 2", time_4)

    start_time_5 = time.time()
    finder = Container().container_for_materials().find()
    print(finder.available_values['subclass_of_material'])
    end_time_5 = time.time()
    time_5 = end_time_5 - start_time_5
    print("Время запроса доступных значений", time_5)


if __name__ == '__main__':
    main("20")



