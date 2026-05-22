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
                question = payload.get("question", "").strip()
                sql = payload.get("sql", "").strip()
                force_risk = bool(payload.get("force_risk", False))
                if not question:
                    self.send_json({"ok": False, "error": "QUESTION_REQUIRED"}, status=400)
                    return

                if not sql:
                    metadata = load_metadata(config)
                    guidance = build_analysis_guidance(metadata)
                    answer = answer_from_metadata(question, metadata, guidance)
                    run_id = save_run(
                        database_name=config.database,
                        question=question,
                        sql_text=None,
                        review_allowed=False,
                        hard_blocks=[],
                        risks=[],
                        status=answer["mode"],
                        timings={"agent_ms": answer["elapsed_ms"]},
                    )
                    self.send_json({"ok": True, "run_id": run_id, **answer})
                    return

                sql_to_review = sql.strip().rstrip(";")
                review = review_sql(sql_to_review)
                blocking_risks = [risk for risk in review.risks if risk in BLOCKING_RISKS]
                if review.hard_blocks or (blocking_risks and not force_risk):
                    run_id = save_run(
                        database_name=config.database,
                        question=question,
                        sql_text=sql_to_review,
                        review_allowed=review.allowed,
                        hard_blocks=review.hard_blocks,
                        risks=review.risks,
                        status="blocked" if review.hard_blocks else "risk_pending",
                        timings={"review_ms": 0},
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
                        }
                    )
                    return

                rows, query_ms = fetch_all(config, sql_to_review)
                report = build_report(rows)
                preview = rows[:20]
                run_id = save_run(
                    database_name=config.database,
                    question=question,
                    sql_text=sql_to_review,
                    review_allowed=True,
                    hard_blocks=[],
                    risks=review.risks,
                    status="executed",
                    timings={"query_ms": query_ms},
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
                    }
                )
                return
        except Exception as exc:
            save_run(
                database_name=config.database,
                question=locals().get("payload", {}).get("question", ""),
                sql_text=locals().get("payload", {}).get("sql", ""),
                review_allowed=False,
                hard_blocks=[],
                risks=[],
                status="error",
                timings={},
                error_message=str(exc),
            )
            self.send_json({"ok": False, "error": str(exc)}, status=500)
            return

        self.send_json({"ok": False, "error": "NOT_FOUND"}, status=404)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("Text2SQL test bench running at http://127.0.0.1:8765")
    server.serve_forever()


if __name__ == "__main__":
    main()
