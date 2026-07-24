#!/usr/bin/env python3
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / "local" / "credentials" / "sr.env"


def load_env():
    env = {}
    for raw in ENV_PATH.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key] = value
    return env


def main():
    env = load_env()
    password = env.get("SR_PASS", "")
    cmd = [
        "mysql",
        "-h",
        env.get("SR_HOST", "127.0.0.1"),
        "-P",
        env.get("SR_PORT", "9030"),
        "-u",
        env.get("SR_USER", "ro1"),
        "-p" + password,
        env.get("SR_DB", "cubeappdata"),
        "-e",
        "SELECT DATABASE(), CURRENT_USER(), VERSION();",
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=25)
    print(f"returncode={proc.returncode}")
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr.replace(password, "<redacted>"))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
