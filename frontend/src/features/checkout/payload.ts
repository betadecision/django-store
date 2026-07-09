import type { CartItem } from '../cart/types'
import type { CreateOrderPayload } from './api'

export function cartItemsToOrderItems(
  items: CartItem[],
): CreateOrderPayload['items'] {
  return items.map((item) => ({
    product: item.productId,
    quantity: item.quantity,
  }))
}
