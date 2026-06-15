from __future__ import annotations

from app.services.sql_draft_service import _unique_columns


FIELDS = [
    {
        "field_name": "shop_name1",
        "field_display_name": "店铺名称",
        "business_definition": "店铺 直播间 抖音小店",
        "warehouse_column": {"column_name": "shop_name1", "column_comment": "店铺名称"},
    },
    {
        "field_name": "sjxsje",
        "field_display_name": "实际销售金额",
        "business_definition": "销售金额 成交金额 支付金额",
        "warehouse_column": {"column_name": "sjxsje", "column_comment": "实际销售金额"},
    },
    {
        "field_name": "drsjxsje",
        "field_display_name": "当日实际销售金额",
        "business_definition": "当日 销售金额",
        "warehouse_column": {"column_name": "drsjxsje", "column_comment": "当日实际销售金额"},
    },
    {
        "field_name": "sales_qty",
        "field_display_name": "销售数量",
        "business_definition": "销量 数量 件数",
        "warehouse_column": {"column_name": "sales_qty", "column_comment": "销售数量"},
    },
    {
        "field_name": "brand_name",
        "field_display_name": "品牌名称",
        "business_definition": "品牌 商品品牌",
        "warehouse_column": {"column_name": "brand_name", "column_comment": "品牌名称"},
    },
    {
        "field_name": "biz_date",
        "field_display_name": "业务日期",
        "business_definition": "日期 时间 天 最近30天",
        "warehouse_column": {"column_name": "biz_date", "column_comment": "业务日期"},
    },
    {
        "field_name": "spu_name",
        "field_display_name": "SPU 名称",
        "business_definition": "商品 SPU 商品名称",
        "warehouse_column": {"column_name": "spu_name", "column_comment": "SPU 名称"},
    },
]


def test_amount_and_shop_question_selects_amount_and_shop_columns() -> None:
    columns = _unique_columns(FIELDS, "SPU 销售金额 店铺", maximum=5)

    assert "sjxsje" in columns
    assert "shop_name1" in columns


def test_brand_quantity_question_selects_brand_and_quantity_columns() -> None:
    columns = _unique_columns(FIELDS, "按品牌看 SPU 销售数量", maximum=5)

    assert "brand_name" in columns
    assert "sales_qty" in columns


def test_date_amount_question_selects_date_and_amount_columns() -> None:
    columns = _unique_columns(FIELDS, "按日期看 SPU 销售金额", maximum=5)

    assert "biz_date" in columns
    assert "sjxsje" in columns


def test_product_amount_question_selects_product_and_amount_columns() -> None:
    columns = _unique_columns(FIELDS, "SPU 商品名称和销售金额", maximum=5)

    assert "spu_name" in columns
    assert "sjxsje" in columns
