# Bidon SDK Skills

Skills for using [Bidon](https://bidon.org) ad monetization SDK on Android, iOS, and Unity. Works with Claude Code and OpenAI Codex.

## Skills

| Skill | Platform | Description |
|-------|----------|-------------|
| using-bidon-android-sdk | Android | Gradle, ad formats, adapters, regulations |
| using-bidon-ios-sdk | iOS | CocoaPods/SPM, ad formats, adapters, regulations |
| using-bidon-unity-sdk | Unity | Plugin setup, ad formats, FirstLook/Postbid, regulations |

## Install

### Claude Code

```bash
# 1. Add the marketplace
/plugin marketplace add bidon-io/bidon-sdk-skills

# 2. Install the plugin
/plugin install bidon-sdk
```

### Claude Desktop

1. Download the latest zip from [Releases](https://github.com/bidon-io/bidon-sdk-skills/releases)
2. Open Cowork tab → Customize → upload the zip

### Codex

Ask Codex to install:

> Install using-bidon-android-sdk skill from bidon-io/bidon-sdk-skills

Or manually:

```bash
# Clone and skills are auto-discovered from .agents/skills/
git clone https://github.com/bidon-io/bidon-sdk-skills.git
```

## Usage

Skills activate automatically when your task matches the skill description. Just ask:

- "Add Bidon SDK to this Android project"
- "Set up banner ads with Bidon in my iOS app"
- "Configure Bidon postbid for Unity with LevelPlay"

Or invoke directly:

**Claude Code:** `/using-bidon-android-sdk`

**Codex:** `$using-bidon-android-sdk`
