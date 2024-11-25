import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm


if __name__ == "__main__":
    # Читаем ссылки из файла
    # Загрузка таблицы из файла
    input_filename = 'materials_part_temp.xlsx'
    df = pd.read_excel(input_filename)

    # Удаление повторяющихся строк по значению в первом столбце
    df_unique = df.drop_duplicates(subset=df.columns[0])

    # Сохранение результата в новый файл
    output_filename = 'materials_part_unique.xlsx'
    df_unique.to_excel(output_filename, index=False)

    print(f"Файл с уникальными значениями сохранен как '{output_filename}'")
