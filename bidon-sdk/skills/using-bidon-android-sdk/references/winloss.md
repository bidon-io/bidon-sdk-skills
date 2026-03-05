# Win/Loss notifications

When BidonSDK is used next to your Mediation SDK, it is important to notify BidonSDK about the result of the auction.
This is necessary for BidonSDK to be able to optimize the auction and to provide you with the best possible results.

The OpenRTB specification defines the following notifications:
- The win notice informs the bidder’s pricing algorithms of a success, whereas the billing notice indicates that spend should actually be applied.
- A loss notification is also available to inform the bidder of the reason their bid did not win.

This specification focuses on the real-time interactions of bid request and response and the win and loss notices.

Each ad type implements WinLossNotifiable interface.

```kotlin
interface WinLossNotifiable {
    fun notifyLoss(winnerNetworkName: String, winnerNetworkPrice: Double)
    fun notifyWin()
}
```

## Win notice

```kotlin
bannerView.notifyWin()
interstitialAd.notifyWin()
rewardedAd.notifyWin()
```

## Loss notice

```kotlin
bannerView.notifyLoss(winnerNetworkName, winnerNetworkPrice)
interstitialAd.notifyLoss(winnerNetworkName, winnerNetworkPrice)
rewardedAd.notifyLoss(winnerNetworkName, winnerNetworkPrice)
```
