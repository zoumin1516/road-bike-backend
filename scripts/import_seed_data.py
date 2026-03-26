from __future__ import annotations

import argparse
from pathlib import Path
import sys

from sqlalchemy import text
from sqlalchemy.engine import create_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import get_settings


def run_sql_file(engine, file_path: Path) -> None:
    sql_text = file_path.read_text(encoding="utf-8")
    statements = [stmt.strip() for stmt in sql_text.split(";") if stmt.strip()]
    with engine.begin() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS road_bike_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        conn.execute(text("USE road_bike_db"))
        for statement in statements:
            conn.execute(text(statement))


def main() -> None:
    parser = argparse.ArgumentParser(description="Import road bike schema and seed SQL files.")
    parser.add_argument(
        "--source-dir",
        default="/Users/jyxc-dz-0100528/.openclaw/workspace",
        help="Directory that contains schema and seed SQL files.",
    )
    args = parser.parse_args()

    settings = get_settings()
    root_engine = create_engine(
        f"mysql+pymysql://{settings.mysql_user}:{settings.mysql_password}"
        f"@{settings.mysql_host}:{settings.mysql_port}/?charset=utf8mb4",
        echo=settings.mysql_echo,
        pool_pre_ping=True,
    )

    source_dir = Path(args.source_dir)
    files = [
        source_dir / "road_bike_mysql_schema.sql",
        source_dir / "road_bike_seed_brands.sql",
        source_dir / "road_bike_seed_models.sql",
        source_dir / "road_bike_seed_builds.sql",
        source_dir / "road_bike_seed_components.sql",
    ]

    for file_path in files:
        if not file_path.exists():
            raise FileNotFoundError(f"Missing SQL file: {file_path}")
        print(f"Importing {file_path.name} ...")
        run_sql_file(root_engine, file_path)

    print("Done.")


if __name__ == "__main__":
    main()
