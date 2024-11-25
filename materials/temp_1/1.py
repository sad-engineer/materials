import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm


def parse_material_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'  # Установка правильной кодировки

        if response.status_code != 200:
            print(f'Error fetching the URL: {response.status_code}')
            return None, None, None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Получаем название марки материала
        material_name_tag = soup.find('b', string=re.compile(r'Марка :'))
        material_name = material_name_tag.find_parent('td').find_next(
            'td').text.strip() if material_name_tag else 'Not found'

        # Обработка случаев, когда указано другое обозначение в скобках
        material_name = re.sub(r'\s*\(\s*другое обозначение\s*(.*?)\s*\)', r',\1', material_name).replace('  ',
                                                                                                          ' ').strip()
        material_name = re.sub(r'\s*,\s*', ', ', material_name)

        # Ищем блок с заменителями
        substitutes_tag = soup.find('b', string=re.compile(r'Заменитель:'))
        substitutes = substitutes_tag.find_parent('td').find_next('td').text.strip() if substitutes_tag else 'Not found'

        # Ищем строку с ГОСТ и годом
        gost_tag = soup.find('a', href=re.compile(r'gost_start\.php\?gost_number=\d+'))
        if gost_tag:
            gost_number = gost_tag.text.strip()
            next_text = gost_tag.find_next_sibling(string=True).strip() if gost_tag.find_next_sibling(
                string=True) else ''
            gost = f'{gost_number} {next_text}'.strip()
            gost = re.sub(r'\s+', ' ', gost)  # Удаляем лишние пробелы
        else:
            gost = 'Not found'

        return material_name, substitutes, gost

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None, None, None


def create_material_table(material_name, substitutes, gost):
    if material_name and gost:
        materials = [material_name]
        if substitutes != 'Not found':
            materials += [s.strip() for s in substitutes.split(',')]
        gosts = [gost] * len(materials)
        df = pd.DataFrame({'Название материала': materials, 'ГОСТ': gosts})
        return df
    else:
        return None


def extract_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'  # Установка правильной кодировки

        if response.status_code != 200:
            print(f'Ошибка при запросе URL: {response.status_code}')
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = requests.compat.urljoin(url, href)
            links.append(full_url)

        return links

    except requests.exceptions.RequestException as e:
        print(f'Произошла ошибка: {e}')
        return []


def filter_links(links):
    filtered_links = [link for link in links if "name_id" in link]
    return filtered_links


def collect_unique_links(url):
    all_links = []
    links = extract_links(url)
    for link in links:
        all_links.append(link)
    unique_links = set(all_links)
    return unique_links

def save_links_to_txt(links, filename):
    with open(filename, 'w') as file:
        for link in links:
            file.write(f"{link}\n")

def read_links_from_txt(filename):
    try:
        with open(filename, 'r') as file:
            links = [line.strip() for line in file]
        return links
    except FileNotFoundError:
        print(f'File {filename} not found.')
        return []


if __name__ == "__main__":
    # Читаем ссылки из файла
    filtered_links = filter_links(read_links_from_txt('filtered_links.txt'))

    # Проходим по всем ссылкам и создаем общую таблицу с сохранением каждые 50 ссылок
    combined_df = pd.DataFrame()
    counter = 0
    for link in tqdm(filtered_links, desc="Processing links", unit="link"):
        material_name, substitutes, gost = parse_material_data(link)
        df = create_material_table(material_name, substitutes, gost)
        if df is not None:
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        counter += 1
        if counter % 50 == 0:
            combined_df.to_excel(f'combined_materials_part_{counter // 50}.xlsx', index=False)
            print(f"Saved combined data up to link {counter} in 'combined_materials_part_{counter // 50}.xlsx'")

    # Сохраняем оставшиеся данные в файл Excel
    if not combined_df.empty:
        combined_df.to_excel('combined_materials_final.xlsx', index=False)
        print("Combined data saved to 'combined_materials_final.xlsx'")
    else:
        print("No data available")

# 4288, 3065, 3064