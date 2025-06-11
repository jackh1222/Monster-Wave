# combine_sprite.py
import os
from PIL import Image

# --- your frame lists here ---
player_frames = [
    "player_idle.png",
    "player_run0.png",
    "player_run1.png",
    "player_corpse.png",
]
enemy_frames = [
    "enemy_run0.png",
    "enemy_run1.png",
    "enemy_corpse.png",
]

# --- load images and build `sprite_sheet` exactly as before ---
imgs = [Image.open(p).convert("RGBA") for p in player_frames]
w, h = imgs[0].size
cols = max(len(player_frames), len(enemy_frames))
rows = 2
sheet = Image.new("RGBA", (w*cols, h*rows), (0,0,0,0))
# paste player row
for i, img in enumerate(imgs):
    sheet.paste(img, (i*w, 0), img)
# paste enemy row
imgs2 = [Image.open(p).convert("RGBA") for p in enemy_frames]
for i, img in enumerate(imgs2):
    sheet.paste(img, (i*w, h), img)

# --- explicit save path & feedback ---
here = os.path.dirname(__file__)            # folder where this script lives
out_name = "sprite_sheet.png"
out_path = os.path.join(here, out_name)
sheet.save(out_path)
print(f"✅  Sprite sheet saved to: {out_path}")
