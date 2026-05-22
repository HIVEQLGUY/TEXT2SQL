from __future__ import annotations

import time
from datetime import datetime
from typing import Any


class Timeline:
    def __init__(self) -> None:
        self.started_at = datetime.now()
        self.started_perf = time.perf_counter()
        self.previous_end_ms = 0.0
        self.nodes: list[dict[str, Any]] = []

    def _offset_ms(self) -> float:
        return round((time.perf_counter() - self.started_perf) * 1000, 2)

    def start(self, key: str, label: str) -> dict[str, Any]:
        start_ms = self._offset_ms()
        node = {
            "key": key,
            "label": label,
            "status": "running",
            "start_ms": start_ms,
            "end_ms": None,
            "duration_ms": None,
            "transition_ms": round(max(start_ms - self.previous_end_ms, 0), 2),
            "started_at": datetime.now().strftime("%H:%M:%S"),
            "ended_at": None,
            "summary": "",
            "details": {},
        }
        self.nodes.append(node)
        return node

    def end(
        self,
        node: dict[str, Any],
        *,
        status: str = "success",
        summary: str = "",
        details: dict[str, Any] | None = None,
    ) -> None:
        end_ms = self._offset_ms()
        node["status"] = status
        node["end_ms"] = end_ms
        node["duration_ms"] = round(end_ms - float(node["start_ms"]), 2)
        node["ended_at"] = datetime.now().strftime("%H:%M:%S")
        node["summary"] = summary
        node["details"] = details or {}
        self.previous_end_ms = end_ms

    def instant(
        self,
        key: str,
        label: str,
        *,
        status: str = "success",
        summary: str = "",
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        node = self.start(key, label)
        self.end(node, status=status, summary=summary, details=details)
        return node

    def fail_open_node(self, error_message: str) -> None:
        for node in reversed(self.nodes):
            if node["status"] == "running":
                self.end(node, status="failed", summary=error_message)
                return

    def as_dict(self) -> dict[str, Any]:
        total_ms = self._offset_ms()
        completed_nodes = [node for node in self.nodes if node["duration_ms"] is not None]
        slowest = max(completed_nodes, key=lambda node: node["duration_ms"], default=None)
        return {
            "started_at": self.started_at.strftime("%Y-%m-%d %H:%M:%S"),
            "total_ms": round(total_ms, 2),
            "slowest_node": slowest,
            "nodes": self.nodes,
        }
