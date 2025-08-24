# Пример запуска из терминала:
# python rating_film_analyzer.py --limit 3 --output top_films_long_report.csv

import argparse
import csv
from database import execute_query

#-------------------------------------------
# БЛОК 1: ФУНКЦИЯ ДЛЯ ПОЛУЧЕНИЯ ДАННЫХ ИЗ БД
#-------------------------------------------
def get_top_rating_film_data(limit):

    # Формируем запрос и вызываем универсальную функцию
    sql_query = """
        with RankedFilms as (
            select
                title,
                rating,
                length,
                dense_rank() over (partition by rating order by length desc) as drnk
            from film
        )
        select
            title,
            rating,
            length
        from 
            RankedFilms
        where
            drnk <= %s
        order by
            case rating
                when 'G'        THEN 1
                WHEN 'PG'       THEN 2
                WHEN 'PG-13'    THEN 3
                WHEN 'R'        THEN 4
                WHEN 'NC-17'    THEN 5
                ELSE 6
            END,
            length desc -- Вторичная сортировка по длине для красоты вывода            
    """

    film_data = execute_query(sql_query,(limit,))
    return film_data

# -------------------------------------------
# БЛОК 2: ФУНКЦИЯ ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ
# -------------------------------------------
def display_results(films, limit):
    if not films:
        print("Нет данных для отображения.")
        return
    print(f"\n--- Топ-{limit} самых длинных фильмов по рейтингам ---")
    current_rating = None #

    for title, rating, length in films:
        if current_rating != rating:
            if current_rating is not None:
                print('-' * 55)
            current_rating = rating
            print(f"\nРейтинг: {current_rating}")
            print('-' * 55)
            print(f"| {'Название фильма':<35} | "
                  f"{'Длительность':>13} |")
            print('-' * 55)

        print(f"| {title:<35} | {length:>9} мин |")

    if films:
        print('-' * 55)

# -------------------------------------------
# БЛОК 3: ФУНКЦИЯ ДЛЯ СОХРАНЕНИЯ В CSV-файл
# -------------------------------------------
def save_report_to_csv(data, filename):
    if not data:
        print("Нет данных для сохранения в файл.")
        return
    header = ['Название фильма', 'Рейтинг', 'Длительность (мин)']
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
            description="Создает отчет по самым длинным "
                        "фильмам для каждого рейтинга."
    )
    parser.add_argument(
            '--limit',
            type=int,
            required=True,
            help="Обязательный параметр. Ранг, до которого "
                 "включать фильмы в отчет (например, 3 для Топ-3)."
    )
    parser.add_argument(
            '--output',
            default="top_films_long_rating.csv",
            help="Имя файла для сохранения CSV-отчета."
    )
    args = parser.parse_args()

    film_data = get_top_rating_film_data(args.limit)
    if film_data:
        display_results(film_data, args.limit)
        save_report_to_csv(film_data, args.output)
    else:
        print("Не удалось получить данные. Программа завершена.")

if __name__ == "__main__":
    main()