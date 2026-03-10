import os
import sys
import tempfile

import pytest

# Force sqlite for tests (override .env if loaded by Makefile)
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Ensure src is in the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from app import create_app  # noqa: E402
from core.database import db  # noqa: E402


@pytest.fixture
def app():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["UPLOAD_DIR"] = tmpdir
        app = create_app()
        app.config.update({"TESTING": True})

        with app.app_context():
            db.create_all()
            yield app
            db.session.remove()
            db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
