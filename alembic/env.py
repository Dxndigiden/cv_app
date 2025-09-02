import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

sys.path.append(os.getcwd())
import app.models
from app.core.config import settings
from app.db.base import Base

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_online():
    """Запуск миграций в онлайн режиме"""
    connectable = create_async_engine(settings.DATABASE_URL, future=True)
    async def do_run():
        async with connectable.connect() as connection:
            await connection.run_sync(do_apply_migrations)
    asyncio.run(do_run())

def do_apply_migrations(connection: Connection):
    """Применение миграций к базе данных"""
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    raise RuntimeError("Оффлайн режим не поддерживается в этом env.py")
else:
    run_migrations_online()
