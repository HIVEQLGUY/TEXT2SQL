import { createClient, type ClickHouseClient } from "@clickhouse/client";
import { config } from "./config";
import { demoColumns, demoCreateTable, demoDatabases, demoRows, demoTables } from "./demo";
import { guardSql, isIdentifier, sanitizeError } from "./sqlGuard";

type QueryResult = {
  rows: Record<string, unknown>[];
  rowCount: number;
  elapsedMs: number;
  sql: string;
};

let client: ClickHouseClient | null = null;

const getClient = (): ClickHouseClient => {
  if (!client) {
    client = createClient({
      url: config.clickhouse.url,
      username: config.clickhouse.username,
      password: config.clickhouse.password,
      database: config.clickhouse.database,
      request_timeout: config.clickhouse.requestTimeoutMs
    });
  }
  return client;
};

const executeJson = async (query: string): Promise<Record<string, unknown>[]> => {
  const result = await getClient().query({
    query,
    format: "JSONEachRow",
    clickhouse_settings: {
      readonly: 1,
      max_result_rows: config.clickhouse.maxResultRows,
      result_overflow_mode: "break",
      max_execution_time: config.clickhouse.maxExecutionSeconds
    }
  });
  return (await result.json()) as Record<string, unknown>[];
};

export const checkStatus = async () => {
  if (config.demoMode) {
    return { ok: true, mode: "demo", database: config.clickhouse.database, version: "demo" };
  }
  try {
    const rows = await executeJson("SELECT currentDatabase() AS database, version() AS version");
    return { ok: true, mode: "clickhouse", ...rows[0] };
  } catch (error) {
    return { ok: false, mode: "clickhouse", error: sanitizeError(error) };
  }
};

export const listDatabases = async () => {
  if (config.demoMode) return demoDatabases.map((name) => ({ name }));
  return executeJson("SHOW DATABASES");
};

export const listTables = async (database: string) => {
  if (!isIdentifier(database)) throw new Error("数据库名不合法");
  if (config.demoMode) return demoTables.filter((table) => table.database === database);
  return executeJson(`
    SELECT database, name, engine, comment, total_rows AS totalRows
    FROM system.tables
    WHERE database = '${database}'
    ORDER BY name
  `);
};

export const listColumns = async (database: string, table: string) => {
  if (!isIdentifier(database) || !isIdentifier(table)) throw new Error("数据库名或表名不合法");
  if (config.demoMode) return demoColumns;
  return executeJson(`
    SELECT name, type, comment
    FROM system.columns
    WHERE database = '${database}' AND table = '${table}'
    ORDER BY position
  `);
};

export const showCreateTable = async (database: string, table: string) => {
  if (!isIdentifier(database) || !isIdentifier(table)) throw new Error("数据库名或表名不合法");
  if (config.demoMode) return { statement: demoCreateTable };
  const rows = await executeJson(`SHOW CREATE TABLE ${database}.${table}`);
  return { statement: Object.values(rows[0] ?? {})[0] ?? "" };
};

export const sampleRows = async (database: string, table: string, limit = 20) => {
  if (!isIdentifier(database) || !isIdentifier(table)) throw new Error("数据库名或表名不合法");
  const safeLimit = Math.min(Math.max(limit, 1), config.clickhouse.maxResultRows);
  if (config.demoMode) return { rows: demoRows.slice(0, safeLimit), rowCount: Math.min(demoRows.length, safeLimit) };
  const rows = await executeJson(`SELECT * FROM ${database}.${table} LIMIT ${safeLimit}`);
  return { rows, rowCount: rows.length };
};

export const runQuery = async (sql: string): Promise<QueryResult> => {
  const guarded = guardSql(sql, config.clickhouse.defaultLimit, config.clickhouse.maxResultRows);
  if (!guarded.ok || !guarded.sql) {
    throw new Error(guarded.reason || "SQL 校验失败");
  }
  const started = performance.now();
  const rows = config.demoMode ? demoRows : await executeJson(guarded.sql);
  return {
    rows,
    rowCount: rows.length,
    elapsedMs: Math.round(performance.now() - started),
    sql: guarded.sql
  };
};

