import os, shutil
from PIL import Image, ImageDraw

res = "android/app/src/main/res"
src = Image.open("icon.png").convert("RGB")

# прибрати адаптивну іконку Capacitor, щоб використовувалась наша
shutil.rmtree(os.path.join(res, "mipmap-anydpi-v26"), ignore_errors=True)

sizes = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
for name, s in sizes.items():
    d = os.path.join(res, "mipmap-" + name)
    os.makedirs(d, exist_ok=True)
    src.resize((s, s), Image.LANCZOS).save(os.path.join(d, "ic_launcher.png"))
    big = src.resize((s * 4, s * 4), Image.LANCZOS)
    mask = Image.new("L", (s * 4, s * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, s * 4 - 1, s * 4 - 1), fill=255)
    rnd = Image.new("RGBA", (s * 4, s * 4), (0, 0, 0, 0))
    rnd.paste(big, (0, 0), mask)
    rnd.resize((s, s), Image.LANCZOS).save(os.path.join(d, "ic_launcher_round.png"))
print("icons done")
