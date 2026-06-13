from app.core.database import get_db


# Les routes pourront importer get_db depuis ce fichier et l'utiliser avec Depends.
__all__ = ["get_db"]
