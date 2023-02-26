#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from dependency_injector import containers, providers
from service import Requester as RequesterContainer

from materials.obj.finders import Finder
from materials.obj.handlers import ChemicalCompositionHandler, HardnessHandler, TensileStrengthHandler
from materials.obj.creators import MaterialCreator, WorkpieceMaterialCreator
from materials.obj.entities import Material, WorkpieceMaterial
from materials.obj.listers import Lister
from materials.obj.constants import DEFAULT_SETTINGS
DB_PATH = DEFAULT_SETTINGS['path']
DB_type = DEFAULT_SETTINGS['db_type']


@containers.copy(RequesterContainer)
class CharacteristicsOfMaterial(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict',
         'tablename': "characteristics_of_material"}
    )
    RequesterContainer.config.from_dict(default_settings())

    find = providers.Factory(
        Finder,
        RequesterContainer.requester,
    )


@containers.copy(RequesterContainer)
class ChemicalComposition(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict',
         'tablename': "chemical_composition"}
    )
    RequesterContainer.config.from_dict(default_settings())

    finder = providers.Factory(
        Finder,
        RequesterContainer.requester,
    )

    handler = providers.Factory(
        ChemicalCompositionHandler,
        finder,
    )


@containers.copy(RequesterContainer)
class Hardness(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict',
         'tablename': "hardness"}
    )
    RequesterContainer.config.from_dict(default_settings())

    finder = providers.Factory(
        Finder,
        RequesterContainer.requester,
    )

    handler = providers.Factory(
        HardnessHandler,
        finder,
    )


@containers.copy(RequesterContainer)
class Materials(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict',
         'tablename': "materials"}
    )
    RequesterContainer.config.from_dict(default_settings())

    find = providers.Factory(
        Finder,
        RequesterContainer.requester,
    )


@containers.copy(RequesterContainer)
class MechanicalProperties(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict',
         'tablename': "mechanical_properties"}
    )
    RequesterContainer.config.from_dict(default_settings())

    finder = providers.Factory(
        Finder,
        RequesterContainer.requester,
    )

    tensile_strength_handler = providers.Factory(
        TensileStrengthHandler,
        finder,
    )


@containers.copy(RequesterContainer)
class TechnologicalProperties(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict',
         'tablename': "technological_properties"}
    )
    RequesterContainer.config.from_dict(default_settings())

    find = providers.Factory(
        Finder,
        RequesterContainer.requester,
    )


class Container(containers.DeclarativeContainer):
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

    container_for_characteristics = providers.Container(
        CharacteristicsOfMaterial,
        config=config.for_characteristics,
    )

    container_for_chemical_composition = providers.Container(
        ChemicalComposition,
        config=config.for_chemical_composition,
    )

    container_for_hardness = providers.Container(
        Hardness,
        config=config.for_hardness,
    )

    container_for_materials = providers.Container(
        Materials,
        config=config.for_materials,
    )

    container_for_mechanical_properties = providers.Container(
        MechanicalProperties,
        config=config.for_mechanical_properties,
    )

    container_for_technological_properties = providers.Container(
        TechnologicalProperties,
        config=config.for_technological_properties,
    )

    material_creator = providers.Factory(
        MaterialCreator,
        chemical_composition_handler=container_for_chemical_composition.handler,
        hardness_handler=container_for_hardness.handler,
        materials_finder=container_for_materials.find,
        tensile_strength_handler=container_for_mechanical_properties.tensile_strength_handler,
    )

    workpiece_material_creator = providers.Factory(
        WorkpieceMaterialCreator,
        chemical_composition_handler=container_for_chemical_composition.handler,
        hardness_handler=container_for_hardness.handler,
        materials_finder=container_for_materials.find,
        tensile_strength_handler=container_for_mechanical_properties.tensile_strength_handler,
    )

    material_lister = providers.Factory(
        Lister,
        material_creator.provider
    )

    workpiece_material_lister = providers.Factory(
        Lister,
        workpiece_material_creator.provider
    )

    material = providers.Factory(
        Material
    )

    workpiece_material = providers.Factory(
        WorkpieceMaterial
    )


