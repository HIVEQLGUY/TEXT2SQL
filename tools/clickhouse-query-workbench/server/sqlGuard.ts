export type SqlGuardResult = {
  ok: boolean;
  sql?: string;
  statementType?: string;
  reason?: string;
};

const dangerousWords = [
  "INSERT",
  "UPDATE",
  "DELETE",
  "ALTER",
  "DROP",
  "TRUNCATE",
  "CREATE",
  "REPLACE",
  "RENAME",
  "EXCHANGE",
  "OPTIMIZE",
  "SYSTEM",
  "GRANT",
  "REVOKE",
  "KILL",
  "ATTACH",
  "DETACH"
];

const allowedStarts = ["SELECT", "WITH", "SHOW", "DESCRIBE", "DESC", "EXPLAIN"];

export const isIdentifier = (value: string): boolean => /^[A-Za-z_][A-Za-z0-9_]*$/.test(value);

const stripComments = (sql: string): string =>
  sql
    .replace(/\/\*[\s\S]*?\*\//g, " ")
    .replace(/--[^\r\n]*/g, " ")
    .replace(/#[^\r\n]*/g, " ");

const hasSemicolonOutsideQuotes = (sql: string): boolean => {
  let quote: "'" | '"' | "`" | null = null;
  for (let i = 0; i < sql.length; i += 1) {
    const char = sql[i];
    const prev = sql[i - 1];
    if (quote) {
      if (char === quote && prev !== "\\") quote = null;
      continue;
    }
    if (char === "'" || char === '"' || char === "`") {
      quote = char;
      continue;
    }
    if (char === ";") return true;
  }
  return false;
};

export const sanitizeError = (message: unknown): string => {
  const text = message instanceof Error ? message.message : String(message ?? "未知错误");
  return text
    .replace(/password\s*=\s*[^,\s]+/gi, "password=***")
    .replace(/CLICKHOUSE_PASSWORD=[^,\s]+/gi, "CLICKHOUSE_PASSWORD=***")
    .replace(/Authorization:\s*Bearer\s+[A-Za-z0-9._-]+/gi, "Authorization: Bearer ***");
};

export const guardSql = (inputSql: string, defaultLimit: number, maxResultRows: number): SqlGuardResult => {
  const trimmed = inputSql.trim();
  if (!trimmed) return { ok: false, reason: "SQL 不能为空" };
  if (hasSemicolonOutsideQuotes(trimmed)) return { ok: false, reason: "禁止多语句执行" };

  const normalized = stripComments(trimmed).replace(/\s+/g, " ").trim();
  const statementType = normalized.split(/\s+/, 1)[0]?.toUpperCase();
  if (!statementType || !allowedStarts.includes(statementType)) {
    return { ok: false, reason: "仅允许 SELECT、WITH、SHOW、DESCRIBE、EXPLAIN" };
  }

  const wordPattern = new RegExp(`\\b(${dangerousWords.join("|")})\\b`, "i");
  if (wordPattern.test(normalized)) {
    return { ok: false, reason: "SQL 包含禁止的写入或管理类关键字" };
  }

  if (statementType === "WITH" && !/\bSELECT\b/i.test(normalized)) {
    return { ok: false, reason: "WITH 查询必须最终返回 SELECT" };
  }

  let safeSql = trimmed;
  if ((statementType === "SELECT" || statementType === "WITH") && !/\bLIMIT\s+\d+/i.test(normalized)) {
    safeSql = `${trimmed} LIMIT ${Math.min(defaultLimit, maxResultRows)}`;
  }

  return { ok: true, sql: safeSql, statementType };
};

