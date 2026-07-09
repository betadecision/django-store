import { describe, expect, it } from 'vitest'

import type { CartItem } from '../cart/types'
import { cartItemsToOrderItems } from './payload'

describe('checkout payload', () => {
  it('maps cart items to order API items', () => {
    const items: CartItem[] = [
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
        productId: 3,
        slug: 'usb-c-dock',
        name: 'USB-C Dock',
        categoryName: 'Accessories',
        price: '3499.00',
        image: null,
        stockQuantity: 15,
        quantity: 1,
      },
    ]

    expect(cartItemsToOrderItems(items)).toEqual([
      { product: 1, quantity: 2 },
      { product: 3, quantity: 1 },
    ])
  })
})
