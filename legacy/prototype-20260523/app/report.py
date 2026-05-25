from __future__ import annotations

from decimal import Decimal
from typing import Any


def to_number(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float, Decimal)):
        return float(value)
    try:
        text = str(value).replace(",", "").strip()
        if text == "":
            return None
        return float(text)
    except ValueError:
        return None


def build_report(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "row_count": 0,
            "columns": [],
            "numeric_columns": [],
            "dimension_columns": [],
            "kpis": [],
            "charts": [],
            "table_preview": [],
        }

    columns = list(rows[0].keys())
    numeric_columns = []
    dimension_columns = []

    for column in columns:
        values = [to_number(row.get(column)) for row in rows]
        numeric_ratio = sum(value is not None for value in values) / max(len(values), 1)
        if numeric_ratio >= 0.8:
            numeric_columns.append(column)
        else:
            dimension_columns.append(column)

    kpis = []
    for column in numeric_columns[:6]:
        values = [to_number(row.get(column)) for row in rows]
        clean_values = [value for value in values if value is not None]
        if not clean_values:
            continue
        total = sum(clean_values)
        kpis.append(
            {
                "column": column,
                "sum": round(total, 4),
                "avg": round(total / len(clean_values), 4),
                "min": round(min(clean_values), 4),
                "max": round(max(clean_values), 4),
            }
        )

    charts = []
    if dimension_columns and numeric_columns:
        label_column = dimension_columns[0]
        for metric in numeric_columns[:3]:
            points = []
            for row in rows[:30]:
                value = to_number(row.get(metric))
                if value is None:
                    continue
                points.append({"label": str(row.get(label_column, "")), "value": value})
            if points:
                charts.append(
                    {
                        "type": "bar",
                        "title": f"{metric} by {label_column}",
                        "label_column": label_column,
                        "metric_column": metric,
                        "points": points,
                    }
                )

    return {
        "row_count": len(rows),
        "columns": columns,
        "numeric_columns": numeric_columns,
        "dimension_columns": dimension_columns,
        "kpis": kpis,
        "charts": charts,
        "table_preview": rows[:100],
    }
