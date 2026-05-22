from __future__ import annotations

import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent.sql_guard import review_sql
from app.agent_runtime import answer_from_metadata
from app.config import load_database_config
from app.db import fetch_all, test_connection
from app.log_store import list_runs, save_run
from app.metadata import build_analysis_guidance, load_metadata
from app.report import build_report
from app.timing import Timeline


STATIC_DIR = ROOT / "web"
BLOCKING_RISKS = {"JOIN_WITHOUT_ON_RISK", "COMMA_JOIN_CARTESIAN_RISK"}


def json_bytes(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def send_json(self, payload: object, status: int = 200) -> None:
        body = json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        config = load_database_config()

        try:
            if path == "/api/connection":
                self.send_json(test_connection(config))
                return
            if path == "/api/heartbeat":
                self.send_json(test_connection(config))
                return
            if path == "/api/metadata":
                metadata = load_metadata(config)
                metadata["guidance"] = build_analysis_guidance(metadata)
                self.send_json(metadata)
                return
            if path == "/api/runs":
                self.send_json({"runs": list_runs()})
                return
        except Exception as exc:
            self.send_json({"ok": False, "error": str(exc), "config": config.safe_info}, status=500)
            return

        return super().do_GET()

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        config = load_database_config()

        try:
            payload = self.read_json()
            if path == "/api/review":
                sql = payload.get("sql", "")
                review = review_sql(sql)
                self.send_json(
                    {
                        "allowed": review.allowed,
                        "hard_blocks": review.hard_blocks,
                        "risks": review.risks,
                        "normalized_sql": review.normalized_sql,
                    }
                )
                return

            if path == "/api/agent":
                timeline = Timeline()
                parse_node = timeline.start("parse_request", "解析用户请求")
                question = payload.get("question", "").strip()
                sql = payload.get("sql", "").strip()
                force_risk = bool(payload.get("force_risk", False))
                if not question:
                    self.send_json({"ok": False, "error": "QUESTION_REQUIRED"}, status=400)
                    return
                timeline.end(
                    parse_node,
                    summary="已读取分析需求和 SQL 输入",
                    details={"has_sql": bool(sql), "force_risk": force_risk},
                )

                if not sql:
                    metadata_node = timeline.start("load_metadata", "读取表结构")
                    metadata = load_metadata(config)
                    timeline.end(
                        metadata_node,
                        summary=f"读取 {metadata['table_count']} 张表",
                        details={"table_count": metadata["table_count"]},
                    )
                    understand_node = timeline.start("understand_question", "理解业务语义")
                    guidance = build_analysis_guidance(metadata)
                    answer = answer_from_metadata(question, metadata, guidance)
                    timeline.end(
                        understand_node,
                        status=answer["mode"],
                        summary=answer["message"],
                        details={"suggestion_count": len(answer.get("suggestions", []))},
                    )
                    log_node = timeline.start("save_run_log", "记录本次运行")
                    timeline.end(log_node, summary="准备写入本地运行记录")
                    timings = {"agent_ms": answer["elapsed_ms"], "timeline": timeline.as_dict()}
                    run_id = save_run(
                        database_name=config.database,
                        question=question,
                        sql_text=None,
                        review_allowed=False,
                        hard_blocks=[],
                        risks=[],
                        status=answer["mode"],
                        timings=timings,
                    )
                    self.send_json({"ok": True, "run_id": run_id, "timeline": timings["timeline"], **answer})
                    return

                sql_node = timeline.start("prepare_sql", "准备 SQL")
                sql_to_review = sql.strip().rstrip(";")
                timeline.end(sql_node, summary="SQL 已规范化", details={"sql": sql_to_review})

                review_node = timeline.start("review_sql", "审查 SQL 安全性")
                review = review_sql(sql_to_review)
                blocking_risks = [risk for risk in review.risks if risk in BLOCKING_RISKS]
                review_status = "blocked" if review.hard_blocks else "risk_pending" if blocking_risks else "success"
                review_summary = "审查通过"
                if review.hard_blocks:
                    review_summary = "存在硬拦截项"
                elif blocking_risks:
                    review_summary = "存在需要人工确认的高风险"
                elif review.risks:
                    review_summary = "审查通过，但存在提示项"
                timeline.end(
                    review_node,
                    status=review_status,
                    summary=review_summary,
                    details={"hard_blocks": review.hard_blocks, "risks": review.risks},
                )
                if review.hard_blocks or (blocking_risks and not force_risk):
                    log_node = timeline.start("save_run_log", "记录本次运行")
                    timeline.end(log_node, summary="准备写入本地运行记录")
                    timings = {"review_ms": review_node["duration_ms"], "timeline": timeline.as_dict()}
                    run_id = save_run(
                        database_name=config.database,
                        question=question,
                        sql_text=sql_to_review,
                        review_allowed=review.allowed,
                        hard_blocks=review.hard_blocks,
                        risks=review.risks,
                        status="blocked" if review.hard_blocks else "risk_pending",
                        timings=timings,
                    )
                    self.send_json(
                        {
                            "ok": False,
                            "run_id": run_id,
                            "status": "blocked" if review.hard_blocks else "risk_pending",
                            "sql": sql_to_review,
                            "hard_blocks": review.hard_blocks,
                            "risks": review.risks,
                            "blocking_risks": blocking_risks,
                            "timeline": timings["timeline"],
                        }
                    )
                    return

                query_node = timeline.start("execute_sql", "执行 SQL 查询")
                rows, query_ms = fetch_all(config, sql_to_review)
                timeline.end(
                    query_node,
                    summary=f"数据库返回 {len(rows)} 行",
                    details={"row_count": len(rows), "database_ms": query_ms},
                )

                report_node = timeline.start("build_report", "生成报表看板")
                report = build_report(rows)
                timeline.end(
                    report_node,
                    summary=f"生成 {len(report['kpis'])} 个指标和 {len(report['charts'])} 个图表",
                    details={"kpi_count": len(report["kpis"]), "chart_count": len(report["charts"])},
                )
                preview = rows[:20]
                log_node = timeline.start("save_run_log", "记录本次运行")
                timeline.end(log_node, summary="准备写入本地运行记录")
                timings = {
                    "query_ms": query_ms,
                    "report_ms": report_node["duration_ms"],
                    "total_ms": timeline.as_dict()["total_ms"],
                    "timeline": timeline.as_dict(),
                }
                run_id = save_run(
                    database_name=config.database,
                    question=question,
                    sql_text=sql_to_review,
                    review_allowed=True,
                    hard_blocks=[],
                    risks=review.risks,
                    status="executed",
                    timings=timings,
                    row_count=len(rows),
                    result_preview=preview,
                )
                self.send_json(
                    {
                        "ok": True,
                        "run_id": run_id,
                        "status": "executed",
                        "sql": sql_to_review,
                        "risks": review.risks,
                        "elapsed_ms": query_ms,
                        "row_count": len(rows),
                        "rows": rows,
                        "report": report,
                        "timeline": timings["timeline"],
                    }
                )
                return
        except Exception as exc:
            if "timeline" in locals():
                timeline.fail_open_node(str(exc))
                error_timeline = timeline.as_dict()
            else:
                error_timeline = None
            save_run(
                database_name=config.database,
                question=locals().get("payload", {}).get("question", ""),
                sql_text=locals().get("payload", {}).get("sql", ""),
                review_allowed=False,
                hard_blocks=[],
                risks=[],
                status="error",
                timings={"timeline": error_timeline} if error_timeline else {},
                error_message=str(exc),
            )
            self.send_json({"ok": False, "error": str(exc), "timeline": error_timeline}, status=500)
            return

        self.send_json({"ok": False, "error": "NOT_FOUND"}, status=404)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("Text2SQL test bench running at http://127.0.0.1:8765")
    server.serve_forever()


if __name__ == "__main__":
    main()
