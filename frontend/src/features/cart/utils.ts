import type { CartItem } from './types'

export function clampQuantity(quantity: number, stockQuantity: number) {
  if (stockQuantity <= 0) {
    return 0
  }

  return Math.min(Math.max(quantity, 1), stockQuantity)
}

export function getCartItemCount(items: CartItem[]) {
  return items.reduce((total, item) => total + item.quantity, 0)
}

export function getCartTotalAmount(items: CartItem[]) {
  return items.reduce(
    (total, item) => total + Number(item.price) * item.quantity,
    0,
  )
}
