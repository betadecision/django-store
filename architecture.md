# Architecture

## Мета

Побудувати підтримуваний інтернет-магазин з Django API backend і React frontend. Перша версія має покривати практичний commerce flow без зайвого ускладнення:

- каталог товарів;
- категорії та пошук/фільтрація;
- кошик;
- підготовка checkout;
- замовлення;
- керування через admin;
- guest checkout у v1;
- акаунти користувачів пізніше, якщо вони дадуть реальну користь;
- платежі пізніше, через чітку інтеграційну межу.

## Рекомендований стек

### Backend

- Python: зафіксовано в `.python-version`
- Django та Python-залежності: зафіксовано в `pyproject.toml` і `uv.lock`
- Django REST Framework
- PostgreSQL
- Redis для кешу, фонових задач і майбутнього rate limiting
- Celery або Django background tasks пізніше, коли справді з'явиться async-робота
- pytest, pytest-django, factory-boy
- Ruff для linting і formatting

Чому так: Django дає auth, admin, ORM, migrations, security defaults і зрілу екосистему. DRF робить API явним і звичним. PostgreSQL є надійним дефолтом для commerce-даних.

### Frontend

- React 19
- TypeScript
- Vite
- React Router
- TanStack Query для server state
- UI-основа після прояснення дизайну: CSS modules, Tailwind CSS або компонентна бібліотека
- Vitest і React Testing Library
- Playwright пізніше для end-to-end checkout flow

Чому так: React + TypeScript добре підходить для сучасної вітрини магазину. TanStack Query прибирає loading, caching і mutations з ручного component state.

### API Contract

- REST API first.
- JSON over HTTPS.
- OpenAPI schema генерується з backend.
- Frontend може споживати typed API client, коли endpoints стабілізуються.

GraphQL не обираємо для v1, бо домен нормально стартує з resource-oriented endpoints.

## Форма репозиторію

Початкова monorepo-структура:

```text
shop/
  project/
    manage.py
    django_store/
  frontend/
    src/
      app/
      features/
      shared/
  agents.md
  architecture.md
  plan.md
  progress.md
  pyproject.toml
  uv.lock
```

Пізніше ці документи можна перенести в `docs/`, якщо root стане шумним. Зараз root-level docs легше знайти.

## Backend-модулі

### `catalog`

Відповідає за:

- товари;
- категорії;
- зображення товарів;
- ціни;
- правила показу наявності.

Не відповідає за:

- стан кошика;
- життєвий цикл замовлення;
- стан платежу.

### `carts`

Відповідає за:

- анонімний кошик;
- кошик авторизованого користувача пізніше, якщо з'являться акаунти;
- позиції кошика;
- зміну кількості;
- totals, пораховані з актуальних даних товарів.

### `orders`

Відповідає за:

- створення замовлення;
- order items як історичні snapshots;
- статус замовлення;
- контактні й delivery-дані покупця;
- перегляд замовлень в admin.

### `accounts`

Відповідає за:

- registration/login flow пізніше, якщо він потрібен;
- профіль покупця пізніше;
- адреси пізніше;
- permissions понад Django defaults, якщо з'явиться така потреба.

### `payments`

Відповідає за:

- межу інтеграції з payment provider;
- створення payment intent/session;
- webhook handling;
- mapping payment status.

Деталі payment provider не мають протікати в `orders` або `carts`.

## Принципи даних

- Ціна товару може змінитися; ціна в order item має бути snapshot.
- Назва товару може змінитися; назву в order item теж варто snapshot-ити.
- Inventory rules мають бути явними до прийняття платежу.
- Гроші зберігаємо як integer minor units або `Decimal`, ніколи як float.
- Часові поля мають бути timezone-aware.

## API Sketch

```text
GET    /api/products/
GET    /api/products/{slug}/
GET    /api/categories/

GET    /api/cart/
POST   /api/cart/items/
PATCH  /api/cart/items/{id}/
DELETE /api/cart/items/{id}/

POST   /api/orders/
GET    /api/orders/
GET    /api/orders/{id}/

POST   /api/payments/session/
POST   /api/payments/webhook/
```

## Frontend-структура

```text
frontend/src/
  app/
    router.tsx
    providers.tsx
  features/
    catalog/
    cart/
    checkout/
    orders/
    account/
  shared/
    api/
    ui/
    lib/
    types/
```

Feature folders мають володіти своїми screens, components, hooks і tests, якщо код не є справді shared.

## Середовища

Очікувані середовища:

- local development;
- test;
- staging пізніше;
- production пізніше.

Конфігурація має приходити з environment variables. Secrets ніколи не комітимо.

## Security Baseline

- Використовуємо Django security middleware.
- Admin тримаємо захищеним і візуально окремим від storefront.
- CSRF protection обов'язковий там, де використовується cookie-based auth.
- Для session auth бажано використовувати secure, HttpOnly cookies.
- Payment webhooks перевіряємо через provider signatures.
- Rate limits для auth і checkout endpoints додаємо до production.

## Testing Strategy

Backend:

- model tests для money, inventory і order snapshot behavior;
- API tests для catalog, cart, checkout і orders;
- webhook tests, коли з'являться payments.

Frontend:

- component tests для cart і checkout states;
- API hook tests там, де це дає користь;
- end-to-end test для happy-path purchase flow перед production.

## Deployment Direction

Стартуємо local-first. Docker Compose додаємо, коли застосунку справді потрібні PostgreSQL і Redis локально. Пізніше deployment обираємо за бюджетом і простотою:

- backend: Render, Fly.io, Railway, VPS або схожий варіант;
- frontend: Vercel/Netlify або serve через backend, якщо простота важливіша;
- database: managed PostgreSQL;
- media: S3-compatible object storage.

## Джерела для версій

- У проєкті зараз зафіксовано Python 3.14: `.python-version`
- У проєкті зараз зафіксовано Django 6.0.5: `pyproject.toml` і `uv.lock`
- Django REST Framework підтримує Django 4.2-6.0 і Python 3.10-3.14: https://www.django-rest-framework.org/
- React 19 стабільний реліз: https://react.dev/blog/2024/12/05/react-19
