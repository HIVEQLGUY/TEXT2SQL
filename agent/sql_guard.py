from __future__ import annotations

import re
from dataclasses import dataclass, field


BLOCKED_KEYWORDS = {
    "insert",
    "update",
    "delete",
    "drop",
    "truncate",
    "alter",
    "create",
    "replace",
    "grant",
    "revoke",
    "call",
    "execute",
    "load",
}

SENSITIVE_PATTERNS = (
    "password",
    "passwd",
    "pwd",
    "token",
    "secret",
    "credential",
    "id_card",
    "identity",
    "phone",
    "mobile",
)


@dataclass
class SQLReviewResult:
    allowed: bool
    hard_blocks: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    normalized_sql: str = ""


def normalize_sql(sql: str) -> str:
    return re.sub(r"\s+", " ", sql.strip())


def strip_trailing_semicolon(sql: str) -> str:
    return sql[:-1].strip() if sql.strip().endswith(";") else sql.strip()


def review_sql(sql: str, *, require_limit: bool = True) -> SQLReviewResult:
    normalized = normalize_sql(sql)
    lowered = normalized.lower()
    result = SQLReviewResult(allowed=True, normalized_sql=normalized)

    if not normalized:
        result.hard_blocks.append("SQL_EMPTY")

    body = strip_trailing_semicolon(normalized)
    if ";" in body:
        result.hard_blocks.append("MULTI_STATEMENT_BLOCKED")

    if not lowered.startswith("select ") and not lowered.startswith("with "):
        result.hard_blocks.append("ONLY_SELECT_ALLOWED")

    tokens = set(re.findall(r"\b[a-z_]+\b", lowered))
    blocked = sorted(tokens & BLOCKED_KEYWORDS)
    if blocked:
        result.hard_blocks.append(f"BLOCKED_KEYWORDS:{','.join(blocked)}")

    if re.search(r"\bselect\s+\*", lowered):
        result.hard_blocks.append("SELECT_STAR_BLOCKED")

    if require_limit and " limit " not in f" {lowered} ":
        result.hard_blocks.append("LIMIT_REQUIRED")

    sensitive_hits = [pattern for pattern in SENSITIVE_PATTERNS if pattern in lowered]
    if sensitive_hits:
        result.hard_blocks.append(f"SENSITIVE_FIELD_BLOCKED:{','.join(sorted(set(sensitive_hits)))}")

    join_count = len(re.findall(r"\bjoin\b", lowered))
    on_count = len(re.findall(r"\bon\b", lowered))
    if join_count and on_count < join_count:
        result.risks.append("JOIN_WITHOUT_ON_RISK")

    if re.search(r"\bfrom\s+\S+\s*,\s*\S+", lowered):
        result.risks.append("COMMA_JOIN_CARTESIAN_RISK")

    if re.search(r"\blike\s+['\"]%", lowered):
        result.risks.append("LEADING_WILDCARD_LIKE_RISK")

    if " order by " in f" {lowered} " and " limit " not in f" {lowered} ":
        result.risks.append("ORDER_BY_WITHOUT_LIMIT_RISK")

    if result.hard_blocks:
        result.allowed = False

    return result


if __name__ == "__main__":
    import sys

    sql = " ".join(sys.argv[1:])
    review = review_sql(sql)
    print(f"allowed={review.allowed}")
    for item in review.hard_blocks:
        print(f"BLOCK: {item}")
    for item in review.risks:
        print(f"RISK: {item}")
