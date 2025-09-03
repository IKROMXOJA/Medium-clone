from starlette_admin.views import CustomView
from starlette_admin.contrib.sqla import Admin as SQLAAdmin, ModelView
from starlette.requests import Request
from fastapi import FastAPI
from ..database import engine
from ..models.user import User
from ..models.article import Article
from ..utils.security import decode_token
from .auth import ADMIN_COOKIE_NAME


def _is_admin(request: Request) -> bool:
    token = request.cookies.get(ADMIN_COOKIE_NAME)
    if not token:
        return False
    try:
        payload = decode_token(token)
        roles = payload.get("roles", [])
        return "admin" in roles
    except Exception:
        return False


class GuardedAdmin(SQLAAdmin):
    async def is_accessible(self, request: Request) -> bool:
        return _is_admin(request)


class UserAdmin(ModelView):
    def __init__(self):
        super().__init__(User)

    # faqat kerakli ustunlarni ko‘rsatamiz
    def get_list_fields(self):
        return ["id", "email", "username", "created_at"]

    def get_detail_fields(self):
        return ["id", "email", "username", "created_at"]

    def get_create_fields(self):
        return ["email", "username"]  # yaratishda hashed_password chiqmasin

    def get_edit_fields(self):
        return ["email", "username"]  # tahrirlashda ham yashirish


class ArticleAdmin(ModelView):
    def __init__(self):
        super().__init__(Article)

    def get_list_fields(self):
        return ["id", "title", "author_id", "created_at"]

    def get_detail_fields(self):
        return ["id", "title", "content", "author_id", "created_at"]

    def get_create_fields(self):
        return ["title", "content", "author_id"]

    def get_edit_fields(self):
        return ["title", "content", "author_id"]


def init_admin(app: FastAPI):
    admin = GuardedAdmin(engine, title="Medium Admin")
    admin.add_view(UserAdmin())
    admin.add_view(ArticleAdmin())
    admin.mount_to(app)
