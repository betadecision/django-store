# Shop

Інтернет-магазин на Django backend + React frontend.

Проєкт задуманий як універсальний магазин: фізичні товари, цифрові товари, послуги або змішаний формат. У v1 стартуємо без обов'язкової реєстрації користувача, через guest checkout.

## Stack

Backend dependencies are managed by `uv` in `pyproject.toml` and locked in `uv.lock`.
Frontend dependencies are managed by `npm` in `frontend/package.json` and `frontend/package-lock.json`.

See `architecture.md` for the full stack and architectural direction.

## Project Structure

```text
shop/
  project/
    manage.py
    django_store/
      settings/
        base.py
        dev.py
        test.py
      urls.py
      asgi.py
      wsgi.py
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

## Setup

By default, `project/manage.py` uses `django_store.settings.dev`.

## MVP Runbook

Start backend:

```bash
uv sync
uv run python project/manage.py migrate
uv run python project/manage.py seed_dev_data
uv run python project/manage.py runserver
```

Start frontend in another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
Frontend: http://127.0.0.1:5173/
Backend admin: http://127.0.0.1:8000/admin/
Products API: http://127.0.0.1:8000/api/products/
```

MVP flow:

1. Open the catalog.
2. Filter products by category.
3. Open a product detail page.
4. Add products to the cart.
5. Open the cart.
6. Change quantity or remove an item.
7. Go to checkout.
8. Submit email, full name, and phone.
9. Confirm that the success page shows the order id and total.
10. Confirm that the order is visible in Django admin.

Verification commands:

```bash
uv run python project/manage.py test catalog orders
uv run python project/manage.py makemigrations --check --dry-run
```

```bash
cd frontend
npm test
npm run build
npm run lint
```

### Backend

Install dependencies:

```bash
uv sync
```

Check Django configuration:

```bash
uv run python project/manage.py check
```

Apply migrations:

```bash
uv run python project/manage.py migrate
```

Seed demo catalog data:

```bash
uv run python project/manage.py seed_dev_data
```

Run development server:

```bash
uv run python project/manage.py runserver
```

Create admin user:

```bash
uv run python project/manage.py createsuperuser
```

### Frontend

Install dependencies:

```bash
cd frontend
npm install
```

Run development server:

```bash
npm run dev
```

Build frontend:

```bash
npm run build
```

Lint frontend:

```bash
npm run lint
```

Run frontend tests:

```bash
npm test
```

The Vite dev server proxies `/api` and `/media` to Django at `http://127.0.0.1:8000`.

## Backend API

Catalog endpoints are exposed under `/api/`:

```text
GET /api/categories/
GET /api/categories/<slug>/
GET /api/products/
GET /api/products/<slug>/
GET /api/products/?category=<category-slug>
POST /api/orders/
```

The current catalog API is read-only. Product and category content is managed through Django admin.
Orders can be created through the API and store item price/name snapshots.

## MVP Scope

Included:

- catalog list and category filter;
- product detail page;
- client-side cart with local persistence;
- guest checkout;
- order creation through the backend API;
- order snapshots for product name, price, quantity, and line total;
- Django admin management for catalog and orders.

Not included yet:

- online payments;
- delivery provider integration;
- user accounts;
- production deployment;
- server-side cart API.

Run backend tests:

```bash
uv run python project/manage.py test catalog orders
```

## Dependencies

Add a Python package:

```bash
uv add package-name
```

Remove a Python package:

```bash
uv remove package-name
```

Sync the virtual environment from `pyproject.toml` and `uv.lock`:

```bash
uv sync
```

## Git Workflow

The human owns Git and GitHub actions. Useful rhythm:

```bash
git status
git diff
git add <files>
git commit -m "Short imperative summary"
git push
```

Before committing, check staged changes:

```bash
git diff --staged --stat
```
