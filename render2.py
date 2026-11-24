#!/usr/bin/env python3
"""Render entry.png v2 — Monday 23 November 2026 world news as a broadsheet front page.

v2 redesign after v1 ranked 10,065/13,031 (score 416,882) in round 3.
v1 diagnosis: 1024px canvas with 13-15px body type (illegible at judging
scale), flat hierarchy (every story identical weight), monotone red bars,
ragged whitespace at the bottom, major stories buried as micro-items, and
story #43 dropped by the fit pass.

v2 fixes: 1600x2240 portrait broadsheet, serif nameplate, a 92px lead
headline with deck, a three-up secondary-lead row (US House, Nvidia, Iran),
a markets ticker band, black region bars, and a three-column body at
19-21px type. All 43 stories included; an auto-fit pass shrinks body type
in steps if the page would overflow, but never drops a story.
Deterministic pure Pillow drawing.
"""
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


W, H = 1600, 2240
MARGIN = 40
PAPER = (250, 249, 244)
INK = (14, 14, 14)
RED = (164, 22, 29)
DARKRED = (118, 14, 20)
GREY = (92, 92, 92)
RULE = (198, 194, 186)
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)

_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def textw(s, f):
    return _probe.textlength(s, font=f)


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


# ---------------------------------------------------------------- stories
LEAD_KICKER = "ANTALYA, TURKEY — THE CLIMATE SUMMIT"
LEAD_HEADLINE = "COP31 ENDS WITHOUT A DEAL"
LEAD_DECK = (
    "The longest UN climate conference in history breaks up two days late and empty-handed: "
    "the EU and climate-vulnerable states reject a draft stripped of any fossil-fuel language. "
    "Some 90 countries salvage a voluntary pledge of a 35% clean-electricity share by 2035 — "
    "and every unresolved fight is carried over to COP32 in Ethiopia."
)

# (kicker, headline, caption) — the three secondary leads under the main story.
SECONDARY = [
    ("WASHINGTON — CONGRESS", "DEMOCRATS WIN 258 HOUSE SEATS",
     "The largest House majority since 1992 redraws the balance of power in Washington."),
    ("MARKETS — THE HUANG EFFECT", "NVIDIA BRINGS BACK ITS CEO",
     "Jensen Huang returns 11 days after quitting: shares leap ~33% and the S&P 500 jumps 4.82%."),
    ("THE GULF — HORMUZ STANDOFF", "TRUMP: IRAN DEAL 'NOT ACCEPTABLE'",
     "Tehran defies the US blockade and claims a US drone downed; Trump threatens to sink tankers."),
]

TICKER = ("MARKETS ON THE DAY:   KOSPI -3.3%   ·   S&P 500 +4.82%   ·   NVIDIA +33%   ·   "
          "SAMSUNG -3.1%   ·   SK HYNIX -2.5%")

# Body regions: (bar title, [(num, headline, caption), ...]) — secondary-lead
# stories 16, 33, 34 live above, so they are not repeated here.
REGIONS = [
    ("EUROPE & THE UKRAINE WAR", [
        (2, "POLAND: 3 RUSSIAN KH-101 MISSILES DOWN",
         "All three objects that crashed on 20 Nov confirmed Russian cruise missiles; NATO council meets in emergency session, Warsaw wants more F-35s and AWACS."),
        (3, "UKRAINE SINKS RUSSIAN CORVETTE MERKURY",
         "Seven naval drones strike at Benghazi, Libya — Zelenskyy confirms the sinking."),
        (4, "RUSSIAN SHIP SPARTA II ABLAZE",
         "Drone hit in the Gulf of Finland; ship towed out as Helsinki summons the Russian ambassador."),
        (5, "DYMER FLATS STRIKE KILLS 11",
         "Kyiv-region apartment block hit, 14 first missing; Zelenskyy slams US Patriot and interceptor delays."),
        (6, "KRYVYI RIH STRIKE KILLS 2",
         "A child and a young woman die; 25 apartment blocks, a hospital and schools damaged."),
        (7, "DRONE HITS KHARKIV KINDERGARTEN",
         "A Russian drone strikes a nursery school in Kharkiv."),
        (8, "SLOVYANSK STRIKES KILL 2",
         "Overnight assault of ~153 drones, some 60 of them jet-powered."),
        (9, "UKRAINE HITS RUSSIAN OIL SITES",
         "Oil infrastructure struck deep inside Russia: Rostov, Perm and Tatarstan."),
        (10, "EU PLANS 22ND SANCTIONS PACKAGE",
         "60 banks, crypto platforms and 70+ shadow-fleet vessels targeted; Russian teams banned under the national flag."),
        (11, "ABU DHABI PEACE TALKS WRAP",
         "Ukraine–Russia–US trilateral ends; negotiator Medinsky holds a firm territorial line."),
        (12, "MOLDOVA: 7 DRONE INCURSIONS",
         "Five Russian drones crash in 2.5 hours; Chisinau warns on online military recruitment."),
        (13, "EX-POLICE CHIEF FOUND DEAD",
         "Gianni De Gennaro, 78, found dead in Tuscany days after prosecutors sought his arrest in the Borsellino mafia-inquiry case."),
        (14, "HUNGARY PM TO VISIT TRANSCARPATHIA",
         "Péter Magyar pledges support to Ukrainians and ethnic Hungarians."),
        (15, "PARIS WEALTH-TAX PUSH GROWS",
         "A global billionaire-tax campaign gathers politicians, economists and unions."),
    ]),
    ("MIDDLE EAST", [
        (17, "IRAN HITS BAHRAIN INDUSTRIAL SITE",
         "Civilian facility struck, 2 injured; the IRGC claims US positions hit as Bahrain's defences intercept further attacks."),
        (18, "GAZA TRUCK STRIKE KILLS 3",
         "Israeli forces hit a truck, Gaza's Health Ministry says; witnesses saw food and WCK-logo papers, WCK says the vehicle was not affiliated."),
        (19, "SETTLER ARSON 'JEWISH TERRORISM'",
         "PM-elect Eisenkot's words as Palestinian vehicles burn near Ramallah under 'Revenge' graffiti."),
        (20, "ISRAEL COALITION TALKS STALL",
         "Netanyahu's Likud and Eisenkot's Yashar end talks without a deal; the next government is uncertain."),
        (21, "VANCE SILENT ON IRAN STRIKES",
         "The vice-president declines to say whether he would have authorised the strikes."),
        (22, "IRAN FLOGS SINGER AHMADI",
         "Parastoo Ahmadi and four band and production members flogged in Qom, their lawyers say."),
    ]),
    ("ASIA", [
        (23, "ASIAN CHIP STOCKS SLIDE",
         "Wall Street's AI-spending rout hits Asia: Kospi falls as much as 5.8% intraday, closes -3.3% at its lowest since January."),
        (24, "INDONESIA FACTORY BLAZE KILLS 24",
         "Dozens still missing as rescuers search the ruins of the factory fire."),
        (25, "INDIA GIVES NEPAL $1.62BN",
         "A ~€1.4bn package to rebuild after the glacier floods."),
        (26, "EU–INDONESIA TRADE DEAL SIGNED",
         "A landmark free-trade and investment pact after a decade of talks, covering 730 million people."),
        (27, "JAKARTA: VP NOMINEES TO COME",
         "Indonesia's president will nominate vice-presidential candidates, state media report."),
        (28, "THAI MP'S ROYAL-INSULT TERM HALVED",
         "An appeal court cuts the lawmaker's jail sentence for royal insult."),
        (29, "S. KOREA EDUCATION CHIEF QUITS",
         "The minister resigns over the exam-cheating chaos."),
        (30, "HASINA FACES ARREST IF SHE RETURNS",
         "Bangladesh will jail the ex-PM if she comes back from India."),
        (31, "INDIA–NETHERLANDS DEEPEN TIES",
         "Jaishankar and FM Berendsen expand the partnership: tech, semiconductors, defence, renewables."),
        (32, "US ASIA LEAD OVER CHINA SHRINKS",
         "Smallest since 2018, the Lowy Asia Power Index finds; China now leads on diplomatic influence and economic ties."),
    ]),
    ("NORTH AMERICA", [
        (35, "TRUMP CALLS PUTIN 'MY FRIEND'",
         "The remark follows his Shenzhen summit with Xi Jinping."),
        (36, "TRUMP FIRES CYBER DIRECTOR",
         "Sean Cairncross replaced as National Cyber Director after a wave of US outages."),
        (37, "GOP OPEN TO IRAN FUNDING CAP",
         "Senate leaders signal a deal to limit war funding and dodge a shutdown; money lapses 11 Dec."),
        (38, "AMTRAK TRAIN DERAILS",
         "A train hits a tractor-trailer near Lafayette, Louisiana; lead locomotive and two baggage cars leave the track."),
        (39, "US PRESSES NVIDIA ON CHINA SALES",
         "Washington demands answers on chip sales to China; the intel chief distances Putin from Trump's praise."),
    ]),
    ("LATIN AMERICA", [
        (40, "'EL CHAPO ISIDRO' CAPTURED",
         "FBI most-wanted fugitive Fausto Isidro Meza Flores seized in Sinaloa by Mexican special forces with US intelligence help."),
    ]),
    ("AFRICA", [
        (41, "NIGERIA VILLA LOSES WATER, POWER",
         "President Tinubu says the presidential villa in Abuja was hit by water and power cuts."),
        (42, "SUDAN EMERGENCY DEEPENS",
         "The humanitarian emergency keeps deteriorating; security and governance strains grow across Niger, Nigeria, Libya and the DRC."),
    ]),
    ("SCIENCE & SPACE", [
        (43, "BEPICOLOMBO MERCURY ALERT",
         "The Europe–Japan Mercury mission flags a software caveat on orbit entry; operational checks needed before arrival."),
    ]),
]


def wrap_story(num, head, cap, f_head, f_cap, f_num, colw):
    """Flow number + bold headline + caption into token lines."""
    tokens = [(f"{num}.", f_num, RED)]
    tokens += [(w, f_head, INK) for w in head.split()]
    tokens += [(w, f_cap, INK) for w in cap.split()]
    fonts = (f_num, f_head, f_cap)
    space = {id(f): textw(" ", f) for f in fonts}
    lines, cur, curw = [], [], 0.0
    for word, f, color in tokens:
        ww = textw(word, f)
        add = ww if not cur else ww + space[id(cur[-1][1])]
        if cur and curw + add > colw:
            lines.append(cur)
            cur, curw = [(word, f, color)], ww
        else:
            cur.append((word, f, color))
            curw += add
    if cur:
        lines.append(cur)
    out = []
    for line in lines:
        x, placed = 0.0, []
        for word, f, color in line:
            placed.append((x, word, f, color))
            x += textw(word, f) + space[id(f)]
        out.append(placed)
    return out


def build_body(f_head, f_cap, f_num, pitch, gap, header_h, colw):
    items = []  # ("header", title, h) | ("story", lines, h)
    for region, stories in REGIONS:
        items.append(("header", region, header_h))
        for num, head, cap in stories:
            lines = wrap_story(num, head, cap, f_head, f_cap, f_num, colw)
            items.append(("story", lines, len(lines) * pitch + gap))
    return items


def place_columns(items, ncols, top, bottom, header_gap):
    """Balanced 3-column placement; headers keep with their first story."""
    total = sum(it[2] for it in items) + header_gap * sum(1 for it in items if it[0] == "header")
    target = total / ncols
    cols, col, y, used = [], 0, top, 0.0
    placed = []
    for i, it in enumerate(items):
        h = it[2] + (header_gap if it[0] == "header" else 0)
        if it[0] == "header":
            nxt = items[i + 1] if i + 1 < len(items) else None
            need = h + (nxt[2] if nxt else 0)
            if col < ncols - 1 and used + need > target and used > 0:
                col += 1
                y, used = top, 0.0
            if y + need > bottom and col < ncols - 1:
                col += 1
                y, used = top, 0.0
        else:
            if col < ncols - 1 and used + h > target and used > target * 0.92:
                col += 1
                y, used = top, 0.0
            if y + h > bottom and col < ncols - 1:
                col += 1
                y, used = top, 0.0
        placed.append((it, col, y))
        y += h
        used += h
        if col == ncols - 1 and y > bottom:
            return None
    cols = placed
    return cols


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    inner = W - 2 * MARGIN

    # ---------------- masthead ----------------
    y = 26
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=3)
    y += 10
    strap = "ONE PAGE  ·  ONE DAY  ·  THE WHOLE WORLD"
    f_strap = font(SANS_B, 19)
    d.text(((W - textw(strap, f_strap)) / 2, y), strap, font=f_strap, fill=GREY)
    y += 30
    f_mast = font(SERIF_B, 84)
    mast = "THE WORLD IN ONE IMAGE"
    d.text(((W - textw(mast, f_mast)) / 2, y), mast, font=f_mast, fill=INK)
    y += 104
    d.rectangle([MARGIN, y, W - MARGIN, y + 54], fill=BLACK)
    f_date = font(SANS_B, 30)
    date = "MONDAY 23 NOVEMBER 2026"
    d.text((MARGIN + 18, y + 10), date, font=f_date, fill=WHITE)
    f_cnt = font(SANS_B, 24)
    cnt = "43 STORIES · 7 REGIONS · 1 PAGE"
    d.text((W - MARGIN - 18 - textw(cnt, f_cnt), y + 14), cnt, font=f_cnt, fill=WHITE)
    y += 54 + 22

    # ---------------- lead story ----------------
    f_kick = font(SANS_B, 24)
    lx = MARGIN + 24
    d.text((lx, y), LEAD_KICKER, font=f_kick, fill=DARKRED)
    f_lead = font(SERIF_B, 88)
    ly = y + 34
    for ln in wrap_plain(LEAD_HEADLINE, f_lead, inner - 24):
        d.text((lx, ly), ln, font=f_lead, fill=RED)
        ly += 100
    f_deck = font(SERIF, 25)
    dy = ly + 4
    for ln in wrap_plain(LEAD_DECK, f_deck, inner - 24):
        d.text((lx, dy), ln, font=f_deck, fill=INK)
        dy += 34
    d.rectangle([MARGIN, y, MARGIN + 8, dy - 8], fill=RED)
    y = dy + 14
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=3)
    y += 18

    # ---------------- secondary leads (3-up) ----------------
    gutter = 28
    colw3 = (inner - 2 * gutter) // 3
    f_skick = font(SANS_B, 18)
    f_shead = font(SANS_B, 31)
    f_scap = font(SANS, 20)
    sec_bottom = y
    for i, (kick, head, cap) in enumerate(SECONDARY):
        x = MARGIN + i * (colw3 + gutter)
        yy = y
        d.text((x, yy), kick, font=f_skick, fill=DARKRED)
        yy += 28
        for ln in wrap_plain(head, f_shead, colw3):
            d.text((x, yy), ln, font=f_shead, fill=INK)
            yy += 38
        yy += 2
        for ln in wrap_plain(cap, f_scap, colw3):
            d.text((x, yy), ln, font=f_scap, fill=INK)
            yy += 26
        sec_bottom = max(sec_bottom, yy)
        if i < 2:
            vx = x + colw3 + gutter // 2
            d.line([vx, y, vx, sec_bottom], fill=RULE, width=1)
    y = sec_bottom + 16

    # ---------------- markets ticker ----------------
    d.rectangle([MARGIN, y, W - MARGIN, y + 44], fill=RED)
    f_tick = font(SANS_B, 20)
    d.text(((W - textw(TICKER, f_tick)) / 2, y + 10), TICKER, font=f_tick, fill=WHITE)
    y += 44 + 18

    # ---------------- body (auto-fit, never drops) ----------------
    body_top = y
    body_bottom = H - 64
    ncols = 3
    colw = (inner - (ncols - 1) * gutter) // ncols
    f_region = font(SANS_B, 23)
    attempts = [
        # (head, cap, pitch, story_gap, header_h, header_gap)
        (21, 19, 25, 9, 36, 10),
        (20, 18, 24, 8, 34, 9),
        (19, 17, 22, 7, 32, 8),
        (18, 16, 21, 6, 30, 7),
    ]
    placed = None
    for hs, cs, pitch, gap, hh, hgap in attempts:
        f_head, f_cap, f_num = font(SANS_B, hs), font(SANS, cs), font(SANS_B, hs)
        items = build_body(f_head, f_cap, f_num, pitch, gap, hh, colw)
        placed = place_columns(items, ncols, body_top, body_bottom, hgap)
        if placed is not None:
            break
    if placed is None:
        raise SystemExit("body overflow at smallest type step")

    col_x = [MARGIN + i * (colw + gutter) for i in range(ncols)]
    for i in range(1, ncols):
        vx = col_x[i] - gutter // 2
        d.line([vx, body_top + 2, vx, body_bottom], fill=RULE, width=1)
    for it, col, yy in placed:
        x = col_x[col]
        if it[0] == "header":
            d.rectangle([x, yy, x + colw, yy + it[2]], fill=BLACK)
            d.text((x + 10, yy + 5), it[1], font=f_region, fill=WHITE)
        else:
            for li, line in enumerate(it[1]):
                for xo, word, f, color in line:
                    d.text((x + xo, yy + li * pitch), word, font=f, fill=color)

    # ---------------- footer ----------------
    fy = H - 46
    d.line([MARGIN, fy - 8, W - MARGIN, fy - 8], fill=INK, width=2)
    f_foot = font(SANS, 19)
    foot = "43 stories · 7 regions · Every item from the verified reporting of Monday 23 November 2026 · The World in One Image"
    d.text(((W - textw(foot, f_foot)) / 2, fy), foot, font=f_foot, fill=GREY)

    out = os.path.join(ROOT, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(f"entry.png: {os.path.getsize(out)} bytes, {img.size[0]}x{img.size[1]}, "
          f"stories: 43 (1 lead + 3 secondary + 39 body)")


if __name__ == "__main__":
    main()
