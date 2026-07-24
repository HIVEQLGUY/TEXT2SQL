export const demoDatabases = ["youmei_sandbox", "system"];

export const demoTables = [
  { database: "youmei_sandbox", name: "dwd_trade_order_df", comment: "DWD_抖店订单主单事实全量快照表", engine: "MergeTree", totalRows: 49695 },
  { database: "youmei_sandbox", name: "dwd_trade_order_item_df", comment: "DWD_抖店订单商品明细事实全量快照表", engine: "MergeTree", totalRows: 85770 }
];

export const demoColumns = [
  { name: "shop_id", type: "String", comment: "店铺ID" },
  { name: "shop_order_id", type: "String", comment: "店铺订单号" },
  { name: "pay_time", type: "Nullable(DateTime)", comment: "支付时间" },
  { name: "pay_amount", type: "Decimal(18, 2)", comment: "支付金额" }
];

export const demoCreateTable = `CREATE TABLE youmei_sandbox.dwd_trade_order_df
(
  shop_id String COMMENT '店铺ID',
  shop_order_id String COMMENT '店铺订单号',
  pay_time Nullable(DateTime) COMMENT '支付时间',
  pay_amount Decimal(18, 2) COMMENT '支付金额'
)
ENGINE = MergeTree
ORDER BY (shop_id, shop_order_id)`;

export const demoRows = [
  { shop_id: "demo_shop_01", shop_order_id: "DD202607240001", pay_time: "2026-07-24 10:00:00", pay_amount: "128.00" },
  { shop_id: "demo_shop_01", shop_order_id: "DD202607240002", pay_time: "2026-07-24 10:12:30", pay_amount: "256.50" }
];

