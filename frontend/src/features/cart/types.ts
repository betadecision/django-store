import type { Product } from '../../shared/types/catalog'

export type CartItem = {
  productId: number
  slug: string
  name: string
  categoryName: string
  price: string
  image: string | null
  stockQuantity: number
  quantity: number
}

export function productToCartItem(product: Product): CartItem {
  return {
    productId: product.id,
    slug: product.slug,
    name: product.name,
    categoryName: product.category.name,
    price: product.price,
    image: product.image,
    stockQuantity: product.stock_quantity,
    quantity: 1,
  }
}
