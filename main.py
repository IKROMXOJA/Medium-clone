from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.middlewares import timing_middleware
from app.database import Base, engine
from app.routers import auth as auth_router, users as users_router, articles as articles_router
from app.admin.admin import init_admin
from app.admin.auth import router as admin_auth_router
from pathlib import Path
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # shu joyda


# Jadvallar (Alembic ishlatmasangiz, dev uchun)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Middleware
app.middleware("http")(timing_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# Static & Media
STATIC_DIR = Path(__file__).resolve().parent / "static"
MEDIA_DIR = Path(__file__).resolve().parent / "media"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

# Templating (faqat bitta usul)
templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(articles_router.router)
app.include_router(admin_auth_router)

# Admin panel
init_admin(app)

# Welcome page
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": settings.PROJECT_NAME}
    )
