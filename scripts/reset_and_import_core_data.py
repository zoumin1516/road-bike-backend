from __future__ import annotations

from pathlib import Path
import sys

from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import get_settings

SOURCE_DIR = Path("/Users/jyxc-dz-0100528/.openclaw/workspace")
SQL_FILES = [
    SOURCE_DIR / "road_bike_mysql_schema.sql",
    SOURCE_DIR / "road_bike_seed_brands.sql",
    SOURCE_DIR / "road_bike_seed_models.sql",
    SOURCE_DIR / "road_bike_seed_builds.sql",
    SOURCE_DIR / "road_bike_seed_components.sql",
]

RESET_SQL = [
    "SET FOREIGN_KEY_CHECKS = 0",
    "TRUNCATE TABLE builds",
    "TRUNCATE TABLE models",
    "TRUNCATE TABLE components",
    "TRUNCATE TABLE brands",
    "SET FOREIGN_KEY_CHECKS = 1",
]


def execute_sql_file(conn, file_path: Path) -> None:
    sql_text = file_path.read_text(encoding="utf-8")
    statements = [stmt.strip() for stmt in sql_text.split(";") if stmt.strip()]
    for statement in statements:
        upper_stmt = statement.upper()
        if upper_stmt.startswith("CREATE DATABASE") or upper_stmt.startswith("USE "):
            continue
        conn.execute(text(statement))


def main() -> None:
    settings = get_settings()
    engine = create_engine(settings.database_url, echo=settings.mysql_echo, pool_pre_ping=True)

    with engine.begin() as conn:
        for stmt in RESET_SQL:
            conn.execute(text(stmt))
        for file_path in SQL_FILES:
            if not file_path.exists():
                raise FileNotFoundError(f"Missing SQL file: {file_path}")
            print(f"Importing {file_path.name} ...")
            execute_sql_file(conn, file_path)

    print("Core tables reset and imported successfully.")


if __name__ == "__main__":
    main()
