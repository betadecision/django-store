# Frontend

React storefront for the Django Store project.

## Stack

- React
- TypeScript
- Vite
- React Router
- TanStack Query

## Setup

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Build:

```bash
npm run build
```

Lint:

```bash
npm run lint
```

Test:

```bash
npm test
```

The Vite dev server proxies `/api` and `/media` to the Django backend at `http://127.0.0.1:8000`.

## Structure

```text
src/
  app/
    providers.tsx
    router.tsx
  features/
    catalog/
  shared/
    api/
    types/
    ui/
```
