# Файл: tests/test_example.py

# Тестируемая функция
def add_two_numbers(a, b):
    """Складывает два числа."""
    return a + b

# Тест для этой функции
def test_add_two_positive_numbers():
    # Arrange (Подготовка)
    num1 = 5
    num2 = 10
    expected_result = 15

    # Act (Действие)
    actual_result = add_two_numbers(num1, num2)

    # Assert (Проверка)
    assert actual_result == expected_result
