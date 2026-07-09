import { CheckCircle2 } from 'lucide-react'
import { Link, useSearchParams } from 'react-router-dom'

import { formatPrice } from '../catalog/formatters'

export function CheckoutSuccessPage() {
  const [searchParams] = useSearchParams()
  const orderId = searchParams.get('order')
  const totalAmount = searchParams.get('total')

  return (
    <main className="catalog-shell">
      <section className="success-panel">
        <CheckCircle2 aria-hidden="true" size={42} />
        <div>
          <p className="eyebrow">Order created</p>
          <h1>{orderId ? `Order #${orderId}` : 'Order submitted'}</h1>
          {totalAmount ? <p>{formatPrice(totalAmount)}</p> : null}
        </div>
        <Link className="text-button" to="/">
          Catalog
        </Link>
      </section>
    </main>
  )
}
