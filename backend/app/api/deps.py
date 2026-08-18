# Dependances FastAPI : session DB, utilisateur courant, services.
from typing import Generator
from sqlalchemy.orm import Session
from app.dao.relational.db import SessionLocal


def get_db() -> Generator[Session, None, None]:
    # One session per HTTP request. Never commits itself: DAOs only add()/
    # flush(), and committing is the endpoint's job (call db.commit() after
    # the service call succeeds) so a request that chains several DAO calls
    # commits as a single transaction. Rolled back on any unhandled
    # exception raised before that commit, then always closed.
    #
    # Endpoint pattern:
    #   def submit_abstract(payload, db: Session = Depends(get_db)):
    #       result = AbstractService(MySQLAbstractDAO(db), ...).submit(payload)
    #       db.commit()
    #       return result
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()