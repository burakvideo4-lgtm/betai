from flask import Flask
import requests
import os
import random

app = Flask(__name__)

# ⚠️ API KEY BURAYA
API_KEY = "BURAYA_API_KEYİNİ_YAPISTIR"


def predict_match():
    home_strength = random.randint(40, 100)
    away_strength = random.randint(40, 100)

    total = home_strength + away_strength

    home_win = home_strength / total
    away_win = away_strength / total
    draw = 1 - (home_win + away_win)

    return home_win, draw, away_win


def odds(p):
    if p <= 0:
        return 0
    return round((1 / p) * 1.07, 2)


def analyze(home, away):
    hw, dr, aw = predict_match()

    if hw >= dr and hw >= aw:
        winner = "HOME"
        conf = hw
    elif aw >= hw and aw >= dr:
        winner = "AWAY"
        conf = aw
    else:
        winner = "DRAW"
        conf = dr

    return {
        "home": home,
        "away": away,
        "home_p": round(hw * 100, 1),
        "draw_p": round(dr * 100, 1),
        "away_p": round(aw * 100, 1),
        "winner": winner,
        "confidence": round(conf * 100, 1),
        "home_odds": odds(hw),
        "draw_odds": odds(dr),
        "away_odds": odds(aw),
    }


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

        data = r.json()
        matches = data.get("response", [])

        if not matches:
            return "<h1>⚠️ Maç verisi yok</h1>"

        analyzed = []

        for m in matches[:20]:
            try:
                home = m["teams"]["home"]["name"]
                away = m["teams"]["away"]["name"]
                analyzed.append(analyze(home, away))
            except:
                continue

        if not analyzed:
            return "<h1>⚠️ Analiz üretilemedi</h1>"

        html = "<h1>⚽ BETAI SAĞLAM SİSTEM</h1><hr>"

        def render(title, data):
            out = f"<h2>{title}</h2>"
            for m in data:
                out += f"""
                <div>
                    <b>{m['home']} vs {m['away']}</b><br>
                    📊 %{m['home_p']} | %{m['draw_p']} | %{m['away_p']}<br>
                    🎯 {m['winner']} (%{m['confidence']})<br>
                    💰 {m['home_odds']} / {m['draw_odds']} / {m['away_odds']}
                </div><hr>
                """
            return out

        html += render("🎯 Tekli", analyzed[:10])
        html += render("🎯🎯 İkili", analyzed[:2])
        html += render("🎯🎯🎯 Üçlü", analyzed[:3])

        top = max(analyzed, key=lambda x: x["confidence"])
        html += render("💣 En Güçlü", [top])

        return html

    except Exception as e:
        return f"Hata: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
