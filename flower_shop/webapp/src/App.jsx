import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Catalog from './components/Catalog'
import ProductCard from './components/ProductCard'
import Cart from './components/Cart'
import Checkout from './components/Checkout'
import OrderSuccess from './components/OrderSuccess'
import './App.css'

function App() {
  const [cart, setCart] = useState([])
  const [user, setUser] = useState(null)
  const [telegram, setTelegram] = useState(null)

  useEffect(() => {
    // Получаем данные пользователя из Telegram
    const tg = window.Telegram?.WebApp;
    if (tg) {
      tg.ready()
      tg.expand()
      setTelegram(tg)
      setUser({
        id: tg.initDataUnsafe?.user?.id,
        username: tg.initDataUnsafe?.user?.username,
        first_name: tg.initDataUnsafe?.user?.first_name,
        last_name: tg.initDataUnsafe?.user?.last_name
      })
    }
  }, [])

  const addToCart = (product, size = 'standard') => {
    const existingItem = cart.find(item => 
      item.product.id === product.id && item.size === size
    )
    
    if (existingItem) {
      setCart(cart.map(item =>
        item.product.id === product.id && item.size === size
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ))
    } else {
      setCart([...cart, { product, size, quantity: 1 }])
    }
  }

  const removeFromCart = (productId, size) => {
    setCart(cart.filter(item => 
      !(item.product.id === productId && item.size === size)
    ))
  }

  const updateQuantity = (productId, size, quantity) => {
    if (quantity <= 0) {
      removeFromCart(productId, size)
      return
    }
    
    setCart(cart.map(item =>
      item.product.id === productId && item.size === size
        ? { ...item, quantity }
        : item
    ))
  }

  const clearCart = () => {
    setCart([])
  }

  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<Catalog />} />
          <Route path="/product/:id" element={<ProductCard addToCart={addToCart} />} />
          <Route 
            path="/cart" 
            element={
              <Cart 
                cart={cart} 
                removeFromCart={removeFromCart}
                updateQuantity={updateQuantity}
                clearCart={clearCart}
              />
            } 
          />
          <Route 
            path="/checkout" 
            element={
              <Checkout 
                cart={cart} 
                user={user}
                telegram={telegram}
                clearCart={clearCart}
              />
            } 
          />
          <Route path="/success" element={<OrderSuccess />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
