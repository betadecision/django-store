import { fetchJson } from '../../shared/api/client'

export type CreateOrderPayload = {
  email: string
  full_name: string
  phone: string
  items: Array<{
    product: number
    quantity: number
  }>
}

export type CreateOrderResponse = {
  id: number
  email: string
  full_name: string
  phone: string
  status: string
  total_amount: string
}

export function createOrder(payload: CreateOrderPayload) {
  return fetchJson<CreateOrderResponse>('/api/orders/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
}
