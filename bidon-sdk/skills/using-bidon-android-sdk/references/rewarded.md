# Rewarded Ad

> To load an rewarded ad, create a `RewardedAd` instance.
Important: for a single instance of an RewardedAd, `load()` and `show()`
can only be called once.
Create new instance for every new rewarded ad.

## Loading an Rewarded Ad

```kotlin
val rewarded = RewardedAd(
    // Auction Keys correspond to the Auction Configurations that you can create in the Bidon Admin Panel
    auctionKey = "AUCTION_KEY" // optional
)
```

Set `RewardedListener` for receiving all-related events,
including loading/displaying and revenue callbacks.

```kotlin
rewarded.setRewardedListener(object : RewardedListener {
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

    override fun onUserRewarded(ad: Ad, reward: Reward?) {
        // reward - contains reward data if exist
    }

    override fun onRevenuePaid(ad: Ad, adValue: AdValue) {
        // adValue.revenue - ad revenue from mediation
    }
})
rewarded.loadAd(activity = activity, pricefloor = pricefloor) // or use BidonSdk.DefaultPricefloor
```

## Displaying rewarded ad

```kotlin
if (rewarded.isReady()) {
    rewarded.showAd(activity = this)
}
```

## Destroying Ad

Destroy the rewarded ad when it's no longer needed.

```kotlin
rewarded.destroyAd()
```
