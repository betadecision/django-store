import { describe, expect, it } from 'vitest'

import { clampQuantity, getCartItemCount, getCartTotalAmount } from './utils'
import type { CartItem } from './types'

const cartItems: CartItem[] = [
  {
    productId: 1,
    slug: 'zenbook-air-14',
    name: 'ZenBook Air 14',
    categoryName: 'Laptops',
    price: '39999.00',
    image: null,
    stockQuantity: 7,
    quantity: 2,
  },
  {
    productId: 2,
    slug: 'usb-c-dock',
    name: 'USB-C Dock',
    categoryName: 'Accessories',
    price: '3499.00',
    image: null,
    stockQuantity: 15,
    quantity: 1,
  },
]

describe('cart utils', () => {
  it('counts all cart item quantities', () => {
    expect(getCartItemCount(cartItems)).toBe(3)
  })

  it('calculates total amount from item prices and quantities', () => {
    expect(getCartTotalAmount(cartItems)).toBe(83497)
  })

  it('clamps quantity between 1 and stock quantity', () => {
    expect(clampQuantity(0, 7)).toBe(1)
    expect(clampQuantity(3, 7)).toBe(3)
    expect(clampQuantity(99, 7)).toBe(7)
  })

  it('returns 0 when product has no stock', () => {
    expect(clampQuantity(1, 0)).toBe(0)
  })
})
