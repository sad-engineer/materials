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
from materials.obj.containers import MaterialContainer
Material = MaterialContainer().material
WorkpieceMaterial = MaterialContainer().workpiece_material
MaterialCreator = MaterialContainer().material_creator
WorkpieceMaterialCreator = MaterialContainer().workpiece_material_creator
MaterialLister = MaterialContainer().material_lister
WorkpieceMaterialLister = MaterialContainer().workpiece_material_lister


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
    "MaterialContainer",
    "Material",
    "WorkpieceMaterial",
    "MaterialCreator",
    "WorkpieceMaterialCreator",
    "MaterialLister",
    "WorkpieceMaterialLister",
    ]
