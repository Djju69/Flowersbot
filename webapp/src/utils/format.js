// Утилиты для форматирования
export const formatVND = (amount) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount)
}

export const formatVNDSimple = (amount) => {
  return amount.toLocaleString('vi-VN') + ' VND'
}

export const calculateItemPrice = (basePrice, size) => {
  const multipliers = {
    'standard': 1.0,
    'large': 1.3,
    'xl': 1.5
  }
  return Math.round(basePrice * multipliers[size])
}

export const calculateCartTotal = (cart) => {
  return cart.reduce((sum, item) => 
    sum + calculateItemPrice(item.product.price, item.size) * item.quantity, 0
  )
}

export const calculateDeliveryCost = (itemsTotal) => {
  return itemsTotal >= 3000000 ? 0 : 100000 // Бесплатно от 3,000,000 VND
}

export const getSizeLabel = (size) => {
  const labels = {
    'standard': 'Стандарт',
    'large': 'Большой (+30%)',
    'xl': 'XL (+50%)'
  }
  return labels[size] || size
}
