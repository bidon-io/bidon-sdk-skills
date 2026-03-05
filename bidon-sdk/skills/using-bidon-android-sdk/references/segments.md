# Segments

Segments are employed to monitor metrics related to different user categories and to control advertisements targeted at these specific categories.
A segment represents a portion of the audience distinguished by certain criteria, such as gender, age, or any other parameter recognized by the app and communicated to the Bidon SDK.
Furthermore, specific ad management configurations can be implemented for each individual segment.

## Segment UID

The segment UID is a unique identifier that is assigned to each user by server.

```kotlin
val segmentUid = BidonSdk.segment.segmentUid //e.x.: "1704325228273860608" – Snowflake ID
```

## User segmentation

Bidon SDK offers versatile user segmentation capabilities, allowing you to finely tailor your ad targeting strategies. With Bidon SDK, you can segment users based on various criteria, including age, gender, game level, in-app purchases, and even custom attributes defined by your specific needs. This granular segmentation empowers you to deliver highly personalized and relevant advertisements, enhancing the overall user experience and maximizing the effectiveness of your ad campaigns. Whether you want to engage specific age groups, cater to distinct genders, reward loyal in-app purchasers, or customize segments based on unique user attributes, Bidon SDK provides you with the tools to optimize your advertising efforts and drive better results.

```kotlin
BidonSdk.segment.setAge(25)
BidonSdk.segment.setGender(Gender.FEMALE)
BidonSdk.segment.setCustomAttributes(mapOf("custom_attribute" to "custom_value"))
BidonSdk.segment.setLevel(5)
BidonSdk.segment.setTotalInAppAmount(100.0)
BidonSdk.segment.setPaying(true)
```
