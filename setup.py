from setuptools import setup, find_packages

setup(
    name="flower-shop",
    version="1.0.0",
    description="Telegram Mini App + Bot для магазина цветов в Нячанге",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "sqlalchemy==2.0.23",
        "psycopg2-binary==2.9.9",
        "pydantic==2.5.0",
        "python-dotenv==1.0.0",
        "aiohttp==3.9.1",
        "aiogram==3.3.0",
    ],
)
