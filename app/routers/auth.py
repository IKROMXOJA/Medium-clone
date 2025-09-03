from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..schemas.auth import RegisterIn, LoginIn, Token, VerifyIn
from ..utils.security import hash_password, verify_password, create_access_token
from ..tasks.email import send_verification_email
import secrets

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Email already registered")
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(400, "Username taken")

    token = secrets.token_urlsafe(32)
    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password),
        is_admin=False,
        is_verified=False,
        verification_token=token,
    )
    db.add(user)
    db.commit()

    # Celery task (asimmetrik)
    send_verification_email.delay(payload.email, token)

    access = create_access_token(sub=user.email, roles=["user"])
    return Token(access_token=access)

@router.post("/login", response_model=Token)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    roles = ["admin"] if user.is_admin else ["user"]
    return Token(access_token=create_access_token(sub=user.email, roles=roles))

@router.post("/verify")
def verify(payload: VerifyIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == payload.token).first()
    if not user:
        raise HTTPException(400, "Invalid token")
    user.is_verified = True
    user.verification_token = None
    db.commit()
    return {"ok": True}
