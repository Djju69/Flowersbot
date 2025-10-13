import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { formatVNDSimple, calculateItemPrice, calculateCartTotal, calculateDeliveryCost } from '../utils/format';

function Checkout({ cart, user, telegram, clearCart }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    phone: '',
    address: '',
    latitude: '',
    longitude: '',
    delivery_date: '',
    delivery_time: '',
    card_text: '',
    is_anonymous: false,
  });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    // Устанавливаем сегодняшнюю дату как минимальную
    const today = new Date().toISOString().split('T')[0];
    setFormData(prev => ({
      ...prev,
      delivery_date: today
    }));
  }, []);

  const itemsTotal = calculateCartTotal(cart);
  const deliveryCost = calculateDeliveryCost(itemsTotal);
  const total = itemsTotal + deliveryCost;

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.phone.trim()) newErrors.phone = 'Телефон обязателен';
    if (!formData.address.trim()) newErrors.address = 'Адрес обязателен';
    if (!formData.delivery_date) newErrors.delivery_date = 'Дата доставки обязательна';
    if (!formData.delivery_time) newErrors.delivery_time = 'Время доставки обязательно';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleGeolocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData(prev => ({
            ...prev,
            latitude: position.coords.latitude.toString(),
            longitude: position.coords.longitude.toString(),
          }));
          setErrors(prev => ({ ...prev, geolocation: '' }));
        },
        (error) => {
          console.error("Error getting geolocation:", error);
          setErrors(prev => ({ ...prev, geolocation: 'Не удалось получить геолокацию.' }));
        }
      );
    } else {
      setErrors(prev => ({ ...prev, geolocation: 'Геолокация не поддерживается вашим браузером.' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) {
      alert('Пожалуйста, заполните все обязательные поля.');
      return;
    }

    setSubmitting(true);
    try {
      const orderItems = cart.map(item => ({
        product_id: item.product.id,
        product_name: item.product.name,
        size: item.size,
        price: calculateItemPrice(item.product.price, item.size),
        quantity: item.quantity,
      }));

      const orderData = {
        telegram_id: user?.id || 0,
        telegram_username: user?.username,
        name: user?.first_name || 'Пользователь',
        phone: formData.phone,
        address: formData.address,
        latitude: formData.latitude,
        longitude: formData.longitude,
        delivery_date: formData.delivery_date,
        delivery_time: formData.delivery_time,
        card_text: formData.card_text,
        is_anonymous: formData.is_anonymous,
        items: orderItems,
        items_total: itemsTotal,
        delivery_cost: deliveryCost,
        total: total,
      };

      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Order created:', result);
      clearCart();
      
      // Закрываем Mini App
      if (telegram) {
        telegram.close();
      } else {
        navigate('/success');
      }
    } catch (e) {
      console.error('Error creating order:', e);
      alert(`Ошибка при оформлении заказа: ${e.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  if (cart.length === 0) {
    return (
      <div className="checkout">
        <h2>Корзина пуста</h2>
        <p>Невозможно оформить заказ без товаров в корзине.</p>
        <button onClick={() => navigate('/')} className="button primary">Перейти в каталог</button>
      </div>
    );
  }

  return (
    <div className="checkout">
      <h2>💳 Оформление заказа</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Телефон (обязательно):</label>
          <input 
            type="tel" 
            name="phone" 
            value={formData.phone} 
            onChange={handleChange} 
            placeholder="+84 XXX XXX XXX"
            className={errors.phone ? 'input-error' : ''}
          />
          {errors.phone && <p className="error-message">{errors.phone}</p>}
        </div>

        <div className="form-group">
          <label>Адрес доставки (обязательно):</label>
          <textarea 
            name="address" 
            value={formData.address} 
            onChange={handleChange} 
            rows="3"
            placeholder="Улица, дом, район, город"
            className={errors.address ? 'input-error' : ''}
          ></textarea>
          {errors.address && <p className="error-message">{errors.address}</p>}
        </div>

        <div className="form-group">
          <label>Геолокация (рекомендуется):</label>
          <button type="button" onClick={handleGeolocation} className="button secondary">
            {formData.latitude && formData.longitude ? '📍 Геолокация получена' : '📍 Получить геолокацию'}
          </button>
          {formData.latitude && formData.longitude && (
            <p className="success-message">Широта: {formData.latitude}, Долгота: {formData.longitude}</p>
          )}
          {errors.geolocation && <p className="error-message">{errors.geolocation}</p>}
        </div>

        <div className="form-group">
          <label>Дата доставки (обязательно):</label>
          <input 
            type="date" 
            name="delivery_date" 
            value={formData.delivery_date} 
            onChange={handleChange} 
            min={new Date().toISOString().split('T')[0]}
            className={errors.delivery_date ? 'input-error' : ''}
          />
          {errors.delivery_date && <p className="error-message">{errors.delivery_date}</p>}
        </div>

        <div className="form-group">
          <label>Время доставки (обязательно):</label>
          <select 
            name="delivery_time" 
            value={formData.delivery_time} 
            onChange={handleChange}
            className={errors.delivery_time ? 'input-error' : ''}
          >
            <option value="">Выберите время</option>
            <option value="09:00-12:00">09:00-12:00</option>
            <option value="12:00-15:00">12:00-15:00</option>
            <option value="15:00-18:00">15:00-18:00</option>
            <option value="18:00-21:00">18:00-21:00</option>
          </select>
          {errors.delivery_time && <p className="error-message">{errors.delivery_time}</p>}
        </div>

        <div className="form-group">
          <label>Текст для открытки (опционально):</label>
          <textarea 
            name="card_text" 
            value={formData.card_text} 
            onChange={handleChange} 
            rows="3"
            maxLength="200"
            placeholder="Поздравление, пожелание..."
          ></textarea>
        </div>

        <div className="form-group checkbox-group">
          <input 
            type="checkbox" 
            name="is_anonymous" 
            checked={formData.is_anonymous} 
            onChange={handleChange} 
            id="is_anonymous"
          />
          <label htmlFor="is_anonymous">Анонимная доставка</label>
        </div>

        <div className="order-summary">
          <h3>Ваш заказ:</h3>
          {cart.map(item => (
            <p key={`${item.product.id}-${item.size}`}>
              {item.product.name} ({item.size === 'standard' ? 'Стандарт' : item.size === 'large' ? 'Большой' : 'XL'}) x {item.quantity} - {formatVNDSimple(calculateItemPrice(item.product.price, item.size) * item.quantity)}
            </p>
          ))}
          <p>Доставка: {deliveryCost === 0 ? 'Бесплатно' : formatVNDSimple(deliveryCost)}</p>
          <h4>Итого к оплате: {formatVNDSimple(total)}</h4>
        </div>

        <button type="submit" className="button primary" disabled={submitting}>
          {submitting ? 'Оформление...' : '✅ Подтвердить и оплатить'}
        </button>
        <button type="button" onClick={() => navigate('/cart')} className="button secondary">
          ◀️ Назад в корзину
        </button>
      </form>
    </div>
  );
}

export default Checkout;
