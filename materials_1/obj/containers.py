#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from dependency_injector import containers, providers
from service_for_my_projects import Requester as RequesterContainer

from materials.obj.finders import MaterialCharacteristicsFinder, MaterialChemicalCompositionFinder,\
    MaterialHardnessFinder, MaterialsFinder, MaterialMechanicalPropertiesFinder, \
    MaterialTechnologicalPropertiesFinder
from materials.obj.handlers import MaterialChemicalCompositionHandler, MaterialHardnessHandler, \
    MaterialTensileStrengthHandler
from materials.obj.creators import MaterialCreator, WorkpieceMaterialCreator
from materials.obj.entities import Material, WorkpieceMaterial
from materials.obj.listers import MaterialLister
from materials.obj.constants import DEFAULT_SETTINGS
DB_PATH = DEFAULT_SETTINGS['path']
DB_type = DEFAULT_SETTINGS['db_type']


class MaterialContainer(containers.DeclarativeContainer):
    default_settings = providers.Object({
        'for_characteristics':
            {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict',
             'tablename': "characteristics_of_material"},
        'for_chemical_composition':
            {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict', 'tablename': "chemical_composition"},
        'for_hardness':
            {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict', 'tablename': "hardness"},
        'for_materials':
            {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict', 'tablename': "materials"},
        'for_mechanical_properties':
            {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict', 'tablename': "mechanical_properties"},
        'for_technological_properties':
            {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict',
             'tablename': "technological_properties"},
    })
    config = providers.Configuration()
    config.from_dict(default_settings())

    # =================================================================================================================
    characteristics_container = providers.Container(
        RequesterContainer,
        config=config.for_characteristics,
    )

    characteristics_finder = providers.Factory(
        MaterialCharacteristicsFinder,
        record_requester=characteristics_container.requester.provider,
    )

    # =================================================================================================================
    chemical_composition_container = providers.Container(
        RequesterContainer,
        config=config.for_chemical_composition,
    )

    chemical_composition_finder = providers.Factory(
        MaterialChemicalCompositionFinder,
        record_requester=chemical_composition_container.requester.provider,
    )

    chemical_composition_handler = providers.Factory(
        MaterialChemicalCompositionHandler,
        chemical_composition_finder=chemical_composition_finder.provider,
    )

    # =================================================================================================================
    hardness_container = providers.Container(
        RequesterContainer,
        config=config.for_hardness,
    )

    hardness_finder = providers.Factory(
        MaterialHardnessFinder,
        record_requester=hardness_container.requester.provider,
    )

    hardness_handler = providers.Factory(
        MaterialHardnessHandler,
        hardness_finder=hardness_finder.provider,
    )

    # =================================================================================================================
    materials_container = providers.Container(
        RequesterContainer,
        config=config.for_materials,
    )

    materials_finder = providers.Factory(
        MaterialsFinder,
        record_requester=materials_container.requester.provider,
    )

    # =================================================================================================================
    mechanical_properties_container = providers.Container(
        RequesterContainer,
        config=config.for_mechanical_properties,
    )

    mechanical_properties_finder = providers.Factory(
        MaterialMechanicalPropertiesFinder,
        record_requester=mechanical_properties_container.requester.provider,
    )

    tensile_strength_handler = providers.Factory(
        MaterialTensileStrengthHandler,
        mechanical_properties_finder=mechanical_properties_finder.provider,
    )

    # =================================================================================================================
    technological_properties_container = providers.Container(
        RequesterContainer,
        config=config.for_technological_properties,
    )

    technological_properties_finder = providers.Factory(
        MaterialTechnologicalPropertiesFinder,
        record_requester=technological_properties_container.requester.provider,
    )

    # =================================================================================================================
    material_creator = providers.Factory(
        MaterialCreator,
        chemical_composition_handler=chemical_composition_handler.provider,
        hardness_handler=hardness_handler.provider,
        materials_finder=materials_finder.provider,
        tensile_strength_handler=tensile_strength_handler.provider,
    )

    workpiece_material_creator = providers.Factory(
        WorkpieceMaterialCreator,
        chemical_composition_handler=chemical_composition_handler.provider,
        hardness_handler=hardness_handler.provider,
        materials_finder=materials_finder.provider,
        tensile_strength_handler=tensile_strength_handler.provider,
    )

    material_lister = providers.Factory(
        MaterialLister,
        creator=material_creator.provider,
        materials_finder=materials_finder.provider
    )

    workpiece_material_lister = providers.Factory(
        MaterialLister,
        creator=workpiece_material_creator.provider,
        materials_finder=materials_finder.provider
    )

    material = providers.Factory(
        Material
    )

    workpiece_material = providers.Factory(
        WorkpieceMaterial
    )
