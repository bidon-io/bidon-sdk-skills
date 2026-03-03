# Bidon SDK Skills

Claude Code plugin and OpenAI Codex skill repository for integrating the Bidon ad monetization SDK across Android, iOS, and Unity.

## Commands

```bash
uv sync                                                        # install dependencies
uv run generate <url> [skills...] [--output-dir DIR] [--dry-run]  # generate skill references

# Examples
uv run generate http://localhost:3000                          # all platforms
uv run generate http://localhost:3000 using-bidon-android-sdk using-bidon-ios-sdk  # specific platforms
uv run generate http://localhost:3000 --dry-run                # preview only
```
