# Bidon Configuration

> Step-by-step guide to set up Bidon and start monetizing your app.

1. Make sure you have a Bidon account. If you don't have one yet, [leave us your email](https://bidon.org/#apply),
and we'll get back to you soon.
2. Follow the [Getting Started with Bidon](/docs/monetization/getting-started.mdx) guide to set up monetization on Bidon.
You need to link your application, configure the ad networks you want to use, add ad network placements (which we call "Line Items"),
and set up the auction configurations you want to use inside LevelPlay.

# All Done

You’re all set! After setting up Bidon monetization, don't forget to [integrate SDK](/docs/level-play/sdk-integration.mdx) and [activate Bidon in your LevelPlay configuration](/docs/level-play/level-play-configuration.mdx).

---

# LevelPlay Configuration

> Step-by-step guide to set up LevelPlay for Bidon adapter.

## LevelPlay Configuration

#### 1. Add Bidon as a Custom Network to LevelPlay.

* Enter `15c0a270d` as **Network Key** to add Bidon as custom adapter, click **Confirm key** and **Save**

* As **Publisher ID** enter `708010` and select **Rate based revenue** as **Reported Revenue** method

#### 2. Add Ad Instance for Bidon

* For selected app go to Instance, choose Bidon, then enter your **Bidon app key** and click **Add Instance**

#### 3. Fill in ad instance data for created ad instance

* For any created ad instance you need to fill following fields:
  - `Instance name` - ad instance name. You can specify any value;
  - `Auction Key` - Bidon auction key;
  - `Price` - pricefloor for Bidon SDK;
  - `should_load` - Status indicating the necessary to load the Bidon ad;
  - `Rate` - pricefloor for LevelPlay SDK. Should be the same as Bidon Price;

##### 3.1. The first placement should have an extremely high CPM Price and the following parameters:

- `Instance name` - for example: Interstitial_500;
- `Auction Key` - your Bidon auction key;
- `Price` - 500;
- `should_load` - **true**;
- `Rate` - 500;

Where `auction_key` is the corresponding Auction Key you set up in Bidon.

We recommend the following prices for the first placements:

- **Interstitial & Rewarded**: 500
- **Banner & MREC**: 50

##### 3.2. The remaining placements should have the following parameters

- `Instance name` - any;
- `Auction Key` - your Bidon auction key;
- `Price` - any;
- `should_load` - **false**;
- `Rate` - any;

The `Price` field in the parameters should match the **Rate** field in the LevelPlay ad unit configurations.
The more placements you set up, the more accurate the price of Bidon impressions will be in the LevelPlay statistics.

:::info

We're working hard to make the LevelPlay configuration process more convenient.

:::

---

You're all set!

---

Add the following repository to your project:

```groovy
repositories {
    maven(url = "https://artifactory.bidon.org/bidon")
}
```

Then, add the dependency:

```kotlin
dependencies {
    implementation("com.ironsource.adapters:bidon-adapter:0.13.0.0")

    // Available Demand Sources (AdNetworks)
    implementation("org.bidon:admob-adapter:+")
    implementation("org.bidon:applovin-adapter:+")
    implementation("org.bidon:amazon-adapter:+")
    implementation("org.bidon:bidmachine-adapter:+")
    implementation("org.bidon:bigoads-adapter:+")
    implementation("org.bidon:chartboost-adapter:+")
    implementation("org.bidon:dtexchange-adapter:+")
    implementation("org.bidon:gam-adapter:+")
    implementation("org.bidon:inmobi-adapter:+")
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

**Adapter Data:**

- **Network name:** Bidon
- **Network key:** `15c0a270d`

## Update Consent Value

To set **GDPR**, **CCPA**, and **COPPA** consent status for the Bidon network adapter, use the following keys:

##### Bidon network key:

- `BIDON_CA_NETWORK_KEY = "15c0a270d"`

##### Consent Keys:
- `BIDON_GDPR_KEY = "BidonCA_GDPR"`
- `BIDON_CCPA_KEY = "BidonCA_CCPA"`
- `BIDON_COPPA_KEY = "BidonCA_COPPA"`

Then put consent `Boolean` value to json with `Bidon network key` and call:

```kotlin
IronSource.setNetworkData(BIDON_CA_NETWORK_KEY, networkData)
```

##### Example:

```kotlin
val networkData = JSONObject()
networkData.put(BIDON_GDPR_KEY, isUserHasGdprConsent)
networkData.put(BIDON_CCPA_KEY, isUserHasCcpaConsent)
networkData.put(BIDON_COPPA_KEY, isUserAgeRestricted)

IronSource.setNetworkData(BIDON_CA_NETWORK_KEY, networkData)
```

where:
- `isUserHasGdprConsent` — Boolean: user’s GDPR consent;
- `isUserHasCcpaConsent` — Boolean: user’s CCPA consent;
- `isUserAgeRestricted` — Boolean: user’s COPPA (age restriction) status.
