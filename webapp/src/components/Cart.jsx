import React from 'react'
import { Link } from 'react-router-dom'

const Cart = ({ cart, removeFromCart, updateQuantity, clearCart }) => {
  const formatPrice = (price) => {
    return `${price.toLocaleString('vi-VN')} ₫`
  }

  const calculateTotal = () => {
    return cart.reduce((total, item) => {
      const itemTotal = item.product.price * item.quantity
      return total + itemTotal
    }, 0)
  }

  const calculateDelivery = () => {
    const total = calculateTotal()
    return total >= 1000000 ? 0 : 100000 // Бесплатная доставка от 1,000,000 VND
  }

  const getTotalWithDelivery = () => {
    return calculateTotal() + calculateDelivery()
  }

  if (cart.length === 0) {
    return (
      <div className="cart">
        <div className="empty-cart">
          <h2>🛒 Корзина пуста</h2>
          <p>Выберите букеты в каталоге!</p>
          <Link to="/" className="go-to-catalog-btn">
            💐 Перейти в каталог
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="cart">
      <header className="cart-header">
        <h2>🛒 Ваша корзина ({cart.length} товаров)</h2>
        <button onClick={clearCart} className="clear-cart-btn">
          🗑 Очистить
        </button>
      </header>

      <div className="cart-items">
        {cart.map((item, index) => (
          <div key={`${item.product.id}-${item.size}`} className="cart-item">
            <div className="item-image">
              <img src={item.product.photo_url} alt={item.product.name} />
            </div>
            
            <div className="item-info">
              <h3 className="item-name">{item.product.name}</h3>
              <p className="item-size">Размер: {item.size}</p>
              <p className="item-price">{formatPrice(item.product.price)}</p>
            </div>
            
            <div className="item-controls">
              <div className="quantity-controls">
                <button 
                  onClick={() => updateQuantity(item.product.id, item.size, item.quantity - 1)}
                  className="quantity-btn"
                >
                  -
                </button>
                <span className="quantity">{item.quantity}</span>
                <button 
                  onClick={() => updateQuantity(item.product.id, item.size, item.quantity + 1)}
                  className="quantity-btn"
                >
                  +
                </button>
              </div>
              
              <button 
                onClick={() => removeFromCart(item.product.id, item.size)}
                className="remove-btn"
              >
                ❌
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="cart-summary">
        <div className="summary-row">
          <span>Товары:</span>
          <span>{formatPrice(calculateTotal())}</span>
        </div>
        <div className="summary-row">
          <span>Доставка:</span>
          <span>{calculateDelivery() === 0 ? 'Бесплатно' : formatPrice(calculateDelivery())}</span>
        </div>
        <div className="summary-row total">
          <span>Итого:</span>
          <span>{formatPrice(getTotalWithDelivery())}</span>
        </div>
      </div>

      <div className="cart-actions">
        <Link to="/" className="continue-shopping-btn">
          ➕ Добавить ещё букет
        </Link>
        <Link to="/checkout" className="checkout-btn">
          💳 Оформить заказ
        </Link>
      </div>
    </div>
  )
}

export default Cart
