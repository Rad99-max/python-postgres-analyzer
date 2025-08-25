# Файл: test_rating_film_analyzer.py.
# Все tests/test_файлы вызываются в терминале командой pytest

# Импортируем функцию, которую будем тестировать
from rating_film_analyzer import get_top_rating_film_data

# `mocker` - это специальный объект от pytest-mock, который мы
# получаем как аргумент
def test_get_top_rating_film_data_returns_correct_data(mocker):
    # --- Шаг 1: Подготовка (Arrange) ---

    # 1.1. Создаем "тестовые" данные, которые якобы вернула БД
    mock_db_return_value = [
        ('Control Anthem', 'G', 185),
        ('Darn Forrester', 'G', 185),
        ('Muscle Bright', 'G', 185),
        ('Moonwalker Fool', 'G', 184),
        ('Worst Banger', 'PG', 185),
        ('Records Zorro', 'PG', 182),
        ('Monsoon Cause', 'PG', 182)
    ]

    # 1.2. Создаем "подделку" для функции execute_query
    # mocker.patch() находит объект по указанному пути
    # и заменяет его.
    mock_execute_query = mocker.patch(
            # Путь к функции, которую подменяем:
            # 'имя_файла.имя_функции'
            'rating_film_analyzer.execute_query',

            # Говорим, что при вызове эта подделка должна
            # вернуть наши данные.
            return_value = mock_db_return_value
    )

    # --- Шаг 2: Действие (Act) ---

    # Вызываем нашу реальную функцию. Она вызовет нашу подделку.
    actual_result = get_top_rating_film_data(limit=2)

    # --- Шаг 3: Проверка (Assert) ---

    # 3.2. Проверяем, С КАКИМИ АРГУМЕНТАМИ была вызвана подделка.
    # Мы ожидаем, что SQL-запрос (он длинный, его можно не
    # проверять) и кортеж с лимитом (2,) были переданы.
    # mocker.ANY - это специальный маркер, который говорит
    # "здесь мог быть любой SQL-запрос".
    mock_execute_query.assert_called_once_with(mocker.ANY, (2,))

    # 3.2. Проверяем, что наша функция вернула именно те данные,
    # которые мы "скормили" нашей подделке.
    assert actual_result == mock_db_return_value
