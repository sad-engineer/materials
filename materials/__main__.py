#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from materials.obj.containers import CreatorsContainer


def main(brand: str):
    workpiece_creator = CreatorsContainer().workpiece_material_creator()
    materiall = workpiece_creator.create(brand)
    materiall.hrc = 50.5
    materiall.heat_treatment = 2
    print(materiall)


if __name__ == '__main__':
    main("20")



