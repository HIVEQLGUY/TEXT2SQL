#!/usr/bin/env bash
set -euo pipefail

mkdir -p /opt/youmei-dataagent-stack/superset
mkdir -p /opt/youmei-dataagent-stack/dolphinscheduler

docker pull apache/superset:latest
docker pull apache/dolphinscheduler-standalone-server:3.2.2

docker rm -f youmei-superset youmei-dolphinscheduler 2>/dev/null || true

docker volume create youmei_superset_home >/dev/null

docker run -d \
  --name youmei-superset \
  --restart unless-stopped \
  -p 8088:8088 \
  -e SUPERSET_SECRET_KEY='youmei-local-superset-restored-20260719' \
  -v youmei_superset_home:/app/superset_home \
  apache/superset:latest \
  /bin/sh -lc "superset db upgrade && superset fab create-admin --username admin --firstname Youmei --lastname Admin --email admin@example.com --password admin || true && superset init && superset run -h 0.0.0.0 -p 8088 --with-threads"

docker run -d \
  --name youmei-dolphinscheduler \
  --restart unless-stopped \
  -p 12345:12345 \
  apache/dolphinscheduler-standalone-server:3.2.2

echo "__containers__"
docker ps -a --format '{{.Names}} {{.Image}} {{.Status}}' | grep -Ei 'superset|dolphin' || true

echo "__ports__"
for p in 8088 12345; do
  for i in $(seq 1 60); do
    if (echo > "/dev/tcp/127.0.0.1/$p") >/dev/null 2>&1; then
      echo "$p open"
      break
    fi
    if [ "$i" = "60" ]; then
      echo "$p closed"
    fi
    sleep 2
  done
done
