"""Skill generator — fetches docs from HTTP server, writes per-platform references."""

import argparse
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen

SHARED_DIR = Path(__file__).parent / "shared"

PLATFORMS = {"android", "ios", "unity"}
SHARED = {"applovin-max", "level-play"}
SKIP = {"changelog"}

_LINK_RE = re.compile(r"^- \[(.+?)]\((.+?)\)")


def fetch(url: str) -> str:
    """Fetch text content from URL."""
    with urlopen(url) as resp:
        return resp.read().decode()


def parse_llms_txt(text: str) -> list[tuple[str, str]]:
    """Return list of (title, url_path) from llms.txt markdown links."""
    results = []
    for line in text.splitlines():
        line = line.strip()
        m = _LINK_RE.match(line)
        if not m:
            continue
        path = urlparse(m.group(2)).path.replace("//", "/").strip("/")
        results.append((m.group(1), path))
    return results


def build_refs(entries: list[tuple[str, str]]) -> dict[str, dict[str, list[str]]]:
    """Map platform -> {ref_filename: [url_paths]}."""
    refs = {p: {} for p in PLATFORMS}

    for _title, path in entries:
        parts = path.split("/")
        slug = parts[-1].removesuffix(".md")

        if slug in SKIP:
            continue

        if len(parts) >= 4 and parts[1] == "sdk" and parts[2] in PLATFORMS:
            refs[parts[2]].setdefault(slug + ".md", []).append(path)
        elif len(parts) >= 2 and parts[1] in SHARED:
            for p in PLATFORMS:
                refs[p].setdefault(parts[1] + ".md", []).append(path)

    return refs


def clean_mdx(text: str) -> str:
    """Strip MDX artifacts: import/export statements (including blockquoted)."""
    lines = []
    for line in text.splitlines():
        bare = re.sub(r"^(?:>\s*)+", "", line).strip()
        if re.match(r"import\s+.*Tab", bare):
            continue
        if re.match(r"export\s+const\s+", bare):
            continue
        lines.append(line)
    return "\n".join(lines)


def strip_tab_tags(text: str) -> str:
    """Remove <Tabs>/<TabItem> tags but keep inner content."""
    text = re.sub(r"</?Tabs[^>]*>\s*\n?", "", text)
    text = re.sub(r"</?TabItem[^>]*>\s*\n?", "", text)
    return text.strip()


def extract_tab_content(text: str, platform: str) -> str:
    """Extract content for a specific platform from <TabItem> blocks."""
    pattern = re.compile(
        rf'<TabItem\s+value="{platform}"[^>]*>\s*\n(.*?)\n\s*</TabItem>',
        re.DOTALL,
    )
    matches = pattern.findall(text)
    if not matches:
        return strip_tab_tags(text)
    return "\n\n".join(m.strip() for m in matches)


def transform_ref(texts: list[str], platform: str, is_shared: bool) -> str:
    """Transform pre-fetched doc texts into platform-specific content."""
    parts = []
    for text in texts:
        text = clean_mdx(text)

        if is_shared and "<TabItem" in text:
            content = extract_tab_content(text, platform)
        else:
            content = strip_tab_tags(text)

        if content:
            parts.append(content)
    return "\n\n---\n\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate skill references from docs server.")
    parser.add_argument("base_url", help="Docs server URL (e.g. http://localhost:3000)")
    parser.add_argument("skills", nargs="*", help="Skills to generate (e.g. using-bidon-android-sdk). Defaults to all.")
    parser.add_argument("--output-dir", default="bidon-sdk/skills", help="Output directory (default: bidon-sdk/skills)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    output_dir = Path(args.output_dir)

    if args.skills:
        platforms = set()
        for skill in args.skills:
            platform = skill.removeprefix("using-bidon-").removesuffix("-sdk")
            if platform not in PLATFORMS:
                parser.error(
                    f"unknown skill {skill!r} "
                    f"(valid: {', '.join(f'using-bidon-{p}-sdk' for p in sorted(PLATFORMS))})"
                )
            platforms.add(platform)
    else:
        platforms = PLATFORMS

    try:
        llms_txt = fetch(f"{base_url}/llms.txt")
    except (URLError, HTTPError) as e:
        print(f"error: cannot reach {base_url}/llms.txt — {e}", file=sys.stderr)
        return 1

    entries = parse_llms_txt(llms_txt)
    refs = build_refs(entries)

    # Fetch all unique doc paths once
    all_paths = {p for items in refs.values() for srcs in items.values() for p in srcs}
    docs: dict[str, str] = {}
    for path in sorted(all_paths):
        url_path = path if path.endswith(".md") else path + ".md"
        try:
            docs[path] = fetch(f"{base_url}/{url_path}")
        except (URLError, HTTPError) as e:
            print(f"error: failed to fetch {path} — {e}", file=sys.stderr)

    errors = 0
    for platform in sorted(refs):
        if platform not in platforms:
            continue
        items = refs[platform]
        ref_dir = output_dir / f"using-bidon-{platform}-sdk" / "references"
        print(f"\n=== {platform} ({len(items)} refs) -> {ref_dir} ===")

        for name, sources in sorted(items.items()):
            missing = [s for s in sources if s not in docs]
            if missing:
                print(f"  [ERROR] {name}: missing docs for {missing}", file=sys.stderr)
                errors += 1
                continue

            is_shared = any(
                s.split("/")[1] in SHARED for s in sources if len(s.split("/")) > 1
            )
            content = transform_ref([docs[s] for s in sources], platform, is_shared)

            out = ref_dir / name
            if args.dry_run:
                print(f"  [dry-run] {name}  ({content.count('\n') + 1} lines)")
            else:
                ref_dir.mkdir(parents=True, exist_ok=True)
                out.write_text(content + "\n")
                print(f"  [ok] {name}  ({len(content)} bytes)")

    # Copy shared files into each platform's references directory
    shared_files = sorted(SHARED_DIR.glob("*.md")) if SHARED_DIR.is_dir() else []
    if shared_files:
        print(f"\n=== shared ({len(shared_files)} files) ===")
        for platform in sorted(platforms):
            ref_dir = output_dir / f"using-bidon-{platform}-sdk" / "references"
            for src in shared_files:
                dest = ref_dir / src.name
                if args.dry_run:
                    print(f"  [dry-run] bidon-{platform}/references/{src.name}")
                else:
                    ref_dir.mkdir(parents=True, exist_ok=True)
                    dest.write_text(src.read_text())
                    print(f"  [ok] bidon-{platform}/references/{src.name}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
