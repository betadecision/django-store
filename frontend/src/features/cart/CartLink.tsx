import { ShoppingCart } from 'lucide-react'
import { Link } from 'react-router-dom'

import { useCart } from './useCart'

export function CartLink() {
  const { itemCount } = useCart()

  return (
    <Link className="cart-link" to="/cart" aria-label={`Cart with ${itemCount} items`}>
      <ShoppingCart aria-hidden="true" size={18} />
      <span>{itemCount}</span>
    </Link>
  )
}
