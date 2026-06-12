import pytest
from app import app
from models import init_db, get_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
            with get_db() as conn:
                conn.execute("DELETE FROM wishes")
        yield client
