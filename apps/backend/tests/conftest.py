import pytest
import os
import sys

# Ensure src is in the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import create_app
from core.database import db

@pytest.fixture
def app():
    # Set up testing config
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

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
