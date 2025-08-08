# Пример запуска из терминала:
"""python top_rented_film_analyzer.py --limit 7
--output top_rented_films.csv"""

import argparse
import csv
from database import execute_query
# -------------------------------------------
# БЛОК 1: ФУНКЦИЯ ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ
# -------------------------------------------
def display_results(films, limit):
    if not films:
        print("Нет данных для отображения.")
        return
    print(f"--- Топ-{limit} самых арендуемых фильмов ---")
    print('-' * 52)
    print(f"| {'Название фильма':<30} | {'Кол-во аренд':>15} |")
    print('-' * 52)
    for title, rental_count in films:
        print(f"| {title:<30} | {rental_count:>15} |")
    print('-' * 52)

# -------------------------------------------
# БЛОК 2: ФУНКЦИЯ ДЛЯ СОХРАНЕНИЯ В CSV-файл
# -------------------------------------------
def save_data_to_csv(data, filename):
    if not data:
        print("Нет данных для сохранения в файл.")
        return
    header = ['Название фильма', 'Количество аренд']
    print(f"\nСохраняю отчет в файл {filename}")

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile) # создаем писателя
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
            description="Создает отчет по самым часто "
                        "арендуемым фильмам."
    )
    parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help="По умолчанию Топ-10 фильмов."
    )
    parser.add_argument(
            '--output',
            default="top_rented_films.csv",
            help="Имя файла для сохранения CSV-отчета."
    )
    args = parser.parse_args()
    sql_query = """
        select
            f.title,
            count(r.rental_id) as rental_count
        from
    	    film f
        join 
    	    inventory using(film_id)
        join 
    	    rental r using(inventory_id)
        group by
    	    f.film_id
        order by 
    	    rental_count desc
        limit %s;
    """

    film_data = execute_query(sql_query,(args.limit,))
    if film_data:
        display_results(film_data, args.limit)
        save_data_to_csv(film_data, args.output)
    else:
        print("Не удалось получить данные. Программа завершена.")

if __name__ == "__main__":
    main()