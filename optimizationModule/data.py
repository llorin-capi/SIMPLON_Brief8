import pandas as pd
import requests
import re  # Для использования регулярных выражений

# API key, contract and base URL
key = "e1d3b29a83a779db2a3c2d64d1d5a255c7560a27"
contrat = "nancy"
api_base_url = "https://api.jcdecaux.com/vls/v3/"

# Функция для очистки названия (удаление цифр, дефисов, пробелов, "CB" и лишних символов)
def clean_name(name):
    # Удаление "CB", цифр, дефисов и лишних пробелов
    cleaned_name = re.sub(r'\bCB\b|[\d-]', '', name)  # Удаляем "CB", цифры и дефисы
    cleaned_name = re.sub(r'[\(\)\[\]\{\}]', '', cleaned_name)  # Удаляем круглые и квадратные скобки
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()  # Убираем лишние пробелы
    return cleaned_name

# Функция для очистки данных
def nettoyer_donnees(stations):
    cleaned_stations = []
    for station in stations:
        # Проверка на наличие всех ключевых данных
        if (station["Address"] and station["Latitude"] and station["Longitude"] and
            station["Station"] and station["Station_ID"] is not None and
            station["CurNumberOfBikes"] is not None and station["MaxNumberOfBikes"] is not None):
            
            # Проверка на корректность данных (например, latitude и longitude должны быть числами)
            try:
                station["Latitude"] = float(station["Latitude"])
                station["Longitude"] = float(station["Longitude"])
                station["CurNumberOfBikes"] = int(station["CurNumberOfBikes"])
                station["MaxNumberOfBikes"] = int(station["MaxNumberOfBikes"])

                # Очистка названия станции и адреса
                station["Station"] = clean_name(station["Station"])
                station["Address"] = clean_name(station["Address"])

                cleaned_stations.append(station)  # Добавляем станцию, если все ок
            except ValueError:
                # Если данные не приводятся к нужным типам, станция игнорируется
                print(f"Ошибка преобразования данных для станции {station['Station']}")
    return cleaned_stations

# Основная функция для получения данных и их очистки
def recup_stations():
    url = f"{api_base_url}stations?contract={contrat}&apiKey={key}"
    response = requests.get(url)

    # Обеспечить правильную кодировку
    response.encoding = response.apparent_encoding

    if response.status_code == 200:
        stations = []
        for stat_station in response.json():
            # Создаем структуру согласно формату CSV файла
            station = {
                "Address": stat_station['name'],  # Предполагаем, что 'name' это адрес
                "Latitude": stat_station['position']['latitude'],
                "Longitude": stat_station['position']['longitude'],
                "Station": stat_station['name'],  # Имя станции
                "CB": None,  # Место для данных по CB (может быть, стоит собрать дополнительные данные позже)
                "Station_ID": stat_station['number'],  # Номер станции как ID
                "CurNumberOfBikes": stat_station['mainStands']['availabilities']['bikes'],
                "MaxNumberOfBikes": stat_station['mainStands']['capacity']
            }
            stations.append(station)

        # Чистим данные перед созданием DataFrame
        stations_cleaned = nettoyer_donnees(stations)

        # Создаем DataFrame
        df_stations = pd.DataFrame(stations_cleaned, columns=[
            "Address", "Latitude", "Longitude", "Station", "CB", 
            "Station_ID", "CurNumberOfBikes", "MaxNumberOfBikes"
        ])
        
        # Сохраняем DataFrame в CSV файл
        df_stations.to_csv('./data/data_statique_clean01.csv', index=False)
        print("Данные успешно сохранены в './data/data_statique_clean01.csv'.")

        return df_stations
    else:
        print("Ошибка:", response.status_code)
        return None

# Пример использования функции
df_stations = recup_stations()

# Вывод первых строк для проверки
if df_stations is not None:
    print(df_stations.head())
