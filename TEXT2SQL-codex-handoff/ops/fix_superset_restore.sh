#!/usr/bin/env bash
set -euo pipefail

docker rm -f youmei-superset 2>/dev/null || true
docker volume create youmei_superset_home >/dev/null

docker run -d \
  --name youmei-superset \
  --restart unless-stopped \
  -p 8088:8088 \
  -e SUPERSET_SECRET_KEY='youmei-local-superset-restored-20260719' \
  -v youmei_superset_home:/app/superset_home \
  apache/superset:latest \
  /bin/sh -lc "/app/.venv/bin/superset db upgrade && /app/.venv/bin/superset fab create-admin --username admin --firstname Youmei --lastname Admin --email admin@example.com --password admin || true; /app/.venv/bin/superset init; /app/.venv/bin/superset run -h 0.0.0.0 -p 8088 --with-threads"

for i in $(seq 1 90); do
  if curl -fsS --max-time 3 http://127.0.0.1:8088/ >/dev/null 2>&1; then
    echo "superset_http_ok"
    docker ps --format '{{.Names}} {{.Status}} {{.Ports}}' | grep -Ei 'superset|dolphin' || true
    exit 0
  fi
  sleep 2
done

echo "superset_http_not_ready"
docker ps -a --format '{{.Names}} {{.Image}} {{.Status}}' | grep -Ei 'superset|dolphin' || true
docker logs --tail 120 youmei-superset 2>&1 || true
exit 1
