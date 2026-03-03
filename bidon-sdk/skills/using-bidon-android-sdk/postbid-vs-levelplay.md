# Postbid: Bidon vs LevelPlay

Bidon competing against LevelPlay eCPM. LevelPlay loads first; if it succeeds, its eCPM becomes the price floor for Bidon. Show whichever wins.

Both SDKs must be initialized. Set regulations for **both** before init.

## Dual SDK Initialization

```kotlin
// Regulations for BOTH SDKs — before any init call
BidonSdk.regulation.gdpr = Gdpr.Applies
BidonSdk.regulation.coppa = Coppa.No
BidonSdk.regulation.usPrivacyString = "1YNN"

IronSource.setConsent(true)
IronSource.setMetaData("is_child_directed", "false")
IronSource.setMetaData("do_not_sell", "false")

// Initialize Bidon
BidonSdk
    .registerDefaultAdapters()
    .setBaseUrl("https://YOUR_BIDON_SERVER_DOMAIN.com")
    .setInitializationCallback { /* ready */ }
    .initialize(context, "YOUR_BIDON_APP_KEY")

// Initialize LevelPlay
LevelPlay.init(
    context = context,
    initRequest = LevelPlayInitRequest.Builder("YOUR_LEVEL_PLAY_APP_KEY").build(),
    listener = object : LevelPlayInitListener {
        override fun onInitFailed(error: LevelPlayInitError) {}
        override fun onInitSuccess(configuration: LevelPlayConfiguration) {}
    }
)
```

## Postbid Flow

### Load LevelPlay ad, extract eCPM

```kotlin
val levelPlayInterstitialAd = LevelPlayInterstitialAd("LEVEL_PLAY_AD_UNIT_ID")

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

### Load Bidon with price floor

`priceFloor = levelPlayRevenue * 1000 + 0.01` — LevelPlay returns revenue in USD, Bidon expects CPM. The `+0.01` offset guarantees Bidon must strictly beat LevelPlay.

```kotlin
var bidonInterstitial: InterstitialAd? = null

fun loadBidonInterstitial(priceFloor: Double = BidonSdk.DefaultPricefloor) {
    bidonInterstitial?.destroyAd()

    val ad = InterstitialAd("BIDON_AUCTION_KEY")
        .also { bidonInterstitial = it }

    ad.setInterstitialListener(object : InterstitialListener {
        override fun onAdLoaded(ad: Ad, auctionInfo: AuctionInfo) {}
        override fun onAdLoadFailed(auctionInfo: AuctionInfo?, cause: BidonError) {}
        override fun onAdShown(ad: Ad) {}
        override fun onAdShowFailed(cause: BidonError) {}
        override fun onAdClicked(ad: Ad) {}
        override fun onAdClosed(ad: Ad) {}
        override fun onAdExpired(ad: Ad) {}
    })

    ad.loadAd(activity = activity, pricefloor = priceFloor)
}
```

### Show winner, fallback to LevelPlay

```kotlin
when {
    bidonInterstitial?.isReady() == true -> {
        // Bidon's eCPM is guaranteed higher than LevelPlay's
        bidonInterstitial?.showAd(activity)
    }
    levelPlayInterstitialAd.isAdReady() -> {
        levelPlayInterstitialAd.showAd(activity)
    }
    else -> {
        // Neither ad loaded — skip show
    }
}
```

## Common Mistakes

- **Wrong multiplier**: `* 100` instead of `* 1000` — floor too low, Bidon always wins (defeats purpose)
- **Missing offset**: no `+ 0.01` — tied bids default to LevelPlay, Bidon never wins
- **No fallback**: if Bidon load fails and there's no fallback to LevelPlay, the ad slot is wasted
- **New instance per cycle**: Bidon ad objects are single-use — always `destroyAd()` and create a new instance

See [references/postbid-for-levelplay.md](references/postbid-for-levelplay.md) for the full reference.
