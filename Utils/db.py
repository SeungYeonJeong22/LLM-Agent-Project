# Utils/get_db.py
from contextlib import contextmanager
from Database.db_init import SessionLocal

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()