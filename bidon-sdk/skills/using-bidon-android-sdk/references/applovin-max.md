# Bidon Configuration

> Step-by-step guide to set up Bidon and start monetizing your app.

# Bidon Configuration 

1. Make sure you have a Bidon account. If you don't have one yet, [leave us your email](https://bidon.org/#apply), and we'll get back to you soon.
2. Follow the [Getting Started with Bidon](/docs/monetization/getting-started.mdx) guide to set up monetization on Bidon. You need to link your application, configure the ad networks you want to use, add ad network placements (which we call "Line Items"), and set up the auction configurations you want to use inside MAX.

# All Done

You’re all set! After setting up Bidon monetization, don't forget to [integrate SDK](/docs/applovin-max/sdk-integration.mdx) and [activate Bidon in your MAX configuration](/docs/applovin-max/max-configuration.mdx).

---

# Max Configuration

> Step-by-Step Guide: Setting Up the Bidon Extension in MAX.

## MAX Configuration

**Prerequisites**:
* Access to the Bidon Extension files (unpacked)
* A MAX account
* Permissions to manage Networks and Ad Units

#### 1. Install the Bidon Extension in Chrome.

Install the Bidon Extension directly from the [Chrome Store](https://chromewebstore.google.com/detail/bidon-extensions/higflbdgeemoolejdmlgjaahcbpclolp?pli=1)

Or install it manually:
- Download the [**Bidon Extensions file**](/files/bidon-extension(v2.3).zip).
- Open your **browser** and navigate to:
[chrome://extensions/](chrome://extensions/) or use the menu: Extensions → Manage Extensions

- Enable **Developer Mode** (toggle in the top-right corner) and click **“Load unpacked”**, select the Bidon extension folder.

* Once loaded, **pin the Bidon extension** to your toolbar.

#### 2. Add Bidon as a Custom Network to MAX

* Log into your **MAX** account.
* Go to the **"Networks"** section and scroll down to find **Custom Adapters**.

* **iOS Adapter Class Name**: BidonMediationAdapter
* **Android / Fire OS Adapter Class Name**: com.applovin.mediation.adapters.BidonMediationAdapter

#### 3. Configure Ad Units for Bidon

* Navigate to the app for which you want to configure ad units.
* Choose an existing **ad unit** or **create a new one**.
* Click the **Bidon extension icon** in the browser toolbar.
* A configuration window will open with **auto-setup options** for Bidon ad units.

#### 4. Customize and Launch Ad Units

1. Select the desired:
* **Ad Type** (e.g. banner, interstitial, rewarded)

* **Platform** (iOS or Android):

2. Enter a **search keyword** for the ad unit and choose the most appropriate **suggested ad unit** from the list.

3. Choose the **Custom Network Bidon (CA)** to configure and set the **price range** (min and max CPM), and insert the necessary **auction key**:

Where **Auction_Key** is the corresponding Auction Key you set up in Bidon:

4. Click **“Create!**” to generate the ad unit with Bidon.

#### 5. Finalize Bidon Configuration in MAX

1. Open the newly created or targeted **Ad unit** in MAX.
2. Scroll to the **Custom Networks list** (CA section).
3. Fill in App ID (optional) credentials for the Bidon Custom Network.

Where **App ID** is the corresponding App Key you can find in Bidon:

The first placement have an extremely high CPM Price and the following parameters:
For **Interstitial**, **Rewarded Video**:

```json
{"ecpm":500,"unicorn":true,"auction_key":"$YOUR_AUCTION_KEY","pricefloor_coef":1,"pricefloor_start":5}
```

For **Banner**:

```json
{"ecpm":50,"unicorn":true,"auction_key":"$YOUR_AUCTION_KEY","pricefloor_coef":1,"pricefloor_start":2}
```

We recommend the following prices for the first placements:

**Interstitial & Rewarded**: 500
**Banner & MREC**: 50

4.1. The remaining placements have the following parameters.

```json
{"ecpm": 450}
```

The **ecpm** field in the parameters should match the **CPM Price** field in the MAX ad unit configurations.
The more placements you set up, the more accurate the price of Bidon impressions will be in the MAX statistics.

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
    implementation("com.applovin.mediation:bidon-adapter:0.13.0.0")

    // Available Demand Sources (AdNetworks)
    implementation("org.bidon:admob-adapter:+")
    implementation("org.bidon:amazon-adapter:+")
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
