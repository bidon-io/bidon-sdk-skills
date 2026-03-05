# Impression-Level Ad Revenue

You're able to use impression-level ad revenue data for any MMP or analytics platform using AdRevenueListener and its AdValue data.

```kotlin
data class AdValue(
    val adRevenue: Double,
    val currency: String = USD,
    val precision: Precision
)
```

```kotlin
interface AdRevenueListener {
    fun onRevenuePaid(ad: Ad, adValue: AdValue)
}
```

```java
interface AdRevenueListener {
    void onRevenuePaid(@NonNull Ad ad,@NonNull AdValue adValue)
}
```

Each AdType AdListener already contains an AdRevenueListener.

```kotlin
interstitialAd.setInterstitialListener(
    object : InterstitialListener {
        ...

        override fun onRevenuePaid(ad: Ad, adValue: AdValue) {
            logFlow.log("onRevenuePaid: ad=$ad, adValue=$adValue")
        }
    }
)
```
