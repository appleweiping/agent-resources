<p align="center">
  <img src="banner.png" alt="agent-resources" width="100%">
</p>

<h1 align="center">agent-resources</h1>

<p align="center">
  <strong>Curated skill library, workflow templates, and reference repositories for multi-agent AI development.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/skills-120+-orange" alt="Skills">
  <img src="https://img.shields.io/badge/repos-15-blue" alt="Repos">
  <img src="https://img.shields.io/badge/slash_commands-22-green" alt="Commands">
  <img src="https://img.shields.io/badge/license-private-red" alt="License">
</p>

---

## Overview

A curated collection of AI agent skills, workflow templates, reference implementations, and operational resources. Used by a 6-agent collaboration system (Claude Opus, Codex GPT-5.5, DeepSeek, OpenCode, Sonnet, Haiku) as a shared skill library.

Agents check this directory before starting complex tasks. If a relevant skill exists here, they use it instead of improvising.

## Structure

```
agent-resources/
├── skills/              # Installable skill collections
│   ├── vipin/           # Personal custom skills (Lark, email, frontend, paper-orchestra)
│   ├── anthropics/      # Anthropic official skills (claude-api, mcp-builder, webapp-testing)
│   ├── obra-superpowers/# Advanced workflows (debugging, TDD, parallel-agents, code-review)
│   ├── composio/        # 1000+ SaaS automation connectors
│   ├── standalone/      # Independent skills (mattpocock, nuwa-skill, deepseek-mcp)
│   ├── context-engineering-kit/  # DDD, TDD, review, reflexion, kaizen
│   └── trailofbits/     # Security audit skills
│
├── slash-commands/      # Reusable slash commands
│   ├── create-pr        # Standard PR creation flow
│   ├── fix-github-issue # Issue resolution workflow
│   ├── pr-review        # PR review checklist
│   ├── commit           # Structured commit flow
│   ├── context-prime    # Context preloading
│   ├── optimize         # Code optimization workflow
│   └── ...              # 22 total
│
├── repos/               # Reference implementations (git submodules)
│   ├── awesome-claude-code/
│   ├── awesome-ai-agents/
│   ├── context-engineering-kit/
│   ├── obra-superpowers/
│   ├── claude-memory-kit/
│   ├── OpenHands/
│   └── ...              # 15 total
│
├── references/          # Documentation and guides
│   ├── official-documentation/
│   ├── claude.md-files/
│   ├── slash-commands/
│   └── workflows-knowledge-guides/
│
├── hooks/               # Git/session hooks
├── templates/           # README and project templates
└── tools/               # Utility scripts
```

## Skill Collections

### vipin/ — Personal Custom Skills

| Skill | Purpose |
|-------|---------|
| paper-orchestra | End-to-end paper writing pipeline |
| email-assistant | Gmail automation |
| communication-assistant | Multi-platform messaging |
| frontend-design | Production UI generation |
| lark-* (11 skills) | Feishu/Lark full integration |
| chrome-automation | Browser automation |

### anthropics/ — Official Anthropic Skills

| Skill | Purpose |
|-------|---------|
| claude-api | Build Claude API applications |
| mcp-builder | Create MCP servers |
| webapp-testing | End-to-end web app testing |
| frontend-design | Anthropic's frontend patterns |
| pdf/docx/pptx/xlsx | Document generation |

### obra-superpowers/ — Advanced Workflows

| Skill | Purpose |
|-------|---------|
| systematic-debugging | Structured bug diagnosis |
| test-driven-development | TDD workflow |
| dispatching-parallel-agents | Multi-agent task distribution |
| receiving-code-review | Handle review feedback |
| requesting-code-review | Request and structure reviews |
| subagent-driven-development | Orchestrate sub-agents |

### context-engineering-kit/ — Context Engineering

| Skill | Purpose |
|-------|---------|
| ddd | Domain-Driven Design |
| tdd | Test-Driven Development |
| review | Code review methodology |
| reflexion | Self-reflection patterns |
| kaizen | Continuous improvement |
| sadd | System Architecture Design |

## Usage Rules

1. **Check before building**: Before starting any complex task, agents check this directory for existing skills.
2. **Vipin skills first**: Custom skills in `skills/vipin/` are tailored and take priority.
3. **Research uses ARIS**: Research projects use ARIS skills (installed in the project repo, not here).
4. **Download new skills**: If no existing skill fits, search GitHub for high-quality alternatives and install here.
5. **Don't duplicate**: If a skill exists here, don't reimplement it in the project.

## Related

| Resource | Location |
|----------|----------|
| ARIS Research Skills | `D:\research\Vipin's Knowledgebase\.claude\skills\aris\` |
| Shared Agent Memory | `D:\research\Vipin's Knowledgebase\memory\` |
| Agent Infrastructure | [devtools](https://github.com/appleweiping/devtools) |
| Knowledge Base | [vipin-wiki](https://github.com/appleweiping/vipin-wiki) |
