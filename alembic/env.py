from logging.config import fileConfig
import os
from sqlalchemy import create_engine, pool
from alembic import context

# Importa il Base dai tuoi modelli
from app.models.document import Base  

# Config Alembic
config = context.config

# Config logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata per autogenerate
target_metadata = Base.metadata

# Funzione per ottenere URL dal .env se vuoi
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:@localhost:5432/docintellect")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode using sync engine."""
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()