import { describe, expect, it } from "vitest";
import { guardSql, isIdentifier, sanitizeError } from "../server/sqlGuard";

describe("SQL 只读安全检查", () => {
  it("允许 SELECT 并自动追加默认 LIMIT", () => {
    const result = guardSql("select number from system.numbers", 100, 500);
    expect(result.ok).toBe(true);
    expect(result.sql).toMatch(/LIMIT 100$/);
  });

  it("保留用户显式 LIMIT", () => {
    const result = guardSql("SELECT 1 LIMIT 10", 100, 500);
    expect(result.ok).toBe(true);
    expect(result.sql).toBe("SELECT 1 LIMIT 10");
  });

  it("阻断多语句", () => {
    const result = guardSql("SELECT 1; SELECT 2", 100, 500);
    expect(result.ok).toBe(false);
  });

  it("阻断危险关键字", () => {
    const result = guardSql("DROP TABLE dwd_trade_order_df", 100, 500);
    expect(result.ok).toBe(false);
  });

  it("校验数据库和表名", () => {
    expect(isIdentifier("youmei_sandbox")).toBe(true);
    expect(isIdentifier("youmei_sandbox;drop")).toBe(false);
  });

  it("脱敏错误信息", () => {
    expect(sanitizeError("connect failed password=abc123")).toContain("password=***");
  });
});

