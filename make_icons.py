import os
from PIL import Image, ImageDraw, ImageFilter

res = "android/app/src/main/res/"
src = Image.open("icon.png").convert("RGB")

# Адаптивна іконка на всю площу: розмитий фон з самої картинки + картинка зверху.
S = 1024
z = int(S * 1.4)
bg = src.resize((z, z), Image.LANCZOS).crop(((z - S) // 2, (z - S) // 2, (z + S) // 2, (z + S) // 2))
bg = bg.filter(ImageFilter.GaussianBlur(S * 0.04))

fs = int(S * 0.70)
art = src.resize((fs, fs), Image.LANCZOS).convert("RGBA")
edge = int(fs * 0.03)
m = Image.new("L", (fs, fs), 0)
ImageDraw.Draw(m).rectangle((edge, edge, fs - 1 - edge, fs - 1 - edge), fill=255)
art.putalpha(m.filter(ImageFilter.GaussianBlur(edge / 2)))
fg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
fg.paste(art, ((S - fs) // 2, (S - fs) // 2), art)

dens = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
for name, k in dens.items():
    d = res + "mipmap-" + name
    os.makedirs(d, exist_ok=True)
    s = int(48 * k)
    img = src.resize((s, s), Image.LANCZOS)
    img.save(d + "/ic_launcher.png")
    big = src.resize((s * 4, s * 4), Image.LANCZOS)
    mask = Image.new("L", (s * 4, s * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, s * 4 - 1, s * 4 - 1), fill=255)
    rnd = Image.new("RGBA", (s * 4, s * 4), (0, 0, 0, 0))
    rnd.paste(big, (0, 0), mask)
    rnd.resize((s, s), Image.LANCZOS).save(d + "/ic_launcher_round.png")
    a = int(108 * k)
    fg.resize((a, a), Image.LANCZOS).save(d + "/ic_launcher_fg.png")
    bg.resize((a, a), Image.LANCZOS).save(d + "/ic_launcher_bg.png")

os.makedirs(res + "mipmap-anydpi-v26", exist_ok=True)
xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
       '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
       '    <background android:drawable="@mipmap/ic_launcher_bg"/>\n'
       '    <foreground android:drawable="@mipmap/ic_launcher_fg"/>\n'
       '</adaptive-icon>\n')
for f in ("ic_launcher.xml", "ic_launcher_round.xml"):
    open(res + "mipmap-anydpi-v26/" + f, "w").write(xml)
print("icons done")
