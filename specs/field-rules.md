# Field rules reference — Kirana daily posts

Read this before drafting. The master prompt (`_KIRANA NEWS RESEARCH + AUTOMATED POSTING AGENT.docx`
in the project) is the full spec; this is the condensed working version.

## The 8 posts

1. **Samachar** — pan-India mandi update. Special inline-styled HTML (hero card + तेज/मंदा cards +
   स्थिर strip + अन्य हलचल table + आज का सवाल + footer). तेज cards = red text `#c62828` on pink
   `#FFF5F5`; मंदा cards = green text `#2e7d32` on light-green `#F1F8F1` (box BGs fixed; only text
   colour flips). Pick the single biggest mover as HERO. Attach correct unit to every price (सोना
   प्रति 10 ग्राम, चांदी प्रति किलो, दालें/चना/चीनी प्रति क्विंटल, तेल प्रति क्विंटल, कच्चा तेल डॉलर
   प्रति बैरल, etc.). **Pack it WIDE** — Samachar is the broadest post: sweep the whole paper
   (front articles + the अनाज/दाल-दलहन/सर्राफा/तेल-तिलहन rate tables + भाव-भविष्य boxes) and
   surface **≥18–22 distinct commodities** via ~3–4 तेज + ~3–4 मंदा cards (bundling related items),
   a 5–8 row अन्य हलचल table and a 3–5 item स्थिर strip. Do NOT ship a thin ~8–10 item Samachar
   when the paper has more. Breadth must not cost relevance or accuracy — only kirana-relevant
   commodities, real PDF prices, correct units, no padding, no fabrication. (Full rule:
   `kirana-posts-content.md` → "COVERAGE MANDATE".)
2. **सोया तेल** — सोया तेल + सरसों तेल combined, one deeper analysis (price change, reason, outlook,
   kirana impact). `commodity` = `सोया तेल`.
3. **दाल/शक्कर** — pick ONE dal OR sugar. Prefer a commodity with a direction change (तेजी/मंदी)
   over स्थिर. Rotate the dal type day to day. `commodity` ∈ {दाल, मूंग दाल, तूर दाल, उड़द दाल,
   चना दाल, शक्कर}.
4. **Other commodities** — spices / dry fruits / gold-silver / grains. `commodity` from the
   approved list (मसाले, हल्दी, जीरा, सोना-चांदी, बादाम, मखाना, चावल, गेहूं, ...).
5. **रुझान** — the day's prediction board. Cover **as many commodities as the VK भाव-भविष्य / जिंस-विश्लेषण
   boxes give** (typically 12–18), each as its own `<p>` line in the fixed 3-part shape: **अभी का भाव**
   (current price + unit from the paper) → **रुझान** (short reason/direction) → **आगे का संभावित भाव**
   (target price where the paper states one, e.g. "6500 की ओर"; else the expected direction). **Where the
   paper's numbers allow it (current price + a stated target or change), ALSO give the expected % rise/fall**
   — either derived from the two paper numbers (e.g. मोठ 5900→6500 ≈ +10%) or a %/figure the paper itself
   prints (e.g. हल्दी वायदा +1.47%). The **% is OPTIONAL and NEVER fabricated**: include it only when it
   follows from real paper numbers, and simply omit it (give direction only) when the paper prints no figure —
   do not write filler like "प्रतिशत नहीं". Bold the commodity name and key numbers with `<b>`. **Categorize
   every commodity by its FORWARD outlook (रुझान) into three clearly-labelled `<p><strong>` sections:**
   `🔺 तेजी के आसार (भाव बढ़ेंगे)`, `🔻 मंदी/नरमी के आसार (भाव घटेंगे)`, and `↔️ स्थिर / सीमित दायरे में` — a
   commodity that fell today but is expected to rise/hold goes by its outlook, not today's move (note the recent
   move in its line). Within the तेजी section, sort strongest-expected-move first. Prices AND percentages come
   ONLY from the paper — never fabricate a target or a %. The 4-card THUMBNAIL must stay consistent with these
   buckets (its arrows match each commodity's outlook).
   `commodity` = `रुझान`. **The रुझान THUMBNAIL still shows only 4 commodities max** (the 4-card image),
   even though the body lists many — pick the 4 with the clearest moves.
6 & 7. **Pan India Trending News 1 & 2** — the **2 most relevant** kirana stories of the day, picked
   from the FULL theme pool (fraud/scam, raids, FMCG, economy/fuel, supply chain, agri/monsoon/weather,
   trade assoc, UPI-payment benefits, rural-demand, new-product/distributorship, festival/seasonal
   demand, ONDC/online, FSSAI/license, store-growth tips, success stories, tech, + a Miscellaneous
   catch-all). **No hard "one must be fraud" rule; neither has to be a scheme.** The two must be
   different themes and unrelated. Web-searched, fresh ≤24h, tier-3 simple Hindi, open-ended question
   at the end. Excluded always: quick-commerce, app/tech-company news, stock market, "kiranas
   dying" narratives. GST normally skipped — only a ground-breaking structural change (GST 2.0 rate
   cut, new merchant incentive) once in a while, and only if explained from scratch in simple Hindi
   across title/thumbnail/PN/body. **Weekly cooldown:** an EVERGREEN topic (scam, monsoon, anything postable on any
   other day) used in the last 7 days is skipped today — unless it's genuinely breaking news-of-the-day.
   **Rank by relevance + historical click/engagement** (Mixpanel 2551336; itemIDs in
   `news_generation_logs`). Rotate so every theme appears over ~2–3 weeks; avoid two heavy-negative
   posts the same day (aim net-positive ≥4/7 days). Full rule: `kirana-posts-content.md` → Section 4.
8. **Pan India Schemes** — one active central scheme with eligibility + apply process + impact +
   CTA ("आज ही आवेदन करें"). Need not be ≤24h, but must be currently active and not recently used.

## post_description format

Standard posts: clean minimal HTML. First `<p><strong>Heading</strong></p>` (2–5 word category
heading, e.g. `तेल–तिलहन बाज़ार अपडेट - 18 जून`), then content in separate `<p>` tags. No nested
`<div>` inside `<p>`. No italics/underline/multi-colour. Every sentence ends with `।`. No source
lines, no links, no citation markers. Samachar OVERRIDES this with its inline-styled card HTML.

## Title format

`[DD महीना]: [Category Label] - [Catchy Hook] [Emoji]`. Date in Arabic numerals + Hindi month.
Direction-driven hooks: TEJI → तेजी/उछाल/महंगा; MANDI → गिरावट/नरमी/सस्ता; STHIR → स्थिर/थमे;
RUJHAN → future tense (बढ़ेगी/गिरेगी); SCHEMES → सौगात/फायदा/मिलेगा. 40–100 chars, dramatic but
tier-3 simple.

## Push notification (3 lines, per post)

- `notification_title` = Line 1 only: `<p><span style="color:[Line1];"><b>[text] [emoji]</b></span></p>`
- `notification_description` = Lines 2+3:
  `<p><span style="color:[Line2];"><b>[L2] [emoji]</b></span><br><span style="color:[Line3];"><b>[L3] [emoji]</b></span></p>`
- Line 1 = specific number/price/shock + 1 emoji. Line 2 = curiosity/context (commodity posts:
  never answer "what to do", just tease). Line 3 = short 3–4 word CTA + emoji. One emoji per line,
  no duplicate emoji across the PN. Complete Hindi phrases with prepositions; no comma-spliced
  fragments. Devanagari `।`. The Samachar PN must use a different commodity from the four commodity
  posts.

### Rujhan PN is a quiz
Title = open-ended question (`[commodity] के भाव आगे कैसे चलेंगे? 🤔`). Description line 1 =
options with exact spacing `A)⬆️बढ़ेंगे |  B)⬇️घटेंगे |  C)↔️स्थिर` (no space after `A)`, no space
after the arrow, ONE space before `|`, TWO spaces after `|`), then a single `<br>`, then a FOMO CTA
(`क्या आप सही हैं? जानें यहां 💡`). Rotate the commodity daily — never back-to-back, avoid चीनी
every day.

## Colour schemes (pick 8 daily = 5 light + 3 dark, assign non-sequentially)

Light: `#E7EEE8`, `#EDEDD9`, `#D6F0EE`, `#EBE0EE`, `#E6D0E0`, `#E8F5F0`, `#F0E8F5`.
Dark: `#461B83`, `#6D370F`, `#114883`. Each scheme has matching Line1/Line2/Line3 text colours —
see the master prompt's colour table; use the colours that go with the chosen bg in each PN.

## image_prompt rules (ALL 8 posts)

Every post MUST have an `image_prompt`. Use the PART 1 + PART 2 templates from the master prompt,
filling variables from the post.

### Samachar / Trending News / Schemes (1920×1080 landscape)
- Samachar: contextual commodity background, date+type, main headline, CTA "पूरी रिपोर्ट पढ़ें →".
- Trending News 1 & 2: relevant contextual background, two-line headline, CTA based on story type.
- Schemes: thumbnail **120×138**, text centred, CTA "अभी आवेदन करें →".

### Commodity posts — सोया तेल, दाल/शक्कर, Other commodities (1920×1080 landscape)
Minimal editorial-style commodity spotlight:
- Full-bleed commodity close-up as background (no English labels, no bottles with text)
- Top-left: dark date pill. Top-right: distinct colored category pill (warm gold for तेल, earthy
  brown for दाल, spice-toned for मसाला, etc.)
- Bottom ~35-40%: smooth transparent-to-dark gradient (NOT a solid bar, NOT blurred — photo stays
  sharp underneath, only darkened). Must cover BOTH text lines.
- LINE 1: commodity name in very large bold white Devanagari
- LINE 2: direction badge pill (RED #D32F2F for तेजी, GREEN #2E7D32 for मंदी, GREY #757575 for
  स्थिर) + price change text in white
- No sparkle, no blur, no lens flare, no decorative effects

### Rujhan (1920×1080 landscape)
4-card layout "मंडी का रुझान" + date, each commodity row with direction text + UP/DOWN arrow
(green up = तेजी, red down = मंदी).

## pn_image_prompt rules (only Samachar, दाल/शक्कर, रुझान, TN1, TN2)

Fixed 4:3 centred glassy-overlay template (TOP_TAG from post_title before " - ", HEADLINE from
notification_title text, SUBTEXT = nd line 1, CTA = nd line 2). Background derives from
post_description only. **रुझान overrides** this with a VAR rotation by `date mod 4`:
1 → VAR1 FOMO Locked Trend; 2 → VAR2 Premium Financial Spotlight (extract the ONE commodity with
largest % change); 3 → VAR3 High-Impact Alert (only if ≥4% change, else fall back to quiz style);
0 → VAR4 Minimal Physical Speedometer. Copy the chosen VAR's full text from the master prompt.

## Language guardrails

Simple spoken Hindi for tier-2/3 owners. Acronyms with no Hindi equivalent stay Roman (UPI, GST,
CSC, FAO, CEO, ATM). Brand names keep original spelling (Nestlé, Reliance, Blinkit). Never write
English words in Devanagari. Never use `$` — write "डॉलर". No stock-market coverage. GST normally
skipped — rare ground-breaking change only, explained from scratch (see post 6 & 7 note). No
quick-commerce promotion. Every item must pass: "does this affect a kirana owner's buying, selling,
stocking, or wallet?" — if not, drop it.

## Avoid repeating yesterday

Before drafting, retrieve yesterday's run (conversation_search "kirana posts" / recent_chats) and
make today differ on: Samachar hero, oil direction, the dal/sugar pick, the Other pick, the rujhan
quiz commodity, both trending topics, and the scheme. **For trending news, keep a 7-day rolling
ledger of used themes** (scam, monsoon, FMCG, etc.) and skip any evergreen theme already used in the
last week unless it's genuinely breaking that day — this is what stops the daily-scam / repeat-monsoon
pattern. Keep a rolling memory of recently used schemes
and avoid the standard already-covered list (Jan Dhan, MUDRA, SVANidhi, Ayushman/PMJAY, PMJJBY,
PMSBY, APY, Shram Yogi Maandhan, PMAY, Ujjwala, Sukanya, Vishwakarma, Lakhpati Didi, Startup/Skill
India, plus any used in the last ~2 weeks).
