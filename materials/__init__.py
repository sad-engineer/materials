#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Константы пакета
from materials.obj.constants import DEFAULT_NAMES_FOR_MATERIALS
from materials.obj.constants import NAMES_OF_CLASS_MATERIALS
from materials.obj.constants import INDEXES_OF_CLASS_MATERIALS
from materials.obj.constants import NAMES_OF_HEAT_TREATMENT
from materials.obj.constants import INDEXES_OF_HEAT_TREATMENT
from materials.obj.constants import NAMES_OF_WORKPIECE
from materials.obj.constants import INDEXES_OF_WORKPIECE
# Методы пакета
from materials.find import by_class
from materials.find import by_index
from materials.find import characteristics
from materials.find import chem_struct
from materials.find import hardness
from materials.find import tensile_strength
# Классы пакета
from materials.obj.material import Material


if __name__ == "__main__":
    material = Material()
    print(material)


    