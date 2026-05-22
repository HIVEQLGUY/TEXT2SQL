# Project Workflow

## Roles

- Codex handles implementation, local tests, branch management, commits, and PR preparation.
- The project owner confirms database operations, GitHub login, production secrets, and business metric definitions.
- Business users should use the final web app or approved MCP client, not the administrator database account.

## Branching

- `main` or `master` is the stable branch.
- Feature work uses `codex/<topic>` branches.
- One branch should represent one coherent milestone, such as `codex/bootstrap-foundation` or `codex/text2sql-prototype`.

## Commit Timing

Codex should commit after meaningful, verified milestones:

- database access foundation is complete;
- SQL review guard is implemented and tested;
- local web prototype can run;
- schema scanner or Text2SQL logic changes pass test cases.

The owner does not need to manually decide branch strategy. The owner should review before pushing to shared remotes or merging.

## GitHub Setup Options

Preferred:

1. Install GitHub CLI.
2. Run `gh auth login`.
3. Create a private GitHub repository.
4. Add it as `origin`.
5. Push the current branch.

Fallback:

1. Create a private repository on github.com manually.
2. Provide the repository HTTPS URL.
3. Codex runs `git remote add origin <url>`.
4. Codex pushes and the owner completes browser-based Git authentication if prompted.

## Secret Handling

- `.env`, `.env.admin`, and `.env.reader` are local-only files.
- `.env.example` or `*.example.env` may be committed without real passwords.
- Administrator credentials are only used by explicit maintenance scripts.
- Application queries must use the read-only account by default.
