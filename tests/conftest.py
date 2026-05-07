import os
import tempfile

import pytest


_TEST_DB_PATH = os.path.join(tempfile.gettempdir(), "restapi_lab3_test.db")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{_TEST_DB_PATH}")


@pytest.fixture(autouse=True)
def _recreate_db():
    from app.database import Base, engine

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
