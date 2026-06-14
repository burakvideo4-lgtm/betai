from flask import Flask
import random
import os

app = Flask(__name__)


# -----------------------------
# 🧠 TAKIM VERİSİ (SİMÜLASYON)
# -----------------------------
TEAMS = [
    "Galatasaray", "Fenerbahçe", "Beşiktaş", "Trabzonspor",
    "Barcelona", "Real Madrid", "Man United", "PSG",
    "Bayern Munich", "Juventus"
]


# -----------------------------
# 🧠 GÜÇ SİSTEMİ
# -----------------------------
def team_power(team):
    base = random.randint(60, 90)

    # büyük takımlar biraz avantajlı
    if team in ["Galatasaray", "Fenerbahçe", "Beşiktaş", "Real Madrid", "Barcelona"]:
        base += 10

    return min(base, 99)


# -----------------------------
# ⚽ MAÇ ÜRET
# -----------------------------
def generate_match():
    home = random.choice(TEAMS)
    away = random.choice(TEAMS)

    while home == away:
        away = random.choice(TEAMS)

    return home, away


# -----------------------------
# 🧠 TAHMİN MOTORU
# -----------------------------
def predict(home, away):

    h = team_power(home)
    a = team_power(away)

    total = h + a

    home_p = h / total
    away_p = a / total
    draw_p = random.uniform(0.10, 0.25)

    probs = {
        "HOME": home_p,
        "DRAW": draw_p,
        "AWAY": away_p
    }

    winner = max(probs, key=probs.get)
    confidence = probs[winner]

    return {
        "home": home,
        "away": away,
        "home_p": round(home_p * 100, 1),
        "draw_p": round(draw_p * 100, 1),
        "away_p": round(away_p * 100, 1),
        "winner": winner,
        "confidence": round(confidence * 100, 1),
        "home_odds": round(1 / home_p, 2),
        "draw_odds": round(1 / draw_p, 2),
        "away_odds": round(1 / away_p, 2),
    }


# -----------------------------
# 🌐 ANA SAYFA
# -----------------------------
@app.route("/")
def home():

    matches = []

    # 15 fake maç üret
    for _ in range(15):
        h, a = generate_match()
        matches.append(predict(h, a))

    # -------------------------
    # 📊 KUYON SİSTEMİ
    # -------------------------
    single = matches[:10]
    double = matches[:2]
    triple = matches[:3]
    quad = matches[:4]

    high = sorted(matches, key=lambda x: x["confidence"], reverse=True)[:10]
    winners = [m for m in matches if m["confidence"] > 60]
    risky = [m for m in matches if m["confidence"] < 50]
    top = max(matches, key=lambda x: x["confidence"])

    # -------------------------
    # 🖥️ UI
    # -------------------------
    html = """
    <h1>⚽ BETAI PRO OFFLINE</h1>
    <p>API YOK - TAMAMEN OFFLINE MODEL</p>
    <hr>
    """

    def box(title, arr):
        out = f"<h2>{title}</h2>"
        for m in arr:
            out += f"""
            <div style="margin-bottom:15px;">
                <b>{m['home']} vs {m['away']}</b><br>
                📊 %{m['home_p']} | %{m['draw_p']} | %{m['away_p']}<br>
                🎯 {m['winner']} (%{m['confidence']})<br>
                💰 {m['home_odds']} / {m['draw_odds']} / {m['away_odds']}
            </div>
            <hr>
            """
        return out

    html += box("🎯 Tekli Kupon", single)
    html += box("🎯🎯 İkili Kupon", double)
    html += box("🎯🎯🎯 Üçlü Kupon", triple)
    html += box("🎯🎯🎯🎯 Dörtlü Kupon", quad)

    html += box("📈 Güçlü Maçlar", high)
    html += box("🏆 Güvenli Tahminler", winners)
    html += box("⚠️ Riskli Maçlar", risky)
    html += box("💣 En Güçlü Maç", [top])

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
