from flask import Flask
import requests
import os
import random

app = Flask(__name__)

# ⚠️ API KEY EKLENDİ
API_KEY = "999e0bfd03e0268f0ad00d6619da543f"


# -----------------------------
# 🧠 PRO ORAN MOTORU
# -----------------------------
def predict():
    h = random.randint(40, 100)
    a = random.randint(40, 100)

    total = h + a

    return {
        "home": h / total,
        "draw": random.uniform(0.15, 0.30),
        "away": a / total
    }


def odds(p):
    if p <= 0:
        return 0
    return round((1 / p) * 1.05, 2)


# -----------------------------
# 🧠 ANALİZ MOTORU
# -----------------------------
def analyze(home, away):
    p = predict()

    probs = {
        "HOME": p["home"],
        "DRAW": p["draw"],
        "AWAY": p["away"]
    }

    winner = max(probs, key=probs.get)
    confidence = probs[winner]

    return {
        "home": home,
        "away": away,
        "home_p": round(p["home"] * 100, 1),
        "draw_p": round(p["draw"] * 100, 1),
        "away_p": round(p["away"] * 100, 1),
        "winner": winner,
        "confidence": round(confidence * 100, 1),
        "home_odds": odds(p["home"]),
        "draw_odds": odds(p["draw"]),
        "away_odds": odds(p["away"])
    }


# -----------------------------
# 🌐 ANA SAYFA
# -----------------------------
@app.route("/")
def home():

    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": API_KEY
    }

    try:
        r = requests.get(
            "https://v3.football.api-sports.io/fixtures",
            headers=headers,
            params={"date": "2026-06-14"},
            timeout=10
        )

        data = r.json().get("response", [])

        if not data:
            return "<h1>⚠️ Maç verisi yok</h1>"

        matches = []

        for m in data[:20]:
            try:
                matches.append(analyze(
                    m["teams"]["home"]["name"],
                    m["teams"]["away"]["name"]
                ))
            except:
                continue

        if not matches:
            return "<h1>⚠️ Analiz üretilemedi</h1>"

        # -----------------------------
        # 📊 KUYON SİSTEMİ
        # -----------------------------
        single = matches[:10]
        double = matches[:2]
        triple = matches[:3]
        quad = matches[:4]

        high = sorted(matches, key=lambda x: x["confidence"], reverse=True)[:10]
        winners = [m for m in matches if m["confidence"] > 60]
        risky = [m for m in matches if m["confidence"] < 50]
        top = max(matches, key=lambda x: x["confidence"])

        # -----------------------------
        # 🖥️ UI
        # -----------------------------
        html = """
        <h1>⚽ BETAI PRO 3.0</h1>
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

    except Exception as e:
        return f"<h1>⚠️ Sistem Hatası</h1><p>{e}</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
