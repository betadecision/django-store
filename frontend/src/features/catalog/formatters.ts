const currencyFormatter = new Intl.NumberFormat('uk-UA', {
  style: 'currency',
  currency: 'UAH',
  minimumFractionDigits: 2,
})

export function formatPrice(price: string) {
  return currencyFormatter.format(Number(price))
}

export function resolveImageUrl(image: string | null) {
  if (!image) {
    return null
  }

  return image
}
