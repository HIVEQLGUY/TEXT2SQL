#!/usr/bin/env bash
set -u

check() {
  local name="$1"
  local host="$2"
  local port="$3"
  if timeout 5 bash -c "</dev/tcp/${host}/${port}" 2>/dev/null; then
    echo "${name} ${host}:${port} open"
  else
    echo "${name} ${host}:${port} closed"
  fi
}

check "阿里云生产ECS" "114.55.148.140" "22"
check "阿里云生产ECS" "114.55.148.140" "80"
check "阿里云生产ECS" "114.55.148.140" "443"
check "工具服务器" "120.26.202.216" "22"
check "工具服务器ClickHouse代理" "120.26.202.216" "28123"
check "测试BI-Lighthouse" "101.34.81.73" "22"
check "测试BI-Lighthouse" "101.34.81.73" "80"
check "测试BI-Lighthouse" "101.34.81.73" "443"
check "旧RDS-youmei_ai" "rm-bp1mx4778wjne596xko.mysql.rds.aliyuncs.com" "3306"
