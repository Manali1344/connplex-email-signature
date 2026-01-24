from fastapi import FastAPI
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
import requests, io, datetime

app = FastAPI()

STOCK_API = "https://connplex-activeled.onrender.com/data"

@app.get("/signature/connplex.png")
def connplex_signature():
    response = requests.get(
        STOCK_API,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=5
    )

    data = response.json()
    s = data["stock"]   # ✅ IMPORTANT

    img = Image.new("RGB", (640, 160), "#000000")
    draw = ImageDraw.Draw(img)

    try:
        font_big = ImageFont.truetype("arial.ttf", 36)
        font_mid = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_big = font_mid = font_small = ImageFont.load_default()

    # Title
    draw.text((20, 10), "Connplex Cinema", fill="#ffffff", font=font_mid)

    # Stock symbol
    draw.text((20, 45), s["symbol"], fill="#aaaaaa", font=font_small)

    # Price
    draw.text((20, 75), f'₹ {s["price"]:.2f}', fill="#00ff66", font=font_big)

    # Change
    color = "#00ff66" if s["change"] >= 0 else "#ff3333"
    draw.text(
        (320, 90),
        f'{s["change"]:+.2f} ({s["change_percent"]}%)',
        fill=color,
        font=font_mid
    )

    # Time
    now = datetime.datetime.now().strftime("%H:%M:%S")
    draw.text((20, 130), f"Updated: {now}", fill="#666666", font=font_small)

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
