"""
FastAPI Backend для магазина цветов "Цветы Нячанг"
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import products, orders

app = FastAPI(title="Flowers Nha Trang API", version="1.0.0")

# CORS для Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты
app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Flowers Nha Trang API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
