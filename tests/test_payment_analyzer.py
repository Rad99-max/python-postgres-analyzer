# Файл: tests/test_payment_analyzer.py

# Импортируем функцию, которую будем тестировать
from payment_analyzer import get_top_customers_data

# `mocker` - это специальный объект от pytest-mock, который
# мы получаем как аргумент
def test_get_top_customers_data_returns_correct_data(mocker):
    # --- Шаг 1: Подготовка (Arrange) ---

    # 1.1. Создаем "игрушечные" данные, которые якобы вернула БД
    mock_db_return_value = [
        ('JOHN DOE', 220.5),
        ('JANE SMITH', 199.9)
    ]

    # 1.2. Создаем "подделку" для функции execute_query
    # mocker.patch() - это наша главная команда.
    # Она находит объект по указанному пути и заменяет его.
    mock_execute_query = mocker.patch(
        # Путь к функции, которую подменяем.
        # ВАЖНО: это путь, как его "видит" тестируемый модуль.
        'payment_analyzer.execute_query',
        # Говорим, что при вызове эта подделка должна вернуть
	    # наши игрушечные данные.
        return_value=mock_db_return_value
    )

    # --- Шаг 2: Действие (Act) ---

    # Вызываем нашу реальную функцию.
    # Внутри нее, когда она попытается вызвать `execute_query`,
    # на самом деле вызовется наша подделка `mock_execute_query`.
    actual_result = get_top_customers_data()

    # --- Шаг 3: Проверка (Assert) ---

    # 3.1. Проверяем, что наша подделка была вызвана ровно 1 раз.
    mock_execute_query.assert_called_once()

    # 3.2. Проверяем, что наша функция вернула именно те данные,
    # которые мы "скормили" нашей подделке.
    assert actual_result == mock_db_return_value
