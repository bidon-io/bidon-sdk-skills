# Using Bidon As Level Play Mediation Postbid

## Overview

This document outlines the integration of **Bidon SDK** as a **post-bidder** alongside **LevelPlay mediation** for interstitial ad formats.

This integration enables LevelPlay to run its auction first. If LevelPlay successfully loads an ad, its eCPM will be used as a price floor for a Bidon SDK request. If Bidon returns a higher bid, the Bidon ad is displayed. Otherwise, fallback to LevelPlay.

This integration ensures:
- Monetization uplift via Bidon post-bidding
- Regulatory compliance
- Fallback logic for reliability

## Useful links

- [Level Play SDK Integration](https://developers.is.com/ironsource-mobile/android/android-sdk/)
- [Level Play Interstitial Mediation Guide](https://developers.is.com/ironsource-mobile/android/android-sdk/)
- [Level Play Regulatory Settings](https://developers.is.com/ironsource-mobile/android/regulation-advanced-settings/)
- [Bidon SDK Integration](../integration)
- [Bidon Interstitial Ads](../ad-formats/interstitials)
- [Bidon Regulations](./regulations)

## Requirements

- **LevelPlay SDK**: `com.unity3d.ads-mediation:mediation-sdk:8.10.0`
- **Bidon SDK**: <code>org.bidon:bidon-sdk:{androidVersion}</code>
- **Android minSdkVersion: 23**

## Setup

### Configure Repositories and Dependencies

Add `Bidon` and `LevelPlay` Maven repositories to your `build.gradle`:
```kotlin
repositories {
  maven { url = uri("https://android-sdk.is.com/") }            // LevelPlay artifacts
  maven { url = uri("https://artifactory.bidon.org/bidon") }    // Bidon artifacts
}
```

Then declare both SDKs and their respective adapters in your module dependencies:

```kotlin
dependencies {
  // LevelPlay core
  implementation("com.unity3d.ads-mediation:mediation-sdk:8.10.0")
  // Include all required LevelPlay adapters (e.g., AdColony, Vungle, Unity)

  // Bidon core
  implementation("org.bidon:bidon-sdk:0.13.0")
  // Exclude Bidon adapters that you do not use in your application
  implementation("org.bidon:admob-adapter:+")
  implementation("org.bidon:amazon-adapter:+")
  implementation("org.bidon:applovin-adapter:+")
  implementation("org.bidon:bidmachine-adapter:+")
  implementation("org.bidon:bigoads-adapter:+")
  implementation("org.bidon:chartboost-adapter:+")
  implementation("org.bidon:dtexchange-adapter:+")
  implementation("org.bidon:gam-adapter:+")
  implementation("org.bidon:inmobi-adapter:+")
  implementation("org.bidon:meta-adapter:+")
  implementation("org.bidon:mintegral-adapter:+")
  implementation("org.bidon:mobilefuse-adapter:+")
  implementation("org.bidon:unityads-adapter:+")
  implementation("org.bidon:vkads-adapter:+")
  implementation("org.bidon:vungle-adapter:+")
  implementation("org.bidon:yandex-adapter:+")
}
```

:::info Important
Missing adapters will result in incomplete demand and degraded fill rates. Ensure all mediation networks used by Bidon and LevelPlay are properly declared.
:::

### Configure Privacy and Regulatory Parameters

Both SDKs must be configured for compliance before they are initialized. These values must be set **early in the app lifecycle** (e.g., before `onCreate()` completes).

```kotlin
// Bidon
BidonSdk.regulation.gdpr = Gdpr.Applies                // For GDPR
BidonSdk.regulation.coppa = Coppa.No                   // For COPPA
BidonSdk.regulation.usPrivacyString = "1YNN"           // For CCPA

// LevelPlay
IronSource.setConsent(true)                            // For GDPR
IronSource.setMetaData("is_child_directed", "false")   // For COPPA
IronSource.setMetaData("do_not_sell", "false")         // For CCPA
```

:::info Important
These flags should reflect your own consent management logic.
If a CMP is used, synchronize these values with the output of that system.
:::

### Initialize Bidon and LevelPlay SDKs
Initialize the SDKs **after** setting all required regulation flags. Always initialize Bidon first if you plan to preload demand in parallel.
```kotlin
// Initialize Bidon SDK
BidonSdk
  .registerDefaultAdapters()
  .setBaseUrl("https://your.bidon.server")
  .setInitializationCallback { /* Initialized */ }
  .initialize(context, "YOUR_BIDON_APP_KEY")

// Initialize LevelPlay SDK
LevelPlay.init(
  context = context,
  initRequest = LevelPlayInitRequest.Builder("YOUR_LEVEL_PLAY_APP_KEY").build(),
  listener = object : LevelPlayInitListener {
    override fun onInitFailed(error: LevelPlayInitError) { /* Initialization Failed */ }
    override fun onInitSuccess(configuration: LevelPlayConfiguration) { /* Initialized */ }
  }
)
```

:::note
SDK initialization should happen **only once**, ideally during the `Application` class.
:::

## Interstitial Post-Bid Flow

### Step 1: Load LevelPlay Interstitial and Determine Price Floor
LevelPlay should always load its ad first, allowing you to extract its eCPM for use as a floor in the Bidon auction.

```kotlin
val levelPlayInterstitialAd = LevelPlayInterstitialAd("LEVEL_PLAY_INTERSTITIAL_AD_UNIT_ID")

levelPlayInterstitialAd.setListener(object : LevelPlayInterstitialAdListener {
    override fun onAdLoaded(levelPlayAdInfo: LevelPlayAdInfo) {
        val priceFloor = levelPlayAdInfo.getRevenue() * 1000 + 0.01
        loadBidonInterstitial(priceFloor)
    }
    override fun onAdLoadFailed(levelPlayAdError: LevelPlayAdError) {
        loadBidonInterstitial(BidonSdk.DefaultPricefloor)
    }
    override fun onAdDisplayed(levelPlayAdInfo: LevelPlayAdInfo) {}
    override fun onAdDisplayFailed(levelPlayAdError: LevelPlayAdError, levelPlayAdInfo: LevelPlayAdInfo) {}
    override fun onAdClicked(levelPlayAdInfo: LevelPlayAdInfo) {}
    override fun onAdClosed(levelPlayAdInfo: LevelPlayAdInfo) {}
    override fun onAdInfoChanged(levelPlayAdInfo: LevelPlayAdInfo) {}
})

levelPlayInterstitialAd.loadAd()
```

:::note Why `*1000 + 0.01`?
LevelPlay returns revenue in USD. Bidon expects the floor price in micro-USD (i.e., CPM). The +0.01 offset guarantees that a bid must strictly beat the LevelPlay offer.
:::

### Step 2: Load Bidon Interstitial With Price Floor
Once the LevelPlay eCPM is available (or default fallback is needed), load Bidon with the calculated floor.

```kotlin
var bidonInterstitial: InterstitialAd? = null

fun loadBidonInterstitial(priceFloor: Double = BidonSdk.DefaultPricefloor) {
    bidonInterstitial?.destroyAd()

    val bidonInterstitial = InterstitialAd("BIDON_INTERSTITIAL_AUCTION_KEY")
            .also { bidonInterstitial = it }

    bidonInterstitial.addExtra("mediation_mode", "post_bid_level_play")
    bidonInterstitial.setInterstitialListener(object :InterstitialListener {
        override fun onAdLoaded(ad: Ad, auctionInfo: AuctionInfo) {}
        override fun onAdLoadFailed(auctionInfo: AuctionInfo?, cause: BidonError) {}
        override fun onAdExpired(ad: Ad) {}
        override fun onAdShown(ad: Ad) {}
        override fun onAdShowFailed(cause: BidonError) {}
        override fun onAdClicked(ad: Ad) {}
        override fun onAdClosed(ad: Ad) {}
    })

    bidonInterstitial.loadAd(activity = activity, pricefloor = priceFloor)
}
```
:::tip
You can preload both SDKs during gameplay or app flow to reduce latency before show.
:::

### Step 3: Show Interstitial with Fallback Logic
After both LevelPlay and Bidon SDKs attempt to load their interstitials, the final decision of which ad to show must follow post-bidding logic.

The Bidon interstitial should only be shown if it has successfully loaded and returned a bid that meets or exceeds the price floor derived from LevelPlay's eCPM. This ensures that the Bidon ad provides **higher value**.

```kotlin
when {
    bidonInterstitial.isReady() -> {
        /**
         * If the Bidon ad is ready, it is guaranteed that Bidon's eCPM is higher than LevelPlay's.
         */
        bidonInterstitial.showAd(activity)
    }
    levelPlayInterstitialAd.isAdReady() -> {
        levelPlayInterstitialAd.showAd(activity)
    }
    else -> {
        // Neither ad loaded – skip show
    }
}
```

## Best Practices
- **Accurately calculate the price floor**: Use the formula `eCPM * 1000 + 0.01` to avoid price floor conflicts and ensure Bidon’s bids remain competitive.
- **Destroy previous interstitial instances before loading new ones**: Always call `destroyAd()` for both Bidon and LevelPlay interstitials before reloading to prevent memory leaks and show conflicts.
- **Manage the Activity context properly**: Pass a valid `Activity` context when loading and showing ads, especially after screen transitions or orientation changes.
- **Handle `onAdLoadFailed` properly**: If Bidon fails to load an ad, ensure a fallback to LevelPlay is implemented without delay.
- **Avoid hard-coded values**: Use constants, `BuildConfig`, or secure storage for App Keys, Auction IDs, and other sensitive parameters.
- **Set all regulatory flags before SDK initialization**: GDPR, COPPA, CCPA, and GPP flags must be configured before calling `initialize()` otherwise, they may be ignored by ad networks.
