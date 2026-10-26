import psycopg2
import psycopg2.extensions
from contextlib import contextmanager
from app.config import settings


def get_connection() -> psycopg2.extensions.connection:
    """Create a new database connection."""
    return psycopg2.connect(settings.dsn)


@contextmanager
def get_db():
    """Context manager for database connections.

    Automatically commits on success and rolls back on error.
    Always closes the connection when done.

    Usage:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ...")
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_db_dependency():
    """FastAPI dependency for database connections.

    Usage in routers:
        @router.get("/items")
        def get_items(conn = Depends(get_db_dependency)):
            cursor = conn.cursor()
            ...
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
