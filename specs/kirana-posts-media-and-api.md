# KIRANA POSTS — IMAGE PROMPTS, MEDIA & API

---

## image_prompt (MANDATORY FOR ALL 8 POSTS)

Every post MUST include an `image_prompt` field. The API uses this to generate AI thumbnails.

**HARD EXCLUSION — सोना-चांदी / सर्राफा (bullion: gold, silver, गिन्नी) must NEVER appear in ANY
`image_prompt` or `pn_image_prompt`:** not as the background photo subject, not as the commodity
name / headline text shown in the image, and not as one of the Rujhan 4-card thumbnail rows. Even
on a day when bullion is the biggest mover (it can never be the Samachar hero anyway), choose a
non-bullion, kirana-relevant commodity for every image background and every image headline. सोना-चांदी
may still be mentioned in the text body (Samachar तेज/मंदा card, अन्य हलचल, रुझान body line) — the ban
is only on depicting or naming it inside image_prompt / pn_image_prompt.

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

**Dimensions:** 1920×1080 landscape (News AND Schemes — same size)

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

For Schemes (SAME dimensions as News — 1920×1080 landscape):
```
Create a highly clickable, eye-catching landscape thumbnail (1920x1080px) for a scheme post in Hindi.
[rest same as the Trending News template above — same 1920x1080 landscape layout, background/date/two-line headline/CTA]
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

### 4. Samachar Post — THE ROTATING ART SYSTEM

**Dimensions:** 1920×1080 landscape. Never square, never portrait, never a circular badge.

Every other image in this file is a fixed template. **Samachar is not — it is composed fresh
every single day.** What follows is a method, not a menu. A shopkeeper scrolling the feed for a
month must never see the same picture twice, while every post is still instantly recognisable as
किराना समाचार within half a second.

That is achieved by holding the **CHASSIS** rigid and letting the **ART** change underneath it.
The art is chosen on two independent axes:

- **SUBJECT** — what the picture actually shows. Drawn from anywhere in the day's market, and
  free to show no commodity at all. Open by design.
- **TREATMENT** — the medium and art direction. Rotates, with a 14-day cooldown.

SUBJECT and TREATMENT are chosen independently. Their product is what keeps the feed alive.
**Never pick a generic "commodity background" again.**

---

#### 4.1 THE CHASSIS — five elements, mandatory, never omitted

These five appear on EVERY Samachar image regardless of art direction. If a treatment is so
strong that it swallows them, **the treatment is wrong, not the chassis.** (This is a real
observed failure: heavy full-bleed poster styles cause the generator to drop the tag, ticker and
CTA and render a pretty poster with no furniture. See 4.6.)

1. **DATE + TAG** — a small pill reading `किराना समाचार`, with the posting date beside it
   (`27 अगस्त 2026`). Top-left.
2. **HEADLINE** — 2 lines, huge, heavy Devanagari. The day's story in ≤18 characters per line.
3. **HERO LINE** — exactly ONE number: the day's single biggest price move, as a self-contained
   sentence, **always with its unit** — e.g. `चीनी 900 रुपये प्रति क्विंटल टूटी`. Accent colour.
   Never drop the unit to dodge a rendering worry: without it a shopkeeper may read 900 as
   per-kilo or per-bag. `क्विंटल` renders correctly in production and is the word to use.
4. **CTA** — a pill reading `पूरी रिपोर्ट पढ़ें →`.
5. **BOTTOM STRIP** — a full-width band across the very bottom, styled like a live TV news
   ticker: a solid RED flag box reading `आज की मंडी`, then 5–6 commodities, each as
   `[name] [triangle arrow]`. **This is the ONLY place direction data appears.**

**Logo is optional.** If the brand mark can sit cleanly at the right end of the bottom strip or
the top-right corner, include it. If it crowds anything, drop it — never at the cost of the five.

**Do NOT add a row of commodity tiles/cards.** An earlier version carried both tiles and a
ticker, which said the same thing twice and ate the middle of the frame. The ticker alone.

---

#### 4.2 LANDSCAPE LAYOUT GRID (1920×1080) — non-negotiable

Landscape is much wider than the drafts were tested at, so positioning is explicit. The frame
splits into a **text column on the left** and a **hero art zone on the right**.

```
x=0 ─────────────── 1100 ──────────────── 1920
│  TEXT COLUMN (left-aligned)   │  HERO ART ZONE      │  y=0
│  ┌ tag + date       y  90-150 │                     │
│  │                            │   the commodity     │
│  ├ HEADLINE line 1 y 250-430  │   subject lives     │
│  ├ HEADLINE line 2 y 430-610  │   here, unobstructed│
│  ├ HERO LINE       y 650-720  │   and never covered │
│  └ CTA pill        y 780-860  │   by text           │
│                                                     │  y=960
├───────────── BOTTOM STRIP (full bleed) ─────────────┤
└─────────────────────────────────────────────────────┘  y=1080
```

- **Safe margin 80px** on all four edges. No text or arrow closer than that to any edge.
- **Everything in the text column is LEFT-ALIGNED on a single rag at x=80.** Not centred, not
  justified, not mixed. One hard left edge is what makes wildly different art directions still
  feel like one publication — and at feed-thumbnail size a single left rag is read fastest.
  The CTA sits on that same rag; do not float it right.
- **Bottom strip is 120px tall (y 960→1080), full bleed edge to edge**, and is the only element
  that touches the canvas edges.
- **Hero art zone (x 1100→1920) must stay clear of all text.** The subject's focal point belongs
  here, roughly on the right third.
- **Scrim:** a smooth LEFT-TO-RIGHT linear gradient — dark at x=0, fully transparent by x≈1250 —
  plus a slight darkening just above the bottom strip. It must only darken; the art stays sharp
  and in focus underneath. **NO gaussian blur, NO frosted glass, NO depth-of-field blur.**
- **Absolutely NO circular, oval, arch or rounded-card mask, and no vignette.** The composition
  is a full-bleed rectangle to all four corners. *(The square-preview generator biases toward a
  circular badge crop; at 1920×1080 this must never appear. State the ban in every prompt.)*

Treatments with a light ground (newsprint, riso, screen print) use dark text on the paper and
skip the scrim — the grid above still governs positions.

---

#### 4.3 AXIS 1 — SUBJECT (open by design)

**Do NOT hard-bind the picture to the Samachar hero commodity.** That is one source among
several, and defaulting to it would collapse this axis to a single idea and make every image a
literal illustration of the headline. The subject only has to feel like *the day's market* — it
does not have to match the headline, and it need not show a commodity at all.

**Step A — pick the SOURCE (rotate this too):**

| Source | What it shows |
|---|---|
| **नायक जिंस** | the hero commodity's world — one option, not the default |
| **कोई और जिंस** | any *other* commodity that moved today — a तेज/मंदा card, a रुझान line, a quiet mover the body mentions |
| **कई जिंसें एक साथ** | an ensemble of the day's movers together — sacks, bowls, heaps side by side |
| **व्यापार** | the trade itself — trade floor, auction, weighing, ledger and cash box, hands haggling; no single commodity foregrounded |
| **दुकान** | the retail side — kirana counter, shelves, jars, the buyer |
| **रास्ता** | the route — trucks, mandi gate, porters, warehouse doors |
| **मौसम / अवसर** | the context — monsoon over fields, festival stocking, harvest calendar |
| **कोई जिंस नहीं** | no commodity at all — a pure typographic, material or print-craft composition where the TREATMENT is the image (a newspaper page, a riso poster, a paper-cut) |

**Step B — if a commodity *is* shown, pick its stage:** खेत/फसल (standing crop, harvest,
threshing) · मिल/कारखाना (crushing, refining, packing, silos) · मंडी (open sacks, weighing) ·
ढुलाई (trucks, gates, porters) · गोदाम/सुखाई (drying yards, stacked bags) · दुकान (shelves,
counter) · मैक्रो (extreme close-up of the raw material).

**Rules**

1. **Rotate the SOURCE, not just the treatment.** If the hero commodity is the source more than
   roughly a third of the time, the axis is being under-used. `कोई जिंस नहीं` and `व्यापार`
   days are just as valid as a harvest day.
2. The subject **may contradict the headline's lead** — a चीनी-led day can perfectly well show a
   wheat harvest, a full mandi floor, or nothing but a printed page. Only the mood must match.
3. Pick what will actually make a beautiful frame that day, then let the ledger stop repeats.
   Do not derive it mechanically from any single field.
4. **Hard exclusion carries over:** सोना-चांदी / सर्राफा is never the subject, even when bullion
   moves most.

---

#### 4.4 AXIS 2 — TREATMENT (rotates, and must be INVENTED each time)

Treatments are grouped into families. **The families are scaffolding, not a list to cycle
through.** Each day, pick a family that respects the cooldown, then *invent a specific new
treatment inside it* — a named, concrete art direction with its own palette, medium and mood.
"Newspaper" is a family; *which* newspaper is a fresh decision every time.

| Family | Invent within it, e.g. |
|---|---|
| **दस्तावेजी फोटो** | golden-hour documentary · blue-hour cinematic · monsoon overcast · harsh noon high-contrast · lantern-lit night shift |
| **छपाई / प्रिंट** | 1960s letterpress b/w · 1980s tabloid with one spot colour · Hindi broadsheet on cream stock · microfiche archive · smudged proof sheet — **always with a halftone photo block, never type alone (see 4.6 #11)** |
| **चित्रण** | two-colour risograph · mid-century screen print · woodcut/linocut · ink-wash brush · flat geometric vector · truck-art folk motif |
| **पदार्थ / मैक्रो** | duotone crystal macro · light-table backlit grain · soft-shadow flat-lay on linen · wet-plate texture |
| **पुरालेख** | sepia archival · faded photo-album print · hand-tinted postcard · vintage almanac plate |
| **रचित** | paper-cut diorama · miniature tabletop set · long-exposure light trails at a mandi gate |

**Rules for the rotation**

1. **14-day cooldown on the specific treatment**, and **no back-to-back family.** Yesterday
   photographic → today print, illustration, macro, archival or constructed.
2. **Never repeat a specific treatment already used in the last 14 days**, even inside an
   allowed family. Newsprint this week must be a visibly different newspaper next time — change
   the era, the stock, the spot colour, the halftone coarseness.
3. **Aim for roughly half photographic, half non-photographic across any 14-day window.** An
   all-photo fortnight reads as one texture; an all-illustration fortnight stops feeling like news.
4. **Invent at least one treatment per week that is not in the table above.** The table is a
   floor, not a ceiling. Write the invented name into the ledger so it enters the cooldown.
5. The treatment must **serve the story's mood.** A crash is not cheerful. A shortage is not
   sunny. Match the palette to the day's news.

---

#### 4.5 LEDGER — new dedup axes

Add to the `kirana-used-log.json` run entry, alongside the existing fields:

- `samachar_art_subject` — the source chosen, plus the stage if a commodity was shown
  (e.g. `कोई और जिंस / गेहूं / खेत`, `व्यापार / मंडी`, `कोई जिंस नहीं`). Rotate the SOURCE
  across the window, not only the stage — the hero commodity should not be the source more than
  about a third of the time.
- `samachar_art_treatment` — the **specific invented treatment name**, not the family
  (e.g. `1980s tabloid spot-red halftone`, not `print`)

Before drafting, read the last 14 runs and drop every treatment and family used. These two are
dedup axes exactly like the Samachar hero and the trending themes — a repeat is a defect.

---

#### 4.6 FAILURE MODES — all observed in testing, all must be defended against

| # | Failure | Defence (state it in the prompt every time) |
|---|---|---|
| 1 | Circular/oval badge crop, vignette | Ban circular/oval/arch masks and vignettes explicitly; demand full-bleed rectangle to all four corners |
| 2 | Heavy art style swallows the chassis — tag/ticker/CTA silently dropped | List the five chassis elements as mandatory; confine the art to the hero zone; draw the chassis as flat UI *on top* |
| 3 | **Ticker arrow colours inverted to the Western scheme** | Give the colour for **each item individually**, and state the Indian rule twice: RED = up = तेज, GREEN = down = मंदा |
| 4 | A Devanagari conjunct renders wrong (seen once: क्विंटल → किवंटल) | Rare, and **not a reason to avoid the word.** `क्विंटल` renders correctly in production — a single bad render is a one-off, not a pattern. Ask for correct spelling and conjuncts explicitly (`spell every word exactly as given`) and eyeball the output; never reword or drop a unit to work around it |
| 5 | Real packaging with legible brand text leaks into photos | Ban packets, wrappers, signage, hoardings, banners, number plates and any readable text inside the photograph |
| 6 | Generator times out (>60s) on long prompts | **Keep the whole image_prompt under ~1800 characters.** Compact phrasing. If it times out, shorten — do not resend the same length. **But shorten the ART paragraph ONLY — see the prompt budget below** |
| 6b | **Compressing the prompt silently kills the chassis** | Observed: trimming a prompt to beat the timeout produced a gorgeous photo with zero text on it. The CHASSIS, LAYOUT and BOTTOM STRIP blocks are load-bearing — never compress them to save characters. Cut adjectives from the art description instead |
| 6c | A strong full-frame photograph overrides the UI | The richer and wider the photographic subject, the likelier the generator treats the brief as "make this photo" and forgets the furniture. For photographic treatments, state the art as occupying the RIGHT THIRD with a clear text field at left, and keep the chassis wording verbatim and complete |
| 7 | Small icons in the ticker render only ~half the time | Icons are **optional**; the arrow carries direction. Never let a missing icon break the row |
| 8 | Hero number reads as a rate without its unit | Hero line must be a complete, honest sentence. Never fabricate a number — it comes from the PDF |
| 9 | Text overflow at thumbnail size | Headline ≤2 lines, ≤18 chars per line. Ticker ≤6 items. If the hero commodity name is long, drop a ticker item rather than shrink type |
| 10 | Bullion appears in the art | सोना-चांदी never as subject, headline or ticker icon (body text is still fine) |
| 11 | **A print treatment renders as a blank page** | Newsprint/riso/screen-print styles will happily produce columns of type texture and nothing else, which reads as empty. **Every print treatment must carry a picture** — name a photo block in the right third, in a thin keyline box. That photo plus the one reason line under it is the entire content; do NOT add headings or page furniture to compensate (see 15, 15b). If it still reads thin, make the photo BIGGER rather than adding elements |
| 12 | Ink misregistration fringes the headline | "Slight misregistration" applied to Devanagari headline type reads as a blur or rendering fault, not as print charm. **Confine misregistration to the spot-colour plate and flat blocks; state that the headline type stays crisp and perfectly registered** |
| 13 | Always framing the art the same way | Full-bleed and a framed inset panel **both look good — neither is wrong.** What is wrong is locking to one. Treat the frame as part of the rotation: some days the art bleeds to the top, right and bottom edges, other days it sits in a panel with a visible edge. Just never the same choice every day |
| 14 | **Devanagari digits (`२७ अगस्त २०२६`)** | Observed even with "Arabic numerals" in the prompt. State it as a prohibition, not a preference: **"Numerals must be Arabic 0-9 — NEVER Devanagari digits (०१२३४५६७८९)"** |
| 15 | **Invented gibberish words, and filler generally** | Image models render short Devanagari strings well and paragraphs never — asking for article text yields broken non-words (`काष्पाय रलेग का बाझाग`). Substituting grey placeholder bars fixes the gibberish but looks like filler, which is worse. **The answer is less, not different.** A print page carries exactly two things: a photo, and one small line beneath it. **No headings, no sub-headlines, no text columns, no grey bars, no charts, no dummy blocks** — the rest is bare paper. See 15b for what that one line says |
| 15b | **The line under the photo — the only body text allowed** | It is not a decorative caption: it states the **REASON the hero commodity moved**, in one short Hindi sentence of about 6–9 words, set very small under the picture. It must be **lifted from the day's VK paper — the actual cause the paper reports — never invented, never generic.** E.g. for a sugar crash driven by the centre ordering full quota offtake: `केंद्र ने अगस्त का पूरा कोटा बेचना अनिवार्य किया`. This also gives the image a real information hierarchy: the headline says *what*, the hero line says *how much*, this line says *why*. If the paper gives no clear reason, shorten it or drop it — never fill the gap |
| 16 | Stray blocks land in the headline column | Page furniture (boxed columns, infographics, captions) drifts left and reads as a redaction block over the text. **Confine ALL furniture to the right third; the left is clean ground** |

**AVOID also:** clutter, poor contrast, rainbow palettes, sparkles, lens flare, glow.

**Amended price rule (supersedes the old "no specific prices" line):** the image may carry
**exactly ONE number — the hero price move.** That number is the hook. No rate table, no
per-commodity levels, no absolute prices in the ticker; those stay in the post body so the click
still pays off.

---

#### 4.7 ASSEMBLED PROMPT — fill and keep under ~1800 characters

**Prompt budget.** Of that ~1800, spend roughly: ART ≈450–600 chars, LAYOUT ≈550, BOTTOM STRIP
≈450, closing rules ≈150. Photographic treatments fit in ~450; **print and illustration
treatments genuinely need ~600**, because the page furniture has to be described or the picture
comes out empty (see 11). **1800 is the hard cap, 450 is only a guide.** If you must cut, **cut
the ART sentence and nothing else** — a thinner art description yields a plainer picture, whereas
a thinner chassis yields no text at all (see 6b). Keep LAYOUT and BOTTOM STRIP verbatim.

```
Hindi market news thumbnail, 1920x1080 landscape, Devanagari script only, no English or Latin letters.

ART: [SUBJECT scene, from 4.3 — any source: a commodity of the day at any stage, the trade itself, the shop, the route, the season, or no commodity at all] rendered as [INVENTED TREATMENT, from 4.4 — medium, palette, mood]. [Framing — rotate this, see 4.6 #13: either "Full-bleed rectangle to all four corners" OR "art sits in a clean framed panel in the right two-fifths with a visible edge".] NO circular or oval mask, NO vignette. Subject sits in the right third. All page furniture stays in the right third; the left is clean ground. [Scrim line: dark left-to-right gradient fading out by mid-frame, darkens only — photo stays sharp, no blur.] No packets, signage, banners or readable text inside the artwork.

LAYOUT: all text left-aligned on one rag at the left margin; right third stays clear of text.
Top-left: [accent] pill with "किराना समाचार", beside it "[DD माह YYYY]".
Headline, huge heavy [colour] Devanagari, two lines: "[LINE 1]" / "[LINE 2]".
Below it in [accent]: "[HERO LINE — one price move, ALWAYS with its unit, e.g. प्रति क्विंटल]".
Below that, left-aligned [accent] pill: "पूरी रिपोर्ट पढ़ें →".
No tiles, no cards, no side panels.

BOTTOM STRIP, full width across the very bottom: solid RED box "आज की मंडी", then names with triangle arrows —
"[c1]" [colour1] [up/down], "[c2]" [colour2] [up/down], "[c3]" [colour3] [up/down], "[c4]" [colour4] [up/down], "[c5]" [colour5] [up/down], "[c6]" [colour6] [up/down].
Indian mandi convention: RED arrow = up = rising, GREEN arrow = down = falling. Do not invert.

Heavy geometric Devanagari. Spell every word correctly with correct conjuncts, exactly as given above. Numerals must be Arabic 0-9 — NEVER Devanagari digits (०१२३४५६७८९). Any word shown inside the artwork must be a short real Hindi phrase from the day's news, and there must be NO filler text of any kind. No logos or watermarks.
```

Fill the ticker colours **per item** from the day's directions — never leave them to the model.

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
