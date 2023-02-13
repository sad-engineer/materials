#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import time

from materials.obj.containers import CharacteristicsOfMaterial
from materials.obj.containers import ChemicalComposition
from materials.obj.containers import Hardness, Materials, MechanicalProperties, TechnologicalProperties
from materials.obj.containers import CreatorsContainer


def main(brand: str):
    # print(CharacteristicsOfMaterial().find().by_brand(brand))
    # print(ChemicalComposition().finder().by_brand(brand))
    # print(Hardness().finder().by_brand(brand))
    # print(Materials().find().by_brand(brand))
    # print(MechanicalProperties().finder().by_brand(brand))
    # print(TechnologicalProperties().find().by_brand(brand))

    container = CreatorsContainer()
    creator = container.creator()
    print(creator)
    creator.by_brand(brand)


if __name__ == '__main__':
    main("20")



