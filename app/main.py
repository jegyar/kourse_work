import os
import json
from typing import Optional
from fastapi import FastAPI, Request, Response, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.database import get_db_dependency
from app.services.product_service import ProductService
from app.routers import auth, products, cart, orders, admin

app = FastAPI(
    title="Auto Parts Store",
    description="Автоматизированная информационная система управления интернет-магазином автозапчастей",
    version="1.0.0",
)

# Paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")

# Templates
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# Load Locales
LOCALES = {}
for lang in ['ru', 'en']:
    path = os.path.join(base_dir, "locales", f"{lang}.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            LOCALES[lang] = json.load(f)

def get_translations(request: Request):
    lang = request.cookies.get("lang", "ru")
    if lang not in LOCALES:
        lang = "ru"
    return LOCALES[lang], lang

# Include Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(admin.router)

@app.get("/set-lang")
async def set_language(lang: str, redirect_to: str = "/"):
    response = RedirectResponse(url=redirect_to)
    response.set_cookie("lang", lang, max_age=31536000)
    return response

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    t, lang = get_translations(request)
    return templates.TemplateResponse(request=request, name="index.html", context={"t": t, "lang": lang})

@app.get("/catalog", response_class=HTMLResponse)
async def catalog_page(
    request: Request,
    search: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    car_model: Optional[str] = None,
    page: int = 1,
    conn = Depends(get_db_dependency)
):
    t, lang = get_translations(request)
    products_items = []
    total_count = 0
    categories = []
    brands = []
    try:
        product_service = ProductService(conn)
        paginated = product_service.get_products(
            skip=(page - 1) * 12,
            limit=12,
            search=search,
            category=category,
            brand=brand,
            car_model=car_model,
            sort_by="product_id",
            sort_desc=False
        )
        products_items = paginated.items
        total_count = paginated.total
        categories = product_service.get_categories()
        brands = product_service.get_brands()
    except Exception as e:
        pass

    return templates.TemplateResponse(
        request=request,
        name="catalog.html",
        context={
            "t": t,
            "lang": lang,
            "products": products_items,
            "total": total_count,
            "page": page,
            "size": 12,
            "categories": categories,
            "brands": brands,
            "active_category": category or "",
            "active_brand": brand or "",
            "active_search": search or "",
            "active_car_model": car_model or "",
        }
    )

@app.get("/cart", response_class=HTMLResponse)
async def cart_page(request: Request):
    t, lang = get_translations(request)
    return templates.TemplateResponse(request=request, name="cart.html", context={"t": t, "lang": lang})

@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request):
    t, lang = get_translations(request)
    return templates.TemplateResponse(request=request, name="orders.html", context={"t": t, "lang": lang})

@app.get("/orders/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    t, lang = get_translations(request)
    return templates.TemplateResponse(request=request, name="checkout.html", context={"t": t, "lang": lang})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    t, lang = get_translations(request)
    return templates.TemplateResponse(request=request, name="login.html", context={"t": t, "lang": lang})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    t, lang = get_translations(request)
    return templates.TemplateResponse(request=request, name="register.html", context={"t": t, "lang": lang})

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    t, lang = get_translations(request)
    return templates.TemplateResponse(request=request, name="admin/dashboard.html", context={"t": t, "lang": lang})

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Auto Parts Store API is running"}

