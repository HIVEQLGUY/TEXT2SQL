#!/usr/bin/env bash
set -u

echo "== time =="
date '+%F %T %z'

echo "== ping/http =="
timeout 5s curl -sS http://127.0.0.1:8123/ping || true
echo

echo "== ports =="
ss -ltnp 2>/dev/null | grep -E ':(8123|9000) ' || true

echo "== processes =="
ps -eo pid,ppid,stat,etime,%cpu,%mem,cmd | grep -E 'clickhouse-server|clickhouse-watchdog' | grep -v grep || true

echo "== resources =="
free -h || true
df -h / /var/lib/clickhouse 2>/dev/null || true

echo "== clickhouse-client =="
command -v clickhouse-client || true

echo "== sql-select-1-client =="
if command -v clickhouse-client >/dev/null 2>&1; then
  timeout 10s clickhouse-client --host 127.0.0.1 --port 9000 --query "SELECT 1 FORMAT TSV" 2>&1 || true
else
  echo "clickhouse-client not found"
fi

echo "== sql-select-1-http =="
timeout 10s curl -sS 'http://127.0.0.1:8123/?database=youmei_sandbox' --data-binary 'SELECT 1 FORMAT TSV' 2>&1 || true
echo

echo "== sql-version-http =="
timeout 10s curl -sS 'http://127.0.0.1:8123/?database=youmei_sandbox' --data-binary 'SELECT currentDatabase(), version() FORMAT TSV' 2>&1 || true
echo

echo "== running-queries =="
if command -v clickhouse-client >/dev/null 2>&1; then
  timeout 10s clickhouse-client --host 127.0.0.1 --port 9000 --query "SELECT query_id, elapsed, read_rows, formatReadableSize(memory_usage), left(replaceRegexpAll(query, '[[:space:]]+', ' '), 160) FROM system.processes ORDER BY elapsed DESC LIMIT 10 FORMAT TSV" 2>&1 || true
else
  timeout 10s curl -sS 'http://127.0.0.1:8123/?database=youmei_sandbox' --data-binary "SELECT query_id, elapsed, read_rows, formatReadableSize(memory_usage), left(replaceRegexpAll(query, '[[:space:]]+', ' '), 160) FROM system.processes ORDER BY elapsed DESC LIMIT 10 FORMAT TSV" 2>&1 || true
fi

echo "== recent-errors =="
for log in /var/log/clickhouse-server/clickhouse-server.err.log /var/log/clickhouse-server/clickhouse-server.log; do
  if [ -f "$log" ]; then
    echo "-- $log --"
    tail -n 80 "$log" | sed -E 's/(password|token|secret|key)=([^ ]+)/\1=<redacted>/Ig' || true
  fi
done
