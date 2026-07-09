import { createBrowserRouter } from 'react-router-dom'

import { CatalogPage } from '../features/catalog/CatalogPage'
import { ProductDetailPage } from '../features/catalog/ProductDetailPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <CatalogPage />,
  },
  {
    path: '/products/:slug',
    element: <ProductDetailPage />,
  },
])
