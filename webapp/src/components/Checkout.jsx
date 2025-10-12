import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const Checkout = ({ cart, user, clearCart }) => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    recipient_name: '',
    contact_type: 'telegram',
    contact_value: '',
    latitude: '',
    longitude: '',
    address_text: '',
    delivery_date: '',
    delivery_time: '',
    card_text: '',
    is_anonymous: false
  })

  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Автоматически заполняем контакт из Telegram
    if (user?.username) {
      setFormData(prev => ({
        ...prev,
        contact_value: `@${user.username}`
      }))
    }
  }, [user])

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
    return total >= 1000000 ? 0 : 100000
  }

  const getTotalWithDelivery = () => {
    return calculateTotal() + calculateDelivery()
  }

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleLocationClick = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData(prev => ({
            ...prev,
            latitude: position.coords.latitude.toString(),
            longitude: position.coords.longitude.toString()
          }))
        },
        (error) => {
          alert('Не удалось получить геолокацию')
        }
      )
    } else {
      alert('Геолокация не поддерживается')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const API_URL = import.meta.env.VITE_API_URL || 'https://your-api-url.com'
      
      const orderData = {
        telegram_id: user?.id || 0,
        telegram_username: user?.username || '',
        name: `${user?.first_name || ''} ${user?.last_name || ''}`.trim(),
        recipient_name: formData.recipient_name,
        contact_type: formData.contact_type,
        contact_value: formData.contact_value,
        latitude: formData.latitude,
        longitude: formData.longitude,
        address_text: formData.address_text,
        delivery_date: formData.delivery_date,
        delivery_time: formData.delivery_time,
        card_text: formData.card_text,
        is_anonymous: formData.is_anonymous,
        items: cart.map(item => ({
          product_id: item.product.id,
          product_name: item.product.name,
          product_photo: item.product.photo_url,
          size: item.size,
          price: item.product.price,
          quantity: item.quantity
        })),
        items_total: calculateTotal(),
        delivery_cost: calculateDelivery(),
        total: getTotalWithDelivery()
      }

      const response = await fetch(`${API_URL}/api/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData)
      })

      if (response.ok) {
        clearCart()
        navigate('/success')
      } else {
        throw new Error('Ошибка создания заказа')
      }
    } catch (error) {
      console.error('Ошибка:', error)
      alert('Ошибка создания заказа')
    } finally {
      setLoading(false)
    }
  }

  if (cart.length === 0) {
    return (
      <div className="checkout">
        <div className="empty-cart">
          <h2>Корзина пуста</h2>
          <p>Добавьте товары в корзину</p>
        </div>
      </div>
    )
  }

  return (
    <div className="checkout">
      <header className="checkout-header">
        <h2>💳 Оформление заказа</h2>
      </header>

      <form onSubmit={handleSubmit} className="checkout-form">
        {/* Получатель */}
        <div className="form-group">
          <label htmlFor="recipient_name">🎁 Имя получателя *</label>
          <input
            type="text"
            id="recipient_name"
            name="recipient_name"
            value={formData.recipient_name}
            onChange={handleInputChange}
            required
            placeholder="Кто будет принимать цветы"
          />
        </div>

        {/* Контакт для связи */}
        <div className="form-group">
          <label htmlFor="contact_type">📱 Контакт для связи *</label>
          <select
            id="contact_type"
            name="contact_type"
            value={formData.contact_type}
            onChange={handleInputChange}
            required
          >
            <option value="telegram">📱 Telegram</option>
            <option value="whatsapp">💬 WhatsApp</option>
            <option value="zalo">💙 Zalo</option>
          </select>
          
          <input
            type="text"
            name="contact_value"
            value={formData.contact_value}
            onChange={handleInputChange}
            required
            placeholder="@username или номер телефона"
          />
        </div>

        {/* Геолокация */}
        <div className="form-group">
          <label>📍 Геолокация *</label>
          <button
            type="button"
            onClick={handleLocationClick}
            className="location-btn"
          >
            📍 Получить мою геолокацию
          </button>
          {formData.latitude && (
            <p className="location-info">
              ✅ Координаты получены: {formData.latitude}, {formData.longitude}
            </p>
          )}
          
          <input
            type="text"
            name="address_text"
            value={formData.address_text}
            onChange={handleInputChange}
            placeholder="Дополнительное описание адреса (опционально)"
          />
        </div>

        {/* Дата и время */}
        <div className="form-group">
          <label htmlFor="delivery_date">📅 Дата доставки *</label>
          <input
            type="date"
            id="delivery_date"
            name="delivery_date"
            value={formData.delivery_date}
            onChange={handleInputChange}
            required
            min={new Date().toISOString().split('T')[0]}
          />
        </div>

        <div className="form-group">
          <label htmlFor="delivery_time">⏰ Время доставки *</label>
          <select
            id="delivery_time"
            name="delivery_time"
            value={formData.delivery_time}
            onChange={handleInputChange}
            required
          >
            <option value="">Выберите время</option>
            <option value="09:00-12:00">09:00-12:00</option>
            <option value="12:00-15:00">12:00-15:00</option>
            <option value="15:00-18:00">15:00-18:00</option>
            <option value="18:00-21:00">18:00-21:00</option>
          </select>
        </div>

        {/* Открытка */}
        <div className="form-group">
          <label htmlFor="card_text">💌 Открытка</label>
          <textarea
            id="card_text"
            name="card_text"
            value={formData.card_text}
            onChange={handleInputChange}
            placeholder="Текст поздравления (опционально)"
            maxLength={200}
          />
        </div>

        {/* Анонимность */}
        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              name="is_anonymous"
              checked={formData.is_anonymous}
              onChange={handleInputChange}
            />
            🎭 Анонимная доставка (курьер не скажет от кого)
          </label>
        </div>

        {/* Итого */}
        <div className="order-summary">
          <h3>💰 Итого к оплате</h3>
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

        <button
          type="submit"
          disabled={loading || !formData.latitude || !formData.longitude}
          className="submit-btn"
        >
          {loading ? 'Обработка...' : '💳 Оформить заказ'}
        </button>
      </form>
    </div>
  )
}

export default Checkout
