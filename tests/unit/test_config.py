import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_short_jwt_secret_is_rejected():
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            database_url="postgresql+asyncpg://u:p@localhost/db",
            jwt_secret_key="too-short",
        )


def test_missing_required_settings_are_rejected(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_secrets_are_masked_in_repr():
    settings = Settings(
        _env_file=None,
        database_url="postgresql+asyncpg://u:supersecret@localhost/db",
        jwt_secret_key="x" * 40,
    )

    assert "supersecret" not in repr(settings)
    assert "x" * 40 not in repr(settings)