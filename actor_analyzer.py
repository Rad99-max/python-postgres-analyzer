# Пример запуска из терминала:
# python ваш_скрипт.py --limit 10 --output top_films_report.csv

import argparse
import psycopg2
from psycopg2 import OperationalError
import csv
import os
from dotenv import load_dotenv

load_dotenv() # Загружает переменные из файла .env
# -------------------------------------------
# БЛОК 1: ФУНКЦИЯ ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ
# -------------------------------------------
def get_data_from_db(limit):
    conn_params = {
        "host": os.getenv("DB_HOST"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": os.getenv("DB_PORT", "5432")
    }
    sql_query = """
        select 
    	    a.first_name,
	        a.last_name,
        	count(*)
        from 
        	actor a
        join 
	        film_actor using(actor_id)
        group by
	        a.actor_id
        order by
	        count(*) desc
        limit %s;
    """
    try:
        print("Подключаюсь к базе данных...")
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query, (limit,))
                results = cursor.fetchall()
                print("Данные успешно получены.")
        print("Соединение с PostgreSQL закрыто.")
        return results
    except OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")
        return None
# -------------------------------------------
# БЛОК 2: ФУНКЦИЯ ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ
# -------------------------------------------
def display_results(actors, limit):
    if not actors:
        print("Нет данных для отображения.")
        return
    print(f"\n--- Топ-{limit} самых популярных актеров ---")
    print('-' * 60)
    print(f"| {'Имя':<20} | {'Фамилия':<20} |"
          f"{'Количество фильмов':>10} |")
    print('-' * 60)
    for first_name, last_name, count_films in actors:
        print(f"| {first_name:<20} | {last_name:<20} |"
              f"{count_films:>10} |")
    print('-' * 60)
# -------------------------------------------
# БЛОК 3: ФУНКЦИЯ ДЛЯ СОХРАНЕНИЯ В CSV-файл
# -------------------------------------------
def save_report_to_csv(data, filename):
    if not data:
        print("Нет данных для сохранения в файл.")
        return
    header = ['Имя', 'Фамилия', 'Количество фильмов']
    print(f"\nСохраняю отчет в файл {filename}...")

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile) # Создаем спец. объект — "писатель"
            writer.writerow(header)
            writer.writerows(data)
        print(f"Отчет успешно сохранен в файл {filename}")

    except IOError as e:
        print(f"Ошибка при сохранении файла: {e}")

# -------------------------------------------
# БЛОК 4: ГЛАВНАЯ ФУНКЦИЯ, УПРАВЛЯЮЩАЯ ЛОГИКОЙ СКРИПТА
# -------------------------------------------
def main():
    parser = argparse.ArgumentParser(
            description="Создает отчет по самым "
                        "популярным актерам"
    )
    parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help=f"По умолчанию Топ-10 актеров"
    )
    parser.add_argument(
            '--output',
            default="top_actors.csv",
            help="Имя файла для сохранения CSV-отчета."
    )
    args = parser.parse_args()
    film_data = get_data_from_db(args.limit)
    if film_data:
        display_results(film_data, args.limit)
        save_report_to_csv(film_data, args.output)
    else:
        print("Не удалось получить данные. Программа завершена.")

if __name__ == "__main__":
    main()