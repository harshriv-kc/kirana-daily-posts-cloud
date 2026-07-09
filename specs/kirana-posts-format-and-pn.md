# KIRANA POSTS — FORMAT, TITLES, PUSH NOTIFICATIONS

---

## TITLE GENERATION GUIDELINES

**Format:** `[Date]: [Category Label] - [Catchy Hook] [Emoji]`

### A. DATE & CATEGORY

**Date:** DD महीना: (e.g., 29 अक्टूबर:)

The POSTING DATE is always mentioned at the top of the prompt. The agent must automatically read this date and use that exact date in every post headline. Always write the date in Arabic numerals (0-9) and Hindi month names — e.g., 08 नवंबर:, 09 दिसंबर:, 10 जनवरी:

While researching, the agent may collect information from the past 24 hours (IST), even if events belong to two different calendar days. However, every generated post must display only the single Posting Date in Hindi format.

**Category Labels:**
- Soya Tel: तेल बाजार-
- Dal/Shakkar: दाल बाजार- OR शक्कर बाजार-
- Other commodities: [Commodity] बाजार- (e.g., मसाला बाजार-, सोना-चांदी-)
- Samachar: किराना समाचार |
- Rujhan: मंडी रुझान -
- Trending News: ट्रेंडिंग न्यूज़ -
- Schemes: सरकारी योजना -

### B. CATCHY HOOK (DYNAMIC - Based on Research)

**For TEJI (Price Increase):** Words: तेजी, बढ़ोतरी, उछाल, चढ़ा, महंगा, आसमान पर
**For MANDI (Price Decrease):** Words: गिरावट, मंदी, नरमी, टूटा, फिसला, सस्ता
**For STHIR (Stable):** Words: स्थिर, थमे, कोई बदलाव नहीं
**For SAMACHAR:** Format: [2-3 commodities] में [directions]
**For RUJHAN:** Use FUTURE TENSE: गिरेगी, बढ़ेगी, होगा, रहेगी
**For SCHEMES:** Words: सौगात, फायदा, मिलेगा, लाभ
**For TRENDING:** Use exclamation marks, numbers, create urgency. Not complex for tier-3 people.

### C. EMOJIS
- Soya Tel: 🛢 | Dal: 🥣 | Shakkar: 📉 or 📈 | Spices: 🌶 | Dry Fruits: 🥜 | Grains: 🌾
- Gold/Silver: 💰 | Samachar: 💹 | Rujhan: 💸 | Schemes: 💸 | Trending: 🔥 🤯 📈 ⚡ (vary)

### D. RULES
- Length: 40-100 characters (excluding date)
- Tone: Conversational, dramatic, urgent Hindi
- Daily Variation: Never repeat exact phrases
- Dynamic: Direction based on actual market research, NOT fixed

### E. EXAMPLES

❌ BAD: "29 अक्टूबर: तेल की कीमत बढ़ी" / "29 अक्टूबर: मंडी अपडेट"

✅ GOOD:
- "29 अक्टूबर: तेल बाजार- सोया तेल में भारी तेजी! दाम आसमान पर 🛢"
- "29 अक्टूबर: दाल बाजार में हलचल! चना टूटा ₹25, अरहर चढ़ी ₹50 🥣"
- "29 अक्टूबर: सरकारी योजना - बड़ी सौगात! छोटे उद्योगों को मिलेगा ₹5 लाख 💸"
- "29 अक्टूबर किराना समाचार | तेल हुआ सस्ता, मसाले हुए महंगे 💹"

---

## POST DESCRIPTION HEADING

Each post description should start with a short, bold heading (2-5 words):

Format: `[Category] बाजार अपडेट` or `[Category] - [Date]`

Examples: शक्कर बाजार अपडेट, ट्रेंडिंग न्यूज़ - 29 अक्टूबर, सरकारी योजना - 29 अक्टूबर

CRITICAL: Always wrap in `<p><strong>Heading Text</strong></p>` tags.

---

## POST DESCRIPTION FORMAT

All post descriptions in clean, minimal HTML with proper paragraph tags.

**OVERRIDE FOR SAMACHAR:** The Samachar post uses a special inline-styled HTML format (see Samachar HTML Template below). All other 7 posts use the standard `<p><strong>` format.

**HTML RULES:**
- DO NOT wrap content in `<div>` tags — causes nesting issues
- Begin with heading using `<strong>` inside first `<p>` tag
- After heading, content in new separate `<p>` tags
- Use `<br>` sparingly, only within paragraphs
- No nested `<div>` inside `<p>` or `<p>` inside `<div>`
- No italics, underline, or multiple colours
- No "Source:" lines or external links
- Every sentence ends with पूर्ण विराम (।) — Devanagari punctuation, NOT English full stop (.)

**Example:**
```html
<p><strong>तेल–तिलहन बाज़ार अपडेट - 26 दिसंबर</strong></p>
<p>आज मंडियों में सोया तेल के भाव ₹142 से घटकर ₹134 प्रति लीटर हो गए हैं, जबकि सरसों तेल ₹160 पर स्थिर है। अंतरराष्ट्रीय बाजार में सप्लाई बढ़ने और मांग घटने से यह मंदी आई है।</p>
<p>किराना दुकानदारों के लिए यह खरीदारी का अच्छा समय है क्योंकि आने वाले दिनों में दाम और नीचे जा सकते हैं।</p>
```

---

## SAMACHAR HTML TEMPLATE

CRITICAL: ALL placeholder values below are examples ONLY. Extract real data from VK PDF. Never copy sample text.

```html
<p style="font-size:15px;color:#333;margin-bottom:14px;line-height:1.55;">🙏 [1-2 LINE SUMMARY OF DAY'S BIGGEST THEMES FROM PDF]. <b>किराना पर सीधा असर:</b></p>

<div style="background:linear-gradient(135deg,[HERO_BG_LIGHT],[HERO_BG_DARK]);border:2px solid [HERO_BORDER];border-radius:12px;padding:14px 14px;margin-bottom:14px;">
<p style="font-size:10px;text-transform:uppercase;color:[HERO_LABEL_COLOR];font-weight:800;letter-spacing:1.5px;margin-bottom:6px;">[HERO_EMOJI] सबसे बड़ी खबर</p>
<p style="font-size:19px;font-weight:900;color:[HERO_HEADLINE_COLOR];margin-bottom:8px;line-height:1.3;">[HERO HEADLINE — BIGGEST MOVER FROM PDF]</p>
<p style="font-size:14px;font-weight:700;color:#333;line-height:1.35;margin-bottom:8px;">[HERO SUB-HEADLINE — KEY DETAIL]</p>
<p style="font-size:12px;color:#666;line-height:1.4;">[HERO CONTEXT/WARNING — 1 LINE]</p>
</div>

<p style="font-size:14px;font-weight:800;color:#c62828;margin:14px 0 10px;border-bottom:1.5px solid #ef9a9a;padding-bottom:4px;">⬆️ तेज — ये बढ़ा</p>

<!-- REPEAT THIS CARD FOR EACH तेज COMMODITY/GROUP -->
<div style="background:#FFF5F5;border:1px solid #FFCDD2;border-radius:10px;padding:10px;margin-bottom:8px;display:flex;gap:10px;">
<span style="font-size:20px;">[EMOJI]</span>
<div>
<p style="font-weight:800;font-size:14px;color:#c62828;margin-bottom:4px;">[COMMODITY NAME/GROUP — तेज]</p>
<p style="font-size:13px;color:#333;line-height:1.5;">[COMMODITY 1]: <b>[PRICE] प्रति [UNIT]</b><br>[COMMODITY 2]: <b>[PRICE] प्रति [UNIT]</b></p>
<p style="font-size:12px;color:#555;margin-top:4px;">[REASON FOR PRICE RISE — FROM PDF]</p>
</div>
</div>
<!-- END REPEAT -->

<p style="font-size:14px;font-weight:800;color:#2e7d32;margin:14px 0 10px;border-bottom:1.5px solid #a5d6a7;padding-bottom:4px;">⬇️ मंदा — ये गिरा</p>

<!-- REPEAT THIS CARD FOR EACH मंदा COMMODITY/GROUP -->
<div style="background:#F1F8F1;border:1px solid #C8E6C9;border-radius:10px;padding:10px;margin-bottom:8px;display:flex;gap:10px;">
<span style="font-size:20px;">[EMOJI]</span>
<div>
<p style="font-weight:800;font-size:14px;color:#2e7d32;margin-bottom:4px;">[COMMODITY NAME/GROUP — मंदा]</p>
<p style="font-size:13px;color:#333;line-height:1.5;">[COMMODITY 1]: <b>[PRICE] प्रति [UNIT]</b> ([CHANGE]↓)<br>[COMMODITY 2]: <b>[PRICE] प्रति [UNIT]</b> ([CHANGE]↓)</p>
<p style="font-size:12px;color:#555;margin-top:4px;">[REASON FOR PRICE FALL — FROM PDF]</p>
</div>
</div>
<!-- END REPEAT -->

<div style="background:#F5F5F5;border-radius:8px;padding:10px;margin:12px 0;font-size:12px;color:#666;line-height:1.8;">
<b style="color:#555;">↔️ स्थिर:</b> [COMMODITY] [PRICE] प्रति [UNIT] | [COMMODITY] [PRICE] प्रति [UNIT]
</div>

<div style="background:linear-gradient(135deg,#FFF8E1,#FFE082);border:1px solid #FFB300;border-radius:10px;padding:10px 12px;margin:10px 0;">
<p style="font-weight:800;font-size:12px;color:#4E342E;margin-bottom:8px;">📌 अन्य हलचल</p>
<!-- REPEAT FOR EACH SMALL MOVER -->
<p style="display:flex;justify-content:space-between;padding:5px 0;font-size:13px;border-bottom:1px dotted #FFD54F;"><span style="color:#795548;">[LABEL]</span><span style="font-weight:700;color:#4E342E;">[VALUE WITH UNIT]</span></p>
<!-- END REPEAT — LAST ROW: remove border-bottom -->
</div>

<div style="background:#E3F2FD;border:1px solid #90CAF9;border-radius:8px;padding:10px;margin-top:10px;font-size:13px;color:#1565C0;line-height:1.5;">
<b>💡 आज का सवाल:</b> [ENGAGING QUESTION BASED ON DAY'S BIGGEST MOVE] 👇 कमेंट करें।
</div>

<p style="text-align:center;font-size:12px;color:#d32f2f;font-weight:700;margin-top:12px;">📆 कल फिर मिलेंगे ताज़ा रेट के साथ। लाइक 👍 और शेयर करें।</p>
```

---

## PUSH NOTIFICATION GENERATION

### COLOR SCHEME ASSIGNMENT LOGIC

1. Daily Selection: Pick any 8 schemes (5 light BG + 3 dark BG) from the 10 available
2. Post Assignment: Assign one scheme to each of the 8 posts
3. Color Assignment: Randomly assign colors to posts daily. Do NOT use sequential order
4. Extract bg_color + Line1_Color, Line2_Color, Line3_Color from selected scheme

**LIGHT BACKGROUND SCHEMES (Pick 5):**
1. BG #E7EEE8 | Line1: #003D5C | Line2: #D32F2F | Line3: #008080
2. BG #EDEDD9 | Line1: #C41F7E | Line2: #2E7D32 | Line3: #7B1FA2
3. BG #D6F0EE | Line1: #D32F2F | Line2: #1565C0 | Line3: #6A1B9A
4. BG #EBE0EE | Line1: #E65100 | Line2: #003D5C | Line3: #2E7D32
5. BG #E6D0E0 | Line1: #D32F2F | Line2: #00695C | Line3: #1565C0
6. BG #E8F5F0 | Line1: #C41F7E | Line2: #E65100 | Line3: #1A237E
7. BG #F0E8F5 | Line1: #1B5E20 | Line2: #880E4F | Line3: #311B92

**DARK BACKGROUND SCHEMES (Pick 3):**
8. BG #461B83 | Line1: #FFFFFF | Line2: #C8E6C9 | Line3: #FFF9C4
9. BG #6D370F | Line1: #FFFFFF | Line2: #B2EBF2 | Line3: #FFF9C4
10. BG #114883 | Line1: #FFF9C4 | Line2: #F8BBD0 | Line3: #C8E6C9

---

### CORE PRINCIPLES

**Fixed Structure (Non-Negotiable):** Every push notification has exactly 3 lines:

**Line 1:**
- Contains specific number/price/quantity (for commodity/scheme posts) OR shocking fact/detail (for trending news)
- Must be a COMPLETE meaningful sentence/phrase using Hindi prepositions (में, की, तक, हुई, से, पर, etc.)
- Ends with exactly 1 emoji
- Attention-grabbing, creates shock/curiosity
- NO comma-separated sub-sentences — write ONE cohesive phrase

**Line 2:**
- Provides context/question/impact OR creates curiosity (varies by post type)
- Must be a complete meaningful statement/question
- Ends with exactly 1 emoji
- Builds on Line 1's hook

**Line 3:**
- Clear action verb with complete phrase
- Ends with exactly 1 emoji
- Creates urgency/value proposition
- Must be meaningful, not just "देखें" or "पढ़ें" alone

**HTML Formatting:**
- notification_title: `<p><span style="color:[Line1_Color];"><b>[Line 1] [emoji]</b></span></p>`
- notification_description: `<p><span style="color:[Line2_Color];"><b>[Line 2] [emoji]</b></span><br><span style="color:[Line3_Color];"><b>[Line 3] [emoji]</b></span></p>`

---

### GENERAL RULES

#### Hindi Language Rules

**Mandatory:**
- Use Devanagari punctuation: । (not English period)
- Pure Devanagari script for all Hindi words
- Correct verb conjugation and case markers
- Simple, conversational vocabulary for tier 2/3 audience
- Natural, spoken Hindi tone
- Use Hindi prepositions properly: में, की, तक, हुई, से, पर, को, का, के लिए

**Allowed English (Roman script only):**
- Brand names: Blinkit, Amazon, Reliance, Jio, etc.
- Acronyms without Hindi equivalent: UPI, BHIM, GST
- Common tech terms: app, smartphone (when no simple Hindi exists)

**Common Errors to Avoid:**
- ❌ यूपीआई → ✅ UPI
- ❌ English period (.) → ✅ Devanagari (।)
- ❌ Mixed script in same word
- ❌ Overly formal/bookish Hindi
- ❌ Comma-separated sub-sentences → ✅ Complete meaningful phrases

#### Emoji Strategy

**Line 1 (Emotion/Impact):**
- Shock/Alert: 😱 🔥 ⚡ 💥 🚨
- Positive: 😍 ✅ 💚 🎉 👏
- Negative: 📈 📉 💸 😤 😨
- Neutral impact: 🌟 💡 🎯
- Special: 🌶️ (spices), 💳 (payment/banking), 📲 (tech), 🎁 (schemes/benefits)

**Line 2 (Context/Question):**
- Thinking: 🤔 💭 🧐
- Data/Analysis: 📊 📈 📉 💹
- Money: 💰 💸 💵
- Planning: 💡 🎯 📋
- Time: ⏰ ⌛
- Impact: 😨 ✅

**Line 3 (Action/Urgency):**
- Immediate: 👆 👇 ⚡ 🚀 🏃
- Discovery: 🔍 📖 📰 👀
- Benefit: 💡 💰 🎁 ✨
- Data: 📊 📲

**Emoji Variation Rules:**
- Never repeat same emoji in same position across consecutive posts
- Match sentiment: price decrease = positive emojis, price increase = negative emojis
- Rotate systematically through emoji banks
- CRITICAL: Two same emojis should NOT be used within a single PN (across all 3 lines)

#### Word Count Guidelines (Flexible)

Priority: MEANINGFUL SENTENCES over strict word limits
- If a sentence needs more words to be meaningful and complete, use them
- If word limit makes sentence meaningless, ignore the limit
- Upper limit exists only to prevent notifications crossing 2 lines in mobile display
- Use complete phrases with proper Hindi structure, not fragmented words
- Total notification under 30 words across all 3 lines

---

### POST-SPECIFIC PN PATTERNS

#### 1. Samachar (Pan-India Market Update)

**Line 1 Logic:** Select the most impactful commodity from the Samachar (biggest price increase or decrease) and write a complete meaningful sentence.
IMP: Commodity selected in the PN should not be exactly same as the commodity in the 3 commodity post PNs.

Structure Examples:
- उरड़ दाल में ₹200 की तेजी? [emoji]
- हल्दी ₹300 तक सस्ती हुई? [emoji]
- सोया तेल में ₹45 की गिरावट? [emoji]
- मूंग दाल ₹180 तक बढ़ी आज? [emoji]

Key Points: Use proper Hindi prepositions (में, की, तक, हुई). Complete sentence, not comma-separated. Must include specific price/amount. Choose commodity with highest impact (₹2 change is not impactful, ignore such small changes).

Emoji Selection: Price increase: 😱 🔥 📈 ⚡ 💥 | Price decrease: 😍 ✅ 💚 🎉

**Line 2 Logic:** Select the second most impactful commodity and write similar complete sentence.

Structure Examples:
- प्याज में भी ₹50 का उछाल [emoji]
- चीनी ₹25 तक गिरी आज [emoji]
- सरसों तेल ₹30 सस्ता हुआ [emoji]
- तूर दाल में ₹40 की गिरावट [emoji]

Emoji Selection: 📊 🤔 💰 💸 💭 📈 📉

**Line 3 (CTA):** Must be a meaningful phrase related to market updates.

Examples:
- मंडी अपडेट अभी देखें 👆
- जानें आज की मंडी भाव 📊
- ताजा मंडी रिपोर्ट यहां 📰
- आज के सभी भाव देखें 👇
- पूरी मंडी रिपोर्ट पढ़ें 📖

NOT acceptable: Just "देखें 👆" or "अभी पढ़ें ⚡" — must have context like "मंडी अपडेट"

**Complete Example:**
- Title: `<p><span style="color:#FF0000;"><b>उरड़ दाल में ₹200 की तेजी 😱</b></span></p>`
- Desc: `<p><span style="color:#4CAF50;"><b>प्याज में भी ₹50 का उछाल 📈</b></span><br><span style="color:#2196F3;"><b>मंडी अपडेट अभी देखें 👆</b></span></p>`

---

#### 2. Commodity Price Posts (Oils, Pulses, Sugar, Spices, Dry Fruits, Gold, Silver)

**Line 1 Logic:** Write a complete meaningful sentence about the single commodity, exactly like Samachar Line 1 logic.

Structure Examples:
- सोया तेल में ₹12 की गिरावट [emoji]
- तूर दाल ₹25 तक महंगी हुई [emoji]
- हल्दी में ₹240 का उछाल आया [emoji]
- चीनी ₹18 तक सस्ती मिली [emoji]
- बादाम ₹350 तक बढ़े आज [emoji]
- सरसों तेल में ₹8 की तेजी [emoji]

Emoji Selection: Price decrease: 😍 ✅ 💚 🎉 | Price increase: 😱 🔥 📈 ⚡ 💥 🌶️ (use 🌶️ for spices)

**Line 2 Logic:** Create a curiosity-driven statement (maximum 10-12 words) that makes shop owner want to click without revealing all information.

**Five Approaches (Use one per PN):**

A) Question Format:
- क्या अभी स्टॉक भरना सही रहेगा या इंतजार करें [emoji]
- आपके मार्जिन पर क्या होगा असर जानते हैं [emoji]
- क्या रेट स्थिर रहेंगे या बदलेंगे [emoji]
- कल और घटेगा या बढ़ जाएगा [emoji]

B) Teasing/Hint Format:
- किराना व्यापारियों के लिए जरूरी अपडेट है ये [emoji]
- व्यापारी क्या कर रहे हैं जानिए अंदर [emoji]
- इस हफ्ते बड़ा बदलाव आने वाला है [emoji]
- थोक बाजार में कुछ अलग हो रहा है [emoji]

C) Alert/Warning Format:
- सतर्क रहें - बड़ा बदलाव संभव है [emoji]
- ये जानकारी आपका नुकसान रोक सकती है [emoji]
- समय पर एक्शन लेना जरूरी है [emoji]

D) Impact Teaser:
- आपके बिजनेस को सीधा प्रभावित करेगा ये [emoji]
- अगले 2 दिन बहुत महत्वपूर्ण हैं [emoji]
- थोक भाव में और बदलाव आ सकता है [emoji]

E) FOMO (Fear of Missing Out):
- ये मिस किया तो पछताएंगे [emoji]
- अभी की गई गलती भारी पड़ेगी [emoji]
- समय रहते जान लें ये बात [emoji]

KEY PRINCIPLE: Never answer "what should I do?" in Line 2. Create curiosity to click.
- ❌ Wrong: थोक भाव और नीचे जा सकते हैं इसलिए अभी खरीदें
- ✅ Right: थोक भाव में और बदलाव आ सकता है

Emoji Selection: 🤔 💭 🧐 📊 💡 🎯 ⚡ 🚨

**Line 3 (CTA) Logic:** Create SHORT action-oriented statement (3-4 words maximum) that connects to Line 2.

CRITICAL RULES: Keep it 3-4 words only. Must connect logically to Line 2 content. Should NOT be completely different from Line 2 topic.

Examples Based on Line 2:
- If Line 2 asks about rates → रेट यहां जानें [emoji]
- If Line 2 asks about timing → जानें अभी [emoji]
- If Line 2 asks about impact → असर देखें 👆
- If Line 2 warns → बचाव यहां [emoji]

Good CTAs (3-4 words): रेट यहां जानें 👆 | जानें अभी ⚡ | पढ़ें यहां 📰 | देखें तुरंत 👇 | अभी चेक करें 📊

NOT acceptable:
- ❌ सभी तेलों के भाव यहां देखें (too long, disconnected)
- ❌ मसालों का बेस्ट रेट यहां पाएं (too long, different topic)
- ❌ दालों की ताजा मंडी रिपोर्ट चेक करें (too long)

Emoji Selection: 👆 👇 ⚡ 📊 📖 📰 💡

**Complete Examples:**

Oil:
- Title: `<p><span style="color:#FF0000;"><b>सोया तेल में ₹12 की गिरावट😍</b></span></p>`
- Desc: `<p><span style="color:#4CAF50;"><b>क्या रेट स्थिर रहेंगे या बदलेंगे🤔</b></span><br><span style="color:#2196F3;"><b>रेट यहां जानें 👆</b></span></p>`

Pulses:
- Title: `<p><span style="color:#FF0000;"><b>तूर दाल ₹25 तक महंगी हुई 😱</b></span></p>`
- Desc: `<p><span style="color:#4CAF50;"><b>किराना व्यापारियों के लिए जरूरी अपडेट है ये 💡</b></span><br><span style="color:#2196F3;"><b>जानें अभी ⚡</b></span></p>`

Spices:
- Title: `<p><span style="color:#FF0000;"><b>हल्दी में ₹240 का उछाल आया 🌶️</b></span></p>`
- Desc: `<p><span style="color:#4CAF50;"><b>समय पर एक्शन लेना जरूरी है ⚡</b></span><br><span style="color:#2196F3;"><b>देखें तुरंत 👇</b></span></p>`

---

#### 3. Rujhan (Market Prediction Quiz)

**CONCEPT:** Uses quiz psychology — ASK shopkeepers to predict instead of telling them. Creates curiosity gap and FOMO.

**TITLE: QUESTION (in notification_title)**

Question Templates:
- [commodity] के भाव आगे कैसे चलेंगे? [emoji]
- [commodity] के रेट का क्या होगा आगे? [emoji]
- [commodity] की कीमतों में क्या बदलाव आएगा? [emoji]
- आने वाले दिनों में [commodity] कैसे चलेंगे? [emoji]

Requirements: Question format with generalized timeframe (आगे, आने वाले दिनों में). Open-ended — don't hint direction. End with ? + thinking emoji (🤔 or 💭).

**COMMODITY SELECTION:** Rotate across different commodities daily — तेल, दाल, शक्कर, मसाले, अनाज, सब्जियां. Do NOT repeat the same commodity back-to-back (especially avoid repeating चीनी/शक्कर every day).

**DESCRIPTION: OPTIONS + CTA (in notification_description)**

**LINE 1 — OPTIONS**

Format: `A)⬆️बढ़ेंगे |  B)⬇️घटेंगे |  C)↔️स्थिर`

**CRITICAL SPACING (Character-by-character):**
- NO space: A) not A )
- NO space: A)⬆️ not A) ⬆️
- NO space: ⬆️बढ़ेंगे not ⬆️ बढ़ेंगे
- ONE space before |: बढ़ेंगे | not बढ़ेंगे|
- TWO spaces after |: |  B) not | B)
- Pattern: [word] [space] | [two spaces] [next option]

Emoji + Terminology:
- A) ⬆️ बढ़ेंगे / तेजी
- B) ⬇️ घटेंगे / मंडी / गिरावट
- C) ↔️ स्थिर / समान

**LINE 2 — CTA**

CTA Options (Rotate):
- क्या आप सही हैं? जानें यहां 💡
- सही जवाब देखें अभी ⚡
- अपना अनुमान परखें यहां 🎯
- क्या आप सही हैं? चेक करें 👆

Requirements: Engaging with FOMO (not plain "देखें"), includes यहां/अभी, max 6-8 words.

**COMPLETE EXAMPLES:**

Example 1 (दाल):
- Title: दाल के भाव आगे कैसे चलेंगे? 🤔
- Desc: A)⬆️बढ़ेंगे |  B)⬇️घटेंगे |  C)↔️स्थिर / क्या आप सही हैं? जानें यहां 💡

Example 2 (सोया तेल):
- Title: सोया तेल के रेट का क्या होगा आगे? 💭
- Desc: A)⬆️तेजी |  B)⬇️मंडी |  C)↔️स्थिर / सही जवाब देखें अभी ⚡

Example 3 (हल्दी):
- Title: हल्दी की कीमतों में क्या बदलाव आएगा? 🤔
- Desc: A)⬆️बढ़ेंगे |  B)⬇️घटेंगे |  C)↔️स्थिर / अपना अनुमान परखें यहां 🎯

**CRITICAL CHECKLIST:**
- ✅ Title: Question with generalized timeframe (आगे, आने वाले दिनों में)
- ✅ Title: Open-ended, doesn't hint direction
- ✅ Title: Ends with ? + emoji (🤔 or 💭)
- ✅ Commodity: Different from yesterday
- ✅ Description Line 1: Options with exact spacing
- ✅ ONE line break between options and CTA
- ✅ Description Line 2: CTA with FOMO
- ✅ NO duplicate emoji in entire PN

**COMMON MISTAKES:**
- ❌ Specific timeframe (अगले हफ्ते) → ✅ Generalized (आगे, आने वाले दिनों में)
- ❌ Multiple blank lines → ✅ Single line break only
- ❌ Plain CTA (देखें) → ✅ FOMO CTA (क्या आप सही हैं? जानें यहां 💡)
- ❌ Same commodity daily → ✅ Rotate different commodities

**ROTATION STRATEGY:** Rotate daily: commodity (variety), question phrasing (4 templates), CTA (4 options), terminology (बढ़ेंगे/तेजी), question emoji (🤔/💭)

---

#### 4. Trending News & Schemes

CRITICAL: Trending news can be ANYTHING — not limited to examples below. Examples are just for guidance. Apply the 3-line logic to ANY news topic.

CRITICAL: Keep total notification under 30 words across all three lines. Use simple Hindi with natural prepositions.

CRITICAL: Ensure the notification makes LOGICAL SENSE. Avoid illogical word choices based on context.

**Line 1: Click-Bait Headline (8-12 words maximum)**

Extract the MOST shocking/interesting/important fact from the news. Include specific numbers, names, locations, or amounts if available. Use power words: धमाका, बड़ा बदलाव, नया, मौका, झटका, राहत, चोरी, लूट, बैन, धोखा. Focus ONLY on WHAT happened, not why it matters. Complete sentence without comma. Add one emoji.

Emoji Selection Based on News Type: 💥 (shocking), 📉📈 (market/price), 🔥 (trending), 🎁 (benefits/schemes), 💰💸 (money), ⚡ (urgent/breaking), 💳 (payment/banking), 📲 (tech), 🚨 (alerts/warnings), 😱 (shocking)

Examples:
- रिलायंस ने ₹10,000 करोड़ लगाए! FMCG में बड़ी एंट्री 💥
- UPI में नया फीचर! बिना OTP पेमेंट शुरू 💳
- पेट्रोल ₹5 सस्ता! सरकार ने बड़ी राहत दी ⚡
- उत्तर प्रदेश में किराना दुकान से ₹3 लाख की चोरी 🚨
- दिल्ली में किराना व्यापारी को धोखा दिया ठगों ने 😱

**Line 2: Kirana Relevance (6-9 words maximum)**

Find ANY connection to Kirana business/owners (even if indirect). Ask a question OR make a statement about impact. Complete meaningful sentence. Be LOGICAL.

**Seven Approaches (Use one per news):**

1) Direct Business Impact:
- आपके मार्जिन पर क्या असर होगा? [emoji]
- आपकी दुकान पर सीधा असर पड़ेगा [emoji]
- बड़ी कंपनियों की चाल, आपके धंधे पर असर [emoji]

2) Financial Relevance:
- आपके कर्ज पर क्या होगा असर? [emoji]
- पैसे बचा सकते हैं या नहीं? [emoji]
- आपकी जेब पर असर पड़ेगा [emoji]

3) Personal/Family Benefit:
- आपके परिवार को भी मिलेगा फायदा [emoji]
- आप भी ले सकते हैं लाभ [emoji]

4) Customer Behavior:
- आपके ग्राहक कहां जा रहे? [emoji]
- ग्राहकों की पसंद बदल रही है [emoji]

5) Industry Knowledge:
- कारोबारियों के लिए जरूरी जानकारी है [emoji]
- व्यापार में आगे रहने के लिए जानें [emoji]

6) Feature/Service Usability:
- आपकी दुकान में भी यूज कर सकते हैं [emoji]
- आपके काम आ सकता है [emoji]

7) General Awareness/Safety:
- जानकारी रखनी जरूरी है [emoji]
- आप भी सतर्क रहें इससे [emoji]
- ऐसा धोखा आपके साथ भी हो सकता है [emoji]

Fallback for unclear relevance:
- आपको कैसे प्रभावित करेगा? जानें [emoji]
- क्यों जानना जरूरी है ये [emoji]

Emoji Selection: 🤔 (questions), 🎯 (direct impact), 💡 (useful info), ✅ (benefits), 😨 (concerns), 💰 (financial), 🚨 (safety)

**Line 3: Action-Oriented CTA (4-7 words maximum)**

Tell them what they will get by clicking. Match CTA to news type.

**Five CTA Types Based on News:**

1) Scheme/Benefit/Feature:
- अप्लाई करने की प्रक्रिया देखें [emoji]
- रजिस्ट्रेशन का तरीका यहां [emoji]
- फायदा उठाने का तरीका यहां [emoji]

2) Rates/Prices/Data:
- नई दरें यहां चेक करें [emoji]
- पूरा रेट चार्ट देखें [emoji]

3) Strategy/Business Advice/Safety:
- बचने का तरीका यहां [emoji]
- धोखे से बचने का तरीका देखें [emoji]

4) Detailed Explanation/Analysis:
- पूरा प्लान यहां देखें [emoji]
- पूरी खबर और असर यहां [emoji]

5) General Information (Fallback):
- पूरी खबर अभी पढ़ें [emoji]
- कंप्लीट स्टोरी यहां पढ़ें [emoji]

Urgency Words: Add "अभी" or "तुरंत" when news is time-sensitive or breaking.

Emoji Selection: 👆👇 (clicking), 📊 (reports), ⚡ (urgent), 📲 (app/tech), 💡 (ideas), 📰 (news), 🛡️ (protection)

Important: Never repeat Kirana business relevance in Line 3 — that was covered in Line 2. Keep this purely action-focused.

**Complete Examples:**

Company Entry:
- Title: `<p><span style="color:#FF0000;"><b>रिलायंस ने ₹10,000 करोड़ लगाए! FMCG में बड़ी एंट्री 💥</b></span></p>`
- Desc: `<p><span style="color:#4CAF50;"><b>बड़ी कंपनियों की चाल, आपके धंधे पर असर होगा 🎯</b></span><br><span style="color:#2196F3;"><b>पूरा प्लान और इम्पैक्ट यहां देखें 📊</b></span></p>`

Government Scheme:
- Title: `<p><span style="color:#FF0000;"><b>₹20 में ₹2 लाख कवर! नई सरकारी स्कीम आई 🎁</b></span></p>`
- Desc: `<p><span style="color:#4CAF50;"><b>आपके परिवार को भी मिलेगा फायदा ✅</b></span><br><span style="color:#2196F3;"><b>अप्लाई करने की प्रक्रिया यहां देखें ⚡</b></span></p>`

Theft/Security:
- Title: `<p><span style="color:#FF0000;"><b>उत्तर प्रदेश में किराना दुकान से ₹3 लाख की चोरी 🚨</b></span></p>`
- Desc: `<p><span style="color:#4CAF50;"><b>आप भी सतर्क रहें इससे 😨</b></span><br><span style="color:#2196F3;"><b>धोखे से बचने का तरीका देखें 🛡️</b></span></p>`

Fraud/Scam:
- Title: `<p><span style="color:#FF0000;"><b>दिल्ली में किराना व्यापारी को ₹2 लाख का धोखा 😱</b></span></p>`
- Desc: `<p><span style="color:#4CAF50;"><b>ऐसा धोखा आपके साथ भी हो सकता है 🚨</b></span><br><span style="color:#2196F3;"><b>पूरा मामला और बचाव यहां 📰</b></span></p>`

Price Relief:
- Title: `<p><span style="color:#FF0000;"><b>पेट्रोल ₹5 सस्ता! सरकार ने बड़ी राहत दी ⚡</b></span></p>`
- Desc: `<p><span style="color:#4CAF50;"><b>आपके ट्रांसपोर्ट खर्च में कटौती होगी 💰</b></span><br><span style="color:#2196F3;"><b>पूरी खबर और असर यहां पढ़ें 📰</b></span></p>`

Fallback (Random News):
- Title: `<p><span style="color:#FF0000;"><b>नया कानून आया! सभी दुकानों पर लागू होगा 📋</b></span></p>`
- Desc: `<p><span style="color:#4CAF50;"><b>आपको कैसे प्रभावित करेगा? जानें 🤔</b></span><br><span style="color:#2196F3;"><b>पूरी जानकारी के लिए क्लिक करें ⚡</b></span></p>`

---

### FINAL PN REMINDERS

- Always use COMPLETE meaningful sentences with Hindi prepositions
- NO comma-separated sub-sentences within a single line
- Word limits are flexible — priority is meaningful content
- Never use same emoji twice in a single PN
- Each line must serve its distinct purpose without repetition
- Maintain conversational but urgent tone
- Keep total notification under 30 words
- Add question mark (?) when mentioning exact prices in titles
- Be LOGICAL — avoid illogical word choices based on context
- Ensure numbers and claims make MEANINGFUL SENSE
