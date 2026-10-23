"""Model registry.

Importing a model module attaches its table to Base.metadata. Alembic imports
this package so that it can see every table. Each model added in Phase 5 gets
one import line here, for example:

    from app.models.user import User  # noqa: F401
"""