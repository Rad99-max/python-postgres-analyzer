# Пример запуска из терминала:
# python client_analyzer.py --limit 10 --output top_clients.csv

import argparse
import csv
from database import execute_query

#----------------------------------------------
# БЛОК 1: ФУНКЦИЯ ДЛЯ ПОЛУЧЕНИЯ ДАННЫХ ИЗ БД
#----------------------------------------------
def get_top_clients_data(limit):
    # --- Формируем запрос и вызываем универсальную функцию ---
    sql_query = """
        select
    	    c.first_name,
    	    c.last_name,
    	    sum(p.amount) as total_spent
        from
    	    customer c 
        join 
    	    payment p on c.customer_id = p.customer_id
        group by
    	    c.customer_id
        order by
    	    total_spent desc
        limit %s;
    """

    film_data = execute_query(sql_query, (limit,))
    return film_data

# -------------------------------------------
# БЛОК 2: ФУНКЦИЯ ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ
# -------------------------------------------
def display_results(customers, limit):
    if not customers:
        print("Нет данных для отображения.")
        return
    print(f"\n--- Топ-{limit} самых активных покупателей ---")
    print('-' * 55)
    print(f"| {'Имя':<20} | {'Фамилия':<20} | {'Сумма':>10} |")
    print('-' * 55)
    for first_name, last_name, amount in customers:
        print(f"| {first_name:<20} | {last_name:<20} | "
              f"{amount:>10} |")
    print('-' * 55)
# -------------------------------------------
# БЛОК 3: ФУНКЦИЯ ДЛЯ СОХРАНЕНИЯ В CSV-файл
# -------------------------------------------
def save_report_to_csv(data, filename):
    if not data:
        print("Нет данных для сохранения в файл.")
        return
    header = ['Имя', 'Фамилия', 'Сумма']
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
            description="Создает отчет по самым активным"
                        "покупателям фильмов"
    )
    parser.add_argument(
            '--limit',
            type=int,
            required=True,
            help="Обязательный параметр. Количество самых "
                 "активных покупателей"
    )
    parser.add_argument(
            '--output',
            default="top_clients.csv",
            help="Имя файла для сохранения CSV-отчета."
    )
    args = parser.parse_args()

    # Получаем данные из БД PostgreSQL
    film_data = get_top_clients_data(args.limit)

    if film_data:
        display_results(film_data, args.limit)
        save_report_to_csv(film_data, args.output)
    else:
        print("Не удалось получить данные. Программа завершена.")

if __name__ == "__main__":
    main()