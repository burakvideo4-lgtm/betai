from flask import Flask
import requests
import os
from datetime import datetime
import random

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


# ⚽ Basit tahmin sistemi
def predict_score():
    home_goals = random.choices([0, 1, 2, 3], weights=[20, 35, 30, 15])[0]
    away_goals = random.choices([0, 1, 2, 3], weights=[25, 35, 25, 15])[0]
    return home_goals, away_goals


@app.route("/")
def home():

    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": API_KEY
    }

    today = datetime.now().strftime("%Y-%m-%d")

    try:
        response = requests.get(
            "https://v3.football.api-sports.io/fixtures",
            headers=headers,
            params={"date": today},
            timeout=10
        )

        data = response.json()
        matches = data.get("response", [])

        html = "<h1>⚽ BETAI</h1>"

        for match in matches[:15]:

            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]

            # 🎯 tahmin
            home_g, away_g = predict_score()

            if home_g > away_g:
                result = "🏠 Ev sahibi kazanır"
            elif home_g < away_g:
                result = "✈️ Deplasman kazanır"
            else:
                result = "🤝 Beraberlik"

            html += f"""
            <div style="margin-bottom:15px;">
                <b>{home}</b> {home_g} - {away_g} <b>{away}</b><br>
                <span>{result}</span>
            </div>
            <hr>
            """

        return html

    except Exception as e:
        return f"Hata: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
