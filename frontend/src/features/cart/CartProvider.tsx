import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from 'react'
import type { ReactNode } from 'react'

import type { Product } from '../../shared/types/catalog'
import { CartContext } from './cartContext'
import type { CartContextValue } from './cartContext'
import { productToCartItem } from './types'
import type { CartItem } from './types'
import {
  clampQuantity,
  getCartItemCount,
  getCartTotalAmount,
} from './utils'

const CART_STORAGE_KEY = 'django-store-cart'

function isCartItem(value: unknown): value is CartItem {
  if (!value || typeof value !== 'object') {
    return false
  }

  const item = value as Record<string, unknown>

  return (
    typeof item.productId === 'number' &&
    typeof item.slug === 'string' &&
    typeof item.name === 'string' &&
    typeof item.categoryName === 'string' &&
    typeof item.price === 'string' &&
    typeof item.stockQuantity === 'number' &&
    typeof item.quantity === 'number'
  )
}

function loadCartItems() {
  const rawValue = window.localStorage.getItem(CART_STORAGE_KEY)

  if (!rawValue) {
    return []
  }

  try {
    const parsedValue: unknown = JSON.parse(rawValue)

    if (!Array.isArray(parsedValue)) {
      return []
    }

    return parsedValue.filter(isCartItem)
  } catch {
    return []
  }
}

type CartProviderProps = {
  children: ReactNode
}

export function CartProvider({ children }: CartProviderProps) {
  const [items, setItems] = useState<CartItem[]>(loadCartItems)

  useEffect(() => {
    window.localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items))
  }, [items])

  const addProduct = useCallback((product: Product) => {
    if (product.stock_quantity <= 0) {
      return
    }

    setItems((currentItems) => {
      const existingItem = currentItems.find((item) => item.productId === product.id)

      if (!existingItem) {
        return [...currentItems, productToCartItem(product)]
      }

      return currentItems.map((item) =>
        item.productId === product.id
          ? {
              ...item,
              quantity: clampQuantity(item.quantity + 1, product.stock_quantity),
              price: product.price,
              stockQuantity: product.stock_quantity,
            }
          : item,
      )
    })
  }, [])

  const updateQuantity = useCallback((productId: number, quantity: number) => {
    setItems((currentItems) =>
      currentItems.flatMap((item) => {
        if (item.productId !== productId) {
          return [item]
        }

        const nextQuantity = clampQuantity(quantity, item.stockQuantity)

        return nextQuantity > 0 ? [{ ...item, quantity: nextQuantity }] : []
      }),
    )
  }, [])

  const removeItem = useCallback((productId: number) => {
    setItems((currentItems) =>
      currentItems.filter((item) => item.productId !== productId),
    )
  }, [])

  const clearCart = useCallback(() => {
    setItems([])
  }, [])

  const value = useMemo<CartContextValue>(() => {
    const itemCount = getCartItemCount(items)
    const totalAmount = getCartTotalAmount(items)

    return {
      items,
      itemCount,
      totalAmount,
      addProduct,
      updateQuantity,
      removeItem,
      clearCart,
    }
  }, [addProduct, clearCart, items, removeItem, updateQuantity])

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}
