#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
from dependency_injector import containers, providers
from service import Requester as RequesterContainer

from materials.obj.finders import Finder
from materials.obj.handlers import ChemicalCompositionHandler, HardnessHandler, TensileStrengthHandler
from materials.obj.creators import MaterialCreator, WorkpieceMaterialCreator
from materials.obj.constants import DEFAULT_SETTINGS
DB_PATH = DEFAULT_SETTINGS['path']
DB_type = DEFAULT_SETTINGS['db_type']


@containers.copy(RequesterContainer)
class CharacteristicsOfMaterial(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'}
    )
    RequesterContainer.config.from_dict(default_settings())

    requester_chars = providers.Factory(
        RequesterContainer.requester,
        tablename="characteristics_of_material",
        )

    find = providers.Factory(
        Finder,
        requester_chars,
    )


@containers.copy(RequesterContainer)
class ChemicalComposition(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'}
    )
    RequesterContainer.config.from_dict(default_settings())

    requester = providers.Factory(
        RequesterContainer.requester,
        tablename="chemical_composition",
    )

    finder = providers.Factory(
        Finder,
        requester,
    )

    handler = providers.Factory(
        ChemicalCompositionHandler,
        finder,
    )


@containers.copy(RequesterContainer)
class Hardness(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'}
    )
    RequesterContainer.config.from_dict(default_settings())

    requester_hardness = providers.Singleton(
        RequesterContainer.requester,
        tablename="hardness",
    )

    finder = providers.Factory(
        Finder,
        requester_hardness,
    )

    handler = providers.Factory(
        HardnessHandler,
        finder,
    )



@containers.copy(RequesterContainer)
class Materials(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'}
    )
    RequesterContainer.config.from_dict(default_settings())

    requester_mats = providers.Singleton(
        RequesterContainer.requester,
        tablename="materials",
    )

    find = providers.Factory(
        Finder,
        requester_mats,
    )


@containers.copy(RequesterContainer)
class MechanicalProperties(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'}
    )
    RequesterContainer.config.from_dict(default_settings())

    requester_mech_props = providers.Singleton(
        RequesterContainer.requester,
        tablename="mechanical_properties",
    )

    finder = providers.Factory(
        Finder,
        requester_mech_props,
    )

    tensile_strength_handler = providers.Factory(
        TensileStrengthHandler,
        finder,
    )


@containers.copy(RequesterContainer)
class TechnologicalProperties(RequesterContainer):
    default_settings = providers.Object(
        {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'}
    )
    RequesterContainer.config.from_dict(default_settings())

    requester_tech_props = providers.Singleton(
        RequesterContainer.requester,
        tablename="technological_properties",
    )

    find = providers.Factory(
        Finder,
        requester_tech_props,
    )


class CreatorsContainer(containers.DeclarativeContainer):
    default_settings = providers.Object({
        'for_characteristics': {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'},
        'for_chemical_composition': {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'},
        'for_hardness': {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'},
        'for_materials': {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'},
        'for_mechanical_properties': {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'},
        'for_technological_properties': {'path': DB_PATH, 'requester_type': DB_type, 'reader_type': 'dict'},
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
