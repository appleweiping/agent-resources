# Computer Junk Audit — advisory (read with `projects-audit.json`)

Generated 2026-06-15 by agent (Claude Opus). **Advisory only. Nothing here authorizes a
delete.** Quarantine = move to `D:\_MIGRATION_QUARANTINE_20260614\` (reversible), never
hard-delete. Pair with `projects-audit.json` (per-project keep/quarantine ledger).

## Read-first rule for all agents
Before cleaning/CRUD-ing files on C:/D:, read THIS file + `projects-audit.json`. Only remove
items in "Safe — already quarantined this session" or obvious regenerable caches. Everything in
"Flagged — owner decision" requires explicit owner approval (large/ambiguous/possibly-unique data).

## Safe — already cleaned/quarantined this session (reversible)
| Item | Action | Where |
|---|---|---|
| `AI for Science`, `project chat records`, `文件管理`, `新建文件夹` (empty dirs) | quarantined | `_MIGRATION_QUARANTINE_20260614\research-empty-dirs\` |
| `truce-auto.tar.gz` (0 bytes) | quarantined | `…\research-junk\` |
| `offline_pkgs_pony75`, `…_linux`, `…_linux.zip` (package caches) | relocated | `D:\Cache\offline-packages\` |
| `D:\Research\OpenViking` (verified identical dup of `AGENT_RESOURCE\repos\OpenViking`) | deduped (consolidated to canonical) | old path now a junction |
| WEIPING_WIKI incomplete source residual (migration leftover) | quarantined | `…\WEIPING_WIKI_residual_incomplete\` |

## Flagged — OWNER DECISION required (not touched)
| Item | Size | Why flagged |
|---|---|---|
| `D:\Research\UncertaintyProtein-AI4S.zip` | 7.3 GB | May hold data/checkpoints NOT in the `-archived` git repo; verify contents before any delete. |
| `D:\_MIGRATION_QUARANTINE_20260614\` | 4.3 GB | This session's reversible safety net (migration residual + cleaned junk). Safe to purge AFTER you confirm nothing broke (a few days). |
| `D:\Research\vipin's` | ~5.7 GB | Real Chrome browser profile (NOT the symlink) — leave; may be an active profile. |
| git-bearing non-research repos already relocated | — | Agent-Gamedevelopmentstudio/Origin/Prompt wiki → AGENTIC_SCIENCE; OpenViking/llm-wiki-skill-ref → AGENT_RESOURCE\repos. Junction-bridged. |

## Regenerable caches (low value; remove anytime, they regenerate)
`__pycache__`, `.pytest_cache`, `.ruff_cache`, `.mypy_cache`, `.ipynb_checkpoints`, `*.pyc`.
Not auto-removed (touch active projects, regenerate instantly). `D:\AGENTIC_SCIENCE\WEIPING_WIKI\.wiki-tmp\quartz`
(~453 MB) is the Quartz build cache — the site build recreates it; safe to delete if reclaiming space.

## Temp roots (small; routine)
`D:\temp` ~90 MB, `D:\tmp` ~20 MB, `D:\OneDriveTemp` ~0 MB. No action taken.

## Standing mechanism
- **Projects**: `python scripts/wiki.py hardness auto` refreshes `projects-audit.json` (the `\WeipingHardnessAutoDaily` daily task).
- **Junk**: re-run a bounded junk pass and refresh this file periodically. Never full-disk recursive scans (CPU); target known junk roots + caches.
- **Hard rule**: no deletion without explicit owner approval; `D:\Research` resolved paths are a no-move boundary except where the owner explicitly directed (this session: weiping family + dep-safe caches).
