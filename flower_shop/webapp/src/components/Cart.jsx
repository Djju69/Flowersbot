import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { formatVNDSimple, calculateItemPrice, calculateCartTotal, calculateDeliveryCost } from '../utils/format';

function Cart({ cart, removeFromCart, updateQuantity, clearCart }) {
  const navigate = useNavigate();

  const itemsTotal = calculateCartTotal(cart);
  const deliveryCost = calculateDeliveryCost(itemsTotal);
  const total = itemsTotal + deliveryCost;
  const bonuses = Math.round(total * 0.10); // 10% бонусов

  if (cart.length === 0) {
    return (
      <div className="cart">
        <h2>🛒 Корзина пуста</h2>
        <p>Выберите букеты в каталоге!</p>
        <Link to="/" className="button primary">💐 Перейти в каталог</Link>
      </div>
    );
  }

  return (
    <div className="cart">
      <h2>🛒 Ваша корзина ({cart.length} товара)</h2>
      
      <div className="cart-items">
        {cart.map(item => (
          <div key={`${item.product.id}-${item.size}`} className="cart-item">
            <img src={item.product.photo_url} alt={item.product.name} className="cart-item-image" />
            <div className="cart-item-details">
              <h3>{item.product.name}</h3>
              <p>Размер: {item.size === 'standard' ? 'Стандарт' : item.size === 'large' ? 'Большой' : 'XL'}</p>
              <p>Цена: {formatVNDSimple(calculateItemPrice(item.product.price, item.size))}</p>
              <div className="quantity-control">
                <button onClick={() => updateQuantity(item.product.id, item.size, item.quantity - 1)}>-</button>
                <span>{item.quantity}</span>
                <button onClick={() => updateQuantity(item.product.id, item.size, item.quantity + 1)}>+</button>
              </div>
              <button onClick={() => removeFromCart(item.product.id, item.size)} className="remove-button">
                ❌ Удалить
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="cart-summary">
        <div className="summary-line">
          <span>💰 Итого за товары:</span>
          <span>{formatVNDSimple(itemsTotal)}</span>
        </div>
        <div className="summary-line">
          <span>🚚 Доставка:</span>
          <span>{deliveryCost === 0 ? 'Бесплатно' : formatVNDSimple(deliveryCost)}</span>
        </div>
        <div className="summary-line total">
          <span>Общая сумма:</span>
          <span>{formatVNDSimple(total)}</span>
        </div>
        <p className="bonuses">✅ Получите {formatVNDSimple(bonuses)} бонусов на следующий заказ!</p>
      </div>

      <div className="cart-actions">
        <Link to="/" className="button secondary">➕ Добавить ещё букет</Link>
        <button onClick={() => navigate('/checkout')} className="button primary">
          💳 Оформить заказ
        </button>
        <button onClick={clearCart} className="button danger">🗑 Очистить корзину</button>
      </div>
    </div>
  );
}

export default Cart;
