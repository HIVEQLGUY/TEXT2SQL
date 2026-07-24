# 数据质量规则配置 browser-act 固化路径

更新时间：2026-07-10

## 目标

用于 Codex 后续稳定进入预策 BI 的任务数据质量配置，并通过 `/api/dqr` 接口批量配置质量规则。

## 已验证 UI 探路路径

Codex in-app browser 对任务详情页右上角三点菜单的 hover/click 不稳定。browser-act 已验证可稳定进入。

```powershell
$ba = 'C:\Users\24796\.local\bin\browser-act.exe'
$session = 'yuce-dq'
& $ba --session $session browser open chrome_local_105875626547740876 'http://47.99.48.26/#/task_detail/Ghu44PRchu' --headed
& $ba --session $session wait stable
& $ba --session $session state
& $ba --session $session hover 23
& $ba --session $session state
& $ba --session $session click 139
& $ba --session $session wait stable
```

实测结果：

- `hover 23` 展开任务详情页右上角三点菜单。
- `click 139` 点击菜单项 `数据质量检查`。
- 页面打开 `质量管理` 抽屉。

## 已确认接口

- 规则列表：`POST /api/dqr/list/dataQualityRule`
- 表规则模板：`GET /api/dqr/list/dataQualityRuleCode?ruleType=1&batch=0`
- 新增/编辑规则：`POST /api/dqr/edit/dataQualityRule`

规则列表请求示例：

```json
{
  "tableId": "Ghu44PRchu",
  "sourceEnum": "TASK"
}
```

## 已确认模板参数

- `单日行数，固定值`：`ruleCode=tableDayRegular`
- `statisticsEnd=1`：T-1 / 昨天
- `queryConditionType=GT`：大于
- `endTask=0`：异常只告警、不阻断任务

## 已配置规则记录

- 任务：`Ghu44PRchu`
- 表：`DWS_抖音_SPU销售明细(dws_douyin_spu_sales_detail)`
- BI tableId：`nM34Tlww6y00`
- 规则：`单日行数，固定值`
- 日期字段：`支付时间(pay_time)`
- 统计日期：T-1 / 昨天
- 阈值：计算值 > 0
- 异常阻断：关闭
- 平台返回规则 id：`42Q35SSEyf`

## 批量配置原则

后续批量配置时，browser-act 只用于登录态验证、UI 抽查和接口发现；正式批量新增/编辑规则优先走 `/api/dqr/edit/dataQualityRule`，避免依赖 UI hover 和表单点击。
