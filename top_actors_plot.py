# Пример запуска из терминала:
# python top_actors.py

import matplotlib.pyplot as plt
from database import execute_query
import os

#-------------------------------------------------
# Получает данные о топ-5 самых популярных актерах.
#-------------------------------------------------
def get_top_actors_data():
    sql_query= """
    select 
        a.first_name || ' ' || a.last_name as actor_name,
        count(fa.film_id) as film_count
    from 
        actor a
    join
        film_actor fa using(actor_id)
    group by
        a.actor_id
    order by
        film_count desc
    limit 5;
    """
    return execute_query(sql_query)

#-----------------------------------------
#  Строит и сохраняет столбчатую диаграмму.
#------------------------------------------
def creat_and_save_barchart(data, filename="top_actors_barchart.png"):
    if not data:
        print("Нет данных для построения графика.")
        return

    # 1. Распаковываем данные
    actor_names = [row[0] for row in data]
    film_counts = [row[1] for row in data]

    # 2. Создаем полотно
    plt.figure(figsize=(10, 6))

    # 3. Рисуем столбчатую диаграмму
    # plt.bar() - основная функция для столбчатых диаграмм
    bars = plt.bar(actor_names, film_counts, color='skyblue')

    # 4. Настраиваем внешний вид
    plt.title('Топ-5 самых популярных актеров', fontsize=16)
    plt.ylabel('Количество фильмов', fontsize=12)
    # Убираем подпись для оси X, так как имена актеров и так
    # понятны
    plt.xticks(rotation=45, ha='right') # Поворачиваем имена для
                                        # лучшей читаемости
    plt.tight_layout() # Подгоняем элементы

    # 5.(Опционально) Добавляем метки со значениями над столбцами
    plt.bar_label(bars, fmt='%d') # fmt='%d' - форматировать как
                                  # целое число

    # 6. Сохраняем график в файл
    try:
        plt.savefig(filename)
        full_path = os.path.abspath(filename)
        print(f"График успешно сохранен в файл: {full_path}")
    except Exception as e:
        print(f"Ошибка при сохранении графика: {e}")

#---------------------------------
#     Главная функция скрипта.
#---------------------------------
def main():
    print("Получаю данные о топ-5 актерах...")
    actors_data = get_top_actors_data()
    if actors_data:
        print("Данные получены. Строю график...")
        creat_and_save_barchart(actors_data)
    else:
        print("Не удалось получить данные из БД.")

if __name__ == "__main__":
    main()