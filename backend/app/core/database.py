from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import DATABASE_URL


# Le moteur gere les connexions entre SQLAlchemy et PostgreSQL.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Chaque requete API utilisera une session creee par SessionLocal.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tous les futurs modeles SQLAlchemy devront heriter de cette classe.
Base = declarative_base()


def get_db():
    """Fournit une session de base de donnees puis la ferme proprement."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
