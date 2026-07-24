import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import CodeMirror from "@uiw/react-codemirror";
import { sql } from "@codemirror/lang-sql";
import { flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import "./styles.css";

type Database = { name: string };
type TableInfo = { database: string; name: string; comment?: string; engine?: string; totalRows?: number };
type ColumnInfo = { name: string; type: string; comment?: string };
type AuditRecord = { id: string; createdAt: string; sql: string; note?: string; ok?: boolean; elapsedMs?: number; rowCount?: number; error?: string };

const requestJson = async <T,>(url: string, init?: RequestInit): Promise<T> => {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...init
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || "请求失败");
  return data as T;
};

const DataTable = ({ rows }: { rows: Record<string, unknown>[] }) => {
  const columns = useMemo(() => {
    const keys = Object.keys(rows[0] ?? {});
    return keys.map((key) => ({ accessorKey: key, header: key }));
  }, [rows]);
  const table = useReactTable({ data: rows, columns, getCoreRowModel: getCoreRowModel() });
  if (!rows.length) return <div className="empty">暂无结果</div>;
  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          {table.getHeaderGroups().map((group) => (
            <tr key={group.id}>
              {group.headers.map((header) => (
                <th key={header.id}>{flexRender(header.column.columnDef.header, header.getContext())}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id}>{String(cell.getValue() ?? "")}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const App = () => {
  const [status, setStatus] = useState<Record<string, unknown>>({});
  const [databases, setDatabases] = useState<Database[]>([]);
  const [tables, setTables] = useState<TableInfo[]>([]);
  const [columns, setColumns] = useState<ColumnInfo[]>([]);
  const [sampleRows, setSampleRows] = useState<Record<string, unknown>[]>([]);
  const [queryRows, setQueryRows] = useState<Record<string, unknown>[]>([]);
  const [history, setHistory] = useState<AuditRecord[]>([]);
  const [favorites, setFavorites] = useState<AuditRecord[]>([]);
  const [database, setDatabase] = useState("");
  const [table, setTable] = useState<TableInfo | null>(null);
  const [createSql, setCreateSql] = useState("");
  const [querySql, setQuerySql] = useState("SELECT * FROM dwd_trade_order_df LIMIT 20");
  const [note, setNote] = useState("");
  const [activeTab, setActiveTab] = useState("overview");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [queryMeta, setQueryMeta] = useState<{ elapsedMs?: number; rowCount?: number; error?: string }>({});

  const loadHistory = async () => setHistory(await requestJson<AuditRecord[]>("/api/history"));
  const loadFavorites = async () => setFavorites(await requestJson<AuditRecord[]>("/api/favorites"));

  useEffect(() => {
    requestJson<Record<string, unknown>>("/api/status").then(setStatus).catch((error) => setMessage(error.message));
    requestJson<Database[]>("/api/databases").then((items) => {
      setDatabases(items);
      setDatabase(items[0]?.name || "");
    }).catch((error) => setMessage(error.message));
    loadHistory();
    loadFavorites();
  }, []);

  useEffect(() => {
    if (!database) return;
    requestJson<TableInfo[]>(`/api/databases/${database}/tables`).then((items) => {
      setTables(items);
      setTable(items[0] || null);
    }).catch((error) => setMessage(error.message));
  }, [database]);

  useEffect(() => {
    if (!database || !table) return;
    setLoading(true);
    Promise.all([
      requestJson<ColumnInfo[]>(`/api/databases/${database}/tables/${table.name}/columns`),
      requestJson<{ statement: string }>(`/api/databases/${database}/tables/${table.name}/create`),
      requestJson<{ rows: Record<string, unknown>[] }>(`/api/databases/${database}/tables/${table.name}/sample?limit=20`)
    ])
      .then(([nextColumns, nextCreate, nextSample]) => {
        setColumns(nextColumns);
        setCreateSql(nextCreate.statement);
        setSampleRows(nextSample.rows);
      })
      .catch((error) => setMessage(error.message))
      .finally(() => setLoading(false));
  }, [database, table]);

  const runQuery = async () => {
    setLoading(true);
    setQueryMeta({});
    try {
      const result = await requestJson<{ rows: Record<string, unknown>[]; elapsedMs: number; rowCount: number; sql: string }>("/api/query", {
        method: "POST",
        body: JSON.stringify({ sql: querySql, note })
      });
      setQueryRows(result.rows);
      setQuerySql(result.sql);
      setQueryMeta({ elapsedMs: result.elapsedMs, rowCount: result.rowCount });
      await loadHistory();
    } catch (error) {
      setQueryMeta({ error: error instanceof Error ? error.message : "查询失败" });
      await loadHistory();
    } finally {
      setLoading(false);
    }
  };

  const copyText = async (text: string) => {
    await navigator.clipboard.writeText(text);
    setMessage("已复制");
    window.setTimeout(() => setMessage(""), 1500);
  };

  const saveCurrentQuery = async () => {
    await requestJson("/api/favorites", { method: "POST", body: JSON.stringify({ sql: querySql, note }) });
    await loadFavorites();
    setMessage("已收藏查询");
  };

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <h1>ClickHouse 查询工作台</h1>
          <p>用于查看表、字段、样例数据，并验证 AI 生成的只读 SQL。</p>
        </div>
        <div className="status">
          <span className={status.ok ? "dot ok" : "dot"} />
          <span>{String(status.mode || "unknown")}</span>
          <strong>{String(status.database || "未连接")}</strong>
        </div>
      </header>

      <section className="layout">
        <aside className="sidebar">
          <label>数据库</label>
          <select value={database} onChange={(event) => setDatabase(event.target.value)}>
            {databases.map((item) => <option key={item.name}>{item.name}</option>)}
          </select>
          <label>表</label>
          <div className="table-list">
            {tables.map((item) => (
              <button key={item.name} className={table?.name === item.name ? "selected" : ""} onClick={() => setTable(item)}>
                <strong>{item.comment || item.name}</strong>
                <span>{item.name}</span>
              </button>
            ))}
          </div>
        </aside>

        <section className="workspace">
          <nav className="tabs">
            {[
              ["overview", "表概览"],
              ["columns", "字段"],
              ["create", "建表语句"],
              ["sample", "样例数据"],
              ["query", "查询"],
              ["history", "查询历史"]
            ].map(([key, label]) => (
              <button key={key} className={activeTab === key ? "active" : ""} onClick={() => setActiveTab(key)}>
                {label}
              </button>
            ))}
          </nav>

          {message && <div className="notice">{message}</div>}
          {loading && <div className="loading">加载中</div>}

          {activeTab === "overview" && table && (
            <section className="panel">
              <h2>{table.comment || table.name}</h2>
              <dl className="meta-grid">
                <div><dt>物理表名</dt><dd>{table.name}</dd></div>
                <div><dt>数据库</dt><dd>{database}</dd></div>
                <div><dt>引擎</dt><dd>{table.engine || "未知"}</dd></div>
                <div><dt>行数</dt><dd>{table.totalRows ?? "未知"}</dd></div>
              </dl>
            </section>
          )}

          {activeTab === "columns" && (
            <section className="panel">
              <h2>字段</h2>
              <DataTable rows={columns as unknown as Record<string, unknown>[]} />
            </section>
          )}

          {activeTab === "create" && (
            <section className="panel">
              <div className="panel-title"><h2>建表语句</h2><button onClick={() => copyText(createSql)}>复制</button></div>
              <pre className="sql-block">{createSql}</pre>
            </section>
          )}

          {activeTab === "sample" && (
            <section className="panel">
              <h2>样例数据</h2>
              <DataTable rows={sampleRows} />
            </section>
          )}

          {activeTab === "query" && (
            <section className="panel query-panel">
              <div className="panel-title">
                <h2>SQL 查询</h2>
                <div className="actions">
                  <button onClick={() => copyText(querySql)}>复制 SQL</button>
                  <button onClick={saveCurrentQuery}>收藏</button>
                  <button className="primary" onClick={runQuery}>执行</button>
                </div>
              </div>
              <CodeMirror value={querySql} height="240px" extensions={[sql()]} onChange={setQuerySql} />
              <textarea value={note} onChange={(event) => setNote(event.target.value)} placeholder="验证备注，例如：用于核对 DWD_抖店订单主单事实全量快照表支付金额合计" />
              {queryMeta.error && <div className="error">{queryMeta.error}</div>}
              {(queryMeta.elapsedMs !== undefined || queryMeta.rowCount !== undefined) && (
                <div className="query-meta">耗时 {queryMeta.elapsedMs} ms，返回 {queryMeta.rowCount} 行</div>
              )}
              <DataTable rows={queryRows} />
            </section>
          )}

          {activeTab === "history" && (
            <section className="panel history">
              <h2>查询历史</h2>
              <div className="history-grid">
                <div>
                  <h3>历史</h3>
                  {history.map((item) => (
                    <button key={item.id} onClick={() => { setQuerySql(item.sql); setNote(item.note || ""); setActiveTab("query"); }}>
                      <span>{new Date(item.createdAt).toLocaleString()}</span>
                      <strong>{item.ok ? "通过" : "失败"}</strong>
                      <code>{item.sql}</code>
                    </button>
                  ))}
                </div>
                <div>
                  <h3>收藏</h3>
                  {favorites.map((item) => (
                    <button key={item.id} onClick={() => { setQuerySql(item.sql); setNote(item.note || ""); setActiveTab("query"); }}>
                      <span>{new Date(item.createdAt).toLocaleString()}</span>
                      <code>{item.sql}</code>
                    </button>
                  ))}
                </div>
              </div>
            </section>
          )}
        </section>
      </section>
    </main>
  );
};

createRoot(document.getElementById("root")!).render(<App />);

