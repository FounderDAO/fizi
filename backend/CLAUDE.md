# Fizi.uz Backend — Django 5

## Проект
Fizi.uz — современный маркетплейс объявлений для Узбекистана.
OLX-конкурент с AI поиском, видео, KYC верификацией, магазинами.

## Стек
- Django 5 + DRF
- PostgreSQL 16
- Redis + Celery
- JWT авторизация (телефон + OTP)

## Git правила
- НИКОГДА не пушить в main напрямую
- feature/* → PR → dev → PR → main
- Conventional Commits: feat/fix/chore/docs/test

## Запуск
```bash
docker compose up -d
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

## API
- Auth: /api/v1/auth/
- Listings: /api/v1/listings/
- Categories: /api/v1/categories/
- Shops: /api/v1/shops/
- Chat: /api/v1/chat/
- Billing: /api/v1/billing/

## Структура приложений
- `users` — кастомный User (phone auth), OTP, отзывы
- `categories` — дерево категорий (ru/uz/en)
- `listings` — объявления, фото, избранное
- `shops` — магазины, тарифные планы
- `chat` — переписка покупатель↔продавец
- `billing` — платежи (Payme), подписки, продвижение
- `notifications` — Celery tasks: SMS (Eskiz), push
- `ai` — Claude AI: генерация описаний, модерация
- `storage` — Cloudflare R2 через django-storages

## Порты (dev)
- Backend: 4600
- DB: 5490
- Redis: 6390
