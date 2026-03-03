# Using Bidon with LevelPlay

Bidon as a custom adapter in LevelPlay (ironSource) mediation. LevelPlay must already be integrated in the project.

## Dependencies

Add the Bidon repository and mediation adapter:

```kotlin
repositories {
    maven { url = uri("https://artifactory.bidon.org/bidon") }
}

dependencies {
    // Bidon mediation adapter for LevelPlay
    implementation("com.ironsource.adapters:bidon-adapter:VERSION")

    // Demand source adapters (add only the ones you need)
    implementation("org.bidon:admob-adapter:VERSION")
    implementation("org.bidon:applovin-adapter:VERSION")
    implementation("org.bidon:amazon-adapter:VERSION")
    implementation("org.bidon:bidmachine-adapter:VERSION")
    implementation("org.bidon:bigoads-adapter:VERSION")
    implementation("org.bidon:chartboost-adapter:VERSION")
    implementation("org.bidon:dtexchange-adapter:VERSION")
    implementation("org.bidon:gam-adapter:VERSION")
    implementation("org.bidon:inmobi-adapter:VERSION")
    implementation("org.bidon:meta-adapter:VERSION")
    implementation("org.bidon:mintegral-adapter:VERSION")
    implementation("org.bidon:mobilefuse-adapter:VERSION")
    implementation("org.bidon:moloco-adapter:VERSION")
    implementation("org.bidon:startio-adapter:VERSION")
    implementation("org.bidon:taurusx-adapter:VERSION")
    implementation("org.bidon:unityads-adapter:VERSION")
    implementation("org.bidon:vkads-adapter:VERSION")
    implementation("org.bidon:vungle-adapter:VERSION")
    implementation("org.bidon:yandex-adapter:VERSION")
}
```

## LevelPlay Dashboard Configuration

- **Network Key**: `15c0a270d`
- **Publisher ID**: `708010`
- **Reported Revenue**: Rate based revenue

### First ad instance

High price, `should_load = true`. Recommended prices: Interstitial/Rewarded = 500, Banner/MRec = 50.

### Subsequent instances

`should_load = false`. The `Price` field should match the `Rate` field. More instances = more accurate price reporting.

## Consent Passthrough

Pass GDPR/CCPA/COPPA consent to Bidon via LevelPlay's network data API:

```kotlin
val BIDON_CA_NETWORK_KEY = "15c0a270d"
val BIDON_GDPR_KEY = "BidonCA_GDPR"     // Boolean
val BIDON_CCPA_KEY = "BidonCA_CCPA"     // Boolean
val BIDON_COPPA_KEY = "BidonCA_COPPA"   // Boolean

val networkData = JSONObject()
networkData.put(BIDON_GDPR_KEY, isUserHasGdprConsent)
networkData.put(BIDON_CCPA_KEY, isUserHasCcpaConsent)
networkData.put(BIDON_COPPA_KEY, isUserAgeRestricted)

IronSource.setNetworkData(BIDON_CA_NETWORK_KEY, networkData)
```

See [references/level-play.md](references/level-play.md) for the full dashboard setup guide and consent key details.
