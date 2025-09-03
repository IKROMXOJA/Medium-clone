from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from ..models.article import Article
import json
from datetime import datetime
from pathlib import Path

DIGEST_DIR = Path("digests")
DIGEST_DIR.mkdir(exist_ok=True)

def generate_weekly_digest_task(db: Session):
    articles = db.query(Article).filter(Article.published == True).order_by(Article.created_at.desc()).limit(50).all()
    data = [
        {"id": a.id, "title": a.title, "author_id": a.author_id, "created_at": a.created_at.isoformat()}
        for a in articles
    ]
    out = DIGEST_DIR / f"digest_{datetime.now().strftime('%Y_%m_%d_%H%M')}.json"
    out.write_text(json.dumps({"count": len(data), "articles": data}, ensure_ascii=False, indent=2))
    return str(out)

def schedule_weekly_digest(background: BackgroundTasks, db: Session):
    background.add_task(generate_weekly_digest_task, db=db)
