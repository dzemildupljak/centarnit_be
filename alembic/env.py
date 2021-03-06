import os
from blog import models as blog_models
from user import models as user_models
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool, MetaData

from alembic import context


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
LOCAL_DATABASE_URL = os.getenv('LOCAL_DATABASE_URL')
config.set_main_option(
    "sqlalchemy.url", LOCAL_DATABASE_URL)
# config.set_main_option(
#     "sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

# config.set_main_option(
#     "sqlalchemy.url", "postgresql://postgres:root@db:5432/centarnit_db")


# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# # add your model's MetaData object here
# # for 'autogenerate' support
# # from myapp import mymodel
# # target_metadata = mymodel.Base.metadata
# # target_metadata = None
# target_metadata = Base.metadata

#############################################################
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata


def combine_metadata():
    # from blog import models  # models file into which all models are imported
    # from sqlalchemy import MetaData
    model_classes = []
    for model_name in user_models.__all__:
        model_classes.append(getattr(user_models, model_name))
    m = MetaData()
    for model in model_classes:
        for t in model.metadata.tables.values():
            t.tometadata(m)
    for model_name in blog_models.__all__:
        model_classes.append(getattr(blog_models, model_name))
    for model in model_classes:
        for t in model.metadata.tables.values():
            t.tometadata(m)
    return m


target_metadata = combine_metadata()
#############################################################


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
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


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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
