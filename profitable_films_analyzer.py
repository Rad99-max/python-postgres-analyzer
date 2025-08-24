# Пример запуска из терминала:
# python profitable_films_analyzer.py --limit 10 --output имя_файла.csv

import argparse
import csv
from database import execute_query

#-------------------------------------------
# БЛОК 1: ФУНКЦИЯ ДЛЯ ПОЛУЧЕНИЯ ДАННЫХ ИЗ БД
#-------------------------------------------
def get_profitable_films_data(limit=15):
    sql_query = """
        select 
	        f.title,
	        sum(p.amount) as total_amount
        from 
	        film f
        join
	        inventory using(film_id)
        join
        	rental using(inventory_id)
        join
	        payment p using(rental_id)
        group by
	        film_id
        order by total_amount desc
        limit %s;
    """
    data = execute_query(sql_query, (limit,))
    return data

# -------------------------------------------
# БЛОК 2: ФУНКЦИЯ ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ
# -------------------------------------------
def display_results(data, limit=15):
    if not data:
        print("Нет данных для отображения.")
        return
    print(f"--- Топ-{limit} самых прибыльных фильмов ---")
    print('-' * 52)
    print(f"| {'Название фильма':<30} | {'Сумма':>15} |")
    print('-' * 52)
    for film_name, amount in data:
        print(f"| {film_name:<30} | {amount:>15} |")
    print('-' * 52)

# -------------------------------------------
# БЛОК 3: ФУНКЦИЯ ДЛЯ СОХРАНЕНИЯ В CSV-файл
# -------------------------------------------
def save_report_to_csv(data, filename):
    if not data:
        print("Нет данных для сохранения в файл.")
        return
    header = ['Название фильма', 'Сумма']
    print(f"\nСохраняю отчет в файл {filename}...")

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(data)
        print(f"Отчет успешно сохранен в файл {filename}")
    except IOError as e:
        print(f"Ошибка при сохранении файла: {e}")

#-------------------------------------------------------
# БЛОК 4: ГЛАВНАЯ ФУНКЦИЯ, УПРАВЛЯЮЩАЯ ЛОГИКОЙ СКРИПТА
# ------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
            description="Создает отчет по самым популярным фильмам"
    )
    parser.add_argument(
            '--limit',
            type=int,
            default=15,
            help="По умолчанию Топ-15 фильмов"
    )
    parser.add_argument(
            '--output',
            default="top_profitable_films_report.csv",
            help="Имя файла для сохранения CSV-отчета."
    )
    args = parser.parse_args()

    profitable_films_data = get_profitable_films_data(args.limit)
    if profitable_films_data:
        display_results(profitable_films_data, args.limit)
        save_report_to_csv(profitable_films_data, args.output)
    else:
        print("Не удалось получить данные. Программа завершена.")
if __name__ == "__main__":
    main()