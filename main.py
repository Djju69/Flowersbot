"""
Railway entry point for Flowers Nha Trang API
"""
import sys
import os

# Add flower_shop to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flower_shop'))

from flower_shop.backend.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)