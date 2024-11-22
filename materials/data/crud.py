from sqlalchemy.orm import Session
from typing import Optional, List
from materials.models import Material, Hardness, ChemicalComposition, TechnologicalProperties, MechanicalProperties, \
    CharacteristicsOfMaterial


# CRUD для Material
def create_material(db: Session, material: Material) -> Material:
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


def get_material_by_id(db: Session, material_id: int) -> Optional[Material]:
    return db.query(Material).filter(Material.id == material_id).first()


def get_all_materials(db: Session) -> List[Material]:
    return db.query(Material).all()


def update_material(db: Session, material_id: int, updates: dict) -> Optional[Material]:
    material = db.query(Material).filter(Material.id == material_id).first()
    if material:
        for key, value in updates.items():
            setattr(material, key, value)
        db.commit()
        db.refresh(material)
    return material


def delete_material(db: Session, material_id: int) -> bool:
    material = db.query(Material).filter(Material.id == material_id).first()
    if material:
        db.delete(material)
        db.commit()
        return True
    return False


# CRUD для Hardness
def create_hardness(db: Session, hardness: Hardness) -> Hardness:
    db.add(hardness)
    db.commit()
    db.refresh(hardness)
    return hardness


def get_hardness_by_id(db: Session, hardness_id: int) -> Optional[Hardness]:
    return db.query(Hardness).filter(Hardness.id == hardness_id).first()


def update_hardness(db: Session, hardness_id: int, updates: dict) -> Optional[Hardness]:
    hardness = db.query(Hardness).filter(Hardness.id == hardness_id).first()
    if hardness:
        for key, value in updates.items():
            setattr(hardness, key, value)
        db.commit()
        db.refresh(hardness)
    return hardness


def delete_hardness(db: Session, hardness_id: int) -> bool:
    hardness = db.query(Hardness).filter(Hardness.id == hardness_id).first()
    if hardness:
        db.delete(hardness)
        db.commit()
        return True
    return False


# CRUD для ChemicalComposition
def create_chemical_composition(db: Session, composition: ChemicalComposition) -> ChemicalComposition:
    db.add(composition)
    db.commit()
    db.refresh(composition)
    return composition


def get_chemical_composition_by_id(db: Session, composition_id: int) -> Optional[ChemicalComposition]:
    return db.query(ChemicalComposition).filter(ChemicalComposition.id == composition_id).first()


def update_chemical_composition(db: Session, composition_id: int, updates: dict) -> Optional[ChemicalComposition]:
    composition = db.query(ChemicalComposition).filter(ChemicalComposition.id == composition_id).first()
    if composition:
        for key, value in updates.items():
            setattr(composition, key, value)
        db.commit()
        db.refresh(composition)
    return composition


def delete_chemical_composition(db: Session, composition_id: int) -> bool:
    composition = db.query(ChemicalComposition).filter(ChemicalComposition.id == composition_id).first()
    if composition:
        db.delete(composition)
        db.commit()
        return True
    return False


# CRUD для TechnologicalProperties
def create_technological_properties(db: Session, properties: TechnologicalProperties) -> TechnologicalProperties:
    db.add(properties)
    db.commit()
    db.refresh(properties)
    return properties


def get_technological_properties_by_id(db: Session, properties_id: int) -> Optional[TechnologicalProperties]:
    return db.query(TechnologicalProperties).filter(TechnologicalProperties.id == properties_id).first()


def update_technological_properties(db: Session, properties_id: int, updates: dict) -> Optional[
    TechnologicalProperties]:
    properties = db.query(TechnologicalProperties).filter(TechnologicalProperties.id == properties_id).first()
    if properties:
        for key, value in updates.items():
            setattr(properties, key, value)
        db.commit()
        db.refresh(properties)
    return properties


def delete_technological_properties(db: Session, properties_id: int) -> bool:
    properties = db.query(TechnologicalProperties).filter(TechnologicalProperties.id == properties_id).first()
    if properties:
        db.delete(properties)
        db.commit()
        return True
    return False


# CRUD для MechanicalProperties
def create_mechanical_properties(db: Session, properties: MechanicalProperties) -> MechanicalProperties:
    db.add(properties)
    db.commit()
    db.refresh(properties)
    return properties


def get_mechanical_properties_by_id(db: Session, properties_id: int) -> Optional[MechanicalProperties]:
    return db.query(MechanicalProperties).filter(MechanicalProperties.id == properties_id).first()


def update_mechanical_properties(db: Session, properties_id: int, updates: dict) -> Optional[MechanicalProperties]:
    properties = db.query(MechanicalProperties).filter(MechanicalProperties.id == properties_id).first()
    if properties:
        for key, value in updates.items():
            setattr(properties, key, value)
        db.commit()
        db.refresh(properties)
    return properties


def delete_mechanical_properties(db: Session, properties_id: int) -> bool:
    properties = db.query(MechanicalProperties).filter(MechanicalProperties.id == properties_id).first()
    if properties:
        db.delete(properties)
        db.commit()
        return True
    return False


# CRUD для CharacteristicsOfMaterial
def create_characteristics(db: Session, characteristics: CharacteristicsOfMaterial) -> CharacteristicsOfMaterial:
    db.add(characteristics)
    db.commit()
    db.refresh(characteristics)
    return characteristics


def get_characteristics_by_id(db: Session, characteristics_id: int) -> Optional[CharacteristicsOfMaterial]:
    return db.query(CharacteristicsOfMaterial).filter(CharacteristicsOfMaterial.id == characteristics_id).first()


def update_characteristics(db: Session, characteristics_id: int, updates: dict) -> Optional[CharacteristicsOfMaterial]:
    characteristics = db.query(CharacteristicsOfMaterial).filter(
        CharacteristicsOfMaterial.id == characteristics_id).first()
    if characteristics:
        for key, value in updates.items():
            setattr(characteristics, key, value)
        db.commit()
        db.refresh(characteristics)
    return characteristics


def delete_characteristics(db: Session, characteristics_id: int) -> bool:
    characteristics = db.query(CharacteristicsOfMaterial).filter(
        CharacteristicsOfMaterial.id == characteristics_id).first()
    if characteristics:
        db.delete(characteristics)
        db.commit()
        return True
    return False
