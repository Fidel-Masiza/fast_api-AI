import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context  # Import the `context` object from Alembic

# Add your application's SQLAlchemy models here
from app.database import Base  # Import your Base class from app.database

# This is the Alembic Config object, which provides access to
# the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# `target_metadata` is the metadata of your SQLAlchemy models
# that Alembic should use to generate migrations
target_metadata = Base.metadata  # Assuming all models use the same Base

# `run_migrations_online` is a function that Alembic will call
# to configure the migration environment
def run_migrations_online():
    # This callback is used to dynamically create an Engine
    # based on settings in the .ini file
    url = config.get_main_option("sqlalchemy.url")
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=url,
    )

    # When Alembic runs migrations, it needs an open connection to the database
    with connectable.connect() as connection:
        # Attach the target metadata to the Alembic context
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        # This line ensures that the current database schema is
        # up-to-date with the models defined in `target_metadata`
        with context.begin_transaction():
            # Generate the migration script automatically
            context.run_migrations()
