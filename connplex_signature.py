from fastapi import FastAPI
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
import requests, io, datetime

# ✅ APP MUST BE DEFINED FIRST
app = FastAPI()

STOCK_API = "https://connplex-activeled.onrender.com/data"


# ---------------- ROOT (OPTIONAL BUT GOOD)
@app.get("/")
def root():
    return {
        "service": "Connplex Email Signature",
        "status": "running"
    }


# ---------------- LIVE STRIP (SMALL)
@app.get("/signature/connplex.png")
def connplex_signature():

    s = requests.get(
        STOCK_API,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=5
    ).json()["stock"]

    W, H = 900, 160
    img = Image.new("RGB", (W, H), "#000000")
    draw = ImageDraw.Draw(img)

    try:
        font_price = ImageFont.truetype("arial.ttf", 32)
        font_mid = ImageFont.truetype("arial.ttf", 22)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font_price = font_mid = font_small = ImageFont.load_default()

    draw.text((30, 30), "Connplex Cinema", fill="#CFCFCF", font=font_mid)
    draw.text((30, 60), s["symbol"], fill="#8A8A8A", font=font_small)
    draw.text((30, 90), f"₹ {s['price']:.2f}", fill="#00FF66", font=font_price)

    change_color = "#00FF66" if s["change"] >= 0 else "#FF4444"
    draw.text(
        (420, 100),
        f"{s['change']:+.2f} ({s['change_percent']}%)",
        fill=change_color,
        font=font_mid
    )

    now = datetime.datetime.now().strftime("%H:%M:%S")
    draw.text((30, 135), f"Updated: {now}", fill="#6F6F6F", font=font_small)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return Response(
        buf.read(),
        media_type="image/png",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

# ---------------- FULL SIGNATURE (WHITE + LOGO)
@app.get("/signature/connplex-full.png")
def connplex_full_signature():

    s = requests.get(
        STOCK_API,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=5
    ).json()["stock"]

    W, H = 900, 420
    img = Image.new("RGB", (W, H), "#FFFFFF")  # ✅ WHITE BACKGROUND
    draw = ImageDraw.Draw(img)

    try:
        title = ImageFont.truetype("arial.ttf", 22)
        text = ImageFont.truetype("arial.ttf", 16)
        bold = ImageFont.truetype("arial.ttf", 18)
        price = ImageFont.truetype("arial.ttf", 28)
        small = ImageFont.truetype("arial.ttf", 13)
    except:
        title = text = bold = price = small = ImageFont.load_default()

    # ---------- LOGO ----------
    try:
        logo = Image.open("assets/connplex_bg.png").convert("RGBA")
        logo = logo.resize((90, 90))
        img.paste(logo, (30, 20), logo)
    except:
        pass  # logo missing → don't crash

    # ---------- PERSONAL INFO ----------
    draw.text((140, 25), "Kunal Jani", fill="#000000", font=title)
    draw.text((140, 50), "General Manager – Technology", fill="#444444", font=text)
    draw.text((140, 72), "+91 98245 38537", fill="#444444", font=text)

    # ---------- COMPANY ----------
    draw.text((30, 120), "CONNPLEX CINEMAS LIMITED", fill="#C9A100", font=bold)
    draw.text((30, 145), "Ahmedabad, Gujarat", fill="#666666", font=small)

    # Divider
    draw.line((30, 180, 870, 180), fill="#DDDDDD", width=1)

    # ---------- STOCK ----------
    draw.text((30, 200), s["symbol"], fill="#777777", font=small)
    draw.text((30, 225), f"₹ {s['price']:.2f}", fill="#00AA44", font=price)

    change_color = "#00AA44" if s["change"] >= 0 else "#CC0000"
    draw.text(
        (420, 235),
        f"{s['change']:+.2f} ({s['change_percent']}%)",
        fill=change_color,
        font=text
    )

    now = datetime.datetime.now().strftime("%H:%M:%S")
    draw.text((30, 270), f"Updated: {now}", fill="#888888", font=small)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return Response(
        buf.read(),
        media_type="image/png",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )
