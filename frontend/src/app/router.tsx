import { createBrowserRouter } from 'react-router-dom'

import { CartPage } from '../features/cart/CartPage'
import { CatalogPage } from '../features/catalog/CatalogPage'
import { ProductDetailPage } from '../features/catalog/ProductDetailPage'
import { CheckoutPage } from '../features/checkout/CheckoutPage'
import { CheckoutSuccessPage } from '../features/checkout/CheckoutSuccessPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <CatalogPage />,
  },
  {
    path: '/products/:slug',
    element: <ProductDetailPage />,
  },
  {
    path: '/cart',
    element: <CartPage />,
  },
  {
    path: '/checkout',
    element: <CheckoutPage />,
  },
  {
    path: '/checkout/success',
    element: <CheckoutSuccessPage />,
  },
])
