from pathlib import Path
import secrets
import string
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".codex_deps"))

import pymysql


ADMIN_ENV = ROOT / ".env.admin"
APP_ENV = ROOT / ".env"
READER_ENV = ROOT / ".env.reader"
READER_USER = "text2sql_reader"
READER_HOST = "%"


def load_env(path: Path) -> dict[str, str]:
    values = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def write_env(path: Path, values: dict[str, str]) -> None:
    lines = [f"{key}={value}" for key, value in values.items()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_password(length: int = 28) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def quote_identifier(name: str) -> str:
    return "`" + name.replace("`", "``") + "`"


def main() -> None:
    admin = load_env(ADMIN_ENV) or load_env(APP_ENV)
    if not admin:
        raise SystemExit("Missing .env.admin or .env with admin database credentials.")

    database = admin["DB_NAME"]
    reader_password = generate_password()

    conn = pymysql.connect(
        host=admin["DB_HOST"],
        port=int(admin.get("DB_PORT", "3306")),
        user=admin["DB_USER"],
        password=admin["DB_PASSWORD"],
        database=database,
        connect_timeout=10,
        read_timeout=10,
        write_timeout=10,
        charset="utf8mb4",
        autocommit=True,
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"CREATE USER IF NOT EXISTS %s@%s IDENTIFIED BY %s",
                (READER_USER, READER_HOST, reader_password),
            )
            cursor.execute(
                f"ALTER USER %s@%s IDENTIFIED BY %s",
                (READER_USER, READER_HOST, reader_password),
            )
            cursor.execute(
                f"GRANT SELECT, SHOW VIEW ON {quote_identifier(database)}.* TO %s@%s",
                (READER_USER, READER_HOST),
            )
            cursor.execute("FLUSH PRIVILEGES")
            cursor.execute("SHOW GRANTS FOR %s@%s", (READER_USER, READER_HOST))
            grants = [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()

    if not ADMIN_ENV.exists():
        write_env(ADMIN_ENV, admin)

    app = {
        "DB_HOST": admin["DB_HOST"],
        "DB_PORT": admin.get("DB_PORT", "3306"),
        "DB_USER": READER_USER,
        "DB_PASSWORD": reader_password,
        "DB_NAME": database,
    }
    write_env(APP_ENV, app)
    write_env(READER_ENV, app)

    print(f"PROVISIONED user={READER_USER} host={READER_HOST} database={database}")
    for grant in grants:
        print(grant)


if __name__ == "__main__":
    main()
