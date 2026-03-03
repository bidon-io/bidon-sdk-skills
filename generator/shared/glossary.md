# Bidon SDK Glossary

## Core Concepts

**Bidon SDK** - a server-side auction SDK for ad monetization that manages competitive bidding across multiple ad networks through a single integration.

**Adapter** - a bridge module that connects Bidon SDK to a specific ad network (e.g., AdMob, Meta, Vungle). Must be registered before SDK initialization.

**Demand Source** - an ad network or bidder that provides advertisements to compete in the auction (e.g., AdMob, Amazon, AppLovin, Meta, Chartboost, Mintegral).

**Mediation** - a technology layer that allows app publishers to manage and serve ads from multiple ad networks through a single SDK integration, routing ad requests to competing demand sources and selecting the highest-value response to maximize fill rate and revenue.

**APP_KEY** - unique identifier for an application within the Bidon system, used during SDK initialization.

**Bidon Admin Panel** - web dashboard for managing auction configurations, app settings, and network setup.

## Ad Formats

**Banner** - a small display ad embedded in app UI. Fixed size 320×50 px, optimized for phones.

**Leaderboard** - a large banner format, 728×90 px, optimized for tablets.

**MRec (Medium Rectangle)** - a medium-sized banner format, 300×250 px.

**Adaptive Banner** - a flexible-width banner that adjusts to screen size with 50 or 90 px height.

**Interstitial** - a full-screen ad displayed between content transitions. Requires user action to close.

**Rewarded Ad** - a full-screen ad that grants the user a reward (e.g., coins, extra lives) upon completion.

## Auction & Pricing

**Auction** - a real-time competitive bidding process where multiple demand sources simultaneously submit bids for an ad impression, and the highest bidder wins. Bidon runs auctions server-side.

**Auction Key** - a configuration identifier linking an ad request to a specific auction setup in the Bidon Admin Panel.

**eCPM (Effective Cost Per Mille)** - the estimated revenue a publisher earns per 1,000 ad impressions, regardless of pricing model (CPM, CPC, CPA). Formula: (Total Revenue / Total Impressions) × 1,000. Used to rank demand sources and as price floor basis.

**CPM (Cost Per Mille)** - the price an advertiser pays per 1,000 ad impressions. This is the advertiser-side metric, while eCPM is the publisher-side equivalent.

**Price Floor** - the minimum acceptable bid price (in CPM) for an ad request. Bids below this value are rejected.

**Line Item** - Bidon's term for an ad placement configuration that maps to a demand source with a specific price.

**OpenRTB** - industry standard specification for real-time bidding requests, responses, and win/loss notifications.

## Mediation Strategies

**Waterfall** - a sequential method of selling ad inventory where ad networks are ranked in a prioritized list (typically by historical eCPM), and ad requests cascade from one network to the next until one fills the impression.

**Waterfall Configuration** - the setup that defines the ordered hierarchy of ad networks in a waterfall, including eCPM values, priorities, and targeting rules.

**Backfill** - the practice of filling unsold or remnant ad inventory by serving ads from lower-priority demand sources when higher-eCPM networks fail to fill.

**FirstLook** - a mediation strategy where Bidon attempts to load ads first, before falling back to AppLovin MAX. If Bidon meets or exceeds a configured threshold, its ad is shown; otherwise MAX serves the ad.

**Postbid** - a mediation strategy where the primary mediation SDK (e.g., LevelPlay) loads first, then its eCPM is used as Bidon's price floor. If Bidon returns a higher bid, its ad is shown; otherwise the original ad is shown.

## Mediation Platforms

**AppLovin MAX** - a mobile ad mediation platform. Bidon integrates as a custom network adapter within MAX.

**LevelPlay** - ironSource's mediation platform. Bidon integrates via a custom adapter with consent key configuration.

**Custom Network** - Bidon configured as a third-party adapter within a mediation platform's dashboard (MAX or LevelPlay).

**Network Key** - identifier for Bidon as a custom network within a mediation platform (e.g., `15c0a270d` in LevelPlay).

**Publisher ID** - account-level identifier within a mediation platform (e.g., `708010` for Bidon in LevelPlay).

**Ad Unit** - a unique entity created on the ad network or mediation platform side to serve ads for a specific placement and format.

**Ad Instance** - LevelPlay's term for an individual ad placement configuration within their mediation setup.

## Revenue & Analytics

**Impression** - a single instance of an ad being rendered and displayed to a user. Per IAB/MRC standards, a viewable impression requires at least 50% of the ad's pixels visible for 1 continuous second (display) or 2 seconds (video).

**Impression-Level Ad Revenue** - per-impression earnings data delivered via callbacks, including revenue amount, currency, and precision level.

**Ad Revenue** - the income a publisher earns from displaying ads to users. Calculated as: (Ad Impressions × eCPM) / 1,000.

**Revenue Precision** - the confidence level of a reported impression-level revenue value. Standard levels (from Google AdMob): Precise (exact bid value), Estimated (from aggregated data), Publisher Provided (manually set CPM), Unknown (insufficient data).

**MMP (Mobile Measurement Partner)** - an analytics platform (e.g., Firebase, AppsFlyer, Adjust) that receives impression-level revenue data for attribution and reporting.

**Network Account** - in mediation platforms like Appodeal, the credential-linked connection between a publisher and a specific ad network. Publishers can use the platform's shared accounts or connect their own for direct control and payouts.

## Win/Loss Notifications

**Win Notification** - an OpenRTB signal sent to Bidon indicating its bid won the auction, informing pricing algorithms of success.

**Loss Notification** - an OpenRTB signal sent to Bidon indicating another demand source won, including the winner's network name and price.

## Regulatory & Compliance

**GDPR (General Data Protection Regulation)** - EU regulation on data protection requiring explicit user consent before collecting and processing personal data. Must be configured before SDK initialization.

**GDPR Consent String** - an IAB Transparency & Consent Framework (TCF) formatted string encoding the user's consent preferences.

**COPPA (Children's Online Privacy Protection Act)** - US federal law protecting the privacy of users under 13. Restricts data collection and ad targeting for children.

**CCPA (California Consumer Privacy Act)** - California privacy law giving consumers control over personal data collection and sale.

**US Privacy String** - an IAB-format 4-character string (e.g., "1YNN") encoding the consumer's CCPA privacy choices.

**Consent** - explicit user permission for personal data processing and ad personalization, required by GDPR, COPPA, and CCPA regulations. Must be obtained and configured before SDK initialization so ad networks read it during init.

## User Targeting

**Segment** - a user audience category distinguished by attributes such as age, gender, game level, or purchase behavior. Specific ad configurations can be applied per segment.

**Segment UID** - a unique server-assigned identifier (Snowflake ID) for a user's segment, available after the first SDK request.

**Custom Attribute** - a developer-defined user property used for targeting beyond the standard attributes (age, gender, level).

**Extra Data** - key-value pairs attached at SDK level or individual ad level to pass additional targeting or analytics information with ad requests.

## Pricing Configuration

**Price Floor Coefficient (`pricefloor_coef`)** - a multiplier used in MAX placement configuration to dynamically calculate price floors.

**Price Floor Start (`pricefloor_start`)** - the initial/minimum price floor value in MAX placement configuration.

**Percentage Increment Strategy** - a postbid price floor increment calculated as a percentage of the first provider's eCPM.

**Fixed Increment Strategy** - a postbid price floor increment calculated as a fixed monetary value added to the first provider's eCPM.

**Threshold** - in FirstLook, the minimum eCPM Bidon must achieve; if the loaded ad's eCPM is below this value, the system falls back to MAX.
