import dotenv from "dotenv";

dotenv.config();

const numberFromEnv = (name: string, fallback: number): number => {
  const raw = process.env[name];
  if (!raw) return fallback;
  const parsed = Number(raw);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
};

export const config = {
  port: numberFromEnv("WORKBENCH_PORT", 4177),
  demoMode: process.env.WORKBENCH_DEMO_MODE !== "false",
  auditDir: process.env.WORKBENCH_AUDIT_DIR || "local/query-workbench-audit",
  clickhouse: {
    url: process.env.CLICKHOUSE_URL || "http://127.0.0.1:8123",
    database: process.env.CLICKHOUSE_DATABASE || "youmei_sandbox",
    username: process.env.CLICKHOUSE_USERNAME || "readonly",
    password: process.env.CLICKHOUSE_PASSWORD || "",
    requestTimeoutMs: numberFromEnv("CLICKHOUSE_REQUEST_TIMEOUT_MS", 10000),
    maxResultRows: numberFromEnv("CLICKHOUSE_MAX_RESULT_ROWS", 500),
    defaultLimit: numberFromEnv("CLICKHOUSE_DEFAULT_LIMIT", 100),
    maxExecutionSeconds: numberFromEnv("CLICKHOUSE_MAX_EXECUTION_SECONDS", 10)
  }
};

