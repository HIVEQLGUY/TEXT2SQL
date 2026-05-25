const state = {
  metadata: null,
  heartbeatTimer: null,
};

const $ = (id) => document.getElementById(id);
const page = document.body.dataset.page;

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `HTTP_${response.status}`);
  return payload;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatNumber(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return String(value ?? "-");
  return number.toLocaleString("zh-CN", { maximumFractionDigits: 4 });
}

function formatDuration(ms) {
  const value = Number(ms);
  if (!Number.isFinite(value)) return "-";
  if (value < 1000) return `${Math.round(value)} 毫秒`;
  if (value < 60000) return `${(value / 1000).toFixed(value < 10000 ? 1 : 0)} 秒`;
  const totalSeconds = Math.round(value / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  if (minutes < 60) return `${minutes} 分 ${seconds} 秒`;
  const hours = Math.floor(minutes / 60);
  const restMinutes = minutes % 60;
  return `${hours} 小时 ${String(restMinutes).padStart(2, "0")} 分`;
}

function statusText(status) {
  const map = {
    success: "成功",
    running: "执行中",
    failed: "失败",
    blocked: "被拦截",
    risk_pending: "等待确认",
    executed: "成功",
    needs_sql: "等待 SQL",
    metadata: "元数据引导",
    analysis_plan: "分析建议",
  };
  return map[status] || status || "-";
}

function setStatus(ok, text) {
  const pill = $("statusPill");
  if (!pill) return;
  pill.classList.toggle("ok", ok === true);
  pill.classList.toggle("bad", ok === false);
  $("statusText").textContent = text;
}

function renderConnection(payload) {
  if (!$("connName")) return;
  $("connName").textContent = payload.config?.name || "-";
  $("connHost").textContent = payload.config ? `${payload.config.host}:${payload.config.port}/${payload.config.database}` : "-";
  $("connUser").textContent = payload.current_user || payload.config?.user || "-";
  $("connVersion").textContent = payload.version || "-";
  $("connLatency").textContent = payload.elapsed_ms ? formatDuration(payload.elapsed_ms) : "-";
  $("connHeartbeat").textContent = new Date().toLocaleTimeString();
  $("heartbeatCopy").textContent = `最近一次心跳正常，耗时 ${formatDuration(payload.elapsed_ms)}`;
  $("dbSubtitle").textContent = payload.config ? `${payload.config.database} · ${payload.config.user}` : "连接状态、连接信息和持续心跳检测";
}

async function testConnection({ heartbeat = false } = {}) {
  try {
    const payload = await api(heartbeat ? "/api/heartbeat" : "/api/connection");
    renderConnection(payload);
    setStatus(true, "在线");
  } catch (error) {
    setStatus(false, "断联");
    if ($("heartbeatCopy")) $("heartbeatCopy").textContent = `连接异常：${error.message}`;
    if ($("connHeartbeat")) $("connHeartbeat").textContent = new Date().toLocaleTimeString();
  }
}

function startHeartbeat() {
  if (state.heartbeatTimer) clearInterval(state.heartbeatTimer);
  state.heartbeatTimer = setInterval(() => testConnection({ heartbeat: true }), 10000);
}

function renderMetadata() {
  const metadata = state.metadata;
  const search = $("metadataSearch");
  if (!metadata || !search) return;
  const query = search.value.trim().toLowerCase();
  $("metadataSummary").textContent = `${metadata.database}：${metadata.table_count} 张表，加载耗时 ${formatDuration(metadata.elapsed_ms)}`;
  const wrap = $("metadataList");
  wrap.innerHTML = "";

  const tables = metadata.tables.filter((table) => {
    const text = [table.name, table.comment, ...table.columns.flatMap((column) => [column.name, column.type, column.comment])]
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
            <span>${escapeHtml(column.type)}${column.key ? ` · ${escapeHtml(column.key)}` : ""}</span>
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
  if (!$("metadataSummary")) return;
  $("metadataSummary").textContent = "加载中...";
  const metadata = await api("/api/metadata");
  state.metadata = metadata;
  renderMetadata();
}

function output(message, tone = "") {
  const box = $("agentOutput");
  if (!box) return;
  box.className = `agent-output ${tone}`;
  box.textContent = message;
}

function renderTimeline(timeline) {
  const summary = $("timelineSummary");
  const wrap = $("timelineWrap");
  if (!summary || !wrap) return;

  if (!timeline || !timeline.nodes) {
    summary.textContent = "等待本次运行开始";
    wrap.innerHTML = "";
    return;
  }

  const nodes = timeline.nodes || [];
  const slowest = timeline.slowest_node;
  const sqlNode = nodes.find((node) => node.key === "execute_sql");
  const sqlShare = sqlNode?.duration_ms && timeline.total_ms ? Math.round((sqlNode.duration_ms / timeline.total_ms) * 100) : null;
  const parts = [`总耗时 ${formatDuration(timeline.total_ms)}`];
  if (slowest) parts.push(`最慢节点：${slowest.label}，${formatDuration(slowest.duration_ms)}`);
  if (sqlNode) parts.push(`SQL 执行 ${formatDuration(sqlNode.duration_ms)}${sqlShare !== null ? `，占 ${sqlShare}%` : ""}`);
  summary.textContent = parts.join(" · ");

  wrap.innerHTML = "";
  for (const node of nodes) {
    const item = document.createElement("div");
    item.className = `timeline-item ${node.status || ""}`;
    const transition = node.transition_ms > 0 ? `<div class="timeline-gap">节点间隔 ${formatDuration(node.transition_ms)}</div>` : "";
    const details = node.details && Object.keys(node.details).length ? `<pre>${escapeHtml(JSON.stringify(node.details, null, 2))}</pre>` : "";
    item.innerHTML = `
      ${transition}
      <div class="timeline-node">
        <div class="timeline-main">
          <strong>${escapeHtml(node.label)}</strong>
          <span class="timeline-status">${escapeHtml(statusText(node.status))}</span>
        </div>
        <div class="timeline-time">
          <span>开始 ${escapeHtml(node.started_at || "-")}</span>
          <span>结束 ${escapeHtml(node.ended_at || "-")}</span>
          <span>耗时 ${formatDuration(node.duration_ms)}</span>
        </div>
        ${node.summary ? `<div class="timeline-summary-line">${escapeHtml(node.summary)}</div>` : ""}
        ${details}
      </div>
    `;
    wrap.appendChild(item);
  }
}

function renderKpis(report) {
  const wrap = $("kpiWrap");
  if (!wrap) return;
  wrap.innerHTML = "";
  for (const kpi of report.kpis || []) {
    const card = document.createElement("div");
    card.className = "kpi-card";
    card.innerHTML = `
      <h3>${escapeHtml(kpi.column)}</h3>
      <div class="kpi-main">${formatNumber(kpi.sum)}</div>
      <div class="kpi-sub">平均 ${formatNumber(kpi.avg)} · 最小 ${formatNumber(kpi.min)} · 最大 ${formatNumber(kpi.max)}</div>
    `;
    wrap.appendChild(card);
  }
}

function renderCharts(report) {
  const wrap = $("chartWrap");
  if (!wrap) return;
  wrap.innerHTML = "";
  for (const chart of report.charts || []) {
    const card = document.createElement("div");
    card.className = "chart-card";
    const max = Math.max(...chart.points.map((point) => Math.abs(Number(point.value)))) || 1;
    const rows = chart.points
      .map(
        (point) => `
          <div class="chart-row">
            <div class="chart-label" title="${escapeHtml(point.label)}">${escapeHtml(point.label)}</div>
            <div class="chart-track"><div class="chart-bar" style="width:${Math.max(2, (Math.abs(Number(point.value)) / max) * 100)}%"></div></div>
            <div class="chart-value">${formatNumber(point.value)}</div>
          </div>
        `
      )
      .join("");
    card.innerHTML = `<div class="chart-title">${escapeHtml(chart.title)}</div>${rows}`;
    wrap.appendChild(card);
  }
}

function renderRows(rows) {
  const wrap = $("resultTableWrap");
  if (!wrap) return;
  wrap.innerHTML = "";
  if (!rows || rows.length === 0) {
    wrap.textContent = "无返回行。";
    return;
  }
  const previewRows = rows.slice(0, 300);
  const columns = Object.keys(previewRows[0]);
  const table = document.createElement("table");
  table.innerHTML = `
    <thead><tr>${columns.map((column) => `<th>${escapeHtml(column)}</th>`).join("")}</tr></thead>
    <tbody>
      ${previewRows.map((row) => `<tr>${columns.map((column) => `<td>${escapeHtml(row[column])}</td>`).join("")}</tr>`).join("")}
    </tbody>
  `;
  wrap.appendChild(table);
  if (rows.length > previewRows.length) {
    const note = document.createElement("p");
    note.className = "muted";
    note.textContent = `页面预览前 ${previewRows.length} 行，完整结果已用于本次报表统计和运行记录。`;
    wrap.appendChild(note);
  }
}

function renderReport(payload) {
  const report = payload.report || { kpis: [], charts: [], table_preview: payload.rows || [] };
  $("reportMeta").textContent = `返回 ${payload.row_count} 行，查询耗时 ${formatDuration(payload.elapsed_ms)}`;
  renderKpis(report);
  renderCharts(report);
  renderRows(payload.rows || report.table_preview || []);
}

async function sendAgent() {
  const question = $("questionInput").value.trim();
  const sql = $("sqlInput").value.trim();
  const forceRisk = $("forceRisk").checked;
  if (!question) {
    output("请先输入分析需求。", "warn");
    return;
  }

  $("sendBtn").disabled = true;
  $("kpiWrap").innerHTML = "";
  $("chartWrap").innerHTML = "";
  $("resultTableWrap").innerHTML = "";
  $("reportMeta").textContent = "处理中";
  renderTimeline(null);
  output("正在审查 SQL、执行查询并生成报表...");
  try {
    const payload = await api("/api/agent", {
      method: "POST",
      body: JSON.stringify({ question, sql, force_risk: forceRisk }),
    });

    renderTimeline(payload.timeline);
    if (payload.ok === false) {
      const blocks = payload.hard_blocks?.length ? `硬拦截：${payload.hard_blocks.join(", ")}` : "";
      const risks = payload.risks?.length ? `风险提示：${payload.risks.join(", ")}` : "";
      output([blocks, risks, `SQL: ${payload.sql || "-"}`].filter(Boolean).join("\n"), payload.status === "risk_pending" ? "warn" : "bad");
      $("reportMeta").textContent = "未执行查询";
      return;
    }

    if (payload.status === "executed") {
      const riskText = payload.risks?.length ? `\n风险提示：${payload.risks.join(", ")}` : "";
      const planText = payload.generated_plan ? `\n识别为：${payload.generated_plan.title}（置信度 ${payload.generated_plan.confidence}）` : "";
      const assumptionText = payload.generated_plan?.assumptions?.length ? `\n口径假设：${payload.generated_plan.assumptions.join("；")}` : "";
      output(`执行成功。${planText}${assumptionText}${riskText}\nSQL: ${payload.sql}`, "ok");
      if (!$("sqlInput").value.trim()) $("sqlInput").value = payload.sql;
      renderReport(payload);
    } else {
      output(`${payload.message}\n\n${JSON.stringify(payload.suggestions || [], null, 2)}`, "ok");
      $("reportMeta").textContent = "等待查询结果";
    }
    await loadRuns();
  } catch (error) {
    output(error.message, "bad");
    $("reportMeta").textContent = "执行失败";
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

function summarizeRun(run) {
  const timeline = run.timings?.timeline;
  if (!timeline) return `rows ${run.row_count} · ${escapeHtml(JSON.stringify(run.timings))}`;
  const sqlNode = timeline.nodes?.find((node) => node.key === "execute_sql");
  const slowest = timeline.slowest_node;
  return [
    `总耗时 ${formatDuration(timeline.total_ms)}`,
    sqlNode ? `SQL ${formatDuration(sqlNode.duration_ms)}` : "",
    slowest ? `最慢：${slowest.label}` : "",
    `返回 ${run.row_count} 行`,
  ]
    .filter(Boolean)
    .join(" · ");
}

async function loadRuns() {
  if (!$("runsList")) return;
  const payload = await api("/api/runs");
  const wrap = $("runsList");
  wrap.innerHTML = "";
  for (const run of payload.runs) {
    const item = document.createElement("div");
    item.className = "run-item";
    item.innerHTML = `
      <div class="run-title">
        <strong>#${run.id} ${escapeHtml(run.question || "-")}</strong>
        <span class="badge ${escapeHtml(run.status)}">${escapeHtml(statusText(run.status))}</span>
      </div>
      <div class="muted">${escapeHtml(run.created_at)} · ${escapeHtml(summarizeRun(run))}</div>
      ${run.sql_text ? `<div><code>${escapeHtml(run.sql_text)}</code></div>` : ""}
      ${run.hard_blocks.length ? `<div class="muted">blocks: ${escapeHtml(run.hard_blocks.join(", "))}</div>` : ""}
      ${run.risks.length ? `<div class="muted">risks: ${escapeHtml(run.risks.join(", "))}</div>` : ""}
      ${run.error_message ? `<div class="muted">error: ${escapeHtml(run.error_message)}</div>` : ""}
    `;
    wrap.appendChild(item);
  }
}

window.addEventListener("DOMContentLoaded", async () => {
  if (page === "connection") {
    $("testConnectionBtn").addEventListener("click", () => testConnection());
    await testConnection();
    startHeartbeat();
  }

  if (page === "agent") {
    $("refreshMetadataBtn").addEventListener("click", () => loadMetadata());
    $("refreshRunsBtn").addEventListener("click", () => loadRuns());
    $("sendBtn").addEventListener("click", sendAgent);
    $("reviewBtn").addEventListener("click", reviewSql);
    $("metadataSearch").addEventListener("input", renderMetadata);
    document.querySelectorAll("[data-prompt]").forEach((button) => {
      button.addEventListener("click", () => {
        $("questionInput").value = button.dataset.prompt;
        $("sqlInput").value = "";
      });
    });
    await loadMetadata();
    await loadRuns();
  }
});
