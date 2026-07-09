export type Category = {
  id: number
  name: string
  slug: string
  description: string
}

export type Product = {
  id: number
  category: Category
  name: string
  slug: string
  description: string
  price: string
  stock_quantity: number
  image: string | null
}
