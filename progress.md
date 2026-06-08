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
