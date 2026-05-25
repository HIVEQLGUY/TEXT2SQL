# Prototype Archive 2026-05-23

This directory contains the earlier lightweight local prototype.

Archived content:

- `app/`: standard-library HTTP server, metadata scanner, local run log, rule-based query planner.
- `web/`: local static test pages.
- `agent/`: early SQL guard implementation.
- `scripts/`: early database connection and reader provisioning scripts.

Reason for archiving:

- The first formal implementation will move toward a cleaner FastAPI + SSE + metadata database + DingTalk metadata sync architecture.
- Keeping this code under `legacy/` avoids mixing prototype logic with the new implementation while preserving useful reference code.

