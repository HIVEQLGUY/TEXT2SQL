from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


DEFAULT_TABLE = "dws_tmall_sales_link_summary"


@dataclass
class QueryPlan:
    sql: str
    title: str
    confidence: str
    assumptions: list[str]


def _columns(metadata: dict[str, Any], table_name: str) -> set[str]:
    for table in metadata.get("tables", []):
        if table.get("name") == table_name:
            return {column["name"] for column in table.get("columns", [])}
    return set()


def _has(cols: set[str], *names: str) -> bool:
    return all(name in cols for name in names)


def _top_limit(question: str) -> str:
    match = re.search(r"(?:top|前)\s*(\d+|十|五|三)", question, flags=re.IGNORECASE)
    if not match:
        return ""
    raw = match.group(1)
    mapping = {"三": 3, "五": 5, "十": 10}
    limit = mapping.get(raw, int(raw) if raw.isdigit() else 10)
    return f"\nLIMIT {limit}"


def _time_filter(question: str) -> tuple[str, list[str]]:
    if "最近7天" in question or "近7天" in question:
        return "WHERE pay_time >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)", ["时间范围按 pay_time 最近 7 天过滤"]
    if "最近30天" in question or "近30天" in question or "近一个月" in question:
        return "WHERE pay_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)", ["时间范围按 pay_time 最近 30 天过滤"]
    if "今年" in question:
        return "WHERE YEAR(pay_time) = YEAR(CURDATE())", ["时间范围按 pay_time 当前年份过滤"]
    if "本月" in question:
        return "WHERE DATE_FORMAT(pay_time, '%Y-%m') = DATE_FORMAT(CURDATE(), '%Y-%m')", ["时间范围按 pay_time 当前月份过滤"]
    return "", []


def plan_query(question: str, metadata: dict[str, Any]) -> QueryPlan | None:
    q = question.strip().lower()
    cols = _columns(metadata, DEFAULT_TABLE)
    if not cols:
        return None

    where_clause, assumptions = _time_filter(question)
    where_line = f"\n{where_clause}" if where_clause else ""
    limit_line = _top_limit(question)

    if any(word in q for word in ("趋势", "按天", "每日", "每天", "日趋势")) and _has(cols, "pay_time", "actual_sales_amt"):
        return QueryPlan(
            sql=(
                "SELECT DATE(pay_time) AS pay_date,\n"
                "       SUM(actual_sales_amt) AS sales_amt,\n"
                "       SUM(real_refund_amt) AS refund_amt,\n"
                "       SUM(pay_buyer_cnt) AS pay_buyer_cnt\n"
                f"FROM {DEFAULT_TABLE}"
                f"{where_line}\n"
                "GROUP BY DATE(pay_time)\n"
                "ORDER BY pay_date"
            ),
            title="销售日趋势",
            confidence="medium",
            assumptions=assumptions + ["销售额使用 actual_sales_amt，退款使用 real_refund_amt。"],
        )

    if any(word in q for word in ("店铺", "门店", "shop")) and any(word in q for word in ("销售", "成交", "金额", "排行", "排名")):
        if _has(cols, "shop_name", "actual_sales_amt"):
            return QueryPlan(
                sql=(
                    "SELECT shop_name,\n"
                    "       SUM(actual_sales_amt) AS sales_amt,\n"
                    "       SUM(real_refund_amt) AS refund_amt,\n"
                    "       SUM(pay_buyer_cnt) AS pay_buyer_cnt\n"
                    f"FROM {DEFAULT_TABLE}"
                    f"{where_line}\n"
                    "GROUP BY shop_name\n"
                    "ORDER BY sales_amt DESC"
                    f"{limit_line}"
                ),
                title="店铺销售排行",
                confidence="high",
                assumptions=assumptions + ["销售额使用 actual_sales_amt，按 shop_name 汇总。"],
            )

    if any(word in q for word in ("商品", "款式", "货品", "item")) and any(word in q for word in ("销售", "排行", "排名", "表现")):
        group_field = "item_name" if "item_name" in cols else "style_code"
        if _has(cols, group_field, "actual_sales_amt"):
            return QueryPlan(
                sql=(
                    f"SELECT {group_field},\n"
                    "       SUM(actual_sales_amt) AS sales_amt,\n"
                    "       SUM(item_qty) AS item_qty,\n"
                    "       SUM(real_refund_amt) AS refund_amt\n"
                    f"FROM {DEFAULT_TABLE}"
                    f"{where_line}\n"
                    f"GROUP BY {group_field}\n"
                    "ORDER BY sales_amt DESC"
                    f"{limit_line}"
                ),
                title="商品销售排行",
                confidence="medium",
                assumptions=assumptions + [f"商品维度使用 {group_field}。"],
            )

    if any(word in q for word in ("退款", "退货", "退货率", "退款率")) and _has(cols, "shop_name", "real_refund_amt", "actual_sales_amt"):
        return QueryPlan(
            sql=(
                "SELECT shop_name,\n"
                "       SUM(real_refund_amt) AS refund_amt,\n"
                "       SUM(actual_sales_amt) AS sales_amt,\n"
                "       CASE WHEN SUM(actual_sales_amt) = 0 THEN 0 ELSE SUM(real_refund_amt) / SUM(actual_sales_amt) END AS refund_rate\n"
                f"FROM {DEFAULT_TABLE}"
                f"{where_line}\n"
                "GROUP BY shop_name\n"
                "ORDER BY refund_amt DESC"
                f"{limit_line}"
            ),
            title="店铺退款分析",
            confidence="medium",
            assumptions=assumptions + ["退款金额使用 real_refund_amt，退款率按 real_refund_amt / actual_sales_amt 计算。"],
        )

    if any(word in q for word in ("推广", "投放", "roi", "花费", "营销")) and _has(cols, "shop_name", "actual_sales_amt", "total_mkt_fee"):
        return QueryPlan(
            sql=(
                "SELECT shop_name,\n"
                "       SUM(total_mkt_fee) AS marketing_fee,\n"
                "       SUM(actual_sales_amt) AS sales_amt,\n"
                "       CASE WHEN SUM(total_mkt_fee) = 0 THEN NULL ELSE SUM(actual_sales_amt) / SUM(total_mkt_fee) END AS roi\n"
                f"FROM {DEFAULT_TABLE}"
                f"{where_line}\n"
                "GROUP BY shop_name\n"
                "ORDER BY marketing_fee DESC"
                f"{limit_line}"
            ),
            title="推广投入产出分析",
            confidence="medium",
            assumptions=assumptions + ["推广花费使用 total_mkt_fee，ROI 按 actual_sales_amt / total_mkt_fee 计算。"],
        )

    if any(word in q for word in ("利润", "毛利", "盈利")) and _has(cols, "shop_name", "est_profit"):
        return QueryPlan(
            sql=(
                "SELECT shop_name,\n"
                "       SUM(est_profit) AS est_profit,\n"
                "       SUM(actual_sales_amt) AS sales_amt,\n"
                "       CASE WHEN SUM(actual_sales_amt) = 0 THEN 0 ELSE SUM(est_profit) / SUM(actual_sales_amt) END AS profit_rate\n"
                f"FROM {DEFAULT_TABLE}"
                f"{where_line}\n"
                "GROUP BY shop_name\n"
                "ORDER BY est_profit DESC"
                f"{limit_line}"
            ),
            title="店铺利润分析",
            confidence="medium",
            assumptions=assumptions + ["利润使用 est_profit，利润率按 est_profit / actual_sales_amt 计算。"],
        )

    if any(word in q for word in ("概览", "总览", "整体", "汇总", "看看")):
        return QueryPlan(
            sql=(
                "SELECT COUNT(*) AS row_count,\n"
                "       MIN(pay_time) AS first_pay_time,\n"
                "       MAX(pay_time) AS last_pay_time,\n"
                "       SUM(actual_sales_amt) AS sales_amt,\n"
                "       SUM(real_refund_amt) AS refund_amt,\n"
                "       SUM(total_mkt_fee) AS marketing_fee,\n"
                "       SUM(est_profit) AS est_profit\n"
                f"FROM {DEFAULT_TABLE}"
                f"{where_line}"
            ),
            title="经营概览",
            confidence="medium",
            assumptions=assumptions + ["概览口径使用销售额、退款、营销费、预估利润等核心字段。"],
        )

    return None
