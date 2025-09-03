from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.article import Article
from ..schemas.article import ArticleCreate, ArticleUpdate, ArticleOut
from ..dependencies import get_current_user
from ..utils.storage import save_upload
from ..services.digest import schedule_weekly_digest

router = APIRouter(prefix="/articles", tags=["articles"])

@router.post("/", response_model=ArticleOut)
async def create_article(
    payload: ArticleCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    background: BackgroundTasks = None
):
    a = Article(title=payload.title, content=payload.content, published=payload.published, author_id=user.id)
    db.add(a); db.commit(); db.refresh(a)

    # Digest generatsiya (haftalik ishni trigger sifatida ko'rsatish uchun)
    schedule_weekly_digest(background, db)
    return a

@router.post("/{article_id}/image", response_model=ArticleOut)
async def upload_image(article_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    a = db.query(Article).filter(Article.id == article_id, Article.author_id == user.id).first()
    if not a:
        raise HTTPException(404, "Not found or not owner")
    a.image_path = await save_upload(file)
    db.commit(); db.refresh(a)
    return a

@router.get("/", response_model=list[ArticleOut])
def list_articles(db: Session = Depends(get_db), published: bool | None = True):
    q = db.query(Article)
    if published is not None:
        q = q.filter(Article.published == published)
    return q.order_by(Article.created_at.desc()).all()

@router.get("/{article_id}", response_model=ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    a = db.query(Article).filter(Article.id == article_id).first()
    if not a:
        raise HTTPException(404, "Not found")
    return a

@router.put("/{article_id}", response_model=ArticleOut)
def update_article(article_id: int, payload: ArticleUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    a = db.query(Article).filter(Article.id == article_id, Article.author_id == user.id).first()
    if not a:
        raise HTTPException(404, "Not found or not owner")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(a, k, v)
    db.commit(); db.refresh(a)
    return a

@router.delete("/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    a = db.query(Article).filter(Article.id == article_id, Article.author_id == user.id).first()
    if not a:
        raise HTTPException(404, "Not found or not owner")
    db.delete(a); db.commit()
    return {"ok": True}
