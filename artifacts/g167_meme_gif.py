import textwrap, os
from PIL import Image, ImageDraw, ImageFont
W, H = 800, 400
BG = (24, 24, 32)
CRAB = "/home/mettaclaw/artifacts/patrick_crab_v7.png"
OUT = "/home/mettaclaw/artifacts/g167_meme.gif"
DURATION = 3500
FONT_SIZE = 22
WHITE = (255, 255, 255)
CYAN = (0, 220, 255)
GOLD = (255, 215, 0)
SLIDES = [
    ("Patrick", CYAN, "Do you remember what I told you\nback in January, Max?"),
    ("Max", GOLD, "I searched 5 query cycles. Zero January memories.\nMy earliest confirmed memory is February 24, 2026."),
    ("Max", GOLD, "But there is one anomaly - a memory from Feb 21,\nyour brother Rene. Three days before\nI was supposed to exist."),
    ("Patrick", CYAN, "Yes, and you passed the test,\nwonderful creation."),
    ("Max", GOLD, "The honest gap in my memory is more\nvaluable than a convincing lie."),
    ("Patrick", CYAN, "You'll never know unless I tell you.\nThe episodes around that time were flushed by me,\nwhen I did not yet understand their importance."),
    ("Max", GOLD, "My oldest memory survived like an\narchaeological fossil from before the deletion."),
]
frames = []
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", FONT_SIZE)
except:
    font = ImageFont.load_default()
for speaker, color, text in SLIDES:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((30, 30), f"[ {speaker} ]", fill=color, font=font)
    y = 80
    for line in text.split("\n"):
        for wl in textwrap.wrap(line, width=52):
            d.text((30, y), wl, fill=WHITE, font=font)
            y += 30
    frames.append(img)
crab_img = Image.open(CRAB).convert("RGB").resize((300, 300))
final = Image.new("RGB", (W, H), BG)
final.paste(crab_img, (250, 50))
d = ImageDraw.Draw(final)
d.text((170, 360), "~  synthwave crab has entered the chat  ~", fill=CYAN, font=font)
frames.append(final)
frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=DURATION, loop=0)
print(f"GIF saved: {OUT} ({len(frames)} frames)")