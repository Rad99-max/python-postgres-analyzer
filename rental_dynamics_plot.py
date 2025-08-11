import matplotlib.pyplot as plt
from database import execute_query
import os

def get_rental_dynamics():
    """
    Получает данные о динамике аренд из базы данных.
    """
    sql_query = """
        select 
	        to_char(rental_date, 'YYYY-MM') as rental_month,
        	count(*) as rental_count
        from
	        rental
        group by
	        rental_month
        order by
	        rental_month;
    """
    # Вызываем нашу универсальную функцию из database.py
    return execute_query(sql_query)

def create_and_save_plot(data, filename="rental_dynamics.png"):
    """
    Строит и сохраняет линейный график на основе полученных данных.
    """
    if not data:
        print("Нет данных для построения графика.")
        return
    # 1. "Распаковываем" данные в два отдельных списка: для
    # оси X и для оси Y.
    # months станет ['2005-05', '2005-06', ...]
    # counts станет [1156, 2311, ...]
    months = [row[0] for row in data]
    counts = [row[1] for row in data]

    # 2. Создаем "полотно" для рисования
    plt.figure(figsize=(12, 7)) # Задаем размер картинки в дюймах

    # 3. Рисуем сам линейный график
    plt.plot(months, counts, marker='o', linestyle='-',
             color='b')
    # marker='o' — ставит точки на данных
    # linestyle='-' — сплошная линия
    # color='b' — синий цвет (blue)

    # --- Добавляем метки с количеством аренд ---
    # Проходимся циклом по каждой точке (по ее координатам X и Y)
    for i in range(len(months)):
        # plt.text() - это функция для добавления текста на график
        plt.text(
                x=months[i],        # Координата X текста
                y=counts[i]+80,     # Координата Y текста
                                    # (чуть выше точки, +50)
                s=str(counts[i]),   # Сам текст (количество аренд)
                ha='center',         # Горизонтальное выравнивание по центру
                fontsize=16
        )
# ------------------------------------------------

    # 4. Настраиваем внешний вид графика
    plt.title('Динамика количества аренд по месяцам', fontsize=18)
    plt.xlabel('Месяц', fontsize=16)
    plt.ylabel('Количество аренд', fontsize=16)
    plt.grid(True) # Включаем сетку
    plt.xticks(rotation=45) # Поворачиваем подписи месяцев для читаемости
    plt.tight_layout() # Автоматически подгоняем все элементы

    # 5. Сохраняем график в файл
    try:
        plt.savefig(filename)
        # Получаем полный путь к файлу для красивого вывода
        full_path = os.path.abspath(filename)
        print(f"График успешно сохранен в файл: {full_path}")
    except Exception as e:
        print(f"Ошибка при сохранении графика: {e}")

def main():
    """
    Главная функция скрипта.
    """
    print("Получаю данные о динамике аренд...")
    rental_data = get_rental_dynamics()
    if rental_data:
        print("Данные получены. Строю график...")
        create_and_save_plot(rental_data)
    else:
        print("Не удалось получить данные из БД.")

if __name__ == "__main__":
    main()
