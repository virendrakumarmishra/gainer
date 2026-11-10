import importlib
import pkgutil
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# 1. Project configurations & Base class import
import app.models
from app.core.config import settings
from app.models.base import Base

# 2. Dynamic Auto-Discovery: app/models folder every model auto import
for _, module_name, _ in pkgutil.walk_packages(
    app.models.__path__, app.models.__name__ + "."
):
    importlib.import_module(module_name)

# Alembic Config object
config = context.config

# Logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Auto-generate migrations set target metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Generates raw SQL statements without connecting directly to the engine.
    """
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Creates an engine and applies migrations directly to the live database.
    """
    # alembic.ini inject DATABASE_URL from config
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()