from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
import os

from ..models.database import Product, get_db


router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="flower_shop/backend/templates")


def get_admin_password() -> str:
    return os.getenv("ADMIN_PASSWORD", "")


def require_login(request: Request) -> None:
    if not request.session.get("is_admin_authenticated"):
        raise HTTPException(status_code=403)


@router.get("/login")
async def admin_login_page(request: Request):
    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request, "error": None},
    )


@router.post("/login")
async def admin_login_submit(request: Request, password: str = Form(...)):
    if not get_admin_password() or password != get_admin_password():
        return templates.TemplateResponse(
            "admin/login.html",
            {"request": request, "error": "Неверный пароль"},
            status_code=401,
        )
    request.session["is_admin_authenticated"] = True
    return RedirectResponse(url="/admin/products", status_code=303)


@router.get("/logout")
async def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/admin/login", status_code=303)


@router.get("/products")
async def products_list(
    request: Request,
    db: AsyncSession = Depends(get_db),
    category: Optional[str] = None,
    popular: Optional[bool] = None,
    available: Optional[bool] = None,
    q: Optional[str] = None,
    sort: str = "created_at",
    order: str = "desc",
    page: int = 1,
    per_page: int = 20,
):
    require_login(request)

    query = select(Product)
    if category:
        query = query.where(Product.category == category)
    if popular is not None:
        query = query.where(Product.is_popular == popular)
    if available is not None:
        query = query.where(Product.is_available == available)
    if q:
        # простейший поиск по вхождению имени/описания (ILIKE недоступен без конкретного диалекта)
        # здесь оставляем фильтрацию на уровне Python после выборки, чтобы не плодить завязки на диалект
        pass

    # сортировка
    sort_field = {
        "name": Product.name,
        "price": Product.price,
        "created_at": Product.created_at,
    }.get(sort, Product.created_at)
    if order == "asc":
        query = query.order_by(sort_field)
    else:
        query = query.order_by(desc(sort_field))

    result = await db.execute(query)
    rows = result.scalars().all()

    if q:
        q_lower = q.lower()
        rows = [
            p for p in rows
            if (p.name and q_lower in p.name.lower())
            or (p.description and q_lower in p.description.lower())
        ]

    total = len(rows)
    start = (page - 1) * per_page
    end = start + per_page
    items = rows[start:end]

    return templates.TemplateResponse(
        "admin/products_list.html",
        {
            "request": request,
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "category": category,
            "popular": popular,
            "available": available,
            "q": q or "",
            "sort": sort,
            "order": order,
        },
    )


@router.get("/products/new")
async def product_new_page(request: Request):
    require_login(request)
    return templates.TemplateResponse(
        "admin/product_form.html",
        {"request": request, "product": None, "error": None},
    )


@router.post("/products")
async def product_create(
    request: Request,
    db: AsyncSession = Depends(get_db),
    name: str = Form(...),
    category: str = Form(...),
    description: str = Form(""),
    price: int = Form(...),
    photo_url: str = Form(""),
    is_popular: Optional[bool] = Form(False),
    is_available: Optional[bool] = Form(True),
):
    require_login(request)

    # Валидации из дополнения к ТЗ
    if not (100_000 <= int(price) <= 10_000_000):
        return templates.TemplateResponse(
            "admin/product_form.html",
            {"request": request, "product": None, "error": "Цена вне диапазона (100k–10M VND)"},
            status_code=400,
        )
    if photo_url:
        ok = photo_url.startswith("https://") and any(photo_url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"])
        if not ok:
            return templates.TemplateResponse(
                "admin/product_form.html",
                {"request": request, "product": None, "error": "Некорректный URL изображения"},
                status_code=400,
            )

    product = Product(
        name=name,
        category=category,
        description=description,
        price=int(price),
        photo_url=photo_url or None,
        is_popular=bool(is_popular),
        is_available=bool(is_available),
    )
    db.add(product)
    await db.commit()

    return RedirectResponse(url="/admin/products", status_code=303)


@router.get("/products/{product_id}")
async def product_edit_page(product_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    require_login(request)
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(
        "admin/product_form.html",
        {"request": request, "product": product, "error": None},
    )


@router.post("/products/{product_id}")
async def product_update(
    product_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    name: str = Form(...),
    category: str = Form(...),
    description: str = Form(""),
    price: int = Form(...),
    photo_url: str = Form(""),
    is_popular: Optional[bool] = Form(False),
    is_available: Optional[bool] = Form(True),
):
    require_login(request)

    if not (100_000 <= int(price) <= 10_000_000):
        return templates.TemplateResponse(
            "admin/product_form.html",
            {"request": request, "product": None, "error": "Цена вне диапазона (100k–10M VND)"},
            status_code=400,
        )
    if photo_url:
        ok = photo_url.startswith("https://") and any(photo_url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"])
        if not ok:
            return templates.TemplateResponse(
                "admin/product_form.html",
                {"request": request, "product": None, "error": "Некорректный URL изображения"},
                status_code=400,
            )

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404)

    product.name = name
    product.category = category
    product.description = description
    product.price = int(price)
    product.photo_url = photo_url or None
    product.is_popular = bool(is_popular)
    product.is_available = bool(is_available)

    await db.commit()

    return RedirectResponse(url="/admin/products", status_code=303)


@router.post("/products/{product_id}/delete")
async def product_delete(product_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    require_login(request)
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404)
    await db.delete(product)
    await db.commit()
    return RedirectResponse(url="/admin/products", status_code=303)


@router.get("/products/{product_id}/toggle-available")
async def product_toggle_available(product_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    require_login(request)
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404)
    product.is_available = not bool(product.is_available)
    await db.commit()
    return RedirectResponse(url="/admin/products", status_code=303)


@router.get("/products/{product_id}/toggle-popular")
async def product_toggle_popular(product_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    require_login(request)
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404)
    product.is_popular = not bool(product.is_popular)
    await db.commit()
    return RedirectResponse(url="/admin/products", status_code=303)



