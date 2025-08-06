import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv()

def execute_query(sql_query, params=None, fetch="all"):
    """
    :param sql_query: Текст SQL-запроса с плейсхолдерами %s.
    :param params: Кортеж с параметрами для запроса.
    :param fetch: Что получить в ответ - "all", "one" или "none".
    :return: Результат запроса или None в случае ошибки.
    """
    conn_params = {
        "host": os.getenv("DB_HOST"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": os.getenv("DB_PORT", "5432")
    }
    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query, params)
                if fetch == "all":
                    return cursor.fetchall()
                elif fetch == "one":
                    return cursor.fetchone()
                # Для fetch="none" или других случаев
                # просто выполнится и вернется None
    except OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")
        return None
