#!/usr/bin/env python3
import datetime as dt
import re
from pathlib import Path

import pymysql


ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / "local" / "credentials" / "sr.env"
LEDGER_PATH = ROOT / "TEXT2SQL-codex-handoff" / "docs" / "RESOURCE-资源登记.md"


def load_env():
    env = {}
    for raw in ENV_PATH.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def update_ledger(status, method, notes):
    if not LEDGER_PATH.exists():
        return
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M +08:00")
    text = LEDGER_PATH.read_text(encoding="utf-8-sig")
    text = re.sub(r"更新时间：[^\r\n]+", f"更新时间：{ts}", text)
    line = (
        "| 预策/魔方源库 `cubeappdata` | 抖店订单基础表等预策侧源表的只读候选来源 | "
        "`127.0.0.1:19030`，默认库 `cubeappdata`，用户 `ro1` | "
        f"{ts} | {status} | {method} | {notes} |"
    )
    text = re.sub(r"(?m)^\| 预策/魔方源库 `cubeappdata` \|.*$", line, text)
    LEDGER_PATH.write_text(text, encoding="utf-8")


def main():
    env = load_env()
    host = env.get("SR_HOST", "127.0.0.1")
    port = int(env.get("SR_PORT", "19030"))
    user = env.get("SR_USER", "ro1")
    password = env.get("SR_PASS", "")
    database = env.get("SR_DB", "cubeappdata")
    method = "Windows Python 读取 `local/credentials/sr.env` 的 `SR_*` 并通过本机隧道执行只读查询"
    notes = "凭据映射：`local/credentials/sr.env` / `SR_*`；`120.26.202.216:9030` 不作为本机登录入口。"
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connect_timeout=8,
            read_timeout=15,
            write_timeout=15,
            charset="utf8mb4",
        )
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT CURRENT_USER(), VERSION()")
                row = cur.fetchone()
                cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s", (database,))
                table_count = cur.fetchone()[0]
        finally:
            conn.close()
        status = f"登录成功；当前用户 `{row[0]}`，版本 `{row[1]}`，`cubeappdata` 表数量 `{table_count}`"
        print("OK yuce-cubeappdata - 预策/魔方源库 cubeappdata")
        print(f"  状态：{status}")
        print(f"  方式：{method}")
        update_ledger(status, method, notes)
        print(f"已更新资源登记表：{LEDGER_PATH}")
        return 0
    except Exception as exc:
        status = f"不可用/待处理：{type(exc).__name__}: {exc}"
        print("FAIL yuce-cubeappdata - 预策/魔方源库 cubeappdata")
        print(f"  状态：{status}")
        print(f"  方式：{method}")
        update_ledger(status, method, notes)
        print(f"已更新资源登记表：{LEDGER_PATH}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
