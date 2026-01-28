from fastapi import FastAPI
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
import requests, io, datetime

app = FastAPI()

STOCK_API = "https://connplex-activeled.onrender.com/data"

@app.get("/signature/connplex.png")
def connplex_signature():

    s = requests.get(
        STOCK_API,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=5
    ).json()["stock"]

    # Image size EXACT like your design
    W, H = 900, 160
    img = Image.new("RGB", (W, H), "#000000")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 20)
        font_symbol = ImageFont.truetype("arial.ttf", 16)
        font_price = ImageFont.truetype("arial.ttf", 32)
        font_change = ImageFont.truetype("arial.ttf", 22)
        font_time = ImageFont.truetype("arial.ttf", 14)
    except:
        font_title = font_symbol = font_price = font_change = font_time = ImageFont.load_default()

    # --- LEFT BLOCK ---
    draw.text((30, 25), "Connplex Cinema", fill="#CFCFCF", font=font_title)
    draw.text((30, 50), s["symbol"], fill="#8A8A8A", font=font_symbol)

    draw.text(
        (30, 80),
        f"₹ {s['price']:.2f}",
        fill="#00FF66",
        font=font_price
    )

    # --- CENTER / RIGHT CHANGE ---
    change_color = "#00FF66" if s["change"] >= 0 else "#FF4444"
    draw.text(
        (420, 90),
        f"{s['change']:+.2f} ({s['change_percent']}%)",
        fill=change_color,
        font=font_change
    )

    # --- TIME ---
    now = datetime.datetime.now().strftime("%H:%M:%S")
    draw.text(
        (30, 130),
        f"Updated: {now}",
        fill="#6F6F6F",
        font=font_time
    )

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return Response(
        content=buf.read(),
        media_type="image/png",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )
