# Runtime Verification Spec

## ADDED Requirements

### Requirement: Worker-side runtime probe

The system MUST provide a repeatable way to verify that the DolphinScheduler worker runtime can access project files, load non-secret configuration, reach Doris, and reach the Douyin OpenAPI network path.

#### Scenario: Probe runs inside the worker environment

WHEN the runtime probe is executed from the DolphinScheduler worker container
THEN it MUST report Python availability, project path availability, Doris connectivity, and external egress IP without printing secrets.

### Requirement: Scheduler command remains production-safe

The DolphinScheduler workflow command MUST run the existing framework ingestion entrypoint from the mounted project path and MUST keep credentials in `.env` or environment variables outside source code.

#### Scenario: Registered workflow is inspected

WHEN the DolphinScheduler schedule is queried through the official API
THEN the workflow `ODS_抖店订单列表接口采集__0715` MUST be ONLINE and its shell command MUST call `scripts/douyin_order_searchlist_ingest.py daily`.

### Requirement: Minimal worker-side collection proof

The system MUST prove worker-side execution with either a non-mutating probe or a narrow low-risk collection window, and MUST validate the result in Doris or the command output.

#### Scenario: Worker-side proof completes

WHEN the worker-side proof command finishes
THEN it MUST either show no-write probe success or show CONNECT/ODS validation evidence with failed pages equal to zero.
