# Banners

> To load a banner, create a `BannerView` instance. 
Important: for a single instance of a banner, load() and show() can only be called once. Create new instance for every new banner (in case refreshing banner by timeout as well).

## Loading an Banners

```kotlin
val banner = BannerView(
    context = context,
    // Auction Keys correspond to the Auction Configurations that you can create in the Bidon Admin Panel
    auctionKey = "AUCTION_KEY" // optional 
)
```

Set `BannerListener` for receiving all-related events, including loading/displaying and revenue callbacks.

```kotlin
banner.setBannerListener(object : BannerListener {
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

    override fun onAdExpired(ad: Ad) {
    }

    override fun onRevenuePaid(ad: Ad, adValue: AdValue) {
        // ad.price - ad revenue from mediation
    }
})
banner.setBannerFormat(BannerFormat.Banner)
banner.loadAd(activity = activity, pricefloor = pricefloor) // or use BidonSdk.DefaultPricefloor
```

## Displaying banners
To show banner, place it to you AdContainer and invoke `showAd()`

```kotlin
if (banner.isReady()) {
    banner.showAd(activity = activity)
}
```

## Hiding Ad

Hide the banner ad.

```kotlin
banner.hideAd(activity = activity)
```

## Destroying Ad

Destroy the banner ad when it's no longer needed.

```kotlin
banner.destroyAd(activity = activity)
```

## BannerSize

| Ad View Format | Size        | Description                    |
|----------------|-------------|--------------------------------|
| Banner         | 320 x 50    | Fixed size banner for phones   |
| LeaderBoard    | 728 x 90    | Fixed size banner for pads     |
| MRec           | 300 x 250   | Fixed medium rectangle banners |
| Adaptive       | -/- x 50/90 | Flexible width banners         |
