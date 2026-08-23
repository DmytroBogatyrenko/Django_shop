# Цитадель — Крамниця Реліквій

[![Django CI](https://github.com/DmytroBogatyrenko/Django_shop/actions/workflows/ci.yml/badge.svg)](https://github.com/DmytroBogatyrenko/Django_shop/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)](https://github.com/DmytroBogatyrenko/Django_shop)
[![Python](https://img.shields.io/badge/python-3.13-blue)](https://python.org)
[![Django](https://img.shields.io/badge/django-6.0.7-green)](https://djangoproject.com)

Повнофункціональний інтернет-магазин побудований на Django 6.

**Live demo:** https://djangoshop-sg08.onrender.com

## Функціонал

- Каталог товарів з ієрархією категорій та фільтрами
- Реєстрація та авторизація користувачів
- Session-based кошик
- Система промокодів зі знижками
- Оформлення замовлень з адресою доставки
- Статуси замовлень з timeline та скасуванням
- Система відгуків (тільки після покупки)
- AJAX пошук з автодоповненням
- Redis кешування
- 43 автоматичних тести, 94% покриття

## Технології

- **Backend:** Django 6.0.7, PostgreSQL, Redis
- **Frontend:** Bootstrap 5, custom CSS (темний стиль)
- **Deploy:** Render.com, Gunicorn, WhiteNoise
- **CI/CD:** GitHub Actions

## Запуск локально

```bash
git clone https://github.com/DmytroBogatyrenko/Django_shop.git
cd Django_shop
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_db
python manage.py createsuperuser
python manage.py runserver
