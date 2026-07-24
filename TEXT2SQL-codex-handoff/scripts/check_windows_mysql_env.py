#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import pymysql


ROOT = Path(__file__).resolve().parents[2]


def load_env(path):
    env = {}
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", required=True)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--query", default="SELECT DATABASE(), CURRENT_USER(), VERSION()")
    args = parser.parse_args()

    env = load_env(ROOT / args.env_file)
    prefix = args.prefix

    def pick(suffix, fallback=None):
        return env.get(f"{prefix}_{suffix}", fallback)

    cfg = {
        "host": pick("HOST"),
        "port": int(pick("PORT", "3306")),
        "user": pick("USER"),
        "password": pick("PASSWORD", pick("PASS")),
        "database": pick("NAME", pick("DB")),
    }
    missing = [key for key, value in cfg.items() if key != "password" and not value]
    if not cfg.get("password"):
        missing.append("password")
    if missing:
        print(json.dumps({"ok": False, "error": "missing " + ", ".join(missing)}, ensure_ascii=False))
        return 2

    conn = pymysql.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        connect_timeout=8,
        read_timeout=15,
        write_timeout=15,
        charset="utf8mb4",
    )
    try:
        with conn.cursor() as cur:
            cur.execute(args.query)
            row = cur.fetchone()
    finally:
        conn.close()

    print(json.dumps({
        "ok": True,
        "host": cfg["host"],
        "port": cfg["port"],
        "database": cfg["database"],
        "user": cfg["user"],
        "row": row,
    }, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
