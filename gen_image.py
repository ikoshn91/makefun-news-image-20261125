#!/usr/bin/env python3
"""THE WORLD TODAY — Wednesday 25 November 2026.

One-page atlas dashboard summing up 25 November 2026 world news:
3 lead cards, a market heatmap strip, 8 region panels (38 dated stories),
a news ticker and a footer. Drawn with Pillow, DejaVu fonts only.
Deterministic: no randomness, no timestamps — two runs write identical bytes.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 16

PAPER = "#f8f4e9"
CARD = "#fffdf6"
INK = "#1a1a1a"
MUTED = "#6b6558"
RULE = "#2b2b2b"
RED = "#b3271e"
NAVY = "#1f3a5f"
AMBER = "#b7791f"
GOLD = "#f2c200"
TEAL = "#0f766e"
ORANGE = "#c2410c"
BROWN = "#7c4a1e"
GREEN = "#15803d"
PURPLE = "#6d28d9"
SLATE = "#1f2937"
LIGHT_RED = "#fca5a5"
LIGHT_GREEN = "#86efac"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 56)
F_DATE = font("DejaVuSans-Bold.ttf", 22)
F_SUB = font("DejaVuSans.ttf", 13)
F_KICKER = font("DejaVuSans-Bold.ttf", 12)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 21)
F_LEAD_BODY = font("DejaVuSans.ttf", 13)
F_HEAT_LABEL = font("DejaVuSans-Bold.ttf", 13)
F_CHIP = font("DejaVuSans-Bold.ttf", 13)
F_PANEL_NAME = font("DejaVuSans-Bold.ttf", 13)
F_PANEL_COUNT = font("DejaVuSans.ttf", 10)
F_STORY_HEAD = font("DejaVuSans-Bold.ttf", 12)
F_STORY_BODY = font("DejaVuSans.ttf", 11)
F_TICK_LABEL = font("DejaVuSans-Bold.ttf", 12)
F_TICK_TEXT = font("DejaVuSans.ttf", 12)
F_FOOTER = font("DejaVuSans.ttf", 12)

LEADS = [
    ("MIDDLE EAST  ·  HORMUZ", RED, "ship",
     "Two tankers hit mines in Hormuz",
     "Ships explode and burn; IRGC says they took an 'unauthorised' route."),
    ("MARKETS  ·  NEW YORK", AMBER, "chart",
     "Dow erases 1,100-pt drop",
     "Closes +0.33% at 50,182.95; S&P -0.25%, Nasdaq -0.62%."),
    ("TRADE  ·  WASHINGTON", NAVY, "stamp",
     "US tariffs hit 14 partners",
     "China 20%, Vietnam 35%, EU 15%; hearing Jan 25, nothing before then."),
]

HEATMAP = [
    ("Dow 50,182.95", GOLD, INK),
    ("S&P \u22120.25%", None, LIGHT_RED),
    ("Nasdaq \u22120.62%", None, LIGHT_RED),
    ("Kospi \u22126.16%", None, LIGHT_RED),
    ("WTI $84.08", None, "#ffffff"),
]

PANELS = [
    ("MIDDLE EAST", RED, [
        ("Israel kills Hamas security chief",
         "Col. Abuelouf + wife, 2 daughters dead in Shati."),
        ("Houthis claim Riyadh refinery hit",
         "4 drones intercepted at Ras Tanura."),
        ("Cairo tanker fire kills 30",
         "Fuel truck blast on Ring Road; 25 hurt."),
        ("UN aid chief lands in Yemen",
         "Fletcher warns war blocks food, medicine."),
        ("US tells citizens: leave Iran",
         "Alert issued as Hormuz tankers burn."),
    ]),
    ("EUROPE", NAVY, [
        ("Ukraine hits 2 Rosneft refineries",
         "Syzran + Kuibyshev ablaze overnight."),
        ("Russia strikes Odesa, Kyiv",
         "2 killed in Odesa; 112 drones, 88 downed."),
        ("Poland seeks permanent US base",
         "After 2 airspace incursions in 4 days."),
        ("Eurostar strike halts trains",
         "Paris walkout cancels London services."),
        ("BBC: 490,334 Russians dead",
         "Leaked stats since 2022, per BBC."),
    ]),
    ("ASIA", TEAL, [
        ("Solomons signs Australia pact",
         "A$740m; no foreign bases; China deal ends."),
        ("First Pakistani in orbit",
         "Zeeshan Ali docks at Tiangong station."),
        ("Bogor mine flood traps 26",
         "3 bodies found; shaft 100m deep."),
        ("Australia CPI 4.9% hot",
         "Raises odds of RBA rate hike."),
        ("Asia rout: Kospi -6.16%",
         "Nikkei -2.78%; Taiex -4.8%; Shanghai -2.0%."),
    ]),
    ("AMERICAS", ORANGE, [
        ("Cartagena hostages freed",
         "All rescued; 1 captor killed in raid."),
        ("US drone helped catch El Chapo Isidro",
         "Mexico: surveillance flight aided arrest."),
        ("US confidence at 2-year high",
         "Consumer mood rises more than expected."),
        ("Democrats set to take Congress",
         "Tariffs now Trump's tool, Reuters says."),
    ]),
    ("AFRICA", BROWN, [
        ("Sudan: 19 killed in RSF strikes",
         "Blue Nile drone attacks, 20 wounded."),
        ("Ebola teams evacuated in DRC",
         "Trapped 3 days by fighting in Ituri."),
        ("2 Libyan officers die in drone hit",
         "Wounds from strike on Russian warship."),
    ]),
    ("MARKETS", AMBER, [
        ("Wall Street swings wildly",
         "Dow +0.33%; S&P -0.25%; Nasdaq -0.62%."),
        ("Core PCE 3.3%, Fed hike 97%",
         "Q3 GDP 4.3%; Dec hike near-certain."),
        ("Dell falls ~7% on AI boom",
         "Revenue +103%; backlog $132.3B record."),
        ("Oil up, gold $3,609",
         "WTI $84.08 +2.47%; gold +0.50%."),
    ]),
    ("SCIENCE", GREEN, [
        ("Huawei guilty on 10 counts",
         "Fraud, sanctions; RICO acquitted."),
        ("AI selloff: Nvidia -3.91%",
         "Anthropic below IPO; SOX -7.88% Tue."),
        ("Pope concerned over COP31",
         "Leo XIV laments climate talks failure."),
        ("Gavi buys Ebola vaccine",
         "Up to 1.5M Bundibugyo doses."),
    ]),
    ("SPORT", PURPLE, [
        ("Liverpool rout Brugge 3\u20130",
         "Isak scores twice."),
        ("Barcelona beat Sabah 4\u20131",
         "Bar\u00e7a win at home."),
        ("PSG draw 2\u20132 with Roma",
         "PSG lose perfect record."),
        ("Lille stun Bayern 2\u20131",
         "Bayern beaten in France."),
        ("Sporting draw 2\u20132 with Man Utd",
         "Tielemans sent off late."),
    ]),
]

TICKER_TEXT = ("Atl\u00e9tico 2\u20130 Viking; Inter 2\u20130 Stuttgart   \u2022   "
               "Fenerbah\u00e7e 1\u20130 Shakhtar; Villarreal 1\u20130 Slavia   \u2022   "
               "VIX jumps 7.32% to 28.29")
FOOTER_TEXT = ("Compiled from reports published 25 November 2026  \u00b7  "
               "Sources: CNN, Reuters, AP, WSJ  \u00b7  One day. 38 stories.")

TOTAL_STORIES = 3 + sum(len(stories) for _, _, stories in PANELS)
assert TOTAL_STORIES == 38, f"story count is {TOTAL_STORIES}, expected 38"


def wrap(text, fnt, max_width):
    """Greedy word wrap; returns list of lines that each fit max_width."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_h(fnt, line_h, n_lines):
    return n_lines * line_h


def fail(msg):
    sys.exit("OVERFLOW: " + msg)


# ---- layout (all y positions computed up front) ----
LEAD_Y, LEAD_H = 140, 138
LEAD_W = (W - 2 * MARGIN - 2 * 8) // 3
HEAT_Y, HEAT_H = 286, 38
PANEL_Y = 332
PANEL_ROW_H = 296
PANEL_GAP = 8
PANEL_W = (W - 2 * MARGIN - 3 * 8) // 4
TICK_Y, TICK_H = 940, 44
FOOT_Y = 992


def measure_all():
    """Measure every text block; raise OVERFLOW before drawing anything."""
    # Leads
    inner = LEAD_W - 20
    for kicker, _c, _i, head, body in LEADS:
        hl = wrap(head, F_LEAD_HEAD, inner)
        bl = wrap(body, F_LEAD_BODY, inner)
        if len(hl) > 2:
            fail(f"lead headline needs {len(hl)} lines: {head!r}")
        if len(bl) > 3:
            fail(f"lead body needs {len(bl)} lines: {body!r}")
        need = 4 + 15 + 3 + len(hl) * 26 + 3 + len(bl) * 16 + 10
        if need > LEAD_H:
            fail(f"lead card needs {need}px, has {LEAD_H}px: {head!r}")
    # Panels
    p_inner = PANEL_W - 20
    story_top_off = 36
    story_area = PANEL_ROW_H - story_top_off - 6
    for name, _c, stories in PANELS:
        total = 0
        for head, body in stories:
            hl = wrap(head, F_STORY_HEAD, p_inner - 10)
            bl = wrap(body, F_STORY_BODY, p_inner - 10)
            if len(hl) > 2:
                fail(f"{name}: headline needs {len(hl)} lines: {head!r}")
            if len(bl) > 2:
                fail(f"{name}: body needs {len(bl)} lines: {body!r}")
            total += len(hl) * 14.5 + len(bl) * 13 + 3
        if total > story_area:
            fail(f"{name}: stories need {total:.0f}px, area is {story_area}px")
    # Ticker (max 2 lines)
    tick_w = W - 2 * MARGIN - 16 - 150
    tl = wrap(TICKER_TEXT, F_TICK_TEXT, tick_w)
    if len(tl) > 2:
        fail(f"ticker needs {len(tl)} lines")


def draw_icon(d, kind, x, y, color):
    """One small geometric icon, 26x26, never overlapping text."""
    if kind == "ship":
        d.polygon([(x, y + 18), (x + 24, y + 18), (x + 20, y + 25), (x + 4, y + 25)],
                  fill=color)
        d.line([(x + 12, y + 18), (x + 12, y + 5)], fill=color, width=2)
        d.polygon([(x + 12, y + 5), (x + 12, y + 16), (x + 20, y + 16)], fill=RED)
    elif kind == "chart":
        d.line([(x + 1, y + 20), (x + 8, y + 14), (x + 14, y + 17), (x + 23, y + 4)],
               fill=color, width=3)
        d.polygon([(x + 23, y + 4), (x + 17, y + 4), (x + 23, y + 10)], fill=color)
    elif kind == "stamp":
        d.ellipse([x + 2, y + 2, x + 24, y + 24], outline=color, width=2)
        d.text((x + 13, y + 13), "%", font=F_KICKER, fill=color, anchor="mm")


def main():
    measure_all()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([MARGIN, 12, W - MARGIN, 14], fill=RULE)
    d.text((W // 2, 18), "THE WORLD TODAY", font=F_TITLE, fill=INK, anchor="ma")
    d.text((W // 2, 84), "WEDNESDAY  25  NOVEMBER  2026",
           font=F_DATE, fill=RED, anchor="ma")
    d.text((W // 2, 112), "38 dated stories  \u00b7  8 regions  \u00b7  all times UTC",
           font=F_SUB, fill=MUTED, anchor="ma")
    d.rectangle([MARGIN, 130, W - MARGIN, 132], fill=RULE)

    # ---- lead cards ----
    for i, (kicker, color, icon, head, body) in enumerate(LEADS):
        x = MARGIN + i * (LEAD_W + 8)
        y = LEAD_Y
        d.rectangle([x, y, x + LEAD_W, y + LEAD_H], fill=CARD, outline=RULE, width=1)
        d.rectangle([x, y, x + LEAD_W, y + 4], fill=color)
        d.text((x + 10, y + 10), kicker, font=F_KICKER, fill=color, anchor="la")
        draw_icon(d, icon, x + LEAD_W - 32, y + 8, color)
        inner = LEAD_W - 20
        hl = wrap(head, F_LEAD_HEAD, inner)
        bl = wrap(body, F_LEAD_BODY, inner)
        ty = y + 32
        for line in hl:
            d.text((x + 10, ty), line, font=F_LEAD_HEAD, fill=INK, anchor="la")
            ty += 26
        ty += 3
        for line in bl:
            d.text((x + 10, ty), line, font=F_LEAD_BODY, fill=MUTED, anchor="la")
            ty += 16

    # ---- market heatmap strip ----
    d.rectangle([MARGIN, HEAT_Y, W - MARGIN, HEAT_Y + HEAT_H], fill=SLATE)
    hx = MARGIN + 12
    d.text((hx, HEAT_Y + HEAT_H // 2), "MARKET HEATMAP", font=F_HEAT_LABEL,
           fill=GOLD, anchor="lm")
    hx += F_HEAT_LABEL.getlength("MARKET HEATMAP") + 18
    for j, (text, bg, fg) in enumerate(HEATMAP):
        if bg is not None:
            tw = F_CHIP.getlength(text)
            d.rounded_rectangle([hx - 5, HEAT_Y + 8, hx + tw + 5, HEAT_Y + HEAT_H - 8],
                                radius=4, fill=bg)
        d.text((hx, HEAT_Y + HEAT_H // 2), text, font=F_CHIP, fill=fg, anchor="lm")
        hx += F_CHIP.getlength(text) + 10
        if j < len(HEATMAP) - 1:
            d.ellipse([hx, HEAT_Y + HEAT_H // 2 - 2, hx + 4, HEAT_Y + HEAT_H // 2 + 2],
                      fill="#6b7280")
            hx += 14

    # ---- region panels ----
    for idx, (name, color, stories) in enumerate(PANELS):
        row, col = divmod(idx, 4)
        x = MARGIN + col * (PANEL_W + 8)
        y = PANEL_Y + row * (PANEL_ROW_H + PANEL_GAP)
        d.rectangle([x, y, x + PANEL_W, y + PANEL_ROW_H], fill=CARD, outline=RULE, width=1)
        d.rectangle([x, y, x + PANEL_W, y + 4], fill=color)
        d.text((x + 10, y + 9), name, font=F_PANEL_NAME, fill=color, anchor="la")
        d.text((x + PANEL_W - 10, y + 11), f"{len(stories)} STORIES",
               font=F_PANEL_COUNT, fill=MUTED, anchor="ra")
        d.line([x + 10, y + 30, x + PANEL_W - 10, y + 30], fill="#d8d2c0", width=1)
        # measure story blocks, then spread them evenly in the area
        p_inner = PANEL_W - 20
        blocks = []
        for head, body in stories:
            hl = wrap(head, F_STORY_HEAD, p_inner - 10)
            bl = wrap(body, F_STORY_BODY, p_inner - 10)
            blocks.append((hl, bl, len(hl) * 14.5 + len(bl) * 13))
        area_top = y + 36
        area_h = PANEL_ROW_H - 36 - 6
        content_h = sum(b[2] for b in blocks)
        n = len(blocks)
        gap = (area_h - content_h) / (n + 1)
        cy = area_top + gap
        for hl, bl, bh in blocks:
            d.ellipse([x + 10, cy + 4, x + 14, cy + 8], fill=color)
            ty = cy
            for line in hl:
                d.text((x + 20, ty), line, font=F_STORY_HEAD, fill=INK, anchor="la")
                ty += 14.5
            for line in bl:
                d.text((x + 20, ty), line, font=F_STORY_BODY, fill=MUTED, anchor="la")
                ty += 13
            cy = ty + gap

    # ---- ticker ----
    d.rectangle([MARGIN, TICK_Y, W - MARGIN, TICK_Y + TICK_H], fill=NAVY)
    d.text((MARGIN + 12, TICK_Y + TICK_H // 2), "ALSO IN THE NEWS",
           font=F_TICK_LABEL, fill=GOLD, anchor="lm")
    tick_w = W - 2 * MARGIN - 16 - 150
    tl = wrap(TICKER_TEXT, F_TICK_TEXT, tick_w)
    tx = MARGIN + 12 + 150
    ty = TICK_Y + (TICK_H - len(tl) * 15) // 2
    for line in tl:
        d.text((tx, ty), line, font=F_TICK_TEXT, fill="#ffffff", anchor="la")
        ty += 15

    # ---- footer ----
    d.text((W // 2, FOOT_Y), FOOTER_TEXT, font=F_FOOTER, fill=MUTED, anchor="ma")

    img.save("entry.png")
    print("wrote entry.png 1024x1024")


if __name__ == "__main__":
    main()
