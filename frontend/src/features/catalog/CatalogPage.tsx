import { useQuery } from '@tanstack/react-query'
import {
  AlertCircle,
  ImageIcon,
  PackageSearch,
  RefreshCw,
  ShoppingBag,
} from 'lucide-react'
import { useSearchParams } from 'react-router-dom'

import type { Product } from '../../shared/types/catalog'
import { getCategories, getProducts } from './api'

const currencyFormatter = new Intl.NumberFormat('uk-UA', {
  style: 'currency',
  currency: 'UAH',
  minimumFractionDigits: 2,
})

function formatPrice(price: string) {
  return currencyFormatter.format(Number(price))
}

function resolveImageUrl(image: string | null) {
  if (!image) {
    return null
  }

  return image
}

export function CatalogPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const activeCategory = searchParams.get('category') ?? ''

  const categoriesQuery = useQuery({
    queryKey: ['categories'],
    queryFn: getCategories,
  })

  const productsQuery = useQuery({
    queryKey: ['products', activeCategory],
    queryFn: () => getProducts({ categorySlug: activeCategory || undefined }),
  })

  const products = productsQuery.data ?? []
  const categories = categoriesQuery.data ?? []

  const activeCategoryName = activeCategory
    ? categories.find((category) => category.slug === activeCategory)?.name ??
      activeCategory
    : 'All products'

  function chooseCategory(categorySlug: string) {
    setSearchParams(categorySlug ? { category: categorySlug } : {})
  }

  function refreshCatalog() {
    void categoriesQuery.refetch()
    void productsQuery.refetch()
  }

  const isLoading = categoriesQuery.isLoading || productsQuery.isLoading
  const hasError = categoriesQuery.isError || productsQuery.isError

  return (
    <main className="catalog-shell">
      <header className="catalog-header">
        <div>
          <p className="eyebrow">Storefront</p>
          <h1>Catalog</h1>
        </div>
        <button
          type="button"
          className="icon-button"
          onClick={refreshCatalog}
          title="Refresh catalog"
          aria-label="Refresh catalog"
        >
          <RefreshCw aria-hidden="true" size={18} />
        </button>
      </header>

      <section className="catalog-toolbar" aria-label="Catalog filters">
        <div className="category-tabs" role="tablist" aria-label="Categories">
          <button
            type="button"
            className={!activeCategory ? 'category-tab active' : 'category-tab'}
            onClick={() => chooseCategory('')}
          >
            All
          </button>
          {categories.map((category) => (
            <button
              type="button"
              key={category.id}
              className={
                activeCategory === category.slug
                  ? 'category-tab active'
                  : 'category-tab'
              }
              onClick={() => chooseCategory(category.slug)}
            >
              {category.name}
            </button>
          ))}
        </div>
        <div className="catalog-count" aria-live="polite">
          <ShoppingBag aria-hidden="true" size={17} />
          <span>{products.length}</span>
        </div>
      </section>

      <section className="catalog-summary" aria-live="polite">
        <div>
          <h2>{activeCategoryName}</h2>
          <p>
            {products.length === 1
              ? '1 product'
              : `${products.length} products`}
          </p>
        </div>
      </section>

      {isLoading ? <CatalogLoading /> : null}
      {hasError ? <CatalogError onRetry={refreshCatalog} /> : null}
      {!isLoading && !hasError && products.length === 0 ? <EmptyCatalog /> : null}
      {!isLoading && !hasError && products.length > 0 ? (
        <ProductGrid products={products} />
      ) : null}
    </main>
  )
}

function ProductGrid({ products }: { products: Product[] }) {
  return (
    <section className="product-grid" aria-label="Products">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </section>
  )
}

function ProductCard({ product }: { product: Product }) {
  const imageUrl = resolveImageUrl(product.image)
  const hasStock = product.stock_quantity > 0

  return (
    <article className="product-card">
      <div className="product-media">
        {imageUrl ? (
          <img src={imageUrl} alt={product.name} loading="lazy" />
        ) : (
          <div className="product-media-fallback" aria-hidden="true">
            <ImageIcon size={28} />
          </div>
        )}
      </div>
      <div className="product-body">
        <div className="product-title-row">
          <h3>{product.name}</h3>
          <span className={hasStock ? 'stock-pill in-stock' : 'stock-pill'}>
            {hasStock ? product.stock_quantity : 'Out'}
          </span>
        </div>
        <p className="product-category">{product.category.name}</p>
        {product.description ? (
          <p className="product-description">{product.description}</p>
        ) : null}
        <div className="product-footer">
          <strong>{formatPrice(product.price)}</strong>
          <span>{hasStock ? 'Available' : 'Unavailable'}</span>
        </div>
      </div>
    </article>
  )
}

function CatalogLoading() {
  return (
    <section className="product-grid" aria-label="Loading products">
      {[1, 2, 3].map((item) => (
        <article className="product-card skeleton" key={item}>
          <div className="product-media" />
          <div className="product-body">
            <div className="skeleton-line wide" />
            <div className="skeleton-line" />
            <div className="skeleton-line short" />
          </div>
        </article>
      ))}
    </section>
  )
}

function CatalogError({ onRetry }: { onRetry: () => void }) {
  return (
    <section className="state-panel" role="alert">
      <AlertCircle aria-hidden="true" size={24} />
      <div>
        <h2>Catalog unavailable</h2>
        <p>Start the Django server and try again.</p>
      </div>
      <button type="button" className="text-button" onClick={onRetry}>
        <RefreshCw aria-hidden="true" size={16} />
        Retry
      </button>
    </section>
  )
}

function EmptyCatalog() {
  return (
    <section className="state-panel">
      <PackageSearch aria-hidden="true" size={24} />
      <div>
        <h2>No products</h2>
        <p>Add active products in Django admin.</p>
      </div>
    </section>
  )
}
