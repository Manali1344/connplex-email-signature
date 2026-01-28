# from fastapi import FastAPI
# from fastapi.responses import Response
# from PIL import Image, ImageDraw, ImageFont
# import requests, io, datetime

# app = FastAPI()

# STOCK_API = "https://connplex-activeled.onrender.com/data"

# @app.get("/signature/connplex.png")
# def connplex_signature():

#     s = requests.get(
#         STOCK_API,
#         headers={"User-Agent": "Mozilla/5.0"},
#         timeout=5
#     ).json()["stock"]

#     # Image size EXACT like your design
#     W, H = 900, 160
#     img = Image.new("RGB", (W, H), "#000000")
#     draw = ImageDraw.Draw(img)

#     try:
#         font_title = ImageFont.truetype("arial.ttf", 20)
#         font_symbol = ImageFont.truetype("arial.ttf", 16)
#         font_price = ImageFont.truetype("arial.ttf", 32)
#         font_change = ImageFont.truetype("arial.ttf", 22)
#         font_time = ImageFont.truetype("arial.ttf", 14)
#     except:
#         font_title = font_symbol = font_price = font_change = font_time = ImageFont.load_default()

#     # --- LEFT BLOCK ---
#     draw.text((30, 25), "Connplex Cinema", fill="#CFCFCF", font=font_title)
#     draw.text((30, 50), s["symbol"], fill="#8A8A8A", font=font_symbol)

#     draw.text(
#         (30, 80),
#         f"₹ {s['price']:.2f}",
#         fill="#00FF66",
#         font=font_price
#     )

#     # --- CENTER / RIGHT CHANGE ---
#     change_color = "#00FF66" if s["change"] >= 0 else "#FF4444"
#     draw.text(
#         (420, 90),
#         f"{s['change']:+.2f} ({s['change_percent']}%)",
#         fill=change_color,
#         font=font_change
#     )

#     # --- TIME ---
#     now = datetime.datetime.now().strftime("%H:%M:%S")
#     draw.text(
#         (30, 130),
#         f"Updated: {now}",
#         fill="#6F6F6F",
#         font=font_time
#     )

#     buf = io.BytesIO()
#     img.save(buf, format="PNG")
#     buf.seek(0)

#     return Response(
#         content=buf.read(),
#         media_type="image/png",
#         headers={
#             "Cache-Control": "no-cache, no-store, must-revalidate",
#             "Pragma": "no-cache",
#             "Expires": "0"
#         }
#     )
# @app.get("/")
# def root():
#     return {
#         "service": "Connplex Live Email Signature",
#         "status": "running",
#         "image_endpoint": "/signature/connplex.png"
#     }
# @app.get("/favicon.ico")
# def favicon():
#     return Response(status_code=204)
@app.get("/signature/connplex-full.png")
def connplex_full_signature():

    s = requests.get(STOCK_API).json()["stock"]

    W, H = 900, 420
    img = Image.new("RGB", (W, H), "#000000")
    draw = ImageDraw.Draw(img)

    try:
        title = ImageFont.truetype("arial.ttf", 26)
        text = ImageFont.truetype("arial.ttf", 18)
        price = ImageFont.truetype("arial.ttf", 30)
        small = ImageFont.truetype("arial.ttf", 14)
    except:
        title = text = price = small = ImageFont.load_default()

    # Name block
    draw.text((30, 20), "Kunal Jani", fill="#FFFFFF", font=title)
    draw.text((30, 55), "General Manager – Technology", fill="#BBBBBB", font=text)
    draw.text((30, 80), "+91 98245 38537", fill="#BBBBBB", font=text)

    # Company
    draw.text((30, 120), "CONNPLEX CINEMAS LIMITED", fill="#FFD700", font=text)
    draw.text((30, 145), "Ahmedabad, Gujarat", fill="#888888", font=small)

    # Divider
    draw.line((30, 180, 870, 180), fill="#333333", width=1)

    # Stock
    draw.text((30, 200), s["symbol"], fill="#AAAAAA", font=small)
    draw.text((30, 225), f"₹ {s['price']:.2f}", fill="#00FF66", font=price)

    change_color = "#00FF66" if s["change"] >= 0 else "#FF4444"
    draw.text((400, 240),
              f"{s['change']:+.2f} ({s['change_percent']}%)",
              fill=change_color,
              font=text)

    now = datetime.datetime.now().strftime("%H:%M:%S")
    draw.text((30, 290), f"Updated: {now}", fill="#666666", font=small)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return Response(buf.read(), media_type="image/png")
