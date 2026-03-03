---
description: Project structure and data flow
---

## Structure

```
.claude-plugin/marketplace.json  → Marketplace registration (owner: bidon-io)
bidon-sdk/
  .claude-plugin/plugin.json     → Plugin metadata (name, version, targets)
  skills/bidon-{android,ios,unity}/
    SKILL.md                     → Skill entry point (YAML front matter + markdown)
    agents/openai.yaml           → OpenAI Codex agent config
    references/*.md              → Auto-generated platform docs
generator/
  generate.py                    → CLI: fetches llms.txt, extracts per-platform content
  templates/                     → Jinja2 templates for SKILL.md and openai.yaml
```

## Data Flow

`docs server → llms.txt → fetch .md pages → clean MDX/extract TabItem per platform → write references/`

Shared docs (from `applovin-max/`, `level-play/` paths) are distributed to all three platforms with platform-specific `<TabItem>` content extracted.
