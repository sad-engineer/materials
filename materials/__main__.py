#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from materials.obj.containers import Container


def main(brand: str):
    # workpiece_creator = Container().workpiece_material_creator()
    # materiall = workpiece_creator.create(brand)
    # materiall.hrc = 50.5
    # materiall.heat_treatment = 2
    # print(materiall)

    material_lister = Container().material_lister()
    materials = material_lister.all
    print(len(materials))
    selection = [material for material in materials if material.index_class == 2]
    print(len(selection))


if __name__ == '__main__':
    main("20")



