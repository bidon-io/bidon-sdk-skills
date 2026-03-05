# BannerManager

> The `BannerManager` interface offers methods for integrating banner advertisements into your Android application. This
documentation will walk you through the integration process and explain the available functions.

## Creating instance 

The `BannerManager` interface is designed for integrating banner advertisements into your Android application.
Create an instance of the `BannerManager` interface and use its methods to load and display banner ads.

```kotlin
val banner = BannerManager(
    // Auction Keys correspond to the Auction Configurations that you can create in the Bidon Admin Panel
    auctionKey = "AUCTION_KEY" // optional
)
```

## Banner position  

### Predefined Banner Positions

```kotlin
fun setPosition(position: BannerPosition)
```

The `BannerPosition` enum represents different positions where banner advertisements can be displayed within an Android
application. It offers four possible banner positions, each serving a unique purpose:

- `HorizontalTop`: This position places the banner at the top of the screen, typically spanning horizontally.

- `HorizontalBottom`: This position places the banner at the bottom of the screen, typically spanning horizontally.

- `VerticalLeft`: This position places the banner on the left side of the screen, typically spanning vertically.

- `VerticalRight`: This position places the banner on the right side of the screen, typically spanning vertically.

#### Default Banner Position

### Custom Position

Set a custom position for the banner. You can specify the top-left offset in pixels, rotation in degrees, and the anchor point in
relative coordinates (0 to 1, starting from the top-left corner).

```kotlin
fun setCustomPosition(offset: Point, rotation: Int, anchor: PointF)
```

### BannerFormat 

Set the desired banner format.

```kotlin
fun setBannerFormat(bannerFormat: BannerFormat)
```

| Ad View Format | Size        | Description                    |
|----------------|-------------|--------------------------------|
| Banner         | 320 x 50    | Fixed size banner for phones   |
| LeaderBoard    | 728 x 90    | Fixed size banner for pads     |
| MRec           | 300 x 250   | Fixed medium rectangle banners |
| Adaptive       | -/- x 50/90 | Flexible width banners         |

### BannerListener 

Set a listener to receive callbacks for banner ad events.

```kotlin
fun setBannerListener(listener: BannerListener?)
```

### Loading Ad 

Load the banner ad. You should provide the current `Activity` where the ad will be displayed. Optionally, you can specify a price
floor for the ad.

```kotlin
fun loadAd(activity: Activity, pricefloor: Double = BidonSdk.DefaultPricefloor)
```

### Displaying Ad 

Show the banner ad on the specified activity.

```kotlin
fun showAd(activity: Activity)
```

Check if the banner ad is ready to be shown.

```kotlin
fun isReady(): Boolean
```

### Hiding Ad 

Hide the banner ad.

```kotlin
fun hideAd()
```

### Destroying Ad 

Destroy the banner ad when it's no longer needed.

```kotlin
fun destroyAd()
```
