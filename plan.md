# Development Plan

План тримаємо окремо від `progress.md`: тут roadmap, а в `progress.md` живий стан проєкту.

## Обраний напрям

- Технічний стек описаний в `architecture.md`; фактичні Python-залежності зафіксовані в `pyproject.toml` і `uv.lock`.
- Магазин універсальний: фізичні товари, цифрові товари, послуги або змішаний формат.
- v1 без реєстрації користувача: стартуємо з guest checkout.

## Етапи

1. Навести лад у репозиторії.
   - Заповнити `README.md`: що це за проєкт і як його запустити.
   - Перевірити `.gitignore` для Python, Django, Node, env-файлів і IDE-сміття.
   - Зафіксувати базові команди через `uv`.

2. Створити backend skeleton.
   - Створити Django project у `project/`.
   - Винести settings у зрозумілу структуру.
   - Перевірити запуск dev server.
   - Додати перший smoke test.

3. Описати домен магазину.
   - Спочатку спроєктувати `catalog`: product, category, product type, availability, price.
   - Врахувати змішаний формат: physical, digital, service.
   - Не зав'язувати модель тільки на доставку фізичних товарів.

4. Побудувати перший backend vertical slice.
   - Моделі catalog.
   - Django admin для catalog.
   - API endpoints для списку товарів і detail-сторінки.
   - API tests для базової поведінки.

5. Створити frontend skeleton.
   - React + Vite + TypeScript у `frontend/`.
   - Router, базова структура `app/`, `features/`, `shared/`.
   - Перший екран каталогу, який читає backend API.

6. Додати cart і guest checkout.
   - Анонімний кошик.
   - Додавання/зміна/видалення позицій.
   - Checkout без реєстрації.
   - Order snapshot: ціна й назва товару фіксуються в замовленні.

7. Після стабільного MVP перейти до інтеграцій.
   - Payment provider.
   - Delivery logic або ручна обробка.
   - Email notifications.
   - Production settings і deployment.

## Git checkpoints

- Після `README.md` і базового repo setup: `Document project setup`
- Після backend skeleton: `Create Django backend skeleton`
- Після першого catalog API: `Add catalog models and API`
- Після frontend skeleton: `Create React frontend skeleton`
- Після cart/checkout: `Add guest checkout flow`
