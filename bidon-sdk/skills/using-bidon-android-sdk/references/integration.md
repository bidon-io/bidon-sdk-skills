# Integration

This page is describing how to import and configure the Bidon SDK.

:::info Minimum requirements:

Android API level 23 (Android OS 6.0) or higher.

:::

## Getting Started

  

**Latest version from Maven:** {androidVersion}

To integrate Bidon SDK through Dependencies, firstly add repository fo Bidon SDK dependencies

```kotlin
repositories {
    // For using Bidon Artifactory
    maven { url = uri("https://artifactory.bidon.org/bidon") }
}
```

secondly add the following lines to your App-level `build.gradle.kts`:

```kotlin
dependencies {
    // Bidon SDK Library
    implementation("org.bidon:bidon-sdk:${androidVersion}")

    // Available Demand Sources (AdNetworks)
    implementation("org.bidon:admob-adapter:+")
    implementation("org.bidon:amazon-adapter:+")
    implementation("org.bidon:applovin-adapter:+")
    implementation("org.bidon:bidmachine-adapter:+")
    implementation("org.bidon:bigoads-adapter:+")
    implementation("org.bidon:chartboost-adapter:+")
    implementation("org.bidon:dtexchange-adapter:+")
    implementation("org.bidon:gam-adapter:+")
    implementation("org.bidon:inmobi-adapter:+")
    implementation("org.bidon:ironsource-adapter:+")
    implementation("org.bidon:meta-adapter:+")
    implementation("org.bidon:mintegral-adapter:+")
    implementation("org.bidon:mobilefuse-adapter:+")
    implementation("org.bidon:moloco-adapter:+")
    implementation("org.bidon:startio-adapter:+")
    implementation("org.bidon:taurusx-adapter:+")
    implementation("org.bidon:unityads-adapter:+")
    implementation("org.bidon:vkads-adapter:+")
    implementation("org.bidon:vungle-adapter:+")
    implementation("org.bidon:yandex-adapter:+")
}
```

## Available Adapters

| Adapter            | Changelog                                                                                            |
|--------------------|------------------------------------------------------------------------------------------------------|
| admob-adapter      | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/admob/CHANGELOG.md)      |
| amazon-adapter     | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/amazon/CHANGELOG.md)     |
| applovin-adapter   | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/applovin/CHANGELOG.md)   |
| bidmachine-adapter | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/bidmachine/CHANGELOG.md) |
| bigoads-adapter    | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/bigoads/CHANGELOG.md)    |
| chartboost-adapter | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/chartboost/CHANGELOG.md) |
| dtexchange-adapter | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/dtexchange/CHANGELOG.md) |
| gam-adapter        | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/gam/CHANGELOG.md)        |
| inmobi-adapter     | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/inmobi/CHANGELOG.md)     |
| ironsource-adapter | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/ironsource/CHANGELOG.md) |
| meta-adapter       | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/meta/CHANGELOG.md)       |
| mintegral-adapter  | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/mintegral/CHANGELOG.md)  |
| mobilefuse-adapter | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/mobilefuse/CHANGELOG.md) |
| moloco-adapter     | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/moloco/CHANGELOG.md)     |
| startio-adapter    | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/startio/CHANGELOG.md)    |
| taurusx-adapter    | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/taurusx/CHANGELOG.md)    |
| unityads-adapter   | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/unityads/CHANGELOG.md)   |
| vkads-adapter      | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/vkads/CHANGELOG.md)      |
| vungle-adapter     | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/vungle/CHANGELOG.md)     |
| yandex-adapter     | [Changelog](https://github.com/bidon-io/bidon-sdk-android/blob/main/adapter/yandex/CHANGELOG.md)     |

Then sync project.

## Initialize the SDK

Receive your `APP_KEY` in the dashboard app settings. Init Bidon SDK in your MainActivity class.

```kotlin
BidonSdk
    .registerDefaultAdapters()
    // .registerAdapters("com.example.YourOwnAdapterClass") // for registering your custom Adapter (AdNetwork) by class name
    // .registerAdapters(YourOwnAdapter()) // for registering your custom Adapter (AdNetwork) by instance. Instance should be initialized and ready to work

    // Bidon's server can either be self-hosted or managed by a third-party service. Please contact us at hi@bidon.org for a list of recommended managed service providers.
    .setBaseUrl("https://[YOUR_BIDON_SERVER_DOMAIN.com]")

    .setInitializationCallback {
        //  Bidon is initialized and ready to work
    }
    .initialize(
        context = this@MainActivity,
        appKey = "APP_KEY",
    )
```

Set logging.

```kotlin
BidonSdk.setLoggerLevel(Logger.Level.Verbose)
```

Set test mode.

```kotlin
BidonSdk.setTestMode(isTestMode = true)
```

## Configure Ad Types

- [Banners](./ad-formats/banners)
- [BannerManager](./ad-formats/banner-manager)
- [Interstitials](./ad-formats/interstitials)
- [Rewarded Ads](./ad-formats/rewarded)
