# Regulations

#### Bidon SDK enforces the regulations with every demand source prior to loading new ads.

## GDPR

This section is included to ensure adherence to the regulations outlined in the European Union's General Data Protection Regulation (GDPR).
To obtain GDPR consent from your users, it is recommended that you utilize the following API to transmit a consent flag to the Bidon SDK:

```kotlin
BidonSdk.regulation.gdpr = Gdpr.Applies
BidonSdk.regulation.gdprConsentString = "GDPR_CONSENT_STRING"

enum class Gdpr {
    Unknown,
    DoesNotApply,
    Applies;
}
```

## COPPA

The Children's Online Privacy Protection Act (COPPA) enforces limitations on the gathering and utilization of data from individuals under the age of 13.
Bidon SDK offers resources to support publishers in creating a secure and favorable user experience.
It is essential for each publisher to indicate whether their application is intended for users below the age of 13.

```kotlin
BidonSdk.regulation.coppa = Coppa.Yes

enum class Coppa {
    Unknown,
    No,
    Yes;
}
```

## US privacy string

The IAB (Interactive Advertising Bureau) introduced the U.S. Privacy String in response to the California Consumer Privacy Act (CCPA).
This U.S. privacy string serves as a cookie that holds data concerning the disclosures made and choices exercised by website visitors regarding their consumer rights.
Publishers and advertisers leverage this cookie to transmit this data to their downstream framework collaborators and technology partners.
This approach ensures that website visitors do not need to opt-out repeatedly, while also establishing a limited-service provider agreement when consumers access the digital property.

```kotlin
BidonSdk.regulation.usPrivacyString = "US_PRIVACY_STRING"
```
