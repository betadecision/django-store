import { fetchJson } from '../../shared/api/client'
import type { Category, Product } from '../../shared/types/catalog'

export function getCategories() {
  return fetchJson<Category[]>('/api/categories/')
}

type GetProductsParams = {
  categorySlug?: string
}

export function getProducts({ categorySlug }: GetProductsParams = {}) {
  const params = new URLSearchParams()

  if (categorySlug) {
    params.set('category', categorySlug)
  }

  const query = params.toString()

  return fetchJson<Product[]>(`/api/products/${query ? `?${query}` : ''}`)
}

export function getProduct(slug: string) {
  return fetchJson<Product>(`/api/products/${slug}/`)
}
