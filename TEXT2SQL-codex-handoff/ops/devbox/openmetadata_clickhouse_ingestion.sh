#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-/mnt/c/Users/24796/Documents/TEXT2SQL/TEXT2SQL-codex-handoff}"
RUNTIME_DIR="${REPO}/local/openmetadata-clickhouse"
LOG_DIR="${REPO}/logs"
CONFIG_FILE="${RUNTIME_DIR}/clickhouse-metadata.yaml"
IMAGE="${OPENMETADATA_INGESTION_IMAGE:-docker.getcollate.io/openmetadata/ingestion:1.12.11}"
SERVICE_NAME="${OPENMETADATA_CLICKHOUSE_SERVICE_NAME:-youmei_clickhouse}"
CLICKHOUSE_HOST_PORT="${OPENMETADATA_CLICKHOUSE_HOST_PORT:-172.16.240.1:18124}"
CLICKHOUSE_DATABASE_SCHEMA="${OPENMETADATA_CLICKHOUSE_SCHEMA:-youmei_sandbox}"
CLICKHOUSE_USERNAME="${OPENMETADATA_CLICKHOUSE_USERNAME:-default}"
CLICKHOUSE_PASSWORD="${OPENMETADATA_CLICKHOUSE_PASSWORD:-}"
OPENMETADATA_API="${OPENMETADATA_API:-http://127.0.0.1:8585/api}"
OPENMETADATA_BASE="${OPENMETADATA_BASE:-http://127.0.0.1:8585/api/v1}"
CREDENTIALS_FILE="${OPENMETADATA_CREDENTIALS_FILE:-${REPO}/web/data-agent-workspace/credentials.local.json}"

mkdir -p "${RUNTIME_DIR}" "${LOG_DIR}"
chmod 700 "${RUNTIME_DIR}" 2>/dev/null || true

LOCK_DIR="${RUNTIME_DIR}/ingestion.lock"
if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
  echo "openmetadata_clickhouse_ingestion already running: ${LOCK_DIR}" >&2
  exit 2
fi
trap 'rmdir "${LOCK_DIR}" 2>/dev/null || true' EXIT

token="$(
  CREDENTIALS_FILE="${CREDENTIALS_FILE}" OPENMETADATA_BASE="${OPENMETADATA_BASE}" python3 - <<'PY'
import base64
import json
import os
import urllib.request

credentials_path = os.environ["CREDENTIALS_FILE"]
base = os.environ["OPENMETADATA_BASE"].rstrip("/")
with open(credentials_path, "r", encoding="utf-8-sig") as fh:
    payload = json.load(fh)
om = payload.get("openmetadata", {})
email = om.get("username", "admin@open-metadata.org")
password = base64.b64encode(om.get("password", "").encode()).decode()
body = json.dumps({"email": email, "password": password}).encode()
req = urllib.request.Request(
    f"{base}/users/login",
    data=body,
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=30) as resp:
    print(json.loads(resp.read().decode())["accessToken"])
PY
)"

CONFIG_FILE="${CONFIG_FILE}" \
SERVICE_NAME="${SERVICE_NAME}" \
CLICKHOUSE_HOST_PORT="${CLICKHOUSE_HOST_PORT}" \
CLICKHOUSE_DATABASE_SCHEMA="${CLICKHOUSE_DATABASE_SCHEMA}" \
CLICKHOUSE_USERNAME="${CLICKHOUSE_USERNAME}" \
CLICKHOUSE_PASSWORD="${CLICKHOUSE_PASSWORD}" \
OPENMETADATA_API="${OPENMETADATA_API}" \
OPENMETADATA_JWT_TOKEN="${token}" \
python3 - <<'PY'
import os
from pathlib import Path

config = Path(os.environ["CONFIG_FILE"])
password = os.environ["CLICKHOUSE_PASSWORD"].replace("'", "''")
token = os.environ["OPENMETADATA_JWT_TOKEN"].replace('"', '\\"')
content = f"""source:
  type: clickhouse
  serviceName: {os.environ["SERVICE_NAME"]}
  serviceConnection:
    config:
      type: Clickhouse
      scheme: clickhouse+http
      username: {os.environ["CLICKHOUSE_USERNAME"]}
      password: '{password}'
      hostPort: {os.environ["CLICKHOUSE_HOST_PORT"]}
      databaseSchema: {os.environ["CLICKHOUSE_DATABASE_SCHEMA"]}
  sourceConfig:
    config:
      type: DatabaseMetadata
      schemaFilterPattern:
        includes:
        - {os.environ["CLICKHOUSE_DATABASE_SCHEMA"]}
        excludes:
        - system.*
        - information_schema.*
        - INFORMATION_SCHEMA.*
sink:
  type: metadata-rest
  config: {{}}
workflowConfig:
  loggerLevel: INFO
  openMetadataServerConfig:
    hostPort: {os.environ["OPENMETADATA_API"]}
    authProvider: openmetadata
    securityConfig:
      jwtToken: "{token}"
"""
config.write_text(content, encoding="utf-8")
os.chmod(config, 0o600)
PY

timestamp="$(date +%Y%m%d-%H%M%S)"
log_file="${LOG_DIR}/openmetadata-clickhouse-ingestion-${timestamp}.log"

docker run --rm --network host \
  -v "${CONFIG_FILE}:/tmp/clickhouse-metadata.yaml:ro" \
  --entrypoint metadata \
  "${IMAGE}" ingest -c /tmp/clickhouse-metadata.yaml 2>&1 | tee "${log_file}"
