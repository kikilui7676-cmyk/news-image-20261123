#!/usr/bin/env python3
"""Render entry.png — Monday 23 November 2026 world news in one dense front page.

Fresh Pillow layout: masthead + date band, a COP31 lead strip, then the rest of
the day as numbered news briefs (bold headline flowing into a short caption),
arranged in region blocks across two columns. A measuring layout pass runs
first; if the page would overflow, the least consequential stories are dropped
in a fixed order until it fits. Pure drawing, no randomness: deterministic.
"""
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = "DejaVuSans-Bold.ttf"
REG = "DejaVuSans.ttf"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


W = H = 1024
MARGIN = 16
GUTTER = 16
COLW = (W - 2 * MARGIN - GUTTER) // 2

PAPER = (250, 249, 245)
INK = (16, 16, 16)
RED = (156, 24, 30)
DARKRED = (120, 16, 22)
GREY = (96, 96, 96)
WHITE = (255, 255, 255)

F_MAST = font(BOLD, 23)
F_MAST_R = font(REG, 13)
F_DATE = font(BOLD, 47)
F_KICK = font(BOLD, 14)
F_LEAD_H = font(BOLD, 34)
F_LEAD_C = font(REG, 16)
F_REGION = font(BOLD, 18)
F_HEAD = font(BOLD, 15)
F_CAP = font(REG, 13)
F_NUM = font(BOLD, 13)
F_FOOT = font(REG, 13)

LEADING = 15          # story line pitch
STORY_GAP = 2         # px after each story
HEADER_H = 23         # region bar height
HEADER_GAP = 4        # px after a region bar
BLOCK_GAP = 4         # extra px before a region bar mid-column

LEAD_HEADLINE = "COP31 ENDS WITHOUT A DEAL"
LEAD_KICKER = "ANTALYA, TURKEY - CLIMATE SUMMIT"
LEAD_CAPTION = (
    "Longest UN climate summit ever ends two days late: EU and vulnerable states reject a "
    "draft with no fossil-fuel language. ~90 countries back a voluntary 35% clean-electricity "
    "share by 2035; disputes move to COP32 in Ethiopia."
)

# (number, headline, caption) grouped by region, in running order.
REGIONS = [
    ("EUROPE & THE UKRAINE WAR", [
        (2, "POLAND: 3 RUSSIAN KH-101 MISSILES DOWN",
         "Wreckage confirmed Russian; NATO council in emergency session; Warsaw wants F-35s."),
        (3, "UKRAINE SINKS RUSSIAN CORVETTE MERKURY",
         "7 naval drones at Benghazi, Libya; Zelenskyy confirms the sinking."),
        (4, "RUSSIAN SHIP SPARTA II ABLAZE",
         "Drone hit in Gulf of Finland; towed out, Helsinki summons ambassador."),
        (5, "DYMER FLATS STRIKE KILLS 11",
         "Kyiv-region block hit, 14 first missing; Zelenskyy slams Patriot delays."),
        (6, "KRYVYI RIH STRIKE KILLS 2",
         "Child and young woman die; 25 blocks, a hospital, schools damaged."),
        (7, "DRONE HITS KHARKIV KINDERGARTEN",
         "Russian drone strikes a nursery school in Kharkiv."),
        (8, "SLOVYANSK STRIKES KILL 2",
         "Night assault: ~153 drones, some 60 of them jet-powered."),
        (9, "UKRAINE HITS RUSSIAN OIL SITES",
         "Infrastructure struck in Rostov, Perm and Tatarstan."),
        (10, "EU PLANS 22ND SANCTIONS PACKAGE",
         "60 banks, crypto platforms, 70+ shadow-fleet ships targeted."),
        (11, "ABU DHABI PEACE TALKS WRAP",
         "Ukraine-Russia-US trilateral; Medinsky firm on territory."),
        (12, "MOLDOVA: 7 DRONE INCURSIONS",
         "5 Russian drones crash inside 2.5 hours."),
        (13, "EX-POLICE CHIEF FOUND DEAD",
         "De Gennaro, 78, in Tuscany amid Borsellino mafia-inquiry case."),
        (14, "HUNGARY PM TO VISIT TRANSCARPATHIA",
         "Magyar pledges support to Ukrainians and ethnic Hungarians."),
        (15, "PARIS WEALTH-TAX PUSH GROWS",
         "Global billionaire-tax campaign gathers momentum."),
    ]),
    ("MIDDLE EAST", [
        (16, "TRUMP: IRAN DEAL NOT ACCEPTABLE",
         "Tehran defies the Hormuz blockade, claims a US drone downed; Trump threatens tankers."),
        (17, "IRAN HITS BAHRAIN INDUSTRIAL SITE",
         "2 injured; IRGC claims US positions hit; Bahrain defences intercept."),
        (18, "GAZA TRUCK STRIKE KILLS 3",
         "Food truck hit, Health Ministry says; WCK: vehicle not affiliated."),
        (19, "SETTLER ARSON 'JEWISH TERRORISM'",
         "PM-elect Eisenkot's words as Palestinian cars burn near Ramallah."),
        (20, "ISRAEL COALITION TALKS STALL",
         "Likud-Yashar negotiations end with no deal."),
        (21, "VANCE SILENT ON IRAN STRIKES",
         "VP won't say whether he'd have authorised them."),
        (22, "IRAN FLOGS SINGER AHMADI",
         "Parastoo Ahmadi and 4 band/production members flogged in Qom."),
    ]),
    ("ASIA", [
        (23, "ASIAN CHIP STOCKS SLIDE",
         "AI-spending rout: Kospi -3.3%, Samsung -3.1%, SK Hynix -2.5%."),
        (24, "INDONESIA FACTORY BLAZE KILLS 24",
         "Dozens missing as rescuers search the ruins."),
        (25, "INDIA GIVES NEPAL $1.62BN",
         "Aid package for glacier-flood rebuilding."),
        (26, "EU-INDONESIA TRADE DEAL SIGNED",
         "Landmark pact after a decade of talks; 730m people covered."),
        (27, "JAKARTA: VP NOMINEES TO COME",
         "President to nominate VP candidates, state media say."),
        (28, "THAI MP'S ROYAL-INSULT TERM HALVED",
         "Appeal court cuts the lawmaker's jail sentence."),
        (29, "S. KOREA EDUCATION CHIEF QUITS",
         "Minister resigns over exam-cheating chaos."),
        (30, "HASINA FACES ARREST IF SHE RETURNS",
         "Bangladesh to jail ex-PM on return from India."),
        (31, "INDIA-NETHERLANDS DEEPEN TIES",
         "Partnership: tech, chips, defence, renewables."),
        (32, "US ASIA LEAD OVER CHINA SHRINKS",
         "Smallest since 2018, Lowy Asia Power Index finds."),
    ]),
    ("NORTH AMERICA", [
        (33, "DEMOCRATS WIN 258 HOUSE SEATS",
         "Largest House majority since 1992."),
        (34, "NVIDIA BRINGS BACK HUANG AS CEO",
         "Returns 11 days after quitting; stock +33%, S&P 500 +4.82%."),
        (35, "TRUMP CALLS PUTIN 'MY FRIEND'",
         "Remark follows the Shenzhen summit with Xi Jinping."),
        (36, "TRUMP FIRES CYBER DIRECTOR",
         "Cairncross out after a wave of US outages."),
        (37, "GOP OPEN TO IRAN FUNDING CAP",
         "Senate move to dodge shutdown; funds lapse 11 Dec."),
        (38, "AMTRAK TRAIN DERAILS",
         "Hit a tractor-trailer near Lafayette, Louisiana."),
        (39, "US PRESSES NVIDIA ON CHINA SALES",
         "Washington demands answers on chip exports."),
    ]),
    ("LATIN AMERICA", [
        (40, "'EL CHAPO ISIDRO' CAPTURED",
         "FBI most-wanted seized in Sinaloa by Mexican forces with US intel."),
    ]),
    ("AFRICA", [
        (41, "NIGERIA VILLA LOSES WATER, POWER",
         "Tinubu says the Abuja presidential villa was hit by cuts."),
        (42, "SUDAN EMERGENCY DEEPENS",
         "The humanitarian crisis keeps deteriorating."),
    ]),
    ("SCIENCE", [
        (43, "BEPICOLOMBO MERCURY ALERT",
         "Software caveat on orbit entry; operational checks needed."),
    ]),
]

DROP_ORDER = [43, 21, 27, 15, 14, 38, 28, 29, 13, 22, 30, 12]

_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def textw(s, f):
    return _probe.textlength(s, font=f)


def wrap_story(num, head, cap):
    """Flow number + bold headline + caption into lines of (word, font, color)."""
    tokens = [(f"{num}.", F_NUM, RED)]
    tokens += [(w, F_HEAD, INK) for w in head.split()]
    tokens += [(w, F_CAP, INK) for w in cap.split()]
    space = {id(F_NUM): textw(" ", F_NUM), id(F_HEAD): textw(" ", F_HEAD),
             id(F_CAP): textw(" ", F_CAP)}
    lines, cur, curw = [], [], 0.0
    for word, f, color in tokens:
        ww = textw(word, f)
        add = ww if not cur else ww + space[id(cur[-1][1])]
        if cur and curw + add > COLW:
            lines.append(cur)
            cur, curw = [(word, f, color)], ww
        else:
            cur.append((word, f, color))
            curw += add
    if cur:
        lines.append(cur)
    # x offsets per line
    out = []
    for line in lines:
        x, placed = 0.0, []
        for word, f, color in line:
            placed.append((x, word, f, color))
            x += textw(word, f) + space[id(f)]
        out.append(placed)
    return out


def wrap_plain(text, f, width):
    lines, cur, curw = [], "", 0.0
    sp = textw(" ", f)
    for w in text.split():
        ww = textw(w, f)
        add = ww if not cur else ww + sp
        if cur and curw + add > width:
            lines.append(cur)
            cur, curw = w, ww
        else:
            cur = f"{cur} {w}" if cur else w
            curw += add
    if cur:
        lines.append(cur)
    return lines


def build_items(dropped):
    items = []
    for region, stories in REGIONS:
        live = [s for s in stories if s[0] not in dropped]
        if not live:
            continue
        items.append(("header", region))
        for num, head, cap in live:
            lines = wrap_story(num, head, cap)
            items.append(("story", num, lines, len(lines) * LEADING + STORY_GAP))
    return items


def layout(items, top, bottom):
    """Place items into two columns. Return placements or None on overflow."""
    col_x = [MARGIN, MARGIN + COLW + GUTTER]
    col, y = 0, top
    placed = []
    for i, item in enumerate(items):
        if item[0] == "header":
            nxt = items[i + 1] if i + 1 < len(items) else None
            need = HEADER_H + HEADER_GAP + (nxt[3] if nxt and nxt[0] == "story" else 0)
            extra = BLOCK_GAP if y > top else 0
            if y + extra + need > bottom:
                col += 1
                y = top
                extra = 0
                if col > 1:
                    return None
            y += extra
            placed.append(("header", item[1], col_x[col], y))
            y += HEADER_H + HEADER_GAP
        else:
            if y + item[3] > bottom:
                col += 1
                y = top
                if col > 1:
                    return None
            placed.append(("story", item[2], col_x[col], y))
            y += item[3]
    return placed


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header: masthead + date band ----
    y = 12
    d.text((MARGIN, y), "THE WORLD IN ONE IMAGE", font=F_MAST, fill=INK)
    tag = "ONE PAGE - ALL THE DAY'S NEWS"
    d.text((W - MARGIN - textw(tag, F_MAST_R), y + 7), tag, font=F_MAST_R, fill=GREY)
    y += 32
    band_h = 52
    d.rectangle([MARGIN, y, W - MARGIN, y + band_h], fill=RED)
    date = "MONDAY 23 NOVEMBER 2026"
    d.text(((W - textw(date, F_DATE)) / 2, y + 2), date, font=F_DATE, fill=WHITE)
    y += band_h + 8

    # ---- lead strip ----
    lead_top = y
    d.rectangle([MARGIN, lead_top, MARGIN + 6, lead_top + 90], fill=RED)
    lx = MARGIN + 16
    d.text((lx, lead_top), LEAD_KICKER, font=F_KICK, fill=DARKRED)
    d.text((lx, lead_top + 18), LEAD_HEADLINE, font=F_LEAD_H, fill=RED)
    cap_lines = wrap_plain(LEAD_CAPTION, F_LEAD_C, W - MARGIN - lx)
    cy = lead_top + 58
    for ln in cap_lines:
        d.text((lx, cy), ln, font=F_LEAD_C, fill=INK)
        cy += 19
    body_top = lead_top + 98
    d.line([MARGIN, body_top - 4, W - MARGIN, body_top - 4], fill=INK, width=2)

    # ---- body: fit, dropping least consequential stories if needed ----
    body_bottom = H - 40
    dropped = set()
    while True:
        items = build_items(dropped)
        placed = layout(items, body_top, body_bottom)
        if placed is not None:
            break
        nxt = next((n for n in DROP_ORDER if n not in dropped), None)
        if nxt is None:
            raise SystemExit("layout overflow with nothing left to drop")
        dropped.add(nxt)

    # faint centre rule
    mid = MARGIN + COLW + GUTTER // 2
    d.line([mid, body_top + 2, mid, body_bottom], fill=(214, 210, 200), width=1)

    for kind, *rest in placed:
        if kind == "header":
            region, x, yy = rest
            d.rectangle([x, yy, x + COLW, yy + HEADER_H], fill=RED)
            d.text((x + 8, yy + 2), region, font=F_REGION, fill=WHITE)
        else:
            lines, x, yy = rest
            for li, line in enumerate(lines):
                for xo, word, f, color in line:
                    d.text((x + xo, yy + li * LEADING), word, font=f, fill=color)

    included = 1 + sum(1 for kind, *r in placed if kind == "story")
    # ---- footer ----
    fy = H - 32
    d.line([MARGIN, fy - 6, W - MARGIN, fy - 6], fill=INK, width=1)
    foot = f"{included} stories - 7 regions - Monday 23 November 2026"
    d.text(((W - textw(foot, F_FOOT)) / 2, fy), foot, font=F_FOOT, fill=GREY)

    out = os.path.join(ROOT, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(f"entry.png: {os.path.getsize(out)} bytes, {img.size[0]}x{img.size[1]}, "
          f"stories included: {included}, dropped: {sorted(dropped) or 'none'}")


if __name__ == "__main__":
    main()
