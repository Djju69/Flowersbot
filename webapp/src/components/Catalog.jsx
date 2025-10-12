import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import ProductCard from './ProductCard'

const Catalog = () => {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [category, setCategory] = useState('all')

  useEffect(() => {
    fetchProducts()
  }, [category])

  const fetchProducts = async () => {
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'https://your-api-url.com'
      const url = category === 'all' 
        ? `${API_URL}/api/products` 
        : `${API_URL}/api/products?category=${category}`
      
      const response = await fetch(url)
      const data = await response.json()
      setProducts(data)
    } catch (error) {
      console.error('Ошибка загрузки товаров:', error)
    } finally {
      setLoading(false)
    }
  }

  const categories = [
    { id: 'all', name: 'Все товары', icon: '🛍️' },
    { id: 'roses', name: 'Розы', icon: '🌹' },
    { id: 'exotic', name: 'Экзотика', icon: '🌺' },
    { id: 'mix', name: 'Микс', icon: '💐' },
    { id: 'mono', name: 'Моно', icon: '🤍' }
  ]

  if (loading) {
    return (
      <div className="catalog">
        <div className="loading">Загрузка товаров...</div>
      </div>
    )
  }

  return (
    <div className="catalog">
      <header className="catalog-header">
        <h1>🌸 Цветы Нячанг</h1>
        <p>Свежие букеты с доставкой за 2-3 часа</p>
      </header>

      <div className="categories">
        {categories.map(cat => (
          <button
            key={cat.id}
            className={`category-btn ${category === cat.id ? 'active' : ''}`}
            onClick={() => setCategory(cat.id)}
          >
            <span className="category-icon">{cat.icon}</span>
            <span className="category-name">{cat.name}</span>
          </button>
        ))}
      </div>

      <div className="products-grid">
        {products.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>

      {products.length === 0 && (
        <div className="no-products">
          <p>Товары не найдены</p>
        </div>
      )}
    </div>
  )
}

export default Catalog
