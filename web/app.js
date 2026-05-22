const state = {
  metadata: null,
  heartbeatTimer: null,
};

const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || `HTTP_${response.status}`);
  }
  return payload;
}

function setStatus(ok, text) {
  const pill = $("statusPill");
  pill.classList.toggle("ok", ok === true);
  pill.classList.toggle("bad", ok === false);
  $("statusText").textContent = text;
}

function renderConnection(payload) {
  $("connName").textContent = payload.config?.name || "-";
  $("connHost").textContent = payload.config ? `${payload.config.host}:${payload.config.port}/${payload.config.database}` : "-";
  $("connUser").textContent = payload.current_user || payload.config?.user || "-";
  $("connVersion").textContent = payload.version || "-";
  $("connLatency").textContent = payload.elapsed_ms ? `${payload.elapsed_ms} ms` : "-";
  $("connHeartbeat").textContent = new Date().toLocaleTimeString();
  $("dbSubtitle").textContent = payload.config ? `${payload.config.database} · ${payload.config.user}` : "数据库连接与取数 Agent 测试台";
}

async function testConnection({ heartbeat = false } = {}) {
  try {
    const payload = await api(heartbeat ? "/api/heartbeat" : "/api/connection");
    renderConnection(payload);
    setStatus(true, "在线");
  } catch (error) {
    setStatus(false, "断联");
    $("connHeartbeat").textContent = `${new Date().toLocaleTimeString()} · ${error.message}`;
  }
}

function renderMetadata() {
  const metadata = state.metadata;
  const query = $("metadataSearch").value.trim().toLowerCase();
  if (!metadata) return;

  $("metadataSummary").textContent = `${metadata.database}：${metadata.table_count} 张表，加载耗时 ${metadata.elapsed_ms} ms`;
  const wrap = $("metadataList");
  wrap.innerHTML = "";

  const tables = metadata.tables.filter((table) => {
    const text = [
      table.name,
      table.comment,
      ...table.columns.flatMap((column) => [column.name, column.type, column.comment]),
    ]
      .join(" ")
      .toLowerCase();
    return !query || text.includes(query);
  });

  for (const table of tables) {
    const card = document.createElement("div");
    card.className = "table-card";
    const columns = table.columns
      .map(
        (column) => `
          <div class="column-item">
            <span class="column-name">${escapeHtml(column.name)}</span>
            <span>${escapeHtml(column.type)} ${column.key ? `· ${escapeHtml(column.key)}` : ""}</span>
          </div>
        `
      )
      .join("");
    card.innerHTML = `
      <div class="table-title">
        ${escapeHtml(table.name)}
        <span class="table-meta">${escapeHtml(table.comment || "")} · rows ${table.rows ?? "-"}</span>
      </div>
      <div class="column-list">${columns}</div>
    `;
    wrap.appendChild(card);
  }
}

async function loadMetadata() {
  $("metadataSummary").textContent = "加载中...";
  const metadata = await api("/api/metadata");
  state.metadata = metadata;
  renderMetadata();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function output(message, tone = "") {
  const box = $("agentOutput");
  box.className = `agent-output ${tone}`;
  box.textContent = message;
}

function renderRows(rows) {
  const wrap = $("resultTableWrap");
  wrap.innerHTML = "";
  if (!rows || rows.length === 0) {
    wrap.textContent = "无返回行。";
    return;
  }

  const columns = Object.keys(rows[0]);
  const table = document.createElement("table");
  table.innerHTML = `
    <thead><tr>${columns.map((column) => `<th>${escapeHtml(column)}</th>`).join("")}</tr></thead>
    <tbody>
      ${rows
        .map((row) => `<tr>${columns.map((column) => `<td>${escapeHtml(row[column])}</td>`).join("")}</tr>`)
        .join("")}
    </tbody>
  `;
  wrap.appendChild(table);
}

function renderChart(rows) {
  const wrap = $("chartWrap");
  wrap.innerHTML = "";
  if (!rows || rows.length === 0) return;

  const columns = Object.keys(rows[0]);
  const numericColumn = columns.find((column) => rows.some((row) => Number.isFinite(Number(row[column]))));
  const labelColumn = columns.find((column) => column !== numericColumn);
  if (!numericColumn || !labelColumn) return;

  const points = rows
    .map((row) => ({ label: String(row[labelColumn]), value: Number(row[numericColumn]) }))
    .filter((point) => Number.isFinite(point.value))
    .slice(0, 12);
  if (points.length === 0) return;

  const max = Math.max(...points.map((point) => Math.abs(point.value))) || 1;
  for (const point of points) {
    const row = document.createElement("div");
    row.className = "chart-row";
    row.innerHTML = `
      <div class="chart-label" title="${escapeHtml(point.label)}">${escapeHtml(point.label)}</div>
      <div class="chart-track"><div class="chart-bar" style="width:${Math.max(2, (Math.abs(point.value) / max) * 100)}%"></div></div>
      <div class="chart-value">${escapeHtml(point.value.toLocaleString())}</div>
    `;
    wrap.appendChild(row);
  }
}

async function sendAgent() {
  const question = $("questionInput").value.trim();
  const sql = $("sqlInput").value.trim();
  const forceRisk = $("forceRisk").checked;
  if (!question) {
    output("请先输入问题。", "warn");
    return;
  }

  $("sendBtn").disabled = true;
  $("resultTableWrap").innerHTML = "";
  $("chartWrap").innerHTML = "";
  output("处理中...");
  try {
    const payload = await api("/api/agent", {
      method: "POST",
      body: JSON.stringify({ question, sql, force_risk: forceRisk }),
    });
    if (payload.status === "executed") {
      output(`执行成功，返回 ${payload.row_count} 行，耗时 ${payload.elapsed_ms} ms。\nSQL: ${payload.sql}`, "ok");
      renderChart(payload.rows);
      renderRows(payload.rows);
    } else {
      output(`${payload.message}\n\n${JSON.stringify(payload.suggestions || [], null, 2)}`, "ok");
    }
    await loadRuns();
  } catch (error) {
    output(error.message, "bad");
    await loadRuns();
  } finally {
    $("sendBtn").disabled = false;
  }
}

async function reviewSql() {
  const sql = $("sqlInput").value.trim();
  if (!sql) {
    output("请先输入 SQL。", "warn");
    return;
  }
  const payload = await api("/api/review", {
    method: "POST",
    body: JSON.stringify({ sql }),
  });
  const tone = payload.allowed && payload.risks.length === 0 ? "ok" : payload.allowed ? "warn" : "bad";
  output(
    `allowed=${payload.allowed}\nblocks=${payload.hard_blocks.join(", ") || "-"}\nrisks=${payload.risks.join(", ") || "-"}\nSQL: ${payload.normalized_sql}`,
    tone
  );
}

async function loadRuns() {
  const payload = await api("/api/runs");
  const wrap = $("runsList");
  wrap.innerHTML = "";
  for (const run of payload.runs) {
    const item = document.createElement("div");
    item.className = "run-item";
    item.innerHTML = `
      <div class="run-title">
        <strong>#${run.id} ${escapeHtml(run.question || "-")}</strong>
        <span class="badge ${escapeHtml(run.status)}">${escapeHtml(run.status)}</span>
      </div>
      <div class="muted">${escapeHtml(run.created_at)} · rows ${run.row_count} · ${escapeHtml(JSON.stringify(run.timings))}</div>
      ${run.sql_text ? `<div><code>${escapeHtml(run.sql_text)}</code></div>` : ""}
      ${run.hard_blocks.length ? `<div class="muted">blocks: ${escapeHtml(run.hard_blocks.join(", "))}</div>` : ""}
      ${run.risks.length ? `<div class="muted">risks: ${escapeHtml(run.risks.join(", "))}</div>` : ""}
      ${run.error_message ? `<div class="muted">error: ${escapeHtml(run.error_message)}</div>` : ""}
    `;
    wrap.appendChild(item);
  }
}

function startHeartbeat() {
  if (state.heartbeatTimer) clearInterval(state.heartbeatTimer);
  state.heartbeatTimer = setInterval(() => testConnection({ heartbeat: true }), 10000);
}

window.addEventListener("DOMContentLoaded", async () => {
  $("testConnectionBtn").addEventListener("click", () => testConnection());
  $("refreshMetadataBtn").addEventListener("click", () => loadMetadata());
  $("refreshRunsBtn").addEventListener("click", () => loadRuns());
  $("sendBtn").addEventListener("click", sendAgent);
  $("reviewBtn").addEventListener("click", reviewSql);
  $("metadataSearch").addEventListener("input", renderMetadata);

  await testConnection();
  await loadMetadata();
  await loadRuns();
  startHeartbeat();
});
