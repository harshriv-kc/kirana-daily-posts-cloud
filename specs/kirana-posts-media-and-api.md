# KIRANA POSTS — IMAGE PROMPTS, MEDIA & API

---

## image_prompt (MANDATORY FOR ALL 8 POSTS)

Every post MUST include an `image_prompt` field. The API uses this to generate AI thumbnails.

---

### 1. Commodity Posts — सोया तेल, दाल/शक्कर, Other commodities

**Dimensions:** 1920×1080 landscape

#### PART 1 — Common Design Elements (copy verbatim into image_prompt)

```
Create a minimal, editorial-style landscape thumbnail (1920x1080px) for a single commodity price update post in Hindi:

LAYOUT:
- Full-bleed high-quality close-up photograph of the commodity as background (artistic, slightly darkened edges for text contrast)
- Top-left corner: date pill badge — dark semi-transparent rounded rectangle (#000000 at 60% opacity) with white bold text
- Top-right corner: category label pill — distinct colored style with a tinted/accent background and thin border (e.g., warm gold-bordered pill for तेल, earthy brown for दाल, spice-toned for मसाला). White bold text inside. Must look premium and distinct from the dark date pill — NOT the same style as the date pill.
- Bottom text area (TWO distinct lines, left-aligned, bottom-left): a smooth transparent-to-dark gradient covers the bottom ~35-40% of the image — it must start well ABOVE the commodity name (LINE 1) so that BOTH text lines sit entirely within the darkened zone. The gradient fades smoothly from fully transparent at top to semi-dark at bottom — NOT a solid bar, NOT a sharp-edged block. The commodity photo must remain SHARP, CRISP, and IN-FOCUS under the gradient — the gradient is a pure black color overlay with transparency only, NO gaussian blur, NO frosted glass, NO depth-of-field blur. The photo details must be just as sharp in the gradient zone as outside it, only darker.
  - LINE 1 (top): Commodity name in very large bold white Devanagari text — this is the dominant text element. Must be fully inside the gradient zone.
  - LINE 2 (below, smaller): Direction badge pill (compact rounded — RED #D32F2F bg for "⬆ तेजी", GREEN #2E7D32 bg for "⬇ मंदी", GREY #757575 bg for "→ स्थिर", all with white text) FOLLOWED BY price change text in white (e.g., "₹15 गिरा प्रति 10 किलो")

DESIGN RULES:
- Background commodity photo must be beautiful, high-resolution, and contextually accurate (real dal grains for dal, oil being poured/seeds for oil, actual spice heaps for spices, gold bars/coins for gold)
- CRITICAL: No English text, labels, brand names, or packaging text visible anywhere in the background photo. Show raw commodities, loose grains, poured liquids, or unlabeled containers only — never branded bottles or packets with printed text
- The bottom gradient must be SMOOTH and GRADUAL (transparent→dark), NOT a solid opaque black bar or sharp-edged strip. The photo should still show through the darkened area. The gradient must be tall enough to cover BOTH text lines — not just the bottom line.
- Bottom text must be in exactly 2 lines: commodity name on line 1 (big), direction badge + price on line 2 (smaller). Not all on one line.
- No sparkle effects, no lens flare, no star particles, no decorative glowing elements, and absolutely NO blur effect in the gradient area — the gradient must only darken the image, the photo underneath must remain sharp and in-focus throughout
- Typography: clean modern Devanagari throughout, no decorative fonts
- Overall feel: premium, clean, instantly readable at mobile thumbnail size
- NO clutter — maximum 4 text elements visible (date, category, commodity name, direction+price)
- Daily variation through different commodity photography angles, lighting moods, and subtle background treatments
```

#### PART 2 — Variable Data (fill from post content)

```
COMMODITY PHOTO CONTEXT: [Describe the commodity visually for the AI — e.g., "golden refined soybean oil being poured from a brass lota into a glass bowl, with loose soybean seeds on rustic wooden surface — no bottles, no labels"]

DATE: [DD माह YYYY — from post_title]
CATEGORY LABEL: [e.g., "तेल बाजार", "दाल बाजार", "शक्कर बाजार", "मसाला बाजार", "सोना-चांदी"]
COMMODITY NAME: [Primary commodity — e.g., "सोया तेल", "तूर दाल", "हल्दी"]
DIRECTION: [तेजी / मंदी / स्थिर]
PRICE CHANGE: [e.g., "₹12 बढ़ा प्रति क्विंटल" or "₹15 गिरा प्रति 10 किलो"]
```

#### How to populate PART 2

**COMMODITY PHOTO CONTEXT** — describe visually, match commodity:
- सोया तेल → oil pouring from brass lota / soybean seeds / glass bowl (no bottles with labels)
- सरसों तेल → yellow mustard oil / mustard flowers / brass container
- तूर दाल → orange-yellow split pigeon pea grains
- उड़द दाल → black/white urad dal grains close-up
- मूंग दाल → yellow moong dal
- चना दाल → golden chana dal with chickpeas
- शक्कर/चीनी → white sugar crystals / sugarcane
- हल्दी → vibrant turmeric powder heaps / raw turmeric roots in clay pot
- जीरा → cumin seeds in brass bowl
- लाल मिर्च → red chili powder / dried red chilies
- सोना-चांदी → gold bars/coins, silver coins
- बादाम/काजू → almonds/cashews in traditional setting

**DATE** — from post_title beginning
**CATEGORY LABEL** — map from post type (तेल बाजार / दाल बाजार / शक्कर बाजार / मसाला बाजार / सोना-चांदी)
**COMMODITY NAME** — single primary commodity
**DIRECTION** — from the `direction` field
**PRICE CHANGE** — extract ₹ change from post_description first paragraph, include unit

---

### 2. Rujhan Post (मंडी का रुझान)

**Dimensions:** 1920×1080 landscape

#### PART 1 — Common Design Elements (copy verbatim)

```
Create a clean, modern landscape thumbnail (1920x1080px) for commodity trends post in Hindi with aesthetic design:

LAYOUT STRUCTURE:
- Header banner at top: Display "मंडी का रुझान" as main heading in bold large Hindi text, with date "DD माह YYYY" in smaller text (positioned beside or below main heading)
- 4 horizontal commodity cards arranged in rows below header (or 2-3 cards if fewer commodities have movement)
- Each card layout: Commodity image in circular/rounded shape (left) → Commodity name in bold Devanagari (center-left) → Direction text in Hindi (center-right) → Trend arrow icon (far right)

DESIGN REQUIREMENTS:
- Use diverse color palettes - can range from minimal pastels to bold vibrant tones, ensuring each day looks fresh and distinct
- Acceptable styles: soft neutrals with accent colors, bold single-color themes, duotone combinations, or elegant gradients
- AVOID: Rainbow multi-color overload, neon/flashy combinations, overly busy patterns
- Cards should have harmonious backgrounds that complement each other
- High contrast between text and background for instant readability
- Modern, clean Devanagari typography throughout
- Trend indicators: GREEN upward arrow/icon for rise (तेजी), RED downward arrow/icon for fall (मंदी)
- Professional, aesthetic design optimized for mobile thumbnail viewing
- Daily variation through different color moods, layout refinements, and style approaches
```

#### PART 2 — Variable Data

```
DATE: DD माह YYYY

COMMODITIES (4 items, or 2-3 if fewer movements):
1. [Commodity Hindi Name] - [मंदी के आसार / तेजी के आसार] - [DOWN/UP]
2. [Commodity Hindi Name] - [मंदी के आसार / तेजी के आसार] - [DOWN/UP]
3. [Commodity Hindi Name] - [मंदी के आसार / तेजी के आसार] - [DOWN/UP]
4. [Commodity Hindi Name] - [मंदी के आसार / तेजी के आसार] - [DOWN/UP]
```

Extract 4 commodities with clear price movement from the rujhan post_description. **Thumbnail cap: max 4
commodity cards, ALWAYS — even though the रुझान body now lists many commodities (12–18) with अभी → रुझान →
आगे का भाव, the image shows only the 4 with the strongest/clearest moves.**

---

### 3. News & Scheme Posts

**Applies to:** Pan India Trending News 1, Pan India Trending News 2, Pan India Schemes

**Dimensions:** 1920×1080 landscape (News) / 120×138 (Schemes — text centred)

#### PART 1 — Common Design Elements (copy verbatim)

For Trending News:
```
Create a highly clickable, eye-catching landscape thumbnail (1920x1080px) for a news/scheme post in Hindi:

REQUIRED CONTENT:
- Background: Relevant contextual image based on the post description
- Date and post type text (smaller emphasis)
- Two-line headline and description (main focus)
- Call-to-action button with arrow

DESIGN GOAL:
Create a professional, modern, visually appealing thumbnail optimized for mobile clicks. Use your creative judgment for:
- Color scheme that looks attractive and harmonious
- Typography hierarchy that makes headline pop
- Layout and composition that draws attention
- Proper contrast ensuring all Hindi text is clearly readable

AVOID: Rainbow colors, cluttered designs, poor text contrast
```

For Schemes (change dimensions):
```
Create a highly clickable, eye-catching thumbnail (120x138px) for a scheme post in Hindi. Text will be in the centre.
[rest same as above]
```

#### PART 2 — Variable Data

```
CONTEXT: [Paste entire post_description here]

CONTENT TO DISPLAY:
Date & Type: [e.g., "20 जनवरी: ट्रेंडिंग न्यूज़" OR "20 जनवरी: सरकारी योजना"]
Main Headline: [Extract headline after dash from post_title, keep emojis]
Description: [One-line summary showing relevance to kirana owners]
CTA Button: [Trending: "पूरी रिपोर्ट पढ़ें →" | Schemes: "अभी आवेदन करें →"]
```

---

### 4. Samachar Post

**Dimensions:** 1920×1080 landscape

#### PART 1 — Common Design Elements (copy verbatim)

```
Create a highly clickable, eye-catching landscape thumbnail (1920x1080px) for a daily commodity news (Samachar) post in Hindi:

REQUIRED CONTENT:
- Background: High-quality, aesthetic image of relevant commodities (artistic shots of pulses, grains, spices, oils, or a clean market scene)
- Date and post type text (smaller emphasis, top banner)
- Main Headline (large, prominent, listing key commodities affected)
- Call-to-action button with arrow

DESIGN GOAL:
- Color scheme harmonious with natural commodity colors (warm earth tones, vibrant spice colors)
- Typography hierarchy that makes headline pop immediately
- Text box styling (translucent overlays, solid banners, glassmorphism — ensure readability)
- Proper contrast for all Hindi text

AVOID: Cluttered designs, poor text contrast, revealing specific prices in text overlay
```

#### PART 2 — Variable Data

```
CONTEXT: [Paste entire post_description — guides background image selection]

CONTENT TO DISPLAY:
Date & Type: [Extract before pipe '|' from post_title, e.g., "02 फरवरी: किराना समाचार"]
Main Headline: [Extract after pipe '|' from post_title, e.g., "तूर दाल उछली, शक्कर मजबूत, सोना टूटा"]
CTA Button: पूरी रिपोर्ट पढ़ें →
```

---

## pn_image_prompt (Only: Samachar, दाल/शक्कर, रुझान, TN1, TN2)

### Standard template (Samachar, दाल/शक्कर, TN1, TN2)

```
Create a highly clickable, eye-catching notification image. Dimensions: width slightly larger than height (4:3 aspect ratio), centered composition.

Background:
[Contextual background derived from post_description]. Background slightly darkened.

Central Text Overlay:
Large centered translucent dark glassy text box with rounded corners. Centered text

Text Content (CENTERED):

Top Tag (Small):
"[TOP_TAG]"

Main Headline (Large, Bold):
"[HEADLINE]"

Sub-text (Medium):
"[SUBTEXT]"

CTA Button:
"[CTA]"

Style:
[STYLE_TONE], bold Hindi typography, mobile-first.
```

**Mapping logic:**
- TOP_TAG → from post_title before first " - ". Do not modify.
- HEADLINE → plain bold text from notification_title. Remove HTML.
- SUBTEXT → first line of notification_description. Remove HTML.
- CTA → second line of notification_description. Remove HTML.
- Background from post_description only.

**STYLE_TONE by post type:**
- Samachar → Professional market update tone
- दाल/शक्कर → Clean commodity-focused tone
- Trending News → Breaking-news tone, high urgency

### रुझान pn_image_prompt (SPECIAL — VAR rotation)

**Rotation Logic:** Extract numerical date from post_title. Calculate `Date MOD 4`:
- Mod 4 = 1 → VAR 1 (FOMO Locked Trend)
- Mod 4 = 2 → VAR 2 (Premium Financial Spotlight)
- Mod 4 = 3 → VAR 3 (High-Impact Alert — requires ≥4% change, else fallback to quiz style)
- Mod 4 = 0 → VAR 4 (Minimal Physical Speedometer)

#### VAR 1: FOMO Locked Trend
- Style: 4:3, dramatic/moody, high contrast. Blurred commodity blend background.
- Card: Dark semi-transparent. Headline: "मंडी में बदलेंगे ये भाव!"
- 3 frosted commodity rows with 🔒 locks and heavily blurred/unreadable trend percentages
- CTA: Glowing yellow-orange "रुझान अनलॉक करें 🔒"

#### VAR 2: Premium Financial Spotlight
- Style: 4:3, premium financial (Bloomberg/Mandi) vibe, dark navy/teal gradient
- Extract ONE commodity with largest % change
- Hero: circular commodity image + bold Hindi name
- Trend chart: line graph with base date + 4 future dates. UP = red curve + "तेजी के आसार", DOWN = green curve + "मंदी के आसार"
- CTA: "जाने बाकी सभी का रुझान →"

#### VAR 3: High-Impact Alert
- TRIGGER: Only if single commodity has ≥4% change. Otherwise fallback to quiz style.
- Style: 4:3, dark charcoal (#0f0f0f), clinical brokerage alert
- UP = RED + ↑, DOWN = GREEN + ↓
- Top banner with theme color stripe. Hero commodity circle. Massive percentage. Reason line.
- CTA: "बाकी रुझान देखें →"

#### VAR 4: Minimal Physical Speedometer
- Style: 4:3, deep dark (#111), matte-metallic physical gauge (NO neon/glowing)
- Randomly select 1 commodity from post_description
- Gauge: 5 sections (भारी मंदी → मंदी → स्थिर → तेजी → भारी तेजी). Asian colors (green = down, red = up). Metallic needle.
- Badge with exact % + arrow in theme color
- CTA: "जानें बाकी सभी का रुझान →"

---

## API MAPPING

**Endpoint:** `POST https://asia-south1-op-d2r.cloudfunctions.net/postAutomation`

**Request Format:** Array of post objects `[{...}, {...}]`

### Required Fields (ALL 8 posts)
- `post_name` — exact value from approved list
- `post_title` — Hindi title with date
- `post_description` — HTML formatted content
- `brand_names` — array (empty `[]` if none)
- `notification_title` — PN Line 1 HTML
- `notification_description` — PN Lines 2+3 HTML
- `bg_color` — hex code from selected colour scheme
- `image_prompt` — AI image generation text

### Conditional Fields
- `commodity` + `direction` — ONLY on: सोया तेल, दाल/शक्कर, Other commodities, रुझान
- `pn_image_prompt` — ONLY on: Samachar, दाल/शक्कर, रुझान, TN1, TN2

### Post Names (exact values)
`Samachar`, `सोया तेल`, `दाल/शक्कर`, `Other commodities`, `रुझान`, `Pan India Trending News 1`, `Pan India Trending News 2`, `Pan India Schemes`

### Commodity Values
Oil: `सोया तेल` | Sugar: `शक्कर` | Pulses: `दाल`, `मूंग दाल`, `तूर दाल`, `उड़द दाल`, `चना दाल` | Spices: `मसाले`, `हल्दी`, `लाल मिर्च`, `जीरा`, `धनिया`, `इलायची` | Dry Fruits: `बादाम`, `काजू`, `मखाना`, `किशमिश`, `अखरोट` | Grains: `चावल`, `गेहूं`, `मक्का` | Other: `सोना-चांदी`, `सब्जियां`, `ट्रेंडिंग न्यूज़`, `रुझान`

### Direction Values
`तेजी` (Rising) | `मंदी` (Falling) | `स्थिर` (Stable)

### brand_names
Always include as array. Extract all brand names from content preserving capitalization. If none: `"brand_names": []`

### bg_color
Required on all 8. Must be a hex code from selected daily colour scheme. Format: `"#RRGGBB"`

---

## VALIDATION CHECKLIST

Before outputting the curl, verify:

- ✓ Exactly 8 posts generated
- ✓ Request body is ARRAY format `[{...}, {...}]`
- ✓ Date format: `[DD]` महीना: (Arabic numerals 0-9, not Devanagari १-९)
- ✓ Zero English words in descriptions (scan entire description)
- ✓ Zero citation markers `【...】` in description
- ✓ All sentences end with `।` (not `.`)
- ✓ `bg_color` field present in all 8 posts with valid hex codes
- ✓ 8 unique bg_colors = 5 light + 3 dark
- ✓ `image_prompt` present on ALL 8 posts
- ✓ `pn_image_prompt` present on: Samachar, दाल/शक्कर, रुझान, TN1, TN2
- ✓ `commodity` + `direction` on: सोया तेल, दाल/शक्कर, Other commodities, रुझान
- ✓ `brand_names` (array) on all 8
- ✓ No `$` symbol anywhere (spell "डॉलर")
- ✓ No ASCII apostrophes (breaks shell payload)
- ✓ No duplicate emoji within a single PN
- ✓ Samachar PN commodity differs from the 3 commodity post PNs
- ✓ Color and formatting exactly as per rules
