# Agent Infrastructure Sync

## Source Layout

The source of this shared skill is:

```text
D:\AGENT_RESOURCE\skills\vipin\workstation-maintenance
```

`D:\agent-resources` is a compatibility junction to the same shared source.

Expose it to agents through junctions or symlinks:

```text
D:\devtools\codex\home\skills\workstation-maintenance
D:\devtools\claude\skills\workstation-maintenance
```

Do not keep independent copies under `D:\devtools`; devtools should expose the shared source rather than owning a second version.

## Documentation To Update Together

When changing workstation maintenance behavior, update the relevant files in the same turn:

- `D:\AGENT_RESOURCE\README.md`
- `D:\AGENT_RESOURCE\SKILL-INDEX.md`
- `D:\devtools\README.md`
- `D:\Research\WEIPING_WIKI\AGENTS.md`
- `D:\Research\WEIPING_WIKI\README.md`
- `D:\Research\WEIPING_WIKI\CLAUDE.md`
- `D:\Research\WEIPING_WIKI\.opencode\OPENCODE.md`
- `D:\Research\WEIPING_WIKI\.claude\skills\README-skills-layout.md`
- `weiping-wiki` / compatibility `vipin-wiki` skill files
- relevant `wiki/` pages, `wiki/index.md`, `wiki/log.md`, and `wiki/catalog.json`

## Commit Boundaries

Commit repositories separately:

- `AGENT_RESOURCE` / `agent-resources`: shared skill source and index/README.
- `devtools`: junction ignore rules and devtools documentation only.
- `WEIPING_WIKI`: wiki, agent docs, and weiping-wiki skill updates only.

Do not stage unrelated dirty files in `D:\devtools`, especially agent settings, automations, caches, or unrelated skills.

## Agentic Method Roots

`D:\AGENTIC_SCIENCE` is a protected record-only root. It can provide UUPF for offline audit/planning of this skill, but raw UUPF run directories and generated reports belong under ignored task-local output such as `.wiki-tmp\uupf-runs\` unless manually curated.
