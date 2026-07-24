#!/usr/bin/env bash
set -euo pipefail

REMOTE="${CLICKHOUSE_TOOL_TUNNEL_REMOTE:-root@120.26.202.216}"
KEY="${CLICKHOUSE_TOOL_TUNNEL_KEY:-$HOME/.ssh/codex_tool_tunnel_ed25519}"
REMOTE_HTTP_PORT="${CLICKHOUSE_TOOL_TUNNEL_HTTP_PORT:-18123}"
REMOTE_NATIVE_PORT="${CLICKHOUSE_TOOL_TUNNEL_NATIVE_PORT:-19000}"
LOCAL_HTTP_PORT="${CLICKHOUSE_LOCAL_HTTP_PORT:-8123}"
LOCAL_NATIVE_PORT="${CLICKHOUSE_LOCAL_NATIVE_PORT:-9000}"
CHECK_USER="${CLICKHOUSE_TUNNEL_CHECK_USER:-}"
CHECK_PASSWORD="${CLICKHOUSE_TUNNEL_CHECK_PASSWORD:-}"
CHECK_DATABASE="${CLICKHOUSE_TUNNEL_CHECK_DATABASE:-youmei_sandbox}"
SLEEP_SECONDS="${CLICKHOUSE_TOOL_TUNNEL_SLEEP_SECONDS:-60}"

SSH_BASE=(
  ssh
  -i "$KEY"
  -o BatchMode=yes
  -o StrictHostKeyChecking=accept-new
  -o ExitOnForwardFailure=yes
  -o ServerAliveInterval=30
  -o ServerAliveCountMax=3
)

tunnel_pattern() {
  printf '%s.*127.0.0.1:%s:127.0.0.1:%s.*127.0.0.1:%s:127.0.0.1:%s' \
    "$KEY" "$REMOTE_HTTP_PORT" "$LOCAL_HTTP_PORT" "$REMOTE_NATIVE_PORT" "$LOCAL_NATIVE_PORT"
}

local_clickhouse_ok() {
  curl -fsS --max-time 3 "http://127.0.0.1:${LOCAL_HTTP_PORT}/ping" >/dev/null
  timeout 3 bash -c "</dev/tcp/127.0.0.1/${LOCAL_NATIVE_PORT}"
}

remote_http_ok() {
  if [[ -n "$CHECK_USER" && -n "$CHECK_PASSWORD" ]]; then
    "${SSH_BASE[@]}" "$REMOTE" \
      "curl -fsS --max-time 5 -u '${CHECK_USER}:${CHECK_PASSWORD}' --data-binary 'SELECT 1' 'http://127.0.0.1:${REMOTE_HTTP_PORT}/?database=${CHECK_DATABASE}'" \
      | grep -qx '1'
  else
    "${SSH_BASE[@]}" "$REMOTE" \
      "curl -fsS --max-time 5 'http://127.0.0.1:${REMOTE_HTTP_PORT}/ping'" \
      | grep -qx 'Ok.'
  fi
}

start() {
  local_clickhouse_ok
  if remote_http_ok; then
    echo "clickhouse_tool_tunnel already healthy"
    return 0
  fi

  "${SSH_BASE[@]}" -fN \
    -R "127.0.0.1:${REMOTE_HTTP_PORT}:127.0.0.1:${LOCAL_HTTP_PORT}" \
    -R "127.0.0.1:${REMOTE_NATIVE_PORT}:127.0.0.1:${LOCAL_NATIVE_PORT}" \
    "$REMOTE"

  remote_http_ok
  echo "clickhouse_tool_tunnel started"
}

status() {
  if remote_http_ok; then
    echo "healthy: ${REMOTE} 127.0.0.1:${REMOTE_HTTP_PORT} -> local 127.0.0.1:${LOCAL_HTTP_PORT}"
  else
    echo "unhealthy"
    return 1
  fi
}

stop() {
  local pattern
  pattern="$(tunnel_pattern)"
  if pgrep -f "$pattern" >/dev/null; then
    pkill -f "$pattern"
    echo "clickhouse_tool_tunnel stopped"
  else
    echo "clickhouse_tool_tunnel not running"
  fi
}

supervise() {
  while true; do
    start || true
    sleep "$SLEEP_SECONDS"
  done
}

case "${1:-status}" in
  start) start ;;
  status) status ;;
  stop) stop ;;
  supervise) supervise ;;
  *)
    echo "usage: $0 {start|status|stop|supervise}" >&2
    exit 2
    ;;
esac
