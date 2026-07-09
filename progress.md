# Progress

Живий журнал руху проєкту. Тут фіксуємо практичний стан: що зроблено, що далі, які питання відкриті, і коли зміни варто зберегти в Git.

## 2026-05-27

### Зроблено

- Стартували планування інтернет-магазину на Django + React.
- Узгодили, що GitHub-дії робить людина, а агент пояснює й підказує.
- Створили `agents.md` з правилами співпраці.
- Створили `architecture.md` зі стартовим стеком і структурою проєкту.
- Замінили `decisions.md` на `progress.md`, бо на старті корисніший живий журнал прогресу.
- Повернули документи українською, бо вони мають бути зручні для щоденної роботи.
- Вирішили, що магазин має бути універсальним і підтримувати змішаний формат: фізичні товари, цифрові товари, послуги або їх комбінації.
- Вирішили, що у v1 реєстрація користувача не потрібна; стартуємо з guest checkout.
- Ініціалізували Git-репозиторій.
- Перейменували основну гілку на `main`.
- Додали remote `origin`: `https://github.com/betadecision/django-store`.
- Створили перший коміт: `848da2a Initial commit`.
- Створили Django backend skeleton у `project/`.
- Винесли Django settings у структуру `settings/base.py`, `settings/dev.py`, `settings/test.py`.

### Поточний стан

- Backend skeleton створений.
- Frontend ще не створений.
- Git працює локально, перший коміт створений.
- Product/order модель має враховувати змішаний формат магазину, а не бути прив'язаною тільки до фізичних товарів.

### Наступні кроки

- Запушити локальні коміти на GitHub, якщо ще не зроблено: `git push`.
- Додати перший smoke test для backend.
- Перевірити запуск dev server.
- Створити React + Vite + TypeScript frontend-проєкт.

### Відкриті питання

- Який payment provider імовірний пізніше: Stripe, WayForPay, LiqPay, Fondy/Whitepay або інший?
- Чи буде delivery-інтеграція з поштовим сервісом, чи почнемо з ручного оформлення?

### Git checkpoint

Наступний checkpoint: після завершення backend skeleton.

## 2026-06-08

### Зроблено

- Повернули `catalog` API на класові DRF views після тренування функціональних views.
- `CategoryViewSet` працює як read-only endpoint для активних категорій.
- `ProductViewSet` працює як read-only endpoint для активних продуктів.
- Detail endpoints використовують `slug`.
- Для продуктів додано фільтр за категорією через query parameter: `?category=<category-slug>`.
- `catalog.urls` знову використовує `DefaultRouter`:
  - `/api/categories/`
  - `/api/categories/<slug>/`
  - `/api/products/`
  - `/api/products/<slug>/`

### Поточний стан

- `catalog` має моделі, admin, serializers, read-only API і базові тести.
- Контент каталогу поки логічно керується через Django admin, а API тільки віддає дані.
- Функціональні views були корисні як практика, але фінальний варіант для цього етапу повернули до `ReadOnlyModelViewSet`.

### Наступні кроки

- Перевірити API вручну в браузері або DRF browsable API.
- За потреби додати API tests для списку продуктів, detail по `slug` і фільтра `?category=`.
- Після перевірки зробити Git checkpoint для catalog API.

### Git checkpoint

Доречний commit message після перевірки: `Add read-only catalog API`.

## 2026-07-09

### Зроблено

- Додали frontend skeleton у `frontend/` на React + Vite + TypeScript.
- Додали React Router і TanStack Query.
- Створили базову структуру:
  - `src/app/`
  - `src/features/catalog/`
  - `src/shared/api/`
  - `src/shared/types/`
- Перший екран frontend показує каталог і читає backend endpoints:
  - `/api/categories/`
  - `/api/products/`
  - `/api/products/?category=<category-slug>`
- Додали Vite proxy для `/api` і `/media` на Django dev server `http://127.0.0.1:8000`.
- Додали order API validation tests і заборонили порожній список `items` при створенні замовлення.
- Оновили `.gitignore` для локальних кешів, frontend build/cache файлів і agent-папок.

### Поточний стан

- Backend має read-only catalog API і basic order creation API.
- Frontend skeleton створений і має робочий catalog screen.
- Frontend поки тільки читає каталог; cart і checkout ще не створені.

### Перевірено

- Backend: `uv run python project/manage.py test catalog orders`
- Frontend: `npm run build`
- Frontend: `npm run lint`

### Наступні кроки

- Перевірити frontend вручну разом із Django dev server.
- Додати cart flow у frontend/backend або спочатку зробити product detail screen, якщо він потрібен перед cart.
- Після перевірки зробити Git checkpoint для frontend skeleton.

### Git checkpoint

Доречний commit message після перевірки: `Create React frontend skeleton`.

## 2026-07-09 - Roadmap to MVP

### Зроблено

- Узгодили, що далі рухаємось послідовно по всьому проекту до usable MVP.
- Оновили `plan.md` з повним roadmap:
  - local demo data;
  - product detail;
  - client-side cart;
  - guest checkout;
  - order/admin hardening;
  - frontend quality pass;
  - MVP docs and manual QA.
- Для v1 вирішили не блокуватися на backend cart API: кошик робимо на frontend, а фінальне замовлення створюємо через вже наявний `POST /api/orders/`.

### Поточний стан

- Поточна гілка: `feature/catalog-orders`.
- Backend і frontend skeleton checkpoints вже запушені.
- Наступний implementation checkpoint: `Local demo data`.

### Наступні кроки

- Додати management command для повторюваного seed dev catalog data.
- Оновити README з командою seed.
- Перевірити backend tests, frontend build і frontend lint.
- Закомітити й запушити checkpoint: `Add development catalog seed data`.

## 2026-07-09 - Local demo data

### Зроблено

- Додали management command `seed_dev_data`.
- Команда створює повторювані dev catalog data:
  - 3 категорії;
  - 5 активних товарів.
- Додали тест, що повторний запуск seed не створює дублікати.
- Оновили README з командою:
  - `uv run python project/manage.py seed_dev_data`

### Поточний стан

- Frontend catalog може показувати реальні локальні товари без ручного створення через admin.
- Наступний implementation checkpoint: `Catalog storefront polish`.

### Наступні кроки

- Додати product detail route `/products/:slug`.
- Додати link з product card на detail screen.
- Додати кнопку add to cart на detail як підготовку до cart flow.

## 2026-07-09 - Product detail screen

### Зроблено

- Додали frontend API helper для `GET /api/products/<slug>/`.
- Додали route `/products/:slug`.
- Додали `ProductDetailPage`.
- Product cards у catalog тепер ведуть на detail screen.
- Винесли форматування ціни й image URL helper у `features/catalog/formatters.ts`.
- Додали loading і error states для detail screen.

### Поточний стан

- Catalog storefront має list, category filter і product detail.
- Кнопку add to cart переносимо в наступний checkpoint, щоб не створювати нефункціональну UI-дію.
- Наступний implementation checkpoint: `Client-side cart`.

### Перевірено

- Backend: `uv run python project/manage.py test catalog orders`
- Frontend: `npm run build`
- Frontend: `npm run lint`
- HTTP: `GET /api/products/zenbook-air-14/`
- HTTP: `GET /products/zenbook-air-14`

## 2026-07-09 - Client-side cart

### Зроблено

- Додали `features/cart`.
- Додали `CartProvider` з localStorage persistence.
- Додали cart hook і cart context.
- Додали cart link з item count у catalog і product detail headers.
- Додали add-to-cart buttons у catalog cards і product detail.
- Додали route `/cart`.
- Додали cart page:
  - список позицій;
  - quantity increase/decrease;
  - remove item;
  - clear cart;
  - items count;
  - total amount.

### Поточний стан

- Покупець може зібрати кошик і змінювати його до checkout.
- Cart переживає refresh сторінки.
- Checkout ще не створений.
- Наступний implementation checkpoint: `Guest checkout`.

### Перевірено

- Frontend: `npm run build`
- Frontend: `npm run lint`

## 2026-07-09 - Guest checkout

### Зроблено

- Додали `features/checkout`.
- Додали checkout API helper для `POST /api/orders/`.
- Додали route `/checkout`.
- Додали checkout form:
  - email;
  - full name;
  - phone.
- Checkout створює order з cart items.
- Після успішного order cart очищається.
- Додали route `/checkout/success`.
- Success screen показує order id і total.
- Cart page тепер веде на checkout.

### Поточний стан

- Базовий commerce flow уже працює локально:
  - catalog;
  - product detail;
  - cart;
  - guest checkout;
  - order creation.
- Наступний implementation checkpoint: `Backend order/admin hardening`.

### Перевірено

- Backend: `uv run python project/manage.py test catalog orders`
- Frontend: `npm run build`
- Frontend: `npm run lint`
- HTTP: `POST /api/orders/`
- HTTP: `GET /checkout`
- HTTP: `GET /checkout/success?order=1&total=39999.00`
