# Register adapters manually

You're able to define which adapters will be used by Bidon SDK in the application runtime by yourself.
You'll need to use the following code to register adapters instead of `registerDefaultAdapters()`
before initialize the Bidon SDK.

```kotlin
BidonSdk.registerAdapter(ApplovinAdapter())
BidonSdk.registerAdapter("org.bidon.applovin.ApplovinAdapter")
```

```java
BidonSdk.registerAdapter(ApplovinAdapter())
BidonSdk.registerAdapter("org.bidon.applovin.ApplovinAdapter")
```
