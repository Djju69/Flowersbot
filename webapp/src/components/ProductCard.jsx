import React from 'react'
import { Link } from 'react-router-dom'

const ProductCard = ({ product, addToCart }) => {
  const formatPrice = (price) => {
    return `${price.toLocaleString('vi-VN')} ₫`
  }

  const handleAddToCart = () => {
    if (addToCart) {
      addToCart(product, 'standard')
    }
  }

  return (
    <div className="product-card">
      <div className="product-image">
        <img src={product.photo_url} alt={product.name} />
        {product.is_popular && <span className="popular-badge">🔥 Популярное</span>}
        {product.is_express && <span className="express-badge">⚡ Экспресс</span>}
      </div>
      
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <p className="product-description">{product.description}</p>
        
        <div className="product-price">
          <span className="price">{formatPrice(product.price)}</span>
        </div>
        
        <div className="product-actions">
          <button 
            className="add-to-cart-btn"
            onClick={handleAddToCart}
          >
            🛒 В корзину
          </button>
          <Link 
            to={`/product/${product.id}`}
            className="view-details-btn"
          >
            Подробнее
          </Link>
        </div>
      </div>
    </div>
  )
}

export default ProductCard
