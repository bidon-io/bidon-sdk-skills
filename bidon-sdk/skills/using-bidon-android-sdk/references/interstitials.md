# Interstitials

> To load an interstitial ad, create a `Interstitial` instance.
Important: for a single instance of an InterstitialAd, `load()`
and `show()` can only be called once. 
Create new instance for every new interstitial ad.

## Loading an Interstitial Ad

```kotlin
val interstitial = InterstitialAd(
    // Auction Keys correspond to the Auction Configurations that you can create in the Bidon Admin Panel
    auctionKey = "AUCTION_KEY" // optional
)
```

Set `InterstitialListener` for receiving all-related events, including loading/displaying and revenue callbacks.

```kotlin
interstitial.setInterstitialListener(object : InterstitialListener {
    override fun onAdLoaded(ad: Ad, auctionInfo: AuctionInfo) {
        // ready to show
    }

    override fun onAdLoadFailed(auctionInfo: AuctionInfo?, cause: BidonError) {
    }

    override fun onAdShowFailed(cause: BidonError) {
    }

    override fun onAdShown(ad: Ad) {
    }

    override fun onAdClicked(ad: Ad) {
    }

    override fun onAdClosed(ad: Ad) {
    }

    override fun onAdExpired(ad: Ad) {
    }

    override fun onRevenuePaid(ad: Ad, adValue: AdValue) {
        // adValue.revenue - ad revenue from mediation
    }
})
interstitial.loadAd(activity = activity, pricefloor = pricefloor) // or use BidonSdk.DefaultPricefloor
```

## Displaying interstitial ad

```kotlin
if (interstitial.isReady()) {
    interstitial.showAd(activity = activity)
}
```

## Destroying Ad

Destroy the interstitial ad when it's no longer needed.

```kotlin
interstitial.destroyAd()
```
