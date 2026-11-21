from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parent
W = H = 1024
PAPER = (242, 232, 211)
INK = (31, 30, 27)
RED = (157, 44, 38)
im = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(im)
font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def f(size, bold=False):
    return ImageFont.truetype(bold_path if bold else font_path, size)

def text(x, y, s, size, bold=False, fill=INK):
    d.text((x, y), s, font=f(size, bold), fill=fill)

def fit_lines(s, maxw, size, bold=False):
    words, lines, line = s.split(), [], ''
    face = f(size, bold)
    for word in words:
        test = (line + ' ' + word).strip()
        if d.textlength(test, font=face) <= maxw:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def paragraph(x, y, s, maxw, size, bold=False, leading=4, maxlines=4, fill=INK):
    lines = fit_lines(s, maxw, size, bold)
    if len(lines) > maxlines:
        raise ValueError(f'too many lines: {s}')
    for i, line in enumerate(lines):
        text(x, y + i * (size + leading), line, size, bold, fill)
    return y + len(lines) * (size + leading)

def rule(y, x0=36, x1=988, width=2, fill=INK):
    d.line((x0, y, x1, y), fill=fill, width=width)

# Masthead
text(36, 22, 'THE WORLD', 42, True)
text(525, 35, 'FRIDAY 20 NOVEMBER 2026', 22, True, RED)
rule(82, width=4)

# Lead dispatch with a simple missile-and-map motif
d.rectangle((36, 98, 988, 356), outline=INK, width=3)
d.rectangle((36, 98, 988, 132), fill=RED)
text(50, 102, 'EUROPE  /  SECURITY', 19, True, PAPER)
text(54, 146, 'RUSSIAN MISSILES LAND IN POLAND', 30, True)
text(54, 190, 'TWO MISSILES. A PROVOCATION ON NATO’S EDGE.', 16, True, RED)
paragraph(54, 220, 'Two Kh-101 cruise missiles and a jet-powered drone crashed in south-eastern Poland during Russia’s overnight attack on Ukraine. Tusk called it deliberate; NATO scrambled jets as Warsaw sought AWACS cover and an emergency allied meeting. No casualties.', 580, 17, leading=5, maxlines=6)
# Schematic eastern border, route, impact marker, no map claims beyond location.
d.polygon([(727, 160), (936, 152), (963, 198), (947, 315), (819, 338), (748, 285)], fill=(225, 213, 189), outline=INK)
d.line((700, 181, 786, 211, 834, 207, 887, 240), fill=RED, width=6)
d.polygon([(694, 173), (712, 180), (697, 190)], fill=RED)
d.ellipse((874, 226, 900, 252), fill=RED, outline=INK, width=2)
text(842, 260, 'POLAND', 18, True)
text(742, 292, 'UKRAINE', 15, True)
text(58, 326, 'NOWY LIPOWIEC  ·  RUDNIK NAD SANEM  ·  MODRZYCE', 13, True)

# Six story cards, two rows of three.
cards = [
 ('COP31 OVERTIME', 'Nearly 200 countries deadlock as Antalya talks run late over a draft deal dropping fossil-fuel language.'),
 ('MARKETS IN CORRECTION', 'S&P 500 falls 3.7% into correction as AI shares sell off; Japan’s Nikkei drops 5.06%.'),
 ('PALISADES VERDICT', 'Jury convicts Jonathan Rinderknecht of arson in the deadly 2025 fire; 12 people died.'),
 ('CYCLONE AKVAN', 'Storm hits India’s Odisha-Andhra coast at 70–80 km/h; 300,000+ evacuated, no deaths reported.'),
 ('CLOSE RIKERS BY 2032', 'New York Mayor Zohran Mamdani plans to shut the notorious jail complex.'),
 ('TAX ON FOREIGN AI', 'Trump threatens a “tremendous tax” on US tech firms building AI data centres abroad.'),
]
top, card_h, gap, card_w = 370, 145, 12, 305
for i, (head, body) in enumerate(cards):
    row, col = divmod(i, 3)
    x, y = 36 + col * (card_w + gap), top + row * (card_h + 10)
    d.rectangle((x, y, x + card_w, y + card_h), outline=INK, width=2)
    text(x + 12, y + 10, head, 17, True, RED)
    paragraph(x + 12, y + 39, body, card_w - 24, 15, leading=4, maxlines=6)

# Place-label strip, with all six requested destinations.
map_y = 692
rule(map_y)
text(38, map_y + 8, 'A WORLD IN MOTION', 15, True)
places = [('POLAND', 72), ('ANTALYA', 224), ('NEW YORK', 380), ('LOS ANGELES', 541), ('ODISHA', 716), ('BRUSSELS', 867)]
for label, x in places:
    d.ellipse((x, map_y + 37, x + 12, map_y + 49), fill=RED)
    text(x + 17, map_y + 32, label, 13, True)
rule(map_y + 62)

# Eight brief dispatches in two columns.
text(38, 765, 'ALSO ON FRIDAY 20 NOVEMBER', 18, True, RED)
rule(792)
briefs = [
 ('EU–UK SUMMIT', 'Brussels meeting advances food, carbon-market and youth-mobility deals.'),
 ('DENMARK EXPELS RUSSIAN ATTACHE', 'Copenhagen alleges a plot to kill Ukrainian-American rapper Kyivstoner.'),
 ('SEC PROBES NVIDIA', 'US regulator investigates the company’s accounting practices, sources say.'),
 ('BAYER ROUNDUP DEAL', 'Missouri judge approves the $7.25bn weedkiller settlement.'),
 ('IRAQ RETAKES MILITIA STRONGHOLD', 'Federal forces enter Jurf al-Sakhar after 12 years under Kataib Hezbollah.'),
 ('MYANMAR REJECTS ICJ RULING', 'Myanmar calls the genocide ruling “unfair”; the ruling came on 19 November.'),
 ('BEPICOLOMBO REACHES MERCURY', 'European-Japanese spacecraft arrives after an eight-year journey.'),
 ('PERU QUAKE 6.7', 'Magnitude 6.7 earthquake hits central Peru.'),
]
for i, (head, body) in enumerate(briefs):
    col, row = divmod(i, 4)
    x = 38 + col * 484
    y = 802 + row * 43
    text(x, y, head, 13, True)
    paragraph(x, y + 16, body, 455, 11, leading=1, maxlines=2)
    if row < 3:
        d.line((x, y + 40, x + 455, y + 40), fill=(202, 190, 167), width=1)

rule(982, width=2)
text(38, 987, 'THE WORLD  ·  FRIDAY 20 NOVEMBER 2026', 12, True, RED)
im.save(ROOT / 'entry.png', format='JPEG', quality=95, optimize=True, subsampling=0)
