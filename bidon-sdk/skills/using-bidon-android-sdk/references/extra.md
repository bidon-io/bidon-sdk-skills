# Extra data

Bidon SDK goes beyond standard ad integration by offering the ability to pass extra data (key, value pairs) with each ad request.
This feature allows you to enhance your ad targeting, analytics, and reporting capabilities, giving you greater control and flexibility over your advertising campaigns.

## SDK Level Extra

SDK enables you to attach SDK-level data to your ad requests. This means you can include specific information related to the SDK configuration, version, user or any other relevant details that help you monitor and optimize your SDK usage.

```kotlin
BidonSdk.addExtra("key", "value")

val extras = BidonSdk.getExtras()
```

## AdType Level Extra

SDK also allows you to include ad type-specific data with your ad-requests. Whether you're dealing with banner ads, interstitials, rewarded videos, you can provide additional context or attributes associated with that particular ad type.

```kotlin
bannerView.addExtra("key", "value")

val extras = bannerView.getExtras()
```

### Benefits:

- Precision Targeting. By passing extra data, you can fine-tune your ad targeting strategies. For example, you can send user demographics, behavior insights, or contextual information to ensure that ads are shown to the most relevant audiences.

- Performance Tracking. With the ability to include SDK and ad type data, you gain comprehensive visibility into the performance of your ads. This data can be invaluable for analyzing ad effectiveness and making data-driven optimizations.

- Custom Reporting. Extra data can be used to create custom reports and dashboards, enabling you to measure the impact of your advertising efforts more accurately and make informed decisions.

- Improved User Experience. By leveraging extra data, you can tailor the ad experience to match user preferences and behavior, ultimately enhancing user engagement and satisfaction.
