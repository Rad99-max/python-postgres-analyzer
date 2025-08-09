# Пример запуска из терминала:
# python actor_analyzer.py --limit 10 --output top_films_report.csv

import datetime  # <-- НАША "ГРЯЗНАЯ" СТРОКА
import math  # <-- НАША "ГРЯЗНАЯ" СТРОКА
import argparse
import csv
from database import execute_query

# -------------------------------------------
# БЛОК 1: ФУНКЦИЯ ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ
# -------------------------------------------
def display_results(actors, limit):
    if not actors:
        print("Нет данных для отображения.")
        return
    print(f"\n--- Топ-{limit} самых популярных актеров ---")
    print('-' * 60)
    print(f"| {'Имя':<17} | {'Фамилия':<19} |"
          f"{'Кол-во фильмов':>15} |")
    print('-' * 60)
    for first_name, last_name, count_films in actors:
        print(f"| {first_name:<17} | {last_name:<19} |"
              f"{count_films:>15} |")
    print('-' * 60)
# -------------------------------------------
# БЛОК 2: ФУНКЦИЯ ДЛЯ СОХРАНЕНИЯ В CSV-файл
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
# БЛОК 3: ГЛАВНАЯ ФУНКЦИЯ, УПРАВЛЯЮЩАЯ ЛОГИКОЙ СКРИПТА
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
            help="По умолчанию Топ-10 актеров"
    )
    parser.add_argument(
            '--output',
            default="top_actors.csv",
            help="Имя файла для сохранения CSV-отчета."
    )
    args = parser.parse_args()

# --- Формируем запрос и вызываем универсальную функцию ---
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
# Вызываем нашу новую функцию, передавая ей запрос и параметры
    film_data = execute_query(sql_query, (args.limit,))
    if film_data:
        display_results(film_data, args.limit)
        save_report_to_csv(film_data, args.output)
    else:
        print("Не удалось получить данные. Программа завершена.")

if __name__ == "__main__":
    main()