import pandas as pd
from sqlalchemy.orm import Session
from materials.database import SessionLocal, engine
from materials.models import Standard


def load_standards_from_csv(csv_file_path: str):
    # Чтение CSV файла с помощью pandas
    df = pd.read_excel(csv_file_path)

    # Ожидается, что CSV содержит столбцы 'Название материала' и 'Стандарт'
    if 'Название материала' not in df.columns or 'Стандарт' not in df.columns:
        raise ValueError("CSV файл должен содержать столбцы 'Название материала' и 'Стандарт'.")

    # Создание сессии для работы с базой данных
    db: Session = SessionLocal()
    try:
        # Добавление данных в таблицу 'Standards'
        for _, row in df.iterrows():
            new_standard = Standard(
                material_name=row['Название материала'],
                standard=row['Стандарт']
            )
            db.add(new_standard)

        # Коммит транзакции
        db.commit()
        print("Данные успешно добавлены в таблицу 'Стандарты'.")

    except Exception as e:
        db.rollback()
        print(f"Ошибка при добавлении данных: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    # Замените путь к CSV на ваш путь
    csv_file_path = "materials_part_unique1.xlsx"
    load_standards_from_csv(csv_file_path)

