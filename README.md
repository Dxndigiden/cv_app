# cv_app - приложение для работы с базой резюме

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat&logo=docker&logoColor=white)

---

## Запуск локально (Docker)

1. Клонируйте репозиторий 
   ```bash
   git clone https://github.com/Dxndigiden/cv_app.git
   ```
2. Скопируйте `.env` из `.env.example` и при необходимости заполните переменные окружения.
3. Запустите контейнеры Docker:
   ```bash
   docker-compose up --build
   ```
4. Сервис будет доступен по: 

   API документация (Swagger): http://localhost:8000/docs

   Веб интерфейс: http://localhost:8000/

## Описание проекта

О проекте

`CV_app` — это простое и современное веб-приложение для управления резюме пользователей.
Позволяет создавать, редактировать, удалять и улучшать резюме с помощью AI-заглушки.
Проект построен на FastAPI, использует асинхронный SQLAlchemy ORM и PostgreSQL, полностью контейнеризован через Docker.

## Функционал

В приложении реализован базовый функционал CRUD для резюме:

- **Create** — создать новое резюме для пользователя  
- **Read** — получить список всех резюме пользователя или одно по ID  
- **Update** — редактировать существующее резюме  
- **Delete** — удалить резюме пользователя  
- **Improve** — улучшить текст резюме через AI-заглушку  

Все действия доступны только для авторизованного пользователя с JWT-токеном.

### Ссылки

- [Развернуто в облаке](ссылки нет пока)

### Автор

Автор: [Dxndigiden](https://github.com/dxndigiden)
