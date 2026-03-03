# Integrating Bidon SDK (Standalone)

Standalone Bidon — no mediation layer. For MAX or LevelPlay mediation, see [SKILL.md § Deployment Modes](SKILL.md#deployment-modes).

## Dependencies

Add the Bidon maven repository and SDK dependency to your app-level `build.gradle.kts`:

```kotlin
repositories {
    maven { url = uri("https://artifactory.bidon.org/bidon") }
}

dependencies {
    // Bidon SDK
    implementation("org.bidon:bidon-sdk:VERSION")

    // Demand source adapters (add only the ones you need)
    implementation("org.bidon:admob-adapter:VERSION")
    implementation("org.bidon:amazon-adapter:VERSION")
    implementation("org.bidon:applovin-adapter:VERSION")
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

Never use `+` as a version — pin to a specific version. See [references/integration.md](references/integration.md) for the full adapter list.

## Adapter Registration

Two approaches:

**Default** — discovers all adapter classes on the classpath. The adapter dependencies must be in build.gradle first, or the call silently registers nothing.

```kotlin
BidonSdk.registerDefaultAdapters()
```

**Manual** — register specific adapters by class name or instance:

```kotlin
BidonSdk.registerAdapter(ApplovinAdapter())
BidonSdk.registerAdapter("org.bidon.applovin.ApplovinAdapter")
```

See [references/adapters.md](references/adapters.md) for the full list of adapter class names.

## Initialization

Regulations → adapters → initialize(). This order is mandatory — ad networks read consent during init and ignore later changes.

```kotlin
// 1. Regulations (only set the ones the user needs — omit the rest)
BidonSdk.regulation.gdpr = Gdpr.Applies           // if GDPR applies
BidonSdk.regulation.coppa = Coppa.No               // if COPPA needed
BidonSdk.regulation.usPrivacyString = "1YNN"       // if CCPA needed

// 2. Register adapters
BidonSdk.registerDefaultAdapters()

// 3. Initialize
BidonSdk
    .setBaseUrl("https://YOUR_BIDON_SERVER_DOMAIN.com")
    .setInitializationCallback { /* ready — load ads here */ }
    .initialize(context = activity, appKey = "APP_KEY")
```

See [references/regulations.md](references/regulations.md) for regulation enum values and consent strings.
