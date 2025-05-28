# Weather Django App

Что реализовано:
- Поиск прогноза через open-meteo
- Автодополнение городов (геокодинг open-meteo)
- История поиска (по сессии) + предложение последнего города
- Эндпоинт `/search_counts/` — JSON-статистика по городам
- Тесты (Django TestCase)
- Сборка в Docker

Технологии:
- Django 5.1, SQLite
- requests для HTTP-запросов
- Gunicorn в контейнере

Запуск:
1. `docker-compose build`
2. `docker-compose up`
3. Открыть http://localhost:8000

Отправка запроса в Postman:
POST localhost:8000 
в body, form-data указать city. 
