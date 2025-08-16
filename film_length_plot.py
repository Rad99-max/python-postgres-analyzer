import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from database import execute_query
import os

#-----------------------------------------------
# Получает 'сырые' данные о продолжительности и
# рейтингах фильмов.
#-----------------------------------------------
def get_film_length_data():
    sql_query = """
        select
            rating,
            length
        from
            film
        where 
            length is not null;
    """
    data = execute_query(sql_query)
    # Преобразуем список кортежей в DataFrame от Pandas для удобства работы
    if data:
        return pd.DataFrame(data, columns=['rating', 'length'])
    return None

#----------------------------------------------------
# Строит и сохраняет скрипичный график.
#----------------------------------------------------
def create_and_save_violinplot(df, filename="film_length_violinplot.png"):
    if df is None or df.empty:
        print("Нет данных для построения графика.")
        return
    # Задаем стиль для более красивого вида
    sns.set_theme(style="whitegrid")

    # Создаем полотно
    plt.figure(figsize=(12, 8))

    # --- ГЛАВНАЯ КОМАНДА: строим Violin Plot одной строкой ---
    sns.violinplot(
            data=df,
            x="rating",
            y="length",
            # Сортируем рейтинги в осмысленном порядке
            order=['G', 'PG', 'PG-13', 'R', 'NC-17']
    )
    #-----------------------------------------------------
    # Настраиваем внешний вид
    plt.title('Распределение продолжительности фильмов по рейтингам', fontsize=16)
    plt.xlabel('Рейтинг MPAA', fontsize=12)
    plt.ylabel('Продолжительность (мин)', fontsize=12)

    # Сохраняем график в файл
    try:
        plt.savefig(filename)
        full_path = os.path.abspath(filename)
        print(f"График успешно сохранен в файл: {full_path}")
    except Exception as e:
        print(f"Ошибка при сохранении графика: {e}")

#--------------------------------------------------
# Главная функция скрипта.
#--------------------------------------------------
def main():
    print("Получаю данные о фильмах...")
    film_df = get_film_length_data()
    if film_df is not None:
        print("Данные получены. Строю график...")
        create_and_save_violinplot(film_df)
    else:
        print("Не удалось получить данные из БД.")

if __name__ == "__main__":
    main()