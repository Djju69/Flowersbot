import React from 'react';
import { useNavigate } from 'react-router-dom';

function OrderSuccess() {
  const navigate = useNavigate();

  return (
    <div className="order-success">
      <h2>🎉 Заказ успешно оформлен!</h2>
      <p>Спасибо за ваш заказ. Мы свяжемся с вами в ближайшее время для подтверждения деталей.</p>
      <button onClick={() => navigate('/')} className="button primary">
        Продолжить покупки
      </button>
    </div>
  );
}

export default OrderSuccess;
