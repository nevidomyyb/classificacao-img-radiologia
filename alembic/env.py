

import os
import sys

from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from classificacao_img_radiologia.models import Usuario, Imagem, Classificacao
from urllib.parse import quote_plus
from pathlib import Path

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

load_dotenv(Path(__file__).resolve().parent.parent / "classificacao_img_radiologia" / ".env")
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
DATABASE = os.getenv("DATABASE")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
PASSWORD_ENCODED = quote_plus(PASSWORD)
NEW_PASSWORD_ENCODED = []
for char in PASSWORD_ENCODED:
    if char == "%":
        NEW_PASSWORD_ENCODED.append("%")
        NEW_PASSWORD_ENCODED.append("%")
    else:
        NEW_PASSWORD_ENCODED.append(char)
PASSWORD_ENCODED = "".join(NEW_PASSWORD_ENCODED)
 
DATABASE_URL = f'mysql+mysqldb://{USERNAME}:{PASSWORD_ENCODED}@{HOST}:{PORT}/{DATABASE}'
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from classificacao_img_radiologia.models.database import Base
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
config.set_main_option("sqlalchemy.url", str(DATABASE_URL))

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
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

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
