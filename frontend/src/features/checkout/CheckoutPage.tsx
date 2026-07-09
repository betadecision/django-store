import { useMutation } from '@tanstack/react-query'
import { AlertCircle, ArrowLeft, CheckCircle2 } from 'lucide-react'
import { type FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { useCart } from '../cart/useCart'
import { formatPrice } from '../catalog/formatters'
import { createOrder } from './api'

export function CheckoutPage() {
  const { clearCart, itemCount, items, totalAmount } = useCart()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [fullName, setFullName] = useState('')
  const [phone, setPhone] = useState('')

  const orderMutation = useMutation({
    mutationFn: createOrder,
    onSuccess: (order) => {
      clearCart()
      navigate(
        `/checkout/success?order=${order.id}&total=${encodeURIComponent(
          order.total_amount,
        )}`,
      )
    },
  })

  function submitOrder(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (items.length === 0) {
      return
    }

    orderMutation.mutate({
      email,
      full_name: fullName,
      phone,
      items: items.map((item) => ({
        product: item.productId,
        quantity: item.quantity,
      })),
    })
  }

  return (
    <main className="catalog-shell">
      <header className="catalog-header">
        <div>
          <p className="eyebrow">Checkout</p>
          <h1>Guest checkout</h1>
        </div>
        <Link className="icon-button" to="/cart" title="Back to cart" aria-label="Back to cart">
          <ArrowLeft aria-hidden="true" size={18} />
        </Link>
      </header>

      {items.length === 0 ? (
        <section className="state-panel">
          <AlertCircle aria-hidden="true" size={24} />
          <div>
            <h2>Your cart is empty</h2>
            <p>Add products before checkout.</p>
          </div>
          <Link className="text-button" to="/">
            Catalog
          </Link>
        </section>
      ) : (
        <section className="checkout-layout">
          <form className="checkout-form" onSubmit={submitOrder}>
            <label>
              Email
              <input
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
                autoComplete="email"
              />
            </label>
            <label>
              Full name
              <input
                type="text"
                value={fullName}
                onChange={(event) => setFullName(event.target.value)}
                required
                maxLength={100}
                autoComplete="name"
              />
            </label>
            <label>
              Phone
              <input
                type="tel"
                value={phone}
                onChange={(event) => setPhone(event.target.value)}
                required
                maxLength={40}
                autoComplete="tel"
              />
            </label>

            {orderMutation.isError ? (
              <div className="form-error" role="alert">
                <AlertCircle aria-hidden="true" size={18} />
                Order was not created. Check the fields and try again.
              </div>
            ) : null}

            <button
              type="submit"
              className="primary-button"
              disabled={orderMutation.isPending}
            >
              <CheckCircle2 aria-hidden="true" size={18} />
              {orderMutation.isPending ? 'Creating order' : 'Create order'}
            </button>
          </form>

          <aside className="cart-summary-panel" aria-label="Checkout summary">
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
          </aside>
        </section>
      )}
    </main>
  )
}
