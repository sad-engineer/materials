#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from materials.obj.containers import MaterialContainer
from service_for_my_projects import timeit, timeit_property

from materials.logger_settings import config
import logging.config
logging.config.dictConfig(config)


def main(brand: str):

    # workpiece_creator = MaterialContainer().workpiece_material_creator()
    # create = workpiece_creator.create
    # timeit("Время запроса одного материала: {}")(create)(brand)
    #
    # material_lister = MaterialContainer().material_lister()
    # timeit_property("Время запроса всех материалов: {}")(material_lister)("all")
    #
    # selection = material_lister.by_class
    # timeit("Время запроса материалов по классу: {}")(selection)(1)
    #
    # selection = material_lister.by_subclass
    # timeit("Время запроса материалов по подклассу 'Силумин': {}")(selection)("Силумин")
    #
    # selection = material_lister.by_subclass
    # timeit("Время запроса материалов по подклассу 'Хромокремнемарганцовистая сталь': {}")(selection)\
    #     ("Хромокремнемарганцовистая сталь")
    #
    # finder = MaterialContainer().container_for_materials().find()
    # values = timeit_property("Время запроса доступных значений: {}")(finder)("available_values")
    # print(values['subclass_of_material'])

    workpiece_creator = MaterialContainer().workpiece_material_creator()
    timeit_property("Время запроса всех материалов: {}")(workpiece_creator)("default")


if __name__ == '__main__':
    main("30")
