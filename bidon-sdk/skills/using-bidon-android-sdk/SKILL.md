---
name: using-bidon-android-sdk
description: >-
  Using, configuring, and troubleshooting Bidon SDK on Android.
  Covers Gradle dependency setup, showing banner/interstitial/rewarded ads
  (BannerView, BannerManager, InterstitialAd, RewardedAd), mediation with
  AppLovin MAX or LevelPlay (ironSource), postbid auction flow, adapter
  registration, GDPR/COPPA/CCPA consent, impression-level ad revenue tracking,
  user segments, extras, and win/loss notifications. Use when Bidon is mentioned
  with Android, Kotlin, Gradle, or build.gradle. Also use when the user asks
  about ad monetization in Android and Bidon is a project dependency. Not for
  iOS (use using-bidon-ios-sdk) or Unity (use using-bidon-unity-sdk).
---

# Using Bidon SDK on Android

Server-side auction SDK for Android ad monetization. Three deployment modes: standalone, AppLovin MAX mediation, LevelPlay mediation. Requires API 23+.

## Response Behavior

**Classify every query before responding:**

1. **Informational** — the user is asking a question or seeking understanding. Answer from this file using the Concepts section. Do not load reference files. Do not show code unless the user explicitly asks for code. Do not ask qualifying questions.

2. **Implementation** — the user is requesting action on their project, or provides project files. Ask clarifying questions if deployment mode is ambiguous. Read each reference file listed by the decision tree — you need exact constructors, listener interfaces, and method signatures. Then write code using the APIs from the references, adapted to the user's project.

**Reference files are your source material, not your output.** Read them to understand APIs, then write code adapted to the user's context. Never reproduce reference file contents verbatim.

**Do not offer unsolicited extras.** No code the user didn't ask for. No follow-up menus. No unrequested next steps.

**Example — informational:**

User: "How do I integrate Bidon SDK into my Android app?"

✅ "Integration has 4 steps: (1) add maven repo + SDK dependency, (2) set regulations before init, (3) call registerDefaultAdapters() then initialize(), (4) create ad objects and load/show/destroy per cycle. Each ad object is single-use."

❌ Asking "which deployment mode?", loading references, reproducing full Gradle setup and listener code.

**Example — implementation:**

User: "Integrate Bidon SDK into my app"

✅ Ask deployment mode (standalone / MAX / LevelPlay) → read each reference file from the decision tree → write code using exact APIs from the references (constructors, listeners, method signatures).

❌ Writing code from memory without reading the reference files. Or summarizing references instead of using their exact APIs.

## Concepts

**How Bidon works.** Bidon runs a server-side auction: the SDK sends an ad request, the server collects bids from demand sources, and returns the winning creative to the SDK. This replaces traditional client-side waterfall mediation with a single unified auction.

**Deployment modes:**

- **Standalone** — Bidon is the primary SDK. Initialize directly, register adapters, use Bidon ad objects (`InterstitialAd`, `RewardedAd`, `BannerView`, `BannerManager`). Choose when no existing mediator is in the project.
- **AppLovin MAX** — Bidon runs as a custom network inside the MAX waterfall. Add `com.applovin.mediation:bidon-adapter` dependency and configure via MAX dashboard. Choose when MAX is already the primary mediator.
- **LevelPlay standard** — Bidon runs as a custom adapter inside LevelPlay mediation via network key `15c0a270d`. Configure via LevelPlay dashboard. Choose when LevelPlay is already the primary mediator.
- **LevelPlay postbid** — LevelPlay auctions first, then Bidon competes on price. Get LevelPlay revenue → set as Bidon price floor (`revenue * 1000 + 0.01`) → show whichever wins. The `* 1000` converts dollars to milliCPM. The `+ 0.01` ensures Bidon must strictly beat LevelPlay's price. Choose when you want both SDKs competing for best yield.

**Ad lifecycle.** Every ad follows: create (with optional `auctionKey`) → set listener → load → show → destroy. Each ad object is single-use — after `showAd()`, destroy and create a new instance for the next cycle. Always pass `auctionKey` in the constructor — it maps to auction configurations in the Bidon dashboard.

**Ad formats:**

- **InterstitialAd** — full-screen ad displayed between content transitions.
- **RewardedAd** — full-screen video that grants a reward via `onUserRewarded` callback (reward can be null — guard with `?.let`).
- **BannerView** — layout-based banner whose position is controlled by XML or Compose layout placement.
- **BannerManager** — floating overlay banner whose position is set via `setPosition()`, requiring no layout changes.

**Regulations.** GDPR/COPPA/CCPA must be set before `initialize()` — ad networks read consent during init, and settings are silently ignored after. In LevelPlay mode, forward consent via `setNetworkData()` with keys `BidonCA_GDPR`, `BidonCA_CCPA`, `BidonCA_COPPA`.

## Decision Tree

```
Deployment mode? (single select)
├─ Standalone → references/integration.md, references/adapters.md
├─ AppLovin MAX
│   ├─ Standard (Bidon as custom network) → references/applovin-max.md
│   └─ FirstLook (Bidon first, MAX fallback) → [no reference yet]
├─ LevelPlay
│   ├─ Standard (Bidon as custom adapter) → references/level-play.md
│   └─ Postbid (LevelPlay first, Bidon competes) → references/postbid-for-levelplay.md

Ad formats? (MULTISELECT — Standalone, FirstLook, Postbid only)
├─ Banner → references/banners.md, references/banner-manager.md
├─ Interstitial → references/interstitials.md
└─ Rewarded → references/rewarded.md

Regulations? (MULTISELECT — all modes)
→ references/regulations.md
→ LevelPlay/Postbid: also references/level-play.md (consent passthrough)

Optional configuration?
├─ Revenue tracking → references/ad-revenue.md
├─ User segments → references/segments.md
├─ Extra key-value data → references/extra.md
└─ Win/loss notifications → references/winloss.md
```

## Critical Rules

### ✅ Always

- Set regulations **before** `initialize()` — ad networks read consent during init
- Call `registerDefaultAdapters()` **before** `initialize()` — discovers adapters on classpath
- Create a **new** ad instance for every load→show cycle — ad objects are single-use
- Set listener **before** `loadAd()` — a late listener misses callbacks
- Call `destroyAd()` after each show cycle completes
- Pin each dependency to a specific version — `+` is a placeholder, not a real version
- Ask the user which ad networks (demand sources) they use — do not assume adapters. `integration.md` lists all available adapters; add only those the user needs

### ❌ Never

- Never set regulations after `initialize()` — silently ignored
- Never reuse an ad object after `showAd()` — undefined behavior
- Never call `loadAd()` before setting the listener — misses callbacks
- Never use `* 100` for postbid price floor — must be `* 1000`

## Common Mistakes

**Init order:**

```kotlin
// ✅ DO THIS — regulations before init
BidonSdk.regulation.gdpr = Gdpr.Applies
BidonSdk.registerDefaultAdapters()
BidonSdk.initialize(context, "APP_KEY")
```

```kotlin
// ❌ DON'T DO THIS — regulations after init (silently ignored)
BidonSdk.initialize(context, "APP_KEY")
BidonSdk.regulation.gdpr = Gdpr.Applies  // too late
```

**Price floor (postbid):**

```kotlin
// ✅ DO THIS — correct multiplier
val priceFloor = levelPlayAdInfo.getRevenue() * 1000 + 0.01
```

```kotlin
// ❌ DON'T DO THIS — wrong multiplier
val priceFloor = levelPlayAdInfo.getRevenue() * 100  // floor too low
```

## Top Errors

| Problem | Cause | Fix |
|---------|-------|-----|
| Ads not loading | Wrong init order | regulations → `registerDefaultAdapters()` → `initialize()` |
| Ads not loading | Adapters not registered | Add adapter dependencies to build.gradle, call `registerDefaultAdapters()` |
| Ads not loading | Missing server URL | Call `.setBaseUrl("https://...")` before `initialize()` |
| Ads show once then stop | Reusing ad instance | Create new instance per load→show cycle |
| Regulations not applied | Set after `initialize()` | Set regulations **before** `initialize()` |
| Reward is null | Expected behavior | Guard with `reward?.let { ... }` |
| No revenue callbacks | Listener missing `onRevenuePaid` | Implement `onRevenuePaid` in listener, set listener before `loadAd()` |
| Postbid: Bidon always wins | Wrong multiplier (`* 100`) | Use `* 1000 + 0.01` |
| Postbid: Bidon never wins | Missing offset | Add `+ 0.01` to price floor |
| Banner not visible | Layout/position not set | BannerView: add to layout + `showAd()`. BannerManager: call `setPosition()` |

Enable verbose logging to diagnose:

```kotlin
BidonSdk.setLoggerLevel(Logger.Level.Verbose)
BidonSdk.setTestMode(isTestMode = true)
```

## When to Load References

| Reference | Load when |
|---|---|
| [integration.md](references/integration.md) | Fresh setup, maven repo config, adapter versions |
| [adapters.md](references/adapters.md) | Manual adapter registration, adapter class names, discovery issues |
| [applovin-max.md](references/applovin-max.md) | MAX project setup, dashboard config, custom network settings |
| [level-play.md](references/level-play.md) | LevelPlay project setup, dashboard config, consent passthrough |
| [postbid-for-levelplay.md](references/postbid-for-levelplay.md) | Postbid flow, dual-SDK init, price floor calculation |
| [banners.md](references/banners.md) | BannerView implementation, BannerListener interface, banner formats |
| [banner-manager.md](references/banner-manager.md) | BannerManager (floating overlay), position options, floating lifecycle |
| [interstitials.md](references/interstitials.md) | Interstitial ads, InterstitialListener interface |
| [rewarded.md](references/rewarded.md) | Rewarded ads, RewardedListener interface, onUserRewarded |
| [regulations.md](references/regulations.md) | GDPR/COPPA/CCPA consent, regulation enums, consent strings |
| [ad-revenue.md](references/ad-revenue.md) | Impression-level revenue tracking, AdValue fields |
| [segments.md](references/segments.md) | User segmentation, segment attributes (age, gender, level) |
| [extra.md](references/extra.md) | Extra key-value pairs per ad request |
| [winloss.md](references/winloss.md) | Win/loss auction notifications |
| [glossary.md](references/glossary.md) | Terms (eCPM, price floor, postbid), placement JSON fields |

## When another platform is needed

**Platforms**: [iOS](../using-bidon-ios-sdk) · [Unity](../using-bidon-unity-sdk)

**Official docs**: https://docs.bidon.org/
