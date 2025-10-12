import React from 'react'
import { Link } from 'react-router-dom'

const OrderSuccess = () => {
  return (
    <div className="order-success">
      <div className="success-content">
        <div className="success-icon">✅</div>
        <h2>Заказ успешно оформлен!</h2>
        <p>Спасибо за покупку! Мы свяжемся с вами для подтверждения заказа.</p>
        
        <div className="success-info">
          <p>📸 Вы получите фото букета перед отправкой</p>
          <p>🚚 Доставка за 2-3 часа</p>
          <p>💬 Следите за обновлениями в Telegram</p>
        </div>

        <div className="success-actions">
          <Link to="/" className="continue-shopping-btn">
            🛍️ Продолжить покупки
          </Link>
        </div>
      </div>
    </div>
  )
}

export default OrderSuccess
