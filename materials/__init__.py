#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Константы пакета
from .obj.constants import DEFAULT_NAMES_FOR_MATERIALS
from .obj.constants import DEFAULT_SETTINGS_FOR_WORKPIECE_MATERIAL
from .obj.constants import DEFAULT_BRAND
from .obj.constants import DEFAULT_NAMES_FOR_MATERIALS
from .obj.constants import CLASSES_MATERIALS
from .obj.constants import HEAT_TREATMENT
from .obj.constants import WORKPIECE
from .obj.constants import DECODING
# Классы пакета
from materials.obj.containers import Container
Material = Container().material
WorkpieceMaterial = Container().workpiece_material
MaterialCreator = Container().material_creator
WorkpieceMaterialCreator = Container().workpiece_material_creator
MaterialLister = Container().material_lister
WorkpieceMaterialLister = Container().workpiece_material_lister


__all__ = [
    # Константы пакета
    "DEFAULT_NAMES_FOR_MATERIALS",
    "DEFAULT_SETTINGS_FOR_WORKPIECE_MATERIAL",
    "DEFAULT_BRAND",
    "DEFAULT_NAMES_FOR_MATERIALS",
    "CLASSES_MATERIALS",
    "HEAT_TREATMENT",
    "WORKPIECE",
    "DECODING",
    # Классы пакета
    "Container",
    "Material",
    "WorkpieceMaterial",
    "MaterialCreator",
    "WorkpieceMaterialCreator",
    "MaterialLister",
    "WorkpieceMaterialLister",
    ]
