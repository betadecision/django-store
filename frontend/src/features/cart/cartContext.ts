import { createContext } from 'react'

import type { Product } from '../../shared/types/catalog'
import type { CartItem } from './types'

export type CartContextValue = {
  items: CartItem[]
  itemCount: number
  totalAmount: number
  addProduct: (product: Product) => void
  updateQuantity: (productId: number, quantity: number) => void
  removeItem: (productId: number) => void
  clearCart: () => void
}

export const CartContext = createContext<CartContextValue | null>(null)
