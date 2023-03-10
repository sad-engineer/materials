#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from materials.obj.containers import Container
from materials.obj.decorators import timeit, timeit_property

from materials.logger_settings import config
import logging.config
logging.config.dictConfig(config)


def main(brand: str):

    workpiece_creator = Container().workpiece_material_creator()
    create = workpiece_creator.create
    timeit("Время запроса одного материала: {}")(create)(brand)

    material_lister = Container().material_lister()
    timeit_property("Время запроса всех материалов: {}")(material_lister)("all")

    selection = material_lister.by_class
    timeit("Время запроса материалов по классу: {}")(selection)(1)

    selection = material_lister.by_subclass
    timeit("Время запроса материалов по подклассу 'Силумин': {}")(selection)("Силумин")

    selection = material_lister.by_subclass
    timeit("Время запроса материалов по подклассу 'Хромокремнемарганцовистая сталь': {}")(selection)\
        ("Хромокремнемарганцовистая сталь")

    finder = Container().container_for_materials().find()
    values = timeit_property("Время запроса доступных значений: {}")(finder)("available_values")
    print(values['subclass_of_material'])


if __name__ == '__main__':
    workpiece_creator = Container().workpiece_material_creator()
    create = workpiece_creator.create
    create("20")


