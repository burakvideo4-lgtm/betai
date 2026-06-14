from flask import Flask
import requests
import os
import random

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


# ------------------------
# 🎯 TAHMİN MOTORU
# ------------------------
def predict_match():
    home_strength = random.randint(40, 100)
    away_strength = random.randint(40, 100)

    total = home_strength + away_strength

    home_win = round(home_strength / total * 100, 1)
    away_win = round(away_strength / total * 100, 1)
    draw = round(100 - (home_win + away_win), 1)

    return home_win, draw, away_win


# ------------------------
# 🧠 ANALİZ
# ------------------------
def analyze_match(home, away):
    home_p, draw_p, away_p = predict_match()

    if home_p > away_p and home_p > draw_p:
        winner = "HOME"
        confidence = home_p
    elif away_p > home_p and away_p > draw_p:
        winner = "AWAY"
        confidence = away_p
    else:
        winner = "DRAW"
        confidence = draw_p

    return {
        "home": home,
        "away": away,
        "home_p": home_p,
        "draw_p": draw_p,
        "away_p": away_p,
        "winner": winner,
        "confidence": confidence,
        "odds": round(100 / confidence, 2)
    }


# ------------------------
# 🖥️ ANA SAYFA
# ------------------------
@app.route("/")
def home():

    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": API_KEY
    }

    try:
        response = requests.get(
            "https://v3.football.api-sports.io/fixtures",
            headers=headers,
            params={"date": "2026-06-14"},
            timeout=10
        )

        matches = response.json().get("response", [])

        analyzed = [
            analyze_match(
                m["teams"]["home"]["name"],
                m["teams"]["away"]["name"]
            )
            for m in matches[:20]
        ]

        # ------------------------
        # 📊 KUYON FİLTRELERİ
        # ------------------------
        single = analyzed[:10]
        double = analyzed[:2]
        triple = analyzed[:3]
        quad = analyzed[:4]

        high_odds = sorted(analyzed, key=lambda x: x["odds"], reverse=True)[:10]
        winners = [m for m in analyzed if m["confidence"] > 60]
        losers = [m for m in analyzed if m["confidence"] < 50]
        top_win = max(analyzed, key=lambda x: x["confidence"])

        # ------------------------
        # 🧾 HTML
        # ------------------------
        html = """
        <h1>⚽ BETAI KUYON SİSTEMİ</h1>
        <hr>
        """

        def render(title, data):
            out = f"<h2>{title}</h2>"
            for m in data:
                out += f"""
                <div style="margin-bottom:15px;">
                    <b>{m['home']}</b> vs <b>{m['away']}</b><br>
                    🔵 %{m['home_p']} | ⚪ %{m['draw_p']} | 🔴 %{m['away_p']}<br>
                    🏆 Tahmin: <b>{m['winner']}</b> | 📊 Güven: %{m['confidence']} | 🎯 Oran: {m['odds']}
                </div>
                <hr>
                """
            return out

        html += render("🎯 Tekli Kupon", single)
        html += render("🎯🎯 İkili Kupon", double)
        html += render("🎯🎯🎯 Üçlü Kupon", triple)
        html += render("🎯🎯🎯🎯 Dörtlü Kupon", quad)

        html += render("📈 Yüksek Oranlı Maçlar", high_odds)
        html += render("🏆 Güvenli Tahminler", winners)
        html += render("❌ Riskli Tahminler", losers)
        html += render("💣 En Güçlü Maç", [top_win])

        return html

    except Exception as e:
        return f"Hata: {e}"


# ------------------------
# 🚀 RUN
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
