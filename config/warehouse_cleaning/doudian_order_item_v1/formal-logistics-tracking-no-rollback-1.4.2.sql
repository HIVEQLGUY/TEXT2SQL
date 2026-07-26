DROP TABLE IF EXISTS youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_2;

RENAME TABLE
    youmei_sandbox.dwd_trade_order_logistics_tracking_no_df
        TO youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_2,
    youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__previous__1_4_2
        TO youmei_sandbox.dwd_trade_order_logistics_tracking_no_df;

DROP TABLE IF EXISTS youmei_sandbox.dwd_trade_order_logistics_tracking_no_df__candidate__1_4_2;
