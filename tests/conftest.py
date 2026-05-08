import os
import sys
import tempfile
from pathlib import Path

import pytest


_REPO_ROOT = str(Path(__file__).resolve().parents[1])
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

_TEST_DB_PATH = os.path.join(tempfile.gettempdir(), "restapi_lab3_test.db")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{_TEST_DB_PATH}")


@pytest.fixture(autouse=True)
def _recreate_db():
    from app.database import Base, engine

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
