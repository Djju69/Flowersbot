import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { formatVNDSimple } from '../utils/format';

function Catalog() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/api/products`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setProducts(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const filteredProducts = filter === 'all' 
    ? products 
    : products.filter(p => p.category === filter);

  if (loading) return <div className="loading">Загрузка товаров...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;

  return (
    <div className="catalog">
      <header className="catalog-header">
        <h1>🌸 Цветы Нячанг</h1>
        <p>Свежие букеты с доставкой за 1-2 часа</p>
      </header>

      <div className="filter-buttons">
        <button 
          className={filter === 'all' ? 'active' : ''} 
          onClick={() => setFilter('all')}
        >
          Все
        </button>
        <button 
          className={filter === 'roses' ? 'active' : ''} 
          onClick={() => setFilter('roses')}
        >
          🌹 Розы
        </button>
        <button 
          className={filter === 'exotic' ? 'active' : ''} 
          onClick={() => setFilter('exotic')}
        >
          🌺 Экзотика
        </button>
        <button 
          className={filter === 'mix' ? 'active' : ''} 
          onClick={() => setFilter('mix')}
        >
          💐 Микс
        </button>
        <button 
          className={filter === 'mono' ? 'active' : ''} 
          onClick={() => setFilter('mono')}
        >
          🤍 Моно
        </button>
      </div>

      <div className="product-list">
        {filteredProducts.length > 0 ? (
          filteredProducts.map(product => (
            <div key={product.id} className="product-card">
              <img src={product.photo_url} alt={product.name} />
              <div className="product-info">
                <h3>{product.name}</h3>
                <p className="description">{product.description}</p>
                <div className="product-footer">
                  <p className="price">{formatVNDSimple(product.price)}</p>
                  <Link to={`/product/${product.id}`} className="button">
                    Подробнее
                  </Link>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p>Товары не найдены.</p>
        )}
      </div>
    </div>
  );
}

export default Catalog;
