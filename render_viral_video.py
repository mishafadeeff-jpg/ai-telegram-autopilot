import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Output dimensions: 1080 x 1920 (Standard 9:16 Vertical for TikTok / Shorts / Reels)
W, H = 1080, 1920
FPS = 30
DURATION_SEC = 8  # 8-second punchy viral clip
TOTAL_FRAMES = FPS * DURATION_SEC

OUTPUT_DIR = os.path.dirname(__file__)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "lucky_wheel_promo.mp4")

# Desktop path if accessible
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "lucky_wheel_promo.mp4")

print(f"Rendering {TOTAL_FRAMES} frames for viral video (1080x1920 @ {FPS}fps)...")

SECTORS = [
    {"label": "TG Premium 👑", "color": (236, 72, 153)},
    {"label": "+1,000 ⭐", "color": (234, 179, 8)},
    {"label": "Золотой Билет 🎟️", "color": (139, 92, 246)},
    {"label": "+250 ⭐", "color": (6, 182, 212)},
    {"label": "Мем Дня 🤪", "color": (249, 115, 22)},
    {"label": "+50 ⭐", "color": (16, 185, 129)},
    {"label": "+2 Крутки 🔄", "color": (59, 130, 246)},
    {"label": "Подарок 🎁", "color": (168, 85, 247)},
]
NUM_SECTORS = len(SECTORS)
ARC = (2 * math.pi) / NUM_SECTORS

# Confetti particles
np.random.seed(42)
CONFETTI = [
    {
        "x": np.random.randint(0, W),
        "y": np.random.randint(-500, 0),
        "vx": np.random.uniform(-4, 4),
        "vy": np.random.uniform(8, 20),
        "size": np.random.randint(12, 25),
        "color": (np.random.randint(150, 255), np.random.randint(150, 255), np.random.randint(50, 255))
    }
    for _ in range(120)
]

try:
    font_title = ImageFont.truetype("arialbd.ttf", 62)
    font_sub = ImageFont.truetype("arialbd.ttf", 44)
    font_wheel = ImageFont.truetype("arialbd.ttf", 32)
    font_win = ImageFont.truetype("arialbd.ttf", 52)
    font_cta = ImageFont.truetype("arialbd.ttf", 46)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_wheel = ImageFont.load_default()
    font_win = ImageFont.load_default()
    font_cta = ImageFont.load_default()

writer = imageio.get_writer(OUTPUT_PATH, fps=FPS, codec="libx264", quality=8)

# Center of wheel
CX, CY = W // 2, 980
RADIUS = 420

for frame_idx in range(TOTAL_FRAMES):
    t = frame_idx / TOTAL_FRAMES
    elapsed = frame_idx / FPS

    # 1. Background Gradient (Dark Cyberpunk Blue to Deep Violet)
    img = Image.new("RGB", (W, H), (10, 15, 30))
    draw = ImageDraw.Draw(img)

    for y in range(0, H, 16):
        ratio = y / H
        r = int(10 + 25 * ratio)
        g = int(15 + 10 * ratio)
        b = int(30 + 60 * ratio)
        draw.rectangle([(0, y), (W, y + 16)], fill=(r, g, b))

    # Background glowing circular aura
    glow_pulse = math.sin(elapsed * 4) * 0.15 + 0.85
    aura_r = int(RADIUS * 1.35 * glow_pulse)
    draw.ellipse([CX - aura_r, CY - aura_r, CX + aura_r, CY + aura_r], outline=(147, 51, 234), width=12)

    # 2. TOP BANNER & HEADLINE
    # Header badge
    draw.rounded_rectangle([W // 2 - 380, 140, W // 2 + 380, 230], radius=45, fill=(168, 85, 247, 200), outline=(234, 179, 8), width=4)
    draw.text((W // 2, 185), "🔥 ХАЛЯВА В TELEGRAM! 🔥", font=font_title, fill=(255, 255, 255), anchor="mm")

    # Subtitles
    draw.text((W // 2, 320), "КРУТИ КОЛЕСО ФОРТУНЫ 🎰", font=font_title, fill=(251, 191, 36), anchor="mm")
    draw.text((W // 2, 400), "Выигрывай Telegram Premium и Stars!", font=font_sub, fill=(226, 232, 240), anchor="mm")

    # 3. SPIN PHYSICS
    # Starts at t=0.1, spins rapidly, slows down at t=0.6, stops on TG Premium (index 0)
    if elapsed < 0.8:
        # Idle gentle rotation
        current_angle = elapsed * 0.5
    elif elapsed < 4.8:
        # Active rapid spin with easing
        spin_progress = (elapsed - 0.8) / 4.0
        ease_out = 1 - math.pow(1 - spin_progress, 3.2)
        total_rotations = 6 * 2 * math.pi + (3 * math.pi / 2 - ARC / 2)
        current_angle = 0.4 + total_rotations * ease_out
    else:
        # Stopped exactly on Premium sector
        current_angle = 0.4 + 6 * 2 * math.pi + (3 * math.pi / 2 - ARC / 2)

    # 4. DRAW WHEEL WEDGES
    for i, sec in enumerate(SECTORS):
        ang_start = current_angle + i * ARC
        ang_end = ang_start + ARC

        # Slice polygon approximation
        points = [(CX, CY)]
        steps = 16
        for s in range(steps + 1):
            a = ang_start + (ang_end - ang_start) * (s / steps)
            px = CX + RADIUS * math.cos(a)
            py = CY + RADIUS * math.sin(a)
            points.append((px, py))
        points.append((CX, CY))
        draw.polygon(points, fill=sec["color"], outline=(15, 23, 42))

        # Wedge Label text
        mid_ang = ang_start + ARC / 2
        tx = CX + (RADIUS - 120) * math.cos(mid_ang)
        ty = CY + (RADIUS - 120) * math.sin(mid_ang)
        draw.text((tx, ty), sec["label"], font=font_wheel, fill=(255, 255, 255), anchor="mm")

    # Outer Golden Rim
    draw.ellipse([CX - RADIUS, CY - RADIUS, CX + RADIUS, CY + RADIUS], outline=(245, 158, 11), width=16)

    # Golden Bulbs
    for b in range(20):
        ba = b * (2 * math.pi / 20)
        bx = CX + (RADIUS + 2) * math.cos(ba)
        by = CY + (RADIUS + 2) * math.sin(ba)
        bulb_col = (254, 240, 138) if (b + int(elapsed * 8)) % 2 == 0 else (168, 85, 247)
        draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=bulb_col, outline=(0, 0, 0), width=2)

    # Center Hub Button
    draw.ellipse([CX - 90, CY - 90, CX + 90, CY + 90], fill=(234, 179, 8), outline=(15, 23, 42), width=8)
    draw.text((CX, CY - 15), "🎰", font=font_title, fill=(0, 0, 0), anchor="mm")
    draw.text((CX, CY + 35), "SPIN", font=font_wheel, fill=(0, 0, 0), anchor="mm")

    # Pointer Arrow (Top)
    pointer_bounce = math.sin(elapsed * 12) * 6 if (0.8 < elapsed < 4.8) else 0
    p_pts = [
        (CX, CY - RADIUS + 40 + pointer_bounce),
        (CX - 35, CY - RADIUS - 50 + pointer_bounce),
        (CX + 35, CY - RADIUS - 50 + pointer_bounce)
    ]
    draw.polygon(p_pts, fill=(251, 191, 36), outline=(255, 255, 255), width=4)

    # 5. WIN EFFECT (From 4.8s onwards)
    if elapsed >= 4.8:
        # Confetti raining down
        for c in CONFETTI:
            c["x"] += c["vx"]
            c["y"] += c["vy"]
            if c["y"] > H:
                c["y"] = -50
                c["x"] = np.random.randint(0, W)
            draw.rectangle([c["x"], c["y"], c["x"] + c["size"], c["y"] + c["size"] * 0.6], fill=c["color"])

        # Flash Win Pop-up Box
        box_y = 1520
        draw.rounded_rectangle([W // 2 - 480, box_y - 120, W // 2 + 480, box_y + 130], radius=35, fill=(15, 23, 42, 240), outline=(234, 179, 8), width=6)
        draw.text((W // 2, box_y - 65), "🎉 ДЖЕКПОТ ВЫИГРАН! 🎉", font=font_win, fill=(250, 204, 21), anchor="mm")
        draw.text((W // 2, box_y), "👑 Telegram Premium на 3 месяца!", font=font_sub, fill=(255, 255, 255), anchor="mm")
        draw.text((W // 2, box_y + 65), "Забирай свою бесплатную крутку в боте!", font=font_wheel, fill=(167, 243, 208), anchor="mm")

    # 6. BOTTOM CTA BUTTON
    cta_y = 1740
    pulse = math.sin(elapsed * 6) * 8
    draw.rounded_rectangle([W // 2 - 440 - pulse, cta_y - 50, W // 2 + 440 + pulse, cta_y + 50], radius=35, fill=(234, 179, 8), outline=(255, 255, 255), width=4)
    draw.text((W // 2, cta_y), "👉 ССЫЛКА В ШАПКЕ ПРОФИЛЯ 👈", font=font_cta, fill=(15, 23, 42), anchor="mm")

    frame_np = np.array(img)
    writer.append_data(frame_np)

    if (frame_idx + 1) % (FPS * 2) == 0:
        print(f"Rendered {frame_idx + 1}/{TOTAL_FRAMES} frames ({(frame_idx + 1)/TOTAL_FRAMES*100:.0f}%)...")

writer.close()
print("✅ Video rendering complete:", OUTPUT_PATH)

# Copy to Desktop for instant access
try:
    import shutil
    shutil.copy2(OUTPUT_PATH, DESKTOP_PATH)
    print("✅ Copied directly to user Desktop:", DESKTOP_PATH)
except Exception as e:
    print("Could not copy to desktop:", e)
