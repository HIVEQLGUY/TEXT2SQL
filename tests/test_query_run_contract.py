from __future__ import annotations

from app.services.query_run_service import QueryRunService, _validate_llm_sql_identifiers


class FakeExecutor:
    def __init__(self, execution: dict) -> None:
        self.execution = execution

    def execute_draft(self, **_: object) -> dict:
        return self.execution


def make_service(execution: dict | None = None, llm_client: object | None = None) -> QueryRunService:
    service = QueryRunService(
        metadata_repository=object(),
        warehouse_repository=object(),
        llm_client=llm_client,
    )
    if execution is not None:
        service._executor = FakeExecutor(execution)  # type: ignore[attr-defined]
    return service


def test_draft_run_returns_stable_contract_fields() -> None:
    execution = {
        "draft": {
            "sql": "SELECT `shop_name1` FROM `dws_douyin_spu_sales_detail` LIMIT 3",
            "ready_to_execute": True,
            "review": {"allowed": True},
            "plan": {
                "selected_table": {
                    "table_id": "hKrBQ2zwwG",
                    "table_name": "dws_douyin_spu_sales_detail",
                    "table_display_name": "DWS_DOUYIN_SPU_SALES_DETAIL",
                }
            },
        },
        "execution_review": {"allowed": True},
        "executed": True,
        "result": {
            "columns": ["shop_name1"],
            "rows": [{"shop_name1": "test-shop"}],
            "row_count": 1,
            "elapsed_ms": 12.3,
        },
        "warnings": [],
    }

    data = make_service(execution).run(question="SPU sales by shop", limit=3)

    assert data["answer_status"] == "ok"
    assert data["error"] is None
    assert data["selected_table"]["table_name"] == "dws_douyin_spu_sales_detail"
    assert data["columns"] == ["shop_name1"]
    assert data["row_count"] == 1
    assert data["trace"]["run_id"] == data["run_id"]
    assert data["trace"]["executed"] is True
    assert [step["step_id"] for step in data["trace"]["steps"]] == [
        "draft_and_execute",
        "sql_execution",
    ]


def test_llm_draft_without_client_returns_not_ready_error_contract() -> None:
    data = make_service(llm_client=None).run(
        question="SPU sales by shop",
        mode="llm_draft",
        limit=3,
    )

    assert data["answer_status"] == "not_ready"
    assert data["error"] == {
        "code": "llm_not_configured",
        "message": "LLM client is not configured.",
        "stage": "llm_sql_generation",
        "status": "not_ready",
        "retryable": False,
    }
    assert data["trace"]["error"] == data["error"]
    assert [step["step_id"] for step in data["trace"]["steps"]] == [
        "llm_sql_generation",
        "sql_review",
        "schema_validation",
        "sql_execution",
    ]
    assert data["trace"]["steps"][0]["status"] == "not_ready"


def test_llm_schema_validator_blocks_identifiers_outside_selected_table() -> None:
    draft = {
        "plan": {
            "selected_table": {
                "table_name": "dws_douyin_spu_sales_detail",
                "warehouse_columns": [
                    {"column_name": "shop_name1"},
                    {"column_name": "sjxsje"},
                ],
            }
        }
    }

    error = _validate_llm_sql_identifiers(
        "SELECT `shop_name1`, `unknown_column` FROM `dws_douyin_spu_sales_detail` LIMIT 3",
        draft,
    )

    assert error == "LLM SQL referenced identifiers outside selected schema: unknown_column"


def test_llm_schema_validator_allows_selected_table_columns() -> None:
    draft = {
        "plan": {
            "selected_table": {
                "table_name": "dws_douyin_spu_sales_detail",
                "warehouse_columns": [
                    {"column_name": "shop_name1"},
                    {"column_name": "sjxsje"},
                ],
            }
        }
    }

    error = _validate_llm_sql_identifiers(
        "SELECT `shop_name1`, `sjxsje` FROM `dws_douyin_spu_sales_detail` LIMIT 3",
        draft,
    )

    assert error is None
