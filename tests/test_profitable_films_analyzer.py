# Файл: test_profitable_films_analyzer.py

# Импортируем функцию, которую будем тестировать
from profitable_films_analyzer import get_profitable_films_data

# `mocker` - это специальный объект от pytest-mock, который мы
# получаем как аргумент
def test_get_profitable_films_data_returns_correct_data(mocker):
    # --- Шаг 1: Подготовка (Arrange) ---

    # 1.1. Создаем "тестовые" данные, которые якобы вернула БД
    mock_db_return_value = [
        (' Telegraph Voyage', 215.75),
        ('Zorro Ark', 199.72),
        ('Wife Turn', 198.73)
    ]

    # 1.2. Создаем "подделку" для функции execute_query
    # mocker.patch() находит объект по указанному пути
    # и заменяет его.
    mock_execute_query = mocker.patch(
            # Путь к функции, которую подменяем:
            # 'имя_файла.имя_функции'
            'profitable_films_analyzer.execute_query',
            # Говорим, что при вызове эта подделка должна
            # вернуть наши данные.
            return_value=mock_db_return_value
    )

    # --- Шаг 2: Действие (Act) ---

    # Вызываем нашу реальную функцию. Она вызовет нашу подделку.
    actual_result = get_profitable_films_data(limit=3)

    # --- Шаг 3: Проверка (Assert) ---

    # 3.1. Проверяем, что наша подделка была вызвана ровно 1 раз.
    mock_execute_query.assert_called_once()

    # 3.2. Проверяем, что наша функция вернула именно те данные,
    # которые мы "скормили" нашей подделке.
    assert actual_result == mock_db_return_value
