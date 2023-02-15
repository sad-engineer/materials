#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Константы пакета
from materials.obj.constants import DEFAULT_NAMES_FOR_MATERIALS
from materials.obj.constants import DEFAULT_SETTINGS_FOR_WORKPIECE_MATERIAL
from materials.obj.constants import DEFAULT_BRAND
from materials.obj.constants import DEFAULT_NAMES_FOR_MATERIALS
from materials.obj.constants import CLASSES_MATERIALS
from materials.obj.constants import HEAT_TREATMENT
from materials.obj.constants import WORKPIECE
from materials.obj.constants import DECODING
# Классы пакета
from materials.obj.containers import Container
Material = Container().material
WorkpieceMaterial = Container().workpiece_material
MaterialCreator = Container().material_creator
WorkpieceMaterialCreator = Container().workpiece_material_creator
MaterialLister = Container().material_lister
WorkpieceMaterialLister = Container().workpiece_material_lister
