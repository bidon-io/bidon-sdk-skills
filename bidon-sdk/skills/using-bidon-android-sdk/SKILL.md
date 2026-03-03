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

Server-side auction SDK for Android ad monetization — standalone, AppLovin MAX mediation, or LevelPlay (ironSource) mediation. Min API 23.

For term definitions (eCPM, price floor, postbid, demand source, etc.), see [references/glossary.md](references/glossary.md).

## Guardrails

Enforce these rules in every code suggestion. Violations cause silent failures.

**Single-use instances** — every ad object (BannerView, BannerManager, InterstitialAd, RewardedAd) supports exactly one load→show cycle. Create a new instance for each request. A second `loadAd()` on the same instance silently fails.

**Initialization order** — regulations → `registerDefaultAdapters()` → `initialize()`. Ad networks read consent during init and ignore later changes. `registerDefaultAdapters()` discovers adapters on the classpath — the adapter dependencies must already be in build.gradle or the call silently registers nothing.

```kotlin
// 1. Regulations first (only set the ones the user needs — omit the rest)
// GDPR example (only if user needs GDPR):
BidonSdk.regulation.gdpr = Gdpr.Applies
// COPPA example (only if user needs COPPA):
BidonSdk.regulation.coppa = Coppa.No
// CCPA example (only if user needs CCPA):
BidonSdk.regulation.usPrivacyString = "1YNN"
// 2. Register adapters
BidonSdk.registerDefaultAdapters()
// 3. Initialize last
BidonSdk
    .setBaseUrl("https://YOUR_BIDON_SERVER_DOMAIN.com")
    .setInitializationCallback { /* ready */ }
    .initialize(context = activity, appKey = "APP_KEY")
```

**Reward null-safety** — `onUserRewarded(ad, reward)` — `reward` can be null. Always null-check: `reward?.let { ... }`.

**Listener before load** — set the listener before calling `loadAd()`. A late listener misses callbacks.

**Postbid price floor** — `priceFloor = levelPlayRevenue * 1000 + 0.01` (USD → CPM + strict-win offset).

**Pin dependency versions** — never use `+` as a version in build.gradle. The `+` in reference docs is a placeholder. Check the project's existing versions or the latest from the Bidon maven repository. If unknown, ask the user.

## Showing Ads

All ad objects are single-use. One load→show cycle per instance. Create a new instance for each request.

### Banner — BannerView

Layout-based banner. User controls placement via XML or Compose.

```kotlin
val banner = BannerView(context = context, auctionKey = "AUCTION_KEY")
banner.setBannerFormat(BannerFormat.Banner) // Banner | LeaderBoard | MRec | Adaptive
banner.setBannerListener(object : BannerListener {
    override fun onAdLoaded(ad: Ad, auctionInfo: AuctionInfo) { /* ready to show */ }
    override fun onAdLoadFailed(auctionInfo: AuctionInfo?, cause: BidonError) {}
    override fun onAdShown(ad: Ad) {}
    override fun onAdShowFailed(cause: BidonError) {}
    override fun onAdClicked(ad: Ad) {}
    override fun onAdExpired(ad: Ad) {}
    override fun onRevenuePaid(ad: Ad, adValue: AdValue) {}
})
banner.loadAd(activity = activity, pricefloor = BidonSdk.DefaultPricefloor)

// When ready
if (banner.isReady()) banner.showAd(activity = activity)

// Cleanup
banner.destroyAd(activity = activity)
```

Full API → [references/banners.md](references/banners.md)

### Banner — BannerManager

Floating overlay banner at a predefined screen position. No layout changes needed.

```kotlin
val banner = BannerManager(auctionKey = "AUCTION_KEY")
banner.setBannerFormat(BannerFormat.Banner) // Banner | LeaderBoard | MRec | Adaptive
banner.setPosition(BannerPosition.HorizontalBottom) // HorizontalTop | HorizontalBottom | VerticalLeft | VerticalRight
banner.setBannerListener(object : BannerListener {
    override fun onAdLoaded(ad: Ad, auctionInfo: AuctionInfo) { /* ready to show */ }
    override fun onAdLoadFailed(auctionInfo: AuctionInfo?, cause: BidonError) {}
    override fun onAdShown(ad: Ad) {}
    override fun onAdShowFailed(cause: BidonError) {}
    override fun onAdClicked(ad: Ad) {}
    override fun onAdExpired(ad: Ad) {}
    override fun onRevenuePaid(ad: Ad, adValue: AdValue) {}
})
banner.loadAd(activity = activity, pricefloor = BidonSdk.DefaultPricefloor)

if (banner.isReady()) banner.showAd(activity = activity)
banner.destroyAd()
```

Full API → [references/banner-manager.md](references/banner-manager.md)

### Interstitial

Full-screen ad shown between content transitions.

```kotlin
val interstitial = InterstitialAd(auctionKey = "AUCTION_KEY")
interstitial.setInterstitialListener(object : InterstitialListener {
    override fun onAdLoaded(ad: Ad, auctionInfo: AuctionInfo) { /* ready to show */ }
    override fun onAdLoadFailed(auctionInfo: AuctionInfo?, cause: BidonError) {}
    override fun onAdShown(ad: Ad) {}
    override fun onAdShowFailed(cause: BidonError) {}
    override fun onAdClicked(ad: Ad) {}
    override fun onAdClosed(ad: Ad) {}
    override fun onAdExpired(ad: Ad) {}
    override fun onRevenuePaid(ad: Ad, adValue: AdValue) {}
})
interstitial.loadAd(activity = activity, pricefloor = BidonSdk.DefaultPricefloor)

if (interstitial.isReady()) interstitial.showAd(activity = activity)
interstitial.destroyAd()
```

Full API → [references/interstitials.md](references/interstitials.md)

### Rewarded

Full-screen ad with reward callback. `reward` can be null — always null-check.

```kotlin
val rewarded = RewardedAd(auctionKey = "AUCTION_KEY")
rewarded.setRewardedListener(object : RewardedListener {
    override fun onAdLoaded(ad: Ad, auctionInfo: AuctionInfo) { /* ready to show */ }
    override fun onAdLoadFailed(auctionInfo: AuctionInfo?, cause: BidonError) {}
    override fun onAdShown(ad: Ad) {}
    override fun onAdShowFailed(cause: BidonError) {}
    override fun onAdClicked(ad: Ad) {}
    override fun onAdClosed(ad: Ad) {}
    override fun onAdExpired(ad: Ad) {}
    override fun onUserRewarded(ad: Ad, reward: Reward?) {
        reward?.let { /* grant reward */ }
    }
    override fun onRevenuePaid(ad: Ad, adValue: AdValue) {}
})
rewarded.loadAd(activity = activity, pricefloor = BidonSdk.DefaultPricefloor)

if (rewarded.isReady()) rewarded.showAd(activity = activity)
rewarded.destroyAd()
```

Full API → [references/rewarded.md](references/rewarded.md)

## Tracking Ad Revenue

Each ad listener includes `onRevenuePaid`. Wire it to your analytics platform:

```kotlin
override fun onRevenuePaid(ad: Ad, adValue: AdValue) {
    // adValue.adRevenue  — Double, revenue in USD
    // adValue.currency   — String, always "USD"
    // adValue.precision  — Precision enum
    sendToAnalytics(adValue.adRevenue, adValue.currency, adValue.precision)
}
```

Full API → [references/ad-revenue.md](references/ad-revenue.md)

## Deployment Modes

- **Standalone** (Bidon only, no mediation) → [integrating.md](integrating.md)
- **AppLovin MAX mediation** → [using-with-applovin-max.md](using-with-applovin-max.md)
- **LevelPlay mediation** (ironSource) → [using-with-levelplay.md](using-with-levelplay.md)
- **Postbid** (Bidon competing against LevelPlay) → [postbid-vs-levelplay.md](postbid-vs-levelplay.md)

## Troubleshooting

First check the user's code against each rule in **Guardrails** — most issues come from violating one.

**Ads not loading?**
→ Check init order: regulations → adapters → initialize()
→ Check adapters are registered
→ Check network connectivity and server URL

**Ads show once then stop?**
→ Check: creating new instance for each load/show cycle?
→ All ad formats are single-use

**Regulations not applied?**
→ Check: set BEFORE initialize()?
→ Setting after init is silently ignored

**Reward is null?**
→ reward param in onUserRewarded can be null
→ Always use reward?.let { ... }

**No revenue callbacks?**
→ Check: onRevenuePaid implemented in listener?
→ Check: listener set before loadAd()?

**Postbid always falls back?**
→ Check price floor formula: * 1000 + 0.01
→ Wrong multiplier = floor too high or too low

**Banner not visible?**
→ BannerView: added to layout? showAd() called?
→ BannerManager: setPosition() called?

If issue persists, enable verbose logging and test mode:

```kotlin
BidonSdk.setLoggerLevel(Logger.Level.Verbose)
BidonSdk.setTestMode(isTestMode = true)
```

## References

### Getting started
**Integration**: Repository, dependencies, adapters, initialization → See [references/integration.md](references/integration.md)
**Adapters**: Manual adapter registration (alternative to registerDefaultAdapters()) → See [references/adapters.md](references/adapters.md)

### Ad formats
**BannerView**: Layout-based banner (user controls placement via XML/Compose) → See [references/banners.md](references/banners.md)
**BannerManager**: Floating overlay banner at predefined position → See [references/banner-manager.md](references/banner-manager.md)
**Interstitials**: Full-screen ads between content transitions → See [references/interstitials.md](references/interstitials.md)
**Rewarded**: Full-screen ads with reward callback → See [references/rewarded.md](references/rewarded.md)

### Mediation
**AppLovin MAX**: Custom network setup, placement JSON → See [references/applovin-max.md](references/applovin-max.md)
**LevelPlay**: ironSource adapter, network key, consent keys → See [references/level-play.md](references/level-play.md)
**Postbid**: Bidon competing against LevelPlay eCPM → See [references/postbid-for-levelplay.md](references/postbid-for-levelplay.md)

### Configuration
**Regulations**: GDPR, COPPA, CCPA consent flags → See [references/regulations.md](references/regulations.md)
**Ad Revenue**: Impression-level revenue tracking (AdValue, onRevenuePaid) → See [references/ad-revenue.md](references/ad-revenue.md)
**Extras**: Key-value pairs on SDK or individual ad requests → See [references/extra.md](references/extra.md)
**Segments**: User segmentation attributes (age, gender, level) → See [references/segments.md](references/segments.md)
**Win/Loss**: Auction result notifications for parallel SDK usage → See [references/winloss.md](references/winloss.md)
**Glossary**: Term definitions for auction, pricing, and mediation concepts → See [references/glossary.md](references/glossary.md)

### Quick search

```bash
grep -i "pricefloor" references/*.md
grep -i "listener" references/banners.md references/interstitials.md references/rewarded.md
grep -i "consent" references/regulations.md references/level-play.md
```

## Quick Reference

### Banner Sizes

| BannerFormat | Size | Use |
|---|---|---|
| `Banner` | 320 x 50 | Phones |
| `LeaderBoard` | 728 x 90 | Tablets |
| `MRec` | 300 x 250 | Medium rectangle |
| `Adaptive` | flex x 50/90 | Flexible width |

### Regulation Enums

| API | Values |
|---|---|
| `BidonSdk.regulation.gdpr` | `Gdpr.Unknown`, `.DoesNotApply`, `.Applies` |
| `BidonSdk.regulation.coppa` | `Coppa.Unknown`, `.No`, `.Yes` |
| `BidonSdk.regulation.usPrivacyString` | 4-char IAB string (e.g. `"1YNN"`) |
| `BidonSdk.regulation.gdprConsentString` | TCF consent string |

### Mediation Keys & Recommended Prices

| Mediation | Adapter dependency | Network key |
|---|---|---|
| AppLovin MAX | `com.applovin.mediation:bidon-adapter` | Adapter class: `com.applovin.mediation.adapters.BidonMediationAdapter` |
| LevelPlay | `com.ironsource.adapters:bidon-adapter` | Network key: `15c0a270d`, Publisher ID: `708010` |

Current adapter versions: `grep 'bidon-adapter:' references/applovin-max.md references/level-play.md`

**Placement JSON (first placement):**

| Format | CPM Price | JSON |
|---|---|---|
| Interstitial / Rewarded | 500 | `{"ecpm":500,"unicorn":true,"auction_key":"KEY","pricefloor_coef":1,"pricefloor_start":5}` |
| Banner / MRec | 50 | `{"ecpm":50,"unicorn":true,"auction_key":"KEY","pricefloor_coef":1,"pricefloor_start":2}` |

Subsequent MAX placements: `{"ecpm": <price>}`. LevelPlay subsequent placements: set `should_load: false`.

See references/glossary.md for placement JSON field definitions (`pricefloor_coef`, `pricefloor_start`, `auction_key`).

### AdValue Fields

| Field | Type | Description |
|---|---|---|
| `adRevenue` | `Double` | Revenue in USD |
| `currency` | `String` | Always `"USD"` |
| `precision` | `Precision` | Revenue precision enum |

### LevelPlay Consent Keys

```kotlin
val BIDON_CA_NETWORK_KEY = "15c0a270d"
val BIDON_GDPR_KEY = "BidonCA_GDPR"     // Boolean
val BIDON_CCPA_KEY = "BidonCA_CCPA"     // Boolean
val BIDON_COPPA_KEY = "BidonCA_COPPA"   // Boolean
```

Pass via `IronSource.setNetworkData(BIDON_CA_NETWORK_KEY, jsonObject)`. See [references/level-play.md](references/level-play.md).

### Listener Callbacks

All ad formats share: `onAdLoaded`, `onAdLoadFailed`, `onAdShowFailed`, `onAdShown`, `onAdClicked`, `onAdExpired`, `onRevenuePaid`.
- InterstitialListener / RewardedListener add `onAdClosed`
- RewardedListener adds `onUserRewarded(ad, reward)`
