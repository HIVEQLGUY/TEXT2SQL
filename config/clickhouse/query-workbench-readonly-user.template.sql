-- ClickHouse 查询工作台只读账号模板。
-- 执行前必须替换密码占位符；不要把真实密码提交到 Git。

CREATE USER IF NOT EXISTS query_workbench_readonly
IDENTIFIED WITH sha256_password BY '<替换为强密码>';

CREATE SETTINGS PROFILE IF NOT EXISTS query_workbench_readonly_profile
SETTINGS
    readonly = 1,
    max_execution_time = 10,
    max_result_rows = 500,
    result_overflow_mode = 'break',
    max_memory_usage = 1000000000;

ALTER USER query_workbench_readonly
SETTINGS PROFILE query_workbench_readonly_profile;

GRANT SELECT ON youmei_sandbox.* TO query_workbench_readonly;
GRANT SHOW DATABASES, SHOW TABLES, SHOW COLUMNS ON *.* TO query_workbench_readonly;

