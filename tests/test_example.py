# Файл: tests/test_example.py

# Это "тестируемый объект" (Subject Under Test - SUT)
# Простая функция, которую мы будем проверять.
def add_two_numbers(a, b):
    """Складывает два числа."""
    return a + b

# --- А вот и наш первый тест ---

# Название тестовой функции ОБЯЗАТЕЛЬНО должно начинаться
# с `test_`
def test_add_two_positive_numbers():
    # Шаг 1: Подготовка (Arrange)
    num1 = 5
    num2 = 10
    expected_result = 15

    # Шаг 2: Действие (Act)
    actual_result = add_two_numbers(num1, num2)

    # Шаг 3: Проверка (Assert)
    # `assert` - это ключевое слово Python.
    # Если условие после него ИСТИННО, тест продолжается.
    # Если условие ЛОЖНО, тест "падает" с ошибкой AssertionError.
    assert actual_result == expected_result
