# Using Bidon with AppLovin MAX

Bidon as a custom network in MAX mediation. MAX must already be integrated in the project.

## Dependencies

Add the Bidon repository and mediation adapter:

```kotlin
repositories {
    maven { url = uri("https://artifactory.bidon.org/bidon") }
}

dependencies {
    // Bidon mediation adapter for MAX
    implementation("com.applovin.mediation:bidon-adapter:VERSION")

    // Demand source adapters (add only the ones you need)
    implementation("org.bidon:admob-adapter:VERSION")
    implementation("org.bidon:amazon-adapter:VERSION")
    implementation("org.bidon:bidmachine-adapter:VERSION")
    implementation("org.bidon:bigoads-adapter:VERSION")
    implementation("org.bidon:chartboost-adapter:VERSION")
    implementation("org.bidon:dtexchange-adapter:VERSION")
    implementation("org.bidon:gam-adapter:VERSION")
    implementation("org.bidon:inmobi-adapter:VERSION")
    implementation("org.bidon:ironsource-adapter:VERSION")
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

## MAX Dashboard Configuration

Add Bidon as a custom network in the MAX dashboard:

- **Android / Fire OS Adapter Class Name**: `com.applovin.mediation.adapters.BidonMediationAdapter`

### First placement — high CPM with full JSON

**Interstitial / Rewarded** (CPM Price: 500):

```json
{"ecpm":500,"unicorn":true,"auction_key":"YOUR_AUCTION_KEY","pricefloor_coef":1,"pricefloor_start":5}
```

**Banner / MRec** (CPM Price: 50):

```json
{"ecpm":50,"unicorn":true,"auction_key":"YOUR_AUCTION_KEY","pricefloor_coef":1,"pricefloor_start":2}
```

### Subsequent placements

```json
{"ecpm": 450}
```

The `ecpm` field must match the CPM Price in the MAX ad unit config. More placements = more accurate price reporting in MAX statistics.

See [references/applovin-max.md](references/applovin-max.md) for the full dashboard setup guide.
