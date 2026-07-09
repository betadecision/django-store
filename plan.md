# Development Plan

План тримаємо окремо від `progress.md`: тут roadmap до usable MVP, а в `progress.md` живий стан проєкту.

## Обраний напрям

- Технічний стек описаний в `architecture.md`; фактичні Python-залежності зафіксовані в `pyproject.toml` і `uv.lock`.
- Магазин універсальний: фізичні товари, цифрові товари, послуги або змішаний формат.
- v1 без реєстрації користувача: стартуємо з guest checkout.
- Для MVP кошик робимо на frontend як client-side cart з local persistence. Backend `orders` API вже приймає фінальний список товарів і створює замовлення.
- Backend cart API, payments, delivery integrations і accounts не блокуємо для MVP; додаємо після стабільного базового commerce flow.

## Definition of Done для MVP

MVP вважаємо готовим, коли:

- адмін може створювати категорії й товари через Django admin;
- покупець бачить список товарів, фільтрує за категорією і відкриває товар;
- покупець додає товари в кошик, змінює кількість і видаляє позиції;
- кошик переживає refresh сторінки;
- checkout приймає email, ім'я, телефон і створює order через `POST /api/orders/`;
- користувач бачить confirmation після успішного замовлення;
- order items зберігають snapshot назви, ціни, кількості й line total;
- backend tests проходять;
- frontend build і lint проходять;
- `README.md`, `plan.md`, `progress.md` відповідають фактичному стану;
- всі змістовні checkpoints закомічені й запушені.

## Робочий ритм

1. Брати один checkpoint за раз.
2. Перед змінами дивитися `git status`.
3. Після зміни запускати релевантні перевірки.
4. Оновлювати `progress.md`, якщо змінився стан проєкту.
5. Робити commit з коротким imperative message.
6. Пушити commit на поточну гілку.

## Roadmap

### 0. Foundation - готово

- Repo docs: `README.md`, `architecture.md`, `plan.md`, `progress.md`.
- `.gitignore` для Python, Django, frontend, IDE і локальних agent/cache файлів.
- Django backend skeleton у `project/`.
- Settings split: `base.py`, `dev.py`, `test.py`.
- GitHub branch workflow через `feature/catalog-orders`.

Checkpoint: `Initial commit`, `Create Django backend skeleton`, `Update ignored local files`.

### 1. Catalog + orders backend slice - готово

- `catalog` models, admin, serializers.
- Read-only catalog API:
  - `GET /api/categories/`
  - `GET /api/categories/<slug>/`
  - `GET /api/products/`
  - `GET /api/products/<slug>/`
  - `GET /api/products/?category=<category-slug>`
- `orders` models і `create_order()` service.
- `POST /api/orders/`.
- Validation tests для order API.

Checkpoint: `Add order API validation tests`.

### 2. Frontend skeleton - готово

- React + Vite + TypeScript у `frontend/`.
- React Router.
- TanStack Query.
- Structure:
  - `frontend/src/app/`
  - `frontend/src/features/catalog/`
  - `frontend/src/shared/api/`
  - `frontend/src/shared/types/`
  - `frontend/src/shared/ui/`
- Catalog screen читає backend API.
- Vite proxy `/api` і `/media` на Django dev server.

Checkpoint: `Create React frontend skeleton`.

### 3. Local demo data - готово

Мета: швидко бачити реальний catalog UI без ручного набивання admin.

- Додати Django management command для dev seed data. Готово.
- Створити 2-3 категорії і кілька активних товарів. Готово.
- Команда має бути повторюваною і не плодити дублікати. Готово.
- Оновити README з командою. Готово.
- Перевірити frontend з реальними товарами. Готово.

Checkpoint: `Add development catalog seed data`.

### 4. Catalog storefront polish - готово

Мета: каталог має бути зручним як перший реальний екран магазину.

- Додати product detail route: `/products/:slug`. Готово.
- Додати link з product card на detail. Готово.
- На detail показати category, description, stock, price. Готово.
- Перевірити loading, empty і error states. Готово.
- Кнопку add to cart переносимо в cart checkpoint, щоб вона одразу мала реальну поведінку.

Checkpoint: `Add product detail screen`.

### 5. Client-side cart - готово

Мета: покупець може зібрати кошик до checkout.

- Додати `features/cart`. Готово.
- Cart state з localStorage persistence. Готово.
- Add to cart з catalog/detail. Готово.
- Cart page або cart drawer. Готово.
- Quantity update. Готово.
- Remove item. Готово.
- Cart totals з поточних product prices. Готово.
- UI states для empty cart і unavailable product. Готово.

Checkpoint: `Add client-side cart flow`.

### 6. Guest checkout - готово

Мета: користувач може оформити замовлення без акаунта.

- Додати `features/checkout`. Готово.
- Checkout route. Готово.
- Form fields: email, full name, phone. Готово.
- Client validation. Готово.
- Submit через `POST /api/orders/`. Готово.
- Success/confirmation screen з order id і total. Готово.
- Error state, якщо backend відхилив order. Готово.
- Очистити cart після успішного order. Готово.

Checkpoint: `Add guest checkout flow`.

### 7. Backend order/admin hardening - готово

Мета: order flow достатньо надійний для MVP demo.

- Перевірити Django admin для orders і order items. Готово.
- За потреби покращити admin list/detail display. Готово.
- Додати backend validation, якщо потрібні inventory rules. Готово.
- Додати tests для edge cases checkout/order creation. Готово.
- Перевірити, що inactive products не проходять у checkout. Готово.

Checkpoint: `Improve order admin and validation`.

### 8. Frontend quality pass

Мета: зменшити ризик регресій перед MVP checkpoint.

- Додати Vitest + React Testing Library, якщо tests дадуть реальну користь.
- Мінімум покрити cart calculations і checkout payload mapping.
- Перевірити responsive layout.
- Перевірити keyboard/focus states для cart і checkout.

Planned commit: `Add frontend flow tests`.

### 9. MVP docs and manual QA

Мета: зафіксувати, як запустити й перевірити проект.

- README: повний local run flow.
- README: seed data, backend server, frontend server.
- progress.md: MVP status, known gaps.
- Manual QA checklist:
  - admin creates products;
  - catalog shows products;
  - category filter works;
  - product detail works;
  - cart works;
  - checkout creates order;
  - order visible in admin.

Planned commit: `Document MVP runbook`.

## Після MVP

Ці речі важливі, але не мають блокувати перший usable flow:

- backend cart API для server-side cart;
- user accounts;
- delivery address model and delivery provider integration;
- payment provider integration;
- email notifications;
- OpenAPI schema and typed frontend client;
- production settings;
- deployment;
- E2E tests with Playwright;
- PostgreSQL/Redis/Docker Compose local stack.

## Поточний наступний крок

Починаємо з checkpoint 8: `Frontend quality pass`.
