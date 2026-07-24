#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "local" / "credentials" / "resources.json"
LEDGER_PATH = ROOT / "TEXT2SQL-codex-handoff" / "docs" / "RESOURCE-资源登记.md"


def now_text():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M +08:00")


def load_config():
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8-sig"))


def load_env(path):
    env = {}
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        env[key.strip()] = value
    return env


def get_prefixed(env, prefix):
    def pick(suffix, fallback=None):
        return env.get(f"{prefix}_{suffix}", fallback)

    return {
        "host": pick("HOST"),
        "port": int(pick("PORT", "3306")),
        "user": pick("USER"),
        "password": pick("PASSWORD", pick("PASS")),
        "database": pick("NAME", pick("DB")),
        "connect_timeout": int(pick("CONNECT_TIMEOUT", "8")),
    }


def check_tcp(host, port, timeout=8):
    started = time.time()
    with socket.create_connection((host, int(port)), timeout=timeout):
        pass
    return time.time() - started


def check_windows_tcp(host, port):
    command = (
        "$r=Test-NetConnection -ComputerName '%s' -Port %s -WarningAction SilentlyContinue;"
        "if($r.TcpTestSucceeded){'True'}else{'False'}"
    ) % (host, int(port))
    proc = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        text=True,
        capture_output=True,
        timeout=20,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or "Windows TCP 检查失败")
    output = (proc.stdout or "").strip()
    if "True" not in output:
        raise ConnectionRefusedError(f"Windows TCP `{host}:{port}` 不可达")
    return 0.0


def ensure_wsl_ssh_tunnel(tunnel):
    host = tunnel.get("local_host", "127.0.0.1")
    port = int(tunnel["local_port"])
    try:
        check_tcp(host, port, timeout=2)
        return f"复用 WSL 本地隧道 `{host}:{port}`"
    except Exception:
        pass

    key = None
    for candidate in tunnel.get("key_candidates", []):
        if Path(candidate).exists():
            key = candidate
            break
    if not key:
        raise RuntimeError("未找到 WSL SSH 隧道私钥候选")

    target = f"{tunnel.get('jump_user', 'root')}@{tunnel['jump_host']}"
    forward = f"{host}:{port}:{tunnel.get('remote_host', '127.0.0.1')}:{int(tunnel['remote_port'])}"
    cmd = [
        "ssh",
        "-i",
        key,
        "-o",
        "BatchMode=yes",
        "-o",
        "IdentitiesOnly=yes",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "ExitOnForwardFailure=yes",
        "-f",
        "-N",
        "-L",
        forward,
        target,
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=15)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or "WSL SSH 隧道启动失败")
    time.sleep(1)
    check_tcp(host, port, timeout=5)
    return f"自动启动 WSL SSH 隧道 `{forward}` via `{tunnel['jump_host']}`"


def run_auto_start(resource):
    cmd = resource.get("auto_start_windows_cmd")
    if not cmd:
        return False, "未配置自动启动命令"
    try:
        win_cmd = cmd.replace("/", "\\")
        subprocess.Popen(
            ["cmd.exe", "/c", "start", '""', win_cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
        wait_seconds = int(resource.get("auto_start_wait_seconds", 5))
        time.sleep(wait_seconds)
        return True, f"已执行自动启动命令并等待 {wait_seconds}s"
    except Exception as exc:
        return False, f"自动启动失败：{exc}"


def check_mysql_env(resource):
    try:
        import pymysql
    except Exception as exc:
        return False, f"PyMySQL 不可用：{exc}", "未执行登录"

    env_file = ROOT / resource["env_file"]
    env = load_env(env_file)
    c = get_prefixed(env, resource["env_prefix"])
    tunnel_method = None
    if resource.get("wsl_ssh_tunnel"):
        tunnel_method = ensure_wsl_ssh_tunnel(resource["wsl_ssh_tunnel"])
    if resource.get("connect_host"):
        c["host"] = resource["connect_host"]
    if resource.get("connect_port"):
        c["port"] = int(resource["connect_port"])
    missing = [k for k in ("host", "port", "user", "password", "database") if not c.get(k)]
    if missing:
        return False, f"缺少配置键：{', '.join(missing)}", f"读取 {resource['env_file']} / {resource['env_prefix']}_*"

    started = time.time()
    conn = pymysql.connect(
        host=c["host"],
        port=c["port"],
        user=c["user"],
        password=c["password"],
        database=c["database"],
        connect_timeout=c["connect_timeout"],
        read_timeout=15,
        write_timeout=15,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.Cursor,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(resource.get("validation_query") or "SELECT 1")
            row = cur.fetchone()
    finally:
        conn.close()
    elapsed = time.time() - started
    return (
        True,
        f"登录成功，库 `{c['database']}` 可查询，耗时 {elapsed:.2f}s",
        (f"{tunnel_method}；" if tunnel_method else "") + f"统一脚本读取 `{resource['env_file']}` 的 `{resource['env_prefix']}_*` 并执行只读查询",
    )


def check_windows_mysql_env(resource):
    python_exe = r"C:\Users\24796\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    script = str(ROOT / "TEXT2SQL-codex-handoff" / "scripts" / "check_windows_mysql_env.py")
    cmd = [
        "/mnt/c/Windows/System32/cmd.exe",
        "/c",
        python_exe,
        script,
        "--env-file",
        resource["env_file"],
        "--prefix",
        resource["env_prefix"],
        "--query",
        resource.get("validation_query") or "SELECT DATABASE(), CURRENT_USER(), VERSION()",
    ]
    started = time.time()
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=30)
    elapsed = time.time() - started
    out = (proc.stdout or "").strip()
    if proc.returncode != 0:
        err = (proc.stderr or out or "Windows MySQL 登录校验失败").strip().splitlines()[-1]
        return False, err, f"Windows Python 读取 `{resource['env_file']}` 的 `{resource['env_prefix']}_*`"
    data = json.loads(out.splitlines()[-1])
    if not data.get("ok"):
        return False, data.get("error", "Windows MySQL 登录校验失败"), f"Windows Python 读取 `{resource['env_file']}` 的 `{resource['env_prefix']}_*`"
    return (
        True,
        f"登录成功，入口 `{data['host']}:{data['port']}`，库 `{data['database']}` 可查询，耗时 {elapsed:.2f}s",
        f"Windows Python 读取 `{resource['env_file']}` 的 `{resource['env_prefix']}_*` 并执行只读查询",
    )


def check_http(resource):
    started = time.time()
    req = urllib.request.Request(resource["url"], headers={"User-Agent": "youmei-resource-check/1.0"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        body = resp.read(300).decode("utf-8", errors="replace")
        status = resp.status
    elapsed = time.time() - started
    expect = resource.get("expect_contains")
    if expect and expect not in body:
        return False, f"HTTP {status}，但返回内容未包含 `{expect}`", f"GET `{resource['url']}`"
    return True, f"HTTP {status} 可访问，耗时 {elapsed:.2f}s", f"GET `{resource['url']}`"


def check_openmetadata_env(resource):
    env_file = ROOT / resource["env_file"]
    env = load_env(env_file)
    prefix = resource.get("env_prefix", "OPENMETADATA")
    base_url = env.get(f"{prefix}_BASE_URL", resource.get("base_url", "http://127.0.0.1:8585")).rstrip("/")
    username = env.get(f"{prefix}_USERNAME", resource.get("username", "admin@open-metadata.org"))
    password = env.get(f"{prefix}_PASSWORD")
    if not password:
        return False, f"缺少配置键：{prefix}_PASSWORD", f"读取 `{resource['env_file']}` 的 `{prefix}_*`"
    login_body = json.dumps({
        "email": username,
        "password": base64.b64encode(password.encode("utf-8")).decode("ascii"),
    }).encode("utf-8")
    login_req = urllib.request.Request(
        base_url + "/api/v1/users/login",
        data=login_body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.time()
    with urllib.request.urlopen(login_req, timeout=15) as resp:
        token = json.loads(resp.read().decode("utf-8")).get("accessToken")
    if not token:
        return False, "登录接口未返回 accessToken", f"读取 `{resource['env_file']}` 的 `{prefix}_*` 并登录"
    version_req = urllib.request.Request(
        base_url + "/api/v1/system/version",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(version_req, timeout=15) as resp:
        version = json.loads(resp.read().decode("utf-8")).get("version", "unknown")
    elapsed = time.time() - started
    return (
        True,
        f"登录成功，版本 `{version}`，耗时 {elapsed:.2f}s",
        f"读取 `{resource['env_file']}` 的 `{prefix}_*` 并调用 OpenMetadata 登录和版本接口",
    )


def check_git_https(resource):
    configured_git = resource.get("git_executable")
    candidates = []
    candidates.append(shutil.which("git"))
    if configured_git:
        if os.name == "nt":
            candidates.extend([configured_git, win_to_wsl(configured_git)])
        else:
            candidates.extend([win_to_wsl(configured_git), configured_git])
    git_executable = next(
        (candidate for candidate in candidates if candidate and Path(candidate).exists()),
        None,
    )
    if not git_executable:
        return False, "未找到可用 Git 可执行文件", "检查 git_executable 或系统 PATH"

    url = resource["url"]
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GCM_INTERACTIVE"] = "never"
    proc = subprocess.run(
        [git_executable, "ls-remote", "--heads", url],
        text=True,
        capture_output=True,
        timeout=30,
        env=env,
    )
    method = f"Git 只读检查 `{url}` 的远程分支"
    if proc.returncode != 0:
        return False, "Git 远程访问失败（凭据或网络校验未通过）", method
    branch_count = len([line for line in (proc.stdout or "").splitlines() if line.strip()])
    return True, f"Git 远程访问成功，发现 {branch_count} 个远程分支", method


def win_to_wsl(path_text):
    if path_text.startswith("/"):
        return path_text
    p = path_text.replace("\\", "/")
    if len(p) >= 3 and p[1:3] == ":/":
        return f"/mnt/{p[0].lower()}/{p[3:]}"
    return p


def check_ssh(resource):
    key = None
    for candidate in resource.get("key_candidates", []):
        wsl_key = Path(win_to_wsl(candidate))
        if wsl_key.exists():
            key = str(wsl_key)
            break
    if not key:
        return False, "未找到可用 SSH 私钥候选", "检查 key_candidates 文件是否存在"

    target = f"{resource.get('user', 'root')}@{resource['host']}"
    cmd = [
        "ssh",
        "-i",
        key,
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=8",
        "-o",
        "StrictHostKeyChecking=accept-new",
        target,
        "hostname",
    ]
    started = time.time()
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=15)
    elapsed = time.time() - started
    if proc.returncode != 0:
        reason = (proc.stderr or proc.stdout).strip().splitlines()[-1:] or ["SSH 登录失败"]
        return False, reason[0], f"SSH BatchMode 登录 `{resource['host']}`"
    hostname = (proc.stdout or "").strip().splitlines()[-1] if proc.stdout else "unknown"
    return True, f"SSH 登录成功，主机名 `{hostname}`，耗时 {elapsed:.2f}s", f"SSH BatchMode 登录 `{resource['host']}`"


def check_resource(name, resource):
    if not resource.get("enabled", True):
        return {
            "name": name,
            "ok": None,
            "status": "默认禁用，未校验",
            "method": "resources.json enabled=false",
            "resource": resource,
        }

    typ = resource["type"]
    try:
        if typ == "mysql_env":
            ok, status, method = check_mysql_env(resource)
        elif typ == "windows_mysql_env":
            ok, status, method = check_windows_mysql_env(resource)
        elif typ in ("tcp", "windows_tcp"):
            try:
                elapsed = check_windows_tcp(resource["host"], resource["port"]) if typ == "windows_tcp" else check_tcp(resource["host"], resource["port"])
                ok, status, method = True, f"TCP 端口可达，耗时 {elapsed:.2f}s", f"TCP `{resource['host']}:{resource['port']}`"
            except Exception as first_exc:
                if not resource.get("auto_start_windows_cmd"):
                    raise
                started, start_msg = run_auto_start(resource)
                if not started:
                    raise RuntimeError(f"{first_exc}; {start_msg}")
                elapsed = check_windows_tcp(resource["host"], resource["port"]) if typ == "windows_tcp" else check_tcp(resource["host"], resource["port"])
                ok = True
                status = f"自动启动后 TCP 端口可达，耗时 {elapsed:.2f}s"
                method = f"自动启动 `{resource['auto_start_windows_cmd']}` 后 TCP `{resource['host']}:{resource['port']}`"
        elif typ == "http":
            ok, status, method = check_http(resource)
        elif typ == "openmetadata_env":
            ok, status, method = check_openmetadata_env(resource)
        elif typ == "git_https":
            ok, status, method = check_git_https(resource)
        elif typ == "ssh":
            ok, status, method = check_ssh(resource)
        else:
            ok, status, method = False, f"未知资源类型 `{typ}`", "未执行"
    except Exception as exc:
        ok, status, method = False, f"校验失败：{exc}", f"{typ} 校验"

    return {"name": name, "ok": ok, "status": status, "method": method, "resource": resource}


def update_ledger(results):
    if not LEDGER_PATH.exists():
        return
    text = LEDGER_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    ts = now_text()
    for result in results:
        resource = result["resource"]
        ledger_name = resource.get("ledger_name")
        if not ledger_name:
            continue
        for i, line in enumerate(lines):
            if not line.startswith("| "):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 7 or cells[0] != ledger_name:
                continue
            ok = result["ok"]
            state = result["status"] if ok else f"不可用/待处理：{result['status']}"
            if ok is None:
                state = result["status"]
            cells[3] = ts
            cells[4] = state
            cells[5] = result["method"]
            note = resource.get("notes", "")
            if resource.get("type") == "mysql_env":
                note = f"凭据映射：`{resource['env_file']}` / `{resource['env_prefix']}_*`；{note}"
            elif resource.get("credential_files"):
                note = f"凭据候选：{', '.join('`' + f + '`' for f in resource['credential_files'])}；{note}"
            cells[6] = note
            lines[i] = "| " + " | ".join(cells) + " |"
            break
    lines = [f"更新时间：{ts}" if line.startswith("更新时间：") else line for line in lines]
    LEDGER_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_result(result):
    mark = "OK" if result["ok"] else ("SKIP" if result["ok"] is None else "FAIL")
    print(f"{mark} {result['name']} - {result['resource'].get('title', result['name'])}")
    print(f"  状态：{result['status']}")
    print(f"  方式：{result['method']}")


def main():
    parser = argparse.ArgumentParser(description="统一资源凭据与访问校验入口")
    parser.add_argument("resource", nargs="?", help="资源别名；用 list 查看")
    parser.add_argument("--all", action="store_true", help="校验所有启用资源")
    parser.add_argument("--list", action="store_true", help="列出资源别名")
    parser.add_argument("--exclude", action="append", default=[], help="从本次校验中排除某个资源别名")
    parser.add_argument("--include-disabled", action="store_true", help="包含默认禁用的历史候选")
    parser.add_argument("--no-update-ledger", action="store_true", help="不更新资源登记表")
    args = parser.parse_args()

    config = load_config()
    resources = config["resources"]

    if args.list:
        for name, r in resources.items():
            flag = "enabled" if r.get("enabled", True) else "disabled"
            print(f"{name}\t{flag}\t{r.get('title', '')}")
        return 0

    names = []
    if args.all:
        names = [n for n, r in resources.items() if args.include_disabled or r.get("enabled", True)]
    elif args.resource:
        if args.resource not in resources:
            print(f"未知资源别名：{args.resource}", file=sys.stderr)
            print("可用别名：", ", ".join(resources.keys()), file=sys.stderr)
            return 2
        names = [args.resource]
    else:
        parser.print_help()
        return 2

    excluded = set(args.exclude or [])
    names = [n for n in names if n not in excluded]
    results = [check_resource(n, resources[n]) for n in names]
    for result in results:
        print_result(result)

    if not args.no_update_ledger and config.get("default_update_ledger", True):
        update_ledger(results)
        print(f"已更新资源登记表：{LEDGER_PATH}")

    return 1 if any(r["ok"] is False for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
