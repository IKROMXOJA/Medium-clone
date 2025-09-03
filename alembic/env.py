from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base, engine
# from app.models import models  # barcha modellaringiz shu yerdan import qilinadi
from app.models.user import User
from app.models.article import Article
# Alembic Config obyekti
config = context.config

# Logging sozlamalari
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Autogenerate uchun metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Offline rejimda migratsiyalarni ishlatish"""
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online rejimda migratsiyalarni ishlatish"""
    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
