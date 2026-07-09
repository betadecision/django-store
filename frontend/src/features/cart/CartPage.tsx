import { ArrowLeft, ImageIcon, Minus, Plus, Trash2 } from 'lucide-react'
import { Link } from 'react-router-dom'

import { formatPrice, resolveImageUrl } from '../catalog/formatters'
import { useCart } from './useCart'
import type { CartItem } from './types'

export function CartPage() {
  const { clearCart, itemCount, items, removeItem, totalAmount, updateQuantity } =
    useCart()

  return (
    <main className="catalog-shell">
      <header className="catalog-header">
        <div>
          <p className="eyebrow">Cart</p>
          <h1>Shopping cart</h1>
        </div>
        <Link className="icon-button" to="/" title="Back to catalog" aria-label="Back to catalog">
          <ArrowLeft aria-hidden="true" size={18} />
        </Link>
      </header>

      {items.length === 0 ? (
        <section className="state-panel">
          <ImageIcon aria-hidden="true" size={24} />
          <div>
            <h2>Your cart is empty</h2>
            <p>Choose products from the catalog.</p>
          </div>
          <Link className="text-button" to="/">
            Catalog
          </Link>
        </section>
      ) : (
        <section className="cart-layout">
          <div className="cart-items" aria-label="Cart items">
            {items.map((item) => (
              <CartRow
                item={item}
                key={item.productId}
                onRemove={() => removeItem(item.productId)}
                onUpdateQuantity={(quantity) =>
                  updateQuantity(item.productId, quantity)
                }
              />
            ))}
          </div>

          <aside className="cart-summary-panel" aria-label="Cart summary">
            <h2>Summary</h2>
            <dl className="detail-meta">
              <div>
                <dt>Items</dt>
                <dd>{itemCount}</dd>
              </div>
              <div>
                <dt>Total</dt>
                <dd>{formatPrice(totalAmount.toFixed(2))}</dd>
              </div>
            </dl>
            <button type="button" className="text-button danger" onClick={clearCart}>
              <Trash2 aria-hidden="true" size={16} />
              Clear cart
            </button>
            <Link className="primary-button" to="/checkout">
              Checkout
            </Link>
          </aside>
        </section>
      )}
    </main>
  )
}

type CartRowProps = {
  item: CartItem
  onRemove: () => void
  onUpdateQuantity: (quantity: number) => void
}

function CartRow({ item, onRemove, onUpdateQuantity }: CartRowProps) {
  const imageUrl = resolveImageUrl(item.image)

  return (
    <article className="cart-item">
      <Link className="cart-item-media" to={`/products/${item.slug}`}>
        {imageUrl ? (
          <img src={imageUrl} alt={item.name} />
        ) : (
          <div className="product-media-fallback" aria-hidden="true">
            <ImageIcon size={24} />
          </div>
        )}
      </Link>

      <div className="cart-item-body">
        <div>
          <Link className="cart-item-title" to={`/products/${item.slug}`}>
            {item.name}
          </Link>
          <p className="product-category">{item.categoryName}</p>
        </div>
        <strong>{formatPrice(item.price)}</strong>
      </div>

      <div className="quantity-control" aria-label={`${item.name} quantity`}>
        <button
          type="button"
          className="icon-button compact"
          onClick={() => onUpdateQuantity(item.quantity - 1)}
          title="Decrease quantity"
          aria-label="Decrease quantity"
        >
          <Minus aria-hidden="true" size={16} />
        </button>
        <span>{item.quantity}</span>
        <button
          type="button"
          className="icon-button compact"
          onClick={() => onUpdateQuantity(item.quantity + 1)}
          title="Increase quantity"
          aria-label="Increase quantity"
        >
          <Plus aria-hidden="true" size={16} />
        </button>
      </div>

      <button
        type="button"
        className="icon-button compact danger"
        onClick={onRemove}
        title="Remove item"
        aria-label="Remove item"
      >
        <Trash2 aria-hidden="true" size={16} />
      </button>
    </article>
  )
}
