# Архитектура

Клиент → Flask → SQLite

Маршруты:
- GET / - главная
- GET/POST /add - добавление
- GET /wish/<id> - детали
- GET/POST /edit/<id> - редактирование
- POST /delete/<id> - удаление
- GET /search - поиск
