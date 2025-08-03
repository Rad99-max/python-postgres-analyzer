# Анализатор базы данных "learning_db"
Этот проект представляет собой набор Python-скриптов для анализа 
данных из учебной базы данных PostgreSQL `learning_db`.

## Функциональность

*   `actor_analyzer.py`: Создает отчет по самым популярным актерам 
(по количеству фильмов, в которых они снялись).
*   `client_analyzer.py`: Создает отчет по самым активным клиентам 
(по количеству взятых в прокат фильмов).

## Как запустить

1.  Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Rad99-max/python-postgres-analyzer.git
    cd python-postgres-analyzer
    ```
2.  Создайте и настройте файл `.env` с вашими данными для 
подключения к БД `learning_db`.


3.  Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4.  Запустите нужный скрипт, например:
    ```bash
    python actor_analyzer.py --limit 5
    ```
