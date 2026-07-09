#!/usr/bin/env python3
"""
Emit Kirana Club daily posts as BOTH a curl .sh and a pretty .json, with validation.

Usage (from your build script):
    from emit_posts import emit
    emit(posts, date_slug="18june", out_dir="/mnt/user-data/outputs")

`posts` is a list of 8 dicts using the API field names:
    post_name, post_title, post_description, bg_color, notification_title,
    notification_description, brand_names  (required on all)
    commodity, direction        (only soya/dal-shakkar/other/rujhan)
    image_prompt                (all 8 posts)
    pn_image_prompt             (only Samachar, Dal/Shakkar, Rujhan, TN1, TN2)

The function raises AssertionError listing every problem; fix and re-run.
"""
import json
import re

ENDPOINT = "https://asia-south1-op-d2r.cloudfunctions.net/postAutomation"

DARK_BGS = {"#461B83", "#6D370F", "#114883"}

IMAGE_PROMPT_POSTS = {
    "Samachar", "रुझान",
    "Pan India Trending News 1", "Pan India Trending News 2", "Pan India Schemes",
    "सोया तेल", "दाल/शक्कर", "Other commodities",
}
PN_IMAGE_POSTS = {
    "Samachar", "दाल/शक्कर", "रुझान",
    "Pan India Trending News 1", "Pan India Trending News 2",
}
COMMODITY_DIR_POSTS = {"सोया तेल", "दाल/शक्कर", "Other commodities", "रुझान"}
VALID_POST_NAMES = {
    "Samachar", "सोया तेल", "दाल/शक्कर", "Other commodities", "रुझान",
    "Pan India Trending News 1", "Pan India Trending News 2", "Pan India Schemes",
}
REQUIRED = ["post_name", "post_title", "post_description", "bg_color",
            "notification_title", "notification_description", "brand_names"]

EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\u2B00-\u2BFF\u2190-\u21FF\u2700-\u27BF\uFE0F]"
)


_MODIFIERS = {"\uFE0F", "\u200D", "\uFE0E"}


def _emojis(text):
    # Ignore variation selectors / ZWJ — they are modifiers, not standalone emoji
    # (the ⬆️⬇️↔️ quiz arrows each legitimately carry U+FE0F).
    return [c for c in text if EMOJI_RE.match(c) and c not in _MODIFIERS]


def _strip_html(s):
    return re.sub(r"<[^>]+>", "", s).strip()


def _first_token(s):
    s = _strip_html(s)
    m = re.match(r"[\u0900-\u097F]+", s)  # leading Devanagari word
    return m.group(0) if m else ""


def validate(posts, date_prefix):
    errs = []
    if len(posts) != 8:
        errs.append(f"Expected 8 posts, got {len(posts)}")

    bgs = [p.get("bg_color") for p in posts]
    if len(set(bgs)) != len(bgs):
        errs.append(f"bg_color values not unique: {bgs}")
    darks = [b for b in bgs if b in DARK_BGS]
    if len(darks) != 3:
        errs.append(f"Expected 3 dark bg_colors, got {len(darks)}: {darks}")

    pn_commodities = []  # commodity-post PN headline (to compare vs Samachar)
    for i, p in enumerate(posts, 1):
        name = p.get("post_name", f"<post{i}>")
        for f in REQUIRED:
            if f not in p:
                errs.append(f"[{name}] missing required field '{f}'")
        if p.get("post_name") not in VALID_POST_NAMES:
            errs.append(f"[{name}] invalid post_name")
        if not isinstance(p.get("brand_names"), list):
            errs.append(f"[{name}] brand_names must be a list")
        if not str(p.get("bg_color", "")).startswith("#"):
            errs.append(f"[{name}] bg_color must be a hex code")

        # title must start with posting date
        if not str(p.get("post_title", "")).startswith(date_prefix):
            errs.append(f"[{name}] post_title must start with '{date_prefix}'")

        # field-presence rules
        has_img = "image_prompt" in p and p["image_prompt"]
        if has_img and name not in IMAGE_PROMPT_POSTS:
            errs.append(f"[{name}] should NOT have image_prompt")
        if name in IMAGE_PROMPT_POSTS and not has_img:
            errs.append(f"[{name}] MUST have image_prompt")

        has_pn = "pn_image_prompt" in p and p["pn_image_prompt"]
        if has_pn and name not in PN_IMAGE_POSTS:
            errs.append(f"[{name}] should NOT have pn_image_prompt")
        if name in PN_IMAGE_POSTS and not has_pn:
            errs.append(f"[{name}] MUST have pn_image_prompt")

        has_cd = ("commodity" in p) or ("direction" in p)
        if has_cd and name not in COMMODITY_DIR_POSTS:
            errs.append(f"[{name}] should NOT have commodity/direction")
        if name in COMMODITY_DIR_POSTS and not ("commodity" in p and "direction" in p):
            errs.append(f"[{name}] MUST have both commodity and direction")
        if name in COMMODITY_DIR_POSTS and name != "रुझान":
            pn_commodities.append(p.get("notification_title", ""))

        # no $ ; no ASCII apostrophe ; no citation markers
        blob = json.dumps(p, ensure_ascii=False)
        if "$" in blob:
            errs.append(f"[{name}] contains '$' (spell out डॉलर)")
        if "'" in blob:
            errs.append(f"[{name}] contains ASCII apostrophe (breaks shell payload)")
        if re.search(r"【.*?】|contentReference|\[\d+\]", blob):
            errs.append(f"[{name}] contains citation marker")

        # duplicate emoji within a single PN (title + description)
        pn = (p.get("notification_title", "") + p.get("notification_description", ""))
        es = _emojis(pn)
        dupes = {e for e in es if es.count(e) > 1}
        if dupes:
            errs.append(f"[{name}] duplicate emoji in PN: {dupes}")

    # Samachar PN commodity must differ from the four commodity posts
    sam = next((p for p in posts if p.get("post_name") == "Samachar"), None)
    if sam:
        sam_word = _first_token(sam.get("notification_title", ""))
        commodity_words = {_first_token(t) for t in pn_commodities}
        if sam_word and sam_word in commodity_words:
            errs.append(
                f"Samachar PN commodity ('{sam_word}') overlaps a commodity-post PN")

    if errs:
        raise AssertionError("VALIDATION FAILED:\n  - " + "\n  - ".join(errs))


def emit(posts, date_slug, date_prefix, out_dir="/mnt/user-data/outputs"):
    """date_slug e.g. '18june' (filename); date_prefix e.g. '18 जून' (title check)."""
    validate(posts, date_prefix)

    body = json.dumps(posts, ensure_ascii=False, indent=2)
    # round-trip safety
    assert json.loads(body) == posts

    sh_path = f"{out_dir}/kirana_posts_{date_slug}.sh"
    json_path = f"{out_dir}/kirana_posts_{date_slug}.json"

    curl = (
        f"curl -X POST {ENDPOINT} \\\n"
        f'  -H "Content-Type: application/json" \\\n'
        f"  -d '{body}'\n"
    )
    with open(sh_path, "w", encoding="utf-8") as f:
        f.write(curl)
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(body)

    print("VALIDATION PASS")
    print(f"Posts: {len(posts)} | unique bg: {len(set(p['bg_color'] for p in posts))} "
          f"(dark {sum(1 for p in posts if p['bg_color'] in DARK_BGS)})")
    print(f"Wrote: {sh_path}")
    print(f"Wrote: {json_path}")
    return sh_path, json_path
