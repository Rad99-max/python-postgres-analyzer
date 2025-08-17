# Пример запуска из терминала:
# python payment_analyzer.py --output top_customers_report.csv

import argparse
import csv
from database import execute_query

#-------------------------------------------
# БЛОК 1: ФУНКЦИЯ ДЛЯ ПОЛУЧЕНИЯ ДАННЫХ ИЗ БД
#-------------------------------------------
def get_top_customers_data(limit=10):
    sql_query = """
        select
            c.first_name || ' ' || c.last_name as customer_name,
            sum(p.amount) as total_amount
        from
            customer c
        join 
            payment p using(customer_id)
        group by
            c.customer_id 
        order by
            total_amount desc
        limit %s;
    """
    data = execute_query(sql_query, (limit,))
    return data

# -------------------------------------------
# БЛОК 2: ФУНКЦИЯ ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ
# -------------------------------------------
def display_results(data, limit=10):
    if not data:
        print("Нет данных для отображения.")
        return
    print(f"--- Топ-{limit} самых активных клиентов ---")
    print('-' * 52)
    print(f"| {'Имя и фамилия':<30} | {'Сумма':>15} |")
    print('-' * 52)
    for full_name, amount in data:
        print(f"| {full_name:<30} | {amount:>15} |")
    print('-' * 52)

# -------------------------------------------
# БЛОК 3: ФУНКЦИЯ ДЛЯ СОХРАНЕНИЯ В CSV-файл
# -------------------------------------------
def save_report_to_csv(data, filename):
    if not data:
        print("Нет данных для сохранения в файл.")
        return
    header = ['Имя Фамилия', 'Сумма']
    print(f"\nСохраняю отчет в файл {filename}...")

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
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
            default=10,
            help="По умолчанию Топ-10 клиентов"
    )
    parser.add_argument(
            '--output',
            default="top_customers_report.csv",
            help="Имя файла для сохранения CSV-отчета."
    )
    args = parser.parse_args()

    payment_data = get_top_customers_data(args.limit)
    if payment_data:
        display_results(payment_data, args.limit)
        save_report_to_csv(payment_data, args.output)
    else:
        print("Не удалось получить данные. Программа завершена.")

if __name__ == "__main__":
    main()