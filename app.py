from fastapi import FastAPI
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
import requests, io, time

app = FastAPI()

# ---------------- EMPLOYEE DATA ----------------
EMPLOYEES = {
    "kunal": {
        "name": "Kunal Jani",
        "role": "General Manager - Technology",
        "phone": "+91 98245 38537",
        "email": "kunal@theconnplex.com"
    }
}

# ---------------- STOCK API ----------------
STOCK_API = "https://connplex-activeled.onrender.com/data"

_cache = {"data": None, "ts": 0}

def get_stock():
    if time.time() - _cache["ts"] < 5:
        return _cache["data"]

    data = requests.get(STOCK_API, timeout=5).json()
    _cache["data"] = data
    _cache["ts"] = time.time()
    return data

# ---------------- IMAGE ENDPOINT ----------------
@app.get("/signature/employee/{emp}.png")
def signature(emp: str):
    if emp not in EMPLOYEES:
        return {"error": "Employee not found"}

    emp_data = EMPLOYEES[emp]
    stock = get_stock()["stock"]

    # Canvas
    img = Image.new("RGB", (1000, 600), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Logo
    logo = Image.open("assets/logo.png").resize((130, 130))
    img.paste(logo, (30, 30), logo)

    # Employee text
    draw.text((190, 40), emp_data["name"], fill="black", font=font)
    draw.text((190, 65), emp_data["role"], fill="black", font=font)
    draw.text((190, 90), emp_data["phone"], fill="#0b5cff", font=font)
    draw.text((190, 115), emp_data["email"], fill="black", font=font)

    # Company block
    draw.text((190, 150), "CONNPLEX CINEMAS LIMITED", fill="black", font=font)
    draw.text(
        (190, 175),
        "Head Office - C-Block, 10 Floor, Krish Cubical, Thaltej, Ahmedabad 380059",
        fill="#333",
        font=font
    )

    # -------- STOCK STRIP (LIVE) --------
    strip_y = 230
    draw.rectangle([30, strip_y, 970, strip_y + 60], fill="black")

    price = stock["price"]
    change = stock["change"]
    pct = stock["change_percent"]
    color = "#00ff66" if change >= 0 else "#ff3333"

    draw.text(
        (50, strip_y + 18),
        f"CONNPLEX STOCK  ₹ {price:.2f}   {change:+.2f} ({pct}%)",
        fill=color,
        font=font
    )

    # Disclaimer
    draw.text(
        (30, 310),
        "IMPORTANT: This email and its contents are confidential. If received by mistake, please delete.",
        fill="#555",
        font=font
    )

    # Banner
    banner = Image.open("assets/tetst.gif").resize((940, 160))
    img.paste(banner, (30, 400))

    # Output
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return Response(buf.read(), media_type="image/png")
