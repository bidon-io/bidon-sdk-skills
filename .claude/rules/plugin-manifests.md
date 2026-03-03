---
description: Claude Code plugin manifest format and conventions
paths:
  - .claude-plugin/**/*
  - bidon-sdk/.claude-plugin/**/*
---

## Official Docs

- Plugin development: https://docs.anthropic.com/en/docs/claude-code/plugins
- Plugin reference: https://docs.anthropic.com/en/docs/claude-code/plugins-reference
- Marketplaces: https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces

## marketplace.json (repo root)

Registers the repo as a marketplace and lists plugins it contains.

```json
{
  "name": "marketplace-name",
  "owner": { "name": "org-name" },
  "plugins": [{
    "name": "plugin-name",
    "source": "./relative-path",
    "description": "...",
    "tags": ["..."]
  }]
}
```

## plugin.json (inside each plugin)

Plugin metadata — name, version, author, optional MCP servers.

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "...",
  "author": { "name": "...", "url": "..." },
  "homepage": "...",
  "repository": "...",
  "license": "...",
  "keywords": ["..."]
}
```

## Rules

- `.claude-plugin/` contains ONLY manifest JSON files — no skills, commands, or other components
- Use `${CLAUDE_PLUGIN_ROOT}` for paths in config (not hardcoded absolute paths)
- Use `./` relative paths in plugin.json source references
