# Skill Provenance Audit - 2026-06-01

This audit records local skill additions that are present in the working tree but are not yet safe to publish or route implicitly.

## Current Decision

Do not commit newly discovered skill packs until each pack has:

- an upstream repository or author/provenance record
- a license compatible with public redistribution
- a strict secret scan
- a clear routing entry in `SKILL-INDEX.md`
- bulky/generated/cache artifacts excluded

## Findings

| Path | Status | Evidence | Decision |
| --- | --- | --- | --- |
| `skills/game-studios/` | Untracked, not provenance-cleared | Many `SKILL.md` files; no top-level README/LICENSE found in the local copy. | Keep local-only until origin and license are confirmed. |
| `skills/godogen/` | Untracked, not provenance-cleared | Contains `godogen` and `godot-api` skills/scripts; no top-level README/LICENSE found in the local copy. | Keep local-only until origin and license are confirmed. |
| `skills/standalone/nuwa-skill/` | Known upstream, not yet curated for this repo | Git remotes show `appleweiping/nuwa-skill` and `alchaincyf/nuwa-skill`; local copy includes MIT license plus generated examples/assets and `__pycache__`. | Publish only after selecting the intended subset and excluding caches/generated artifacts. |

## Public Routing Rule

Implicit routing may reference only committed, provenance-cleared skills. Untracked skill folders are available for local inspection but should not be treated as public-safe installed capabilities.
