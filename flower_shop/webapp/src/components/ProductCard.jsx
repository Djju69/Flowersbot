import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { formatVNDSimple, calculateItemPrice, getSizeLabel } from '../utils/format';

function ProductCard({ addToCart }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedSize, setSelectedSize] = useState('standard');

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/api/products/${id}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setProduct(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleAddToCart = () => {
    if (product) {
      addToCart(product, selectedSize);
      navigate('/cart');
    }
  };

  if (loading) return <div className="loading">Загрузка товара...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;
  if (!product) return <div className="error">Товар не найден.</div>;

  const currentPrice = calculateItemPrice(product.price, selectedSize);

  return (
    <div className="product-detail">
      <button onClick={() => navigate(-1)} className="back-button">
        ◀️ Назад
      </button>
      
      <div className="product-image">
        <img src={product.photo_url} alt={product.name} />
      </div>
      
      <div className="product-content">
        <h2>{product.name}</h2>
        <p className="description">{product.description}</p>
        
        <div className="size-selection">
          <h3>Выберите размер:</h3>
          <div className="size-options">
            <label className={selectedSize === 'standard' ? 'selected' : ''}>
              <input 
                type="radio" 
                value="standard" 
                checked={selectedSize === 'standard'} 
                onChange={() => setSelectedSize('standard')} 
              />
              <span>{getSizeLabel('standard')}</span>
              <span className="price">{formatVNDSimple(calculateItemPrice(product.price, 'standard'))}</span>
            </label>
            
            <label className={selectedSize === 'large' ? 'selected' : ''}>
              <input 
                type="radio" 
                value="large" 
                checked={selectedSize === 'large'} 
                onChange={() => setSelectedSize('large')} 
              />
              <span>{getSizeLabel('large')}</span>
              <span className="price">{formatVNDSimple(calculateItemPrice(product.price, 'large'))}</span>
            </label>
            
            <label className={selectedSize === 'xl' ? 'selected' : ''}>
              <input 
                type="radio" 
                value="xl" 
                checked={selectedSize === 'xl'} 
                onChange={() => setSelectedSize('xl')} 
              />
              <span>{getSizeLabel('xl')}</span>
              <span className="price">{formatVNDSimple(calculateItemPrice(product.price, 'xl'))}</span>
            </label>
          </div>
        </div>

        <div className="product-actions">
          <button onClick={handleAddToCart} className="button primary">
            🛒 В корзину - {formatVNDSimple(currentPrice)}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ProductCard;
