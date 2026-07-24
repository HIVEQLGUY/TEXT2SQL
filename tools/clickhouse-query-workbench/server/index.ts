import express from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { z } from "zod";
import { appendHistory, deleteFavorite, readFavorites, readHistory, saveFavorite } from "./audit";
import { config } from "./config";
import { checkStatus, listColumns, listDatabases, listTables, runQuery, sampleRows, showCreateTable } from "./clickhouse";
import { sanitizeError } from "./sqlGuard";

const app = express();
app.use(express.json({ limit: "1mb" }));

const tableParams = z.object({
  database: z.string().min(1),
  table: z.string().min(1)
});

app.get("/api/status", async (_req, res) => {
  res.json(await checkStatus());
});

app.get("/api/databases", async (_req, res) => {
  try {
    res.json(await listDatabases());
  } catch (error) {
    res.status(500).json({ error: sanitizeError(error) });
  }
});

app.get("/api/databases/:database/tables", async (req, res) => {
  try {
    res.json(await listTables(req.params.database));
  } catch (error) {
    res.status(400).json({ error: sanitizeError(error) });
  }
});

app.get("/api/databases/:database/tables/:table/columns", async (req, res) => {
  try {
    const params = tableParams.parse(req.params);
    res.json(await listColumns(params.database, params.table));
  } catch (error) {
    res.status(400).json({ error: sanitizeError(error) });
  }
});

app.get("/api/databases/:database/tables/:table/create", async (req, res) => {
  try {
    const params = tableParams.parse(req.params);
    res.json(await showCreateTable(params.database, params.table));
  } catch (error) {
    res.status(400).json({ error: sanitizeError(error) });
  }
});

app.get("/api/databases/:database/tables/:table/sample", async (req, res) => {
  try {
    const params = tableParams.parse(req.params);
    const limit = Number(req.query.limit ?? 20);
    res.json(await sampleRows(params.database, params.table, Number.isFinite(limit) ? limit : 20));
  } catch (error) {
    res.status(400).json({ error: sanitizeError(error) });
  }
});

app.post("/api/query", async (req, res) => {
  const body = z.object({ sql: z.string().min(1), note: z.string().optional() }).safeParse(req.body);
  if (!body.success) {
    res.status(400).json({ error: "SQL 不能为空" });
    return;
  }
  try {
    const result = await runQuery(body.data.sql);
    await appendHistory({ sql: result.sql, note: body.data.note, ok: true, elapsedMs: result.elapsedMs, rowCount: result.rowCount });
    res.json(result);
  } catch (error) {
    const message = sanitizeError(error);
    await appendHistory({ sql: body.data.sql, note: body.data.note, ok: false, error: message });
    res.status(400).json({ error: message });
  }
});

app.get("/api/history", async (_req, res) => {
  res.json(await readHistory());
});

app.get("/api/favorites", async (_req, res) => {
  res.json(await readFavorites());
});

app.post("/api/favorites", async (req, res) => {
  const body = z.object({ sql: z.string().min(1), note: z.string().optional() }).safeParse(req.body);
  if (!body.success) {
    res.status(400).json({ error: "收藏 SQL 不能为空" });
    return;
  }
  res.json(await saveFavorite(body.data.sql, body.data.note));
});

app.delete("/api/favorites/:id", async (req, res) => {
  await deleteFavorite(req.params.id);
  res.json({ ok: true });
});

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const clientDist = path.resolve(__dirname, "../dist/client");
app.use(express.static(clientDist));
app.get("*", (_req, res) => {
  res.sendFile(path.join(clientDist, "index.html"));
});

app.listen(config.port, "127.0.0.1", () => {
  console.log(`ClickHouse 查询工作台后端已启动: http://127.0.0.1:${config.port}`);
});

