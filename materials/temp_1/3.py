from sqlalchemy.orm import Session
from materials.database import SessionLocal
from materials.models import ChemicalComposition, Standard


def update_chemical_composition_with_standard_ids():
    db: Session = SessionLocal()
    try:
        # Получаем все записи из таблицы ChemicalComposition
        compositions = db.query(ChemicalComposition).all()

        for composition in compositions:
            # Найти соответствующий стандарт для материала
            standard = db.query(Standard).filter(Standard.material_name == composition.material.brand).first()

            if standard:
                # Обновить standard_id в записи ChemicalComposition
                composition.standard_id = standard.id
                print(f"Обновлен material_id: {composition.material_id} с standard_id: {standard.id}")

        # Применить изменения к базе данных
        db.commit()
        print("Все записи успешно обновлены.")

    except Exception as e:
        db.rollback()
        print(f"Ошибка при обновлении записей: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    update_chemical_composition_with_standard_ids()
