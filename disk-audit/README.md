# Disk Audit — canonical advisory ledger for ALL agents

This folder is the **single read-first point** before any agent moves, deletes, or
cleans up a project on the D: drive. It is produced by the WEIPING_WIKI project-hardness
engine (`scripts/hardness/audit.py`, run via `python scripts/wiki.py hardness auto`).

## Files
- `projects-audit.json` — generated snapshot of every discovered project + an advisory verdict. Git history is the rotation (no dated copies).
- `overrides.json` — **human-owned**. Force `keep`/`quarantine` on specific projects. The writer reads it and never edits it.
- `README.md` — this file.

## The ONLY two verdicts
- `keep` — do not move or delete. Active project, or unknown/incomplete scan (fail-safe default).
- `quarantine` — **advisory review/move-to-staging only. NEVER a delete.** Emitted only for non-git dirs that match a scratch name pattern AND are stale (>180d) AND hold almost no code.

`safe-delete` is **never** produced by the machine. Deletion is always an explicit human decision.

## Read-first rules for agents (fail-closed)
Before ANY move/delete/cleanup of a D:-drive project:
1. **Staleness**: if `generated_at` is older than 24h, treat the ledger as STALE → do NOT delete; re-run `python scripts/wiki.py hardness auto` or escalate to the owner.
2. **Quarantine**: a `quarantine` verdict means *move to a review area at most*, then report — never delete.
3. **Absence is not permission**: if the target project is absent from this file, treat it as `keep`. Absence is NOT a license to delete.
4. Actual deletion always requires explicit human approval via the existing `workstation-maintenance` manifest / batch-approval flow.

## Record schema (per project)
`name, root, is_git, git_head, git_unpushed, code_file_count, scan_complete, last_hardened, verdict, evidence[], decided_by(heuristic|override), decided_at`.
`scan_complete:false` means the scan hit a cap / was unreadable → forced `keep`.
