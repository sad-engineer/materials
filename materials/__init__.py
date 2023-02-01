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
from materials.obj.constants import DECODING
# Методы пакета
from materials.find import by_class
from materials.find import by_index
from materials.find import characteristics
from materials.find import chem_struct
from materials.find import hardness
from materials.find import tensile_strength
# Классы пакета
from materials.obj.material import Material
from materials.obj.material import MaterialData
from materials.obj.workpiece_material import WorkpieceMaterial
# from materials.obj.notifier import Notifier
# from materials.obj.file_printer import FilePrinter
# from materials.obj.logger import Logger


if __name__ == "__main__":
    from logger import Logger
    from logger import StandardResultTerminalPrinter, StandardObjectTerminalPrinter
    from logger import StandardResultFilePrinter, StandardObjectFilePrinter

    logger = Logger()
    file_printer = StandardResultTerminalPrinter
    # file_printer = StandardObjectTerminalPrinter
    # file_printer = StandardResultFilePrinter
    # file_printer = StandardObjectFilePrinter
    file_printer.DECODING = DECODING

    material = WorkpieceMaterial()
    print(material)
    logger.log(material, notifier=file_printer, message='### Параметры материала ###')
