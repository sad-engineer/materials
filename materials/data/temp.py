from sqlalchemy.orm import Session
import pandas as pd
from materials.models import Material, Hardness, ChemicalComposition, TechnologicalProperties, MechanicalProperties, \
    CharacteristicsOfMaterial
from materials.data.crud import create_material, create_hardness, create_chemical_composition, \
    create_technological_properties, create_mechanical_properties, create_characteristics
from materials.database import SessionLocal  # Импорт SessionLocal для создания сессии
from materials.database import engine
from materials.models import Base


# Функции для загрузки данных из CSV
def load_materials_from_csv(file_path: str, db: Session):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        existing_material = db.query(Material).filter(Material.brand == row['brand']).first()
        if existing_material:
            print(f"Материал с брендом '{row['brand']}' уже существует, пропускаем.")
            continue
        material = Material(
            brand=row['brand'],
            class_of_material=row['class_of_material'],
            index_of_material_class=row['index_of_material_class'],
            subclass_of_material=row.get('subclass_of_material')
        )
        create_material(db, material)


def load_hardness_from_csv(file_path: str, db: Session):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        # Получаем material_id по brand
        material = db.query(Material).filter(Material.brand == row['brand']).first()
        if not material:
            print(f"Материал с брендом '{row['brand']}' не найден, пропускаем.")
            continue

        hardness = Hardness(
            material_id=material.id,  # Используем полученный material_id
            hardness_value=row['hardness']
        )
        create_hardness(db, hardness)


def load_chemical_composition_from_csv(file_path: str, db: Session):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        if 'brand' not in row or pd.isna(row['brand']):
            print("Отсутствует brand в строке, пропускаем.")
            continue
        # Получаем material_id по brand
        material = db.query(Material).filter(Material.brand == row['brand']).first()
        if not material:
            print(f"Материал с брендом '{row['brand']}' не найден, пропускаем.")
            continue

        composition = ChemicalComposition(
            material_id=material.id,
            Ag=row['Ag'],
            Al=row['Al'],
            Al_and_Mg=row['AlandMg'],
            Arsenicum=row['Arsenicum'],
            B=row['B'],
            Ba=row['Ba'],
            Be=row['Be'],
            Bi=row['Bi'],
            C=row['C'],
            Ca=row['Ca'],
            Cd=row['Cd'],
            Ce=row['Ce'],
            Co=row['Co'],
            Cr=row['Cr'],
            Cu=row['Cu'],
            Cu_and_Ag=row['CuandAg'],
            Cu_and_P=row['CuandP'],
            F=row['F'],
            Fe=row['Fe'],
            Ga=row['Ga'],
            Hf=row['Hf'],
            La=row['La'],
            Li=row['Li'],
            Mg=row['Mg'],
            Mn=row['Mn'],
            Mo=row['Mo'],
            N=row['N'],
            Na=row['Na'],
            Nb=row['Nb'],
            Ni=row['Ni'],
            Ni_and_Co=row['NiandCo'],
            O=row['O'],
            Other=row['Other'],
            P=row['P'],
            Pb=row['Pb'],
            S=row['S'],
            Sb=row['Sb'],
            Sc=row['Sc'],
            Se=row['Se'],
            Si=row['Si'],
            Sn=row['Sn'],
            Sr=row['Sr'],
            Ta=row['Ta'],
            Te=row['Te'],
            Ti=row['Ti'],
            V=row['V'],
            W=row['W'],
            Y=row['Y'],
            Zn=row['Zn'],
            Zr=row['Zr'],
            Impurities=row['Примесей'],
            Rare_Earth_elements=row['РЗМ'],
        )
        create_chemical_composition(db, composition)


def load_technological_properties_from_csv(file_path: str, db: Session):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        if 'brand' not in row or pd.isna(row['brand']):
            print("Отсутствует brand в строке, пропускаем.")
            continue
        # Получаем material_id по brand
        material = db.query(Material).filter(Material.brand == row['brand']).first()
        if not material:
            print(f"Материал с брендом '{row['brand']}' не найден, пропускаем.")
            continue

        properties = TechnologicalProperties(
            material_id=material.id,
            weldability=row['Свариваемость'],
            flock_sensitivity=row['Флокеночувствительность'],
            temper_brittleness=row['Склонность_к_отпускной_хрупкости']
        )
        create_technological_properties(db, properties)


def load_mechanical_properties_from_csv(file_path: str, db: Session):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        if 'brand' not in row or pd.isna(row['brand']):
            print("Отсутствует brand в строке, пропускаем.")
            continue
        # Получаем material_id по brand
        material = db.query(Material).filter(Material.brand == row['brand']).first()
        if not material:
            print(f"Материал с брендом '{row['brand']}' не найден, пропускаем.")
            continue

        properties = MechanicalProperties(
            material_id=material.id,
            tensile_strength=row['tensile_strength'],
            yield_strength=row['yield_strength'],
            elongation_at_break=row['elongation_at_break'],
            relative_narrowing=row['relative_narrowing'],
            impact_strength=row['impact_strength']
        )
        create_mechanical_properties(db, properties)


def load_characteristics_from_csv(file_path: str, db: Session):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        return
    for _, row in df.iterrows():
        if 'brand' not in row or pd.isna(row['brand']):
            print("Отсутствует brand в строке, пропускаем.")
            continue
        # Получаем material_id по brand
        material = db.query(Material).filter(Material.brand == row['brand']).first()
        if not material:
            print(f"Материал с брендом '{row['brand']}' не найден, пропускаем.")
            continue
        characteristics = CharacteristicsOfMaterial(
            material_id=material.id,
            classification=row.get('Классификация'),
            application=row.get('Применение'),
            foreign_analogs=row.get('Зарубежные_аналоги'),
            additional_info=row.get('Дополнение'),
            replacement=row.get('Заменитель')
        )
        create_characteristics(db, characteristics)


# Пример вызова функций загрузки данных из CSV
def load_all_data():
    # # Создание всех таблиц, если они еще не существуют
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # load_materials_from_csv('C:\\Users\\Korenyk.A\\Documents\\Projects\\materials\\materials\\data\\materials.csv', db)
        # load_hardness_from_csv('C:\\Users\\Korenyk.A\\Documents\\Projects\\materials\\materials\\data\\hardness.csv', db)
        load_chemical_composition_from_csv(
            'C:\\Users\\Korenyk.A\\Documents\\Projects\\materials\\materials\\data\\chemical_composition.csv', db)
        # load_technological_properties_from_csv('C:\\Users\\Korenyk.A\\Documents\\Projects\\materials\\materials\\data\\technological_properties.csv', db)
        # load_mechanical_properties_from_csv('C:\\Users\\Korenyk.A\\Documents\\Projects\\materials\\materials\\data\\mechanical_properties.csv', db)
        # load_characteristics_from_csv('C:\\Users\\Korenyk.A\\Documents\\Projects\\materials\\materials\\data\\characteristics_of_material.csv', db)
        print("Данные успешно загружены в базу данных.")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
    finally:
        db.close()


# Функция для удаления записей с пропущенными данными во всех полях, кроме id, material_id, brand
def delete_empty_rows(db: Session):
    # Удаление пустых строк из таблицы Hardness
    db.query(Hardness).filter(
        Hardness.hardness_value == None
    ).delete(synchronize_session=False)
    #
    # # Удаление пустых строк из таблицы ChemicalComposition
    # db.query(ChemicalComposition).filter(
    #     ChemicalComposition.Ag == None,
    #     ChemicalComposition.Al == None,
    #     ChemicalComposition.Al_and_Mg == None,
    #     ChemicalComposition.Arsenicum == None,
    #     ChemicalComposition.B == None,
    #     ChemicalComposition.Ba == None,
    #     ChemicalComposition.Be == None,
    #     ChemicalComposition.Bi == None,
    #     ChemicalComposition.C == None,
    #     ChemicalComposition.Ca == None,
    #     ChemicalComposition.Cd == None,
    #     ChemicalComposition.Ce == None,
    #     ChemicalComposition.Co == None,
    #     ChemicalComposition.Cr == None,
    #     ChemicalComposition.Cu == None,
    #     ChemicalComposition.Cu_and_Ag == None,
    #     ChemicalComposition.Cu_and_P == None,
    #     ChemicalComposition.F == None,
    #     ChemicalComposition.Fe == None,
    #     ChemicalComposition.Ga == None,
    #     ChemicalComposition.Hf == None,
    #     ChemicalComposition.La == None,
    #     ChemicalComposition.Li == None,
    #     ChemicalComposition.Mg == None,
    #     ChemicalComposition.Mn == None,
    #     ChemicalComposition.Mo == None,
    #     ChemicalComposition.N == None,
    #     ChemicalComposition.Na == None,
    #     ChemicalComposition.Nb == None,
    #     ChemicalComposition.Ni == None,
    #     ChemicalComposition.Ni_and_Co == None,
    #     ChemicalComposition.O == None,
    #     ChemicalComposition.Other == None,
    #     ChemicalComposition.P == None,
    #     ChemicalComposition.Pb == None,
    #     ChemicalComposition.S == None,
    #     ChemicalComposition.Sb == None,
    #     ChemicalComposition.Sc == None,
    #     ChemicalComposition.Se == None,
    #     ChemicalComposition.Si == None,
    #     ChemicalComposition.Sn == None,
    #     ChemicalComposition.Sr == None,
    #     ChemicalComposition.Ta == None,
    #     ChemicalComposition.Te == None,
    #     ChemicalComposition.Ti == None,
    #     ChemicalComposition.V == None,
    #     ChemicalComposition.W == None,
    #     ChemicalComposition.Y == None,
    #     ChemicalComposition.Zn == None,
    #     ChemicalComposition.Zr == None,
    #     ChemicalComposition.Impurities == None,
    #     ChemicalComposition.Rare_Earth_elements == None,
    # ).delete(synchronize_session=False)
    #
    # # Удаление пустых строк из таблицы TechnologicalProperties
    # db.query(TechnologicalProperties).filter(
    #     TechnologicalProperties.weldability == None,
    #     TechnologicalProperties.flock_sensitivity == None,
    #     TechnologicalProperties.temper_brittleness == None
    # ).delete(synchronize_session=False)
    #
    # # Удаление пустых строк из таблицы MechanicalProperties
    # db.query(MechanicalProperties).filter(
    #     MechanicalProperties.tensile_strength == None,
    #     MechanicalProperties.yield_strength == None,
    #     MechanicalProperties.elongation_at_break == None,
    #     MechanicalProperties.relative_narrowing == None,
    #     MechanicalProperties.impact_strength == None
    # ).delete(synchronize_session=False)
    #
    # # Удаление пустых строк из таблицы CharacteristicsOfMaterial
    # db.query(CharacteristicsOfMaterial).filter(
    #     CharacteristicsOfMaterial.classification == None,
    #     CharacteristicsOfMaterial.application == None,
    #     CharacteristicsOfMaterial.foreign_analogs == None,
    #     CharacteristicsOfMaterial.additional_info == None,
    #     CharacteristicsOfMaterial.replacement == None
    # ).delete(synchronize_session=False)

    db.commit()


# Пример вызова функции для удаления пустых строк
def clean_data():
    db = SessionLocal()
    try:
        delete_empty_rows(db)
        print("Пустые строки успешно удалены.")
    except Exception as e:
        print(f"Ошибка при удалении пустых строк: {e}")
    finally:
        db.close()


clean_data()
