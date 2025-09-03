from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserOut, UserCreate
from ..dependencies import get_current_user, require_admin
from ..models.user import User
from ..tasks.email import send_verification_email

router = APIRouter(prefix="/users", tags=["users"])

# --- EXISTING ROUTES ---
@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user

@router.get("/", response_model=list[UserOut], dependencies=[Depends(require_admin)])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# --- NEW ROUTE: REGISTER USER ---
@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Email tekshirish
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Foydalanuvchini yaratish
    new_user = User(email=user.email, password=user.password)  # parolni hash qilish tavsiya qilinadi
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Token yaratish (misol uchun oddiy string, real loyihada JWT ishlatiladi)
    verification_token = f"verify-{new_user.id}"

    # Celery orqali verification email yuborish
    send_verification_email.delay(new_user.email, verification_token)

    return new_user
