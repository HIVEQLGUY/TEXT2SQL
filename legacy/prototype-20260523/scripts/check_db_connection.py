from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".codex_deps"))

import pymysql


def load_env(path: Path) -> dict[str, str]:
    values = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def main() -> None:
    env = load_env(ROOT / ".env")
    conn = pymysql.connect(
        host=env["DB_HOST"],
        port=int(env.get("DB_PORT", "3306")),
        user=env["DB_USER"],
        password=env["DB_PASSWORD"],
        database=env["DB_NAME"],
        connect_timeout=10,
        read_timeout=10,
        write_timeout=10,
        charset="utf8mb4",
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DATABASE(), VERSION()")
            database_name, version = cursor.fetchone()
        print(f"CONNECTED database={database_name} version={version}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
