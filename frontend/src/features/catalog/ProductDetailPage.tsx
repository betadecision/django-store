import { useQuery } from '@tanstack/react-query'
import {
  AlertCircle,
  ArrowLeft,
  ImageIcon,
  RefreshCw,
  ShoppingCart,
} from 'lucide-react'
import { Link, useParams } from 'react-router-dom'

import { CartLink } from '../cart/CartLink'
import { useCart } from '../cart/useCart'
import { getProduct } from './api'
import { formatPrice, resolveImageUrl } from './formatters'

export function ProductDetailPage() {
  const { slug } = useParams()
  const { addProduct } = useCart()

  const productQuery = useQuery({
    queryKey: ['product', slug],
    queryFn: () => getProduct(slug ?? ''),
    enabled: Boolean(slug),
  })

  const product = productQuery.data

  return (
    <main className="catalog-shell">
      <header className="catalog-header">
        <div>
          <p className="eyebrow">Product</p>
          <h1>{product?.name ?? 'Product details'}</h1>
        </div>
        <div className="header-actions">
          <CartLink />
          <Link
            className="icon-button"
            to="/"
            title="Back to catalog"
            aria-label="Back to catalog"
          >
            <ArrowLeft aria-hidden="true" size={18} />
          </Link>
        </div>
      </header>

      {productQuery.isLoading ? <ProductDetailLoading /> : null}
      {productQuery.isError || !slug ? (
        <ProductDetailError onRetry={() => void productQuery.refetch()} />
      ) : null}
      {product ? (
        <section className="product-detail" aria-label={product.name}>
          <div className="detail-media">
            {resolveImageUrl(product.image) ? (
              <img src={resolveImageUrl(product.image) ?? ''} alt={product.name} />
            ) : (
              <div className="product-media-fallback" aria-hidden="true">
                <ImageIcon size={34} />
              </div>
            )}
          </div>
          <div className="detail-panel">
            <div>
              <p className="product-category">{product.category.name}</p>
              <h2>{product.name}</h2>
            </div>

            {product.description ? (
              <p className="detail-description">{product.description}</p>
            ) : null}

            <dl className="detail-meta">
              <div>
                <dt>Price</dt>
                <dd>{formatPrice(product.price)}</dd>
              </div>
              <div>
                <dt>Stock</dt>
                <dd>{product.stock_quantity}</dd>
              </div>
              <div>
                <dt>Status</dt>
                <dd>{product.stock_quantity > 0 ? 'Available' : 'Unavailable'}</dd>
              </div>
            </dl>

            <button
              type="button"
              className="primary-button"
              onClick={() => addProduct(product)}
              disabled={product.stock_quantity <= 0}
            >
              <ShoppingCart aria-hidden="true" size={18} />
              Add to cart
            </button>
          </div>
        </section>
      ) : null}
    </main>
  )
}

function ProductDetailLoading() {
  return (
    <section className="product-detail skeleton" aria-label="Loading product">
      <div className="detail-media" />
      <div className="detail-panel">
        <div className="skeleton-line short" />
        <div className="skeleton-line wide" />
        <div className="skeleton-line" />
      </div>
    </section>
  )
}

function ProductDetailError({ onRetry }: { onRetry: () => void }) {
  return (
    <section className="state-panel" role="alert">
      <AlertCircle aria-hidden="true" size={24} />
      <div>
        <h2>Product unavailable</h2>
        <p>Check the product link and try again.</p>
      </div>
      <button type="button" className="text-button" onClick={onRetry}>
        <RefreshCw aria-hidden="true" size={16} />
        Retry
      </button>
    </section>
  )
}
