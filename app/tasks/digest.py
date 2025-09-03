import json
from datetime import datetime
from celery import Celery
from app.database import get_db
from app.models.article import Article
from sqlalchemy.orm import Session

# Celery konfiguratsiyasi
celery_app = Celery(
    "digest_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def generate_weekly_digest():
    """
    Weekly digest yaratish vazifasi.
    Barcha nashr qilingan maqolalarni olib JSON faylga saqlaydi.
    """
    # DB sessiyasini olish
    db: Session = next(get_db())

    # Faqat nashr qilingan maqolalarni olish
    articles = db.query(Article).filter(Article.is_published == True).all()

    # Digest yaratish
    digest = [
        {
            "title": article.title,
            "author": article.author.email if article.author else "Unknown",
            "created_at": article.created_at.strftime("%Y-%m-%d %H:%M:%S") if article.created_at else ""
        }
        for article in articles
    ]

    # JSON fayl nomi
    filename = f"weekly_digest_{datetime.now().strftime('%Y%m%d')}.json"

    # Digestni faylga yozish
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(digest, f, indent=4, ensure_ascii=False)

    return filename
